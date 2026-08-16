#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -eq 0 ]]; then
  echo "Run this installer as the ordinary user who will own the monitor, without sudo." >&2
  exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_ROOT="${PROJECT_ROOT}/venv"
VENV_PYTHON="${VENV_ROOT}/bin/python"
SERVICE_PATH="${HOME}/.config/systemd/user/server-monitor.service"
STATE_PATH="${HOME}/.local/state/server-monitor"

if ! command -v systemctl >/dev/null 2>&1; then
  echo "systemd is required for background service installation." >&2
  exit 1
fi

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "Python was not found: ${PYTHON_BIN}" >&2
  exit 1
fi

if ! "${PYTHON_BIN}" -c \
  'import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)'; then
  echo "Python 3.9 or newer is required. Found: $("${PYTHON_BIN}" --version 2>&1)" >&2
  exit 1
fi

PIP_BOOTSTRAP_VERSION="26.0.1"
PIP_BOOTSTRAP_URL="https://files.pythonhosted.org/packages/de/f0/c81e05b613866b76d2d1066490adf1a3dbc4ee9d9c839961c3fc8a6997af/pip-26.0.1-py3-none-any.whl"
PIP_BOOTSTRAP_SHA256="bdb1b08f4274833d62c1aa29e20907365a2ceb950410df15fc9521bad440122b"

if [[ ! -x "${VENV_PYTHON}" ]]; then
  if ! "${PYTHON_BIN}" -m venv "${VENV_ROOT}"; then
    echo "python3-venv/ensurepip is unavailable; creating an isolated environment without pip." >&2
    "${PYTHON_BIN}" -m venv --without-pip "${VENV_ROOT}"
  fi
fi

if ! "${VENV_PYTHON}" -c \
  'import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)'; then
  echo "The existing venv uses Python older than 3.9. Remove ${VENV_ROOT} and rerun." >&2
  exit 1
fi

if ! "${VENV_PYTHON}" -m pip --version >/dev/null 2>&1; then
  BOOTSTRAP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/server-monitor-pip.XXXXXX")"
  PIP_WHEEL="${BOOTSTRAP_ROOT}/pip-${PIP_BOOTSTRAP_VERSION}-py3-none-any.whl"
  trap 'rm -rf -- "${BOOTSTRAP_ROOT}"' EXIT
  echo "Bootstrapping pip ${PIP_BOOTSTRAP_VERSION} from the verified PyPI wheel..."
  "${PYTHON_BIN}" -c \
    'import sys, urllib.request; urllib.request.urlretrieve(sys.argv[1], sys.argv[2])' \
    "${PIP_BOOTSTRAP_URL}" "${PIP_WHEEL}"
  ACTUAL_SHA256="$("${PYTHON_BIN}" -c \
    'import hashlib, pathlib, sys; print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())' \
    "${PIP_WHEEL}")"
  if [[ "${ACTUAL_SHA256}" != "${PIP_BOOTSTRAP_SHA256}" ]]; then
    echo "pip bootstrap checksum mismatch." >&2
    exit 1
  fi
  PYTHONPATH="${PIP_WHEEL}" "${VENV_PYTHON}" -m pip install --no-index "${PIP_WHEEL}"
fi

"${VENV_PYTHON}" -m pip install --upgrade "pip==${PIP_BOOTSTRAP_VERSION}"
"${VENV_PYTHON}" -m pip install -r "${PROJECT_ROOT}/requirements.txt"
mkdir -p "$(dirname "${SERVICE_PATH}")" "${STATE_PATH}"
"${VENV_PYTHON}" "${PROJECT_ROOT}/deploy/linux/render_service.py" \
  "${PROJECT_ROOT}" "${SERVICE_PATH}"

systemctl --user daemon-reload
systemctl --user enable --now server-monitor.service

if command -v loginctl >/dev/null 2>&1; then
  if [[ "$(loginctl show-user "${USER}" -p Linger --value 2>/dev/null || true)" != "yes" ]]; then
    if ! loginctl enable-linger "${USER}" 2>/dev/null; then
      echo "Warning: the service starts at login, but boot-before-login needs an administrator to run:" >&2
      echo "  loginctl enable-linger ${USER}" >&2
    fi
  fi
fi

for _ in {1..20}; do
  if "${VENV_PYTHON}" -c \
    'import urllib.request; urllib.request.urlopen("http://127.0.0.1:6543/api/v1/health", timeout=2).read()' \
    >/dev/null 2>&1; then
    echo "Server Monitor is running as a systemd user service."
    echo "Health endpoint: http://127.0.0.1:6543/api/v1/health"
    exit 0
  fi
  sleep 0.5
done

echo "Service installation completed, but the health check failed." >&2
systemctl --user status server-monitor.service --no-pager >&2 || true
exit 1
