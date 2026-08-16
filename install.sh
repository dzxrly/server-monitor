#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -eq 0 ]]; then
  echo "Run this installer as the ordinary user who will own the monitor, without sudo." >&2
  exit 1
fi

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "This bootstrap installer supports Linux. Use deploy.bat on Windows." >&2
  exit 1
fi

REPOSITORY="${SERVER_MONITOR_REPOSITORY:-dzxrly/server-monitor}"
REF="${SERVER_MONITOR_REF:-backend-dev}"
INSTALL_ROOT="${SERVER_MONITOR_INSTALL_DIR:-${HOME}/server-monitor}"
ARCHIVE_URL="${SERVER_MONITOR_ARCHIVE_URL:-https://codeload.github.com/${REPOSITORY}/tar.gz/refs/heads/${REF}}"

if [[ "${INSTALL_ROOT}" != /* ]]; then
  INSTALL_ROOT="$(pwd)/${INSTALL_ROOT}"
fi

INSTALL_BASENAME="$(basename "${INSTALL_ROOT}")"
INSTALL_PARENT="$(dirname "${INSTALL_ROOT}")"
if [[ -z "${INSTALL_BASENAME}" || "${INSTALL_BASENAME}" == "." || \
  "${INSTALL_BASENAME}" == ".." ]]; then
  echo "The installation directory is not safe: ${INSTALL_ROOT}" >&2
  exit 1
fi

mkdir -p "${INSTALL_PARENT}"
INSTALL_PARENT="$(cd "${INSTALL_PARENT}" && pwd -P)"
INSTALL_ROOT="${INSTALL_PARENT}/${INSTALL_BASENAME}"
if [[ "${INSTALL_ROOT}" == "/" || "${INSTALL_ROOT}" == "${HOME}" ]]; then
  echo "Refusing to install into a broad directory: ${INSTALL_ROOT}" >&2
  exit 1
fi
if [[ -e "${INSTALL_ROOT}" && ! -d "${INSTALL_ROOT}" ]]; then
  echo "The installation target exists and is not a directory: ${INSTALL_ROOT}" >&2
  exit 1
fi

for required_command in tar find mktemp; do
  if ! command -v "${required_command}" >/dev/null 2>&1; then
    echo "Required command not found: ${required_command}" >&2
    exit 1
  fi
done

TEMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/server-monitor-install.XXXXXX")"
trap 'rm -rf -- "${TEMP_ROOT}"' EXIT
ARCHIVE_PATH="${TEMP_ROOT}/server-monitor.tar.gz"
SOURCE_ROOT="${TEMP_ROOT}/source"
mkdir -p "${SOURCE_ROOT}"

echo "Downloading Server Monitor from ${ARCHIVE_URL}..."
if command -v curl >/dev/null 2>&1; then
  curl --fail --location --silent --show-error "${ARCHIVE_URL}" --output "${ARCHIVE_PATH}"
elif command -v wget >/dev/null 2>&1; then
  wget --quiet "${ARCHIVE_URL}" --output-document="${ARCHIVE_PATH}"
else
  echo "curl or wget is required to download the source archive." >&2
  exit 1
fi

tar -xzf "${ARCHIVE_PATH}" -C "${SOURCE_ROOT}" --strip-components=1
if [[ ! -f "${SOURCE_ROOT}/server.py" || ! -f "${SOURCE_ROOT}/deploy.sh" ]]; then
  echo "The downloaded archive is not a valid Server Monitor backend package." >&2
  exit 1
fi

BACKUP_PATH=""
HAD_PREVIOUS_INSTALLATION=false
if [[ -d "${INSTALL_ROOT}" ]] && \
  [[ -n "$(find "${INSTALL_ROOT}" -mindepth 1 -maxdepth 1 -print -quit)" ]]; then
  HAD_PREVIOUS_INSTALLATION=true
  BACKUP_PATH="${INSTALL_ROOT}-backup-$(date -u +%Y%m%dT%H%M%SZ).tar.gz"
  echo "Backing up the existing source to ${BACKUP_PATH}..."
  tar \
    --exclude='./.git' \
    --exclude='./venv' \
    --exclude='./log' \
    -czf "${BACKUP_PATH}" -C "${INSTALL_ROOT}" .
else
  mkdir -p "${INSTALL_ROOT}"
fi

replace_source() {
  find "${INSTALL_ROOT}" \
    -mindepth 1 -maxdepth 1 \
    ! -name .git ! -name venv ! -name log \
    -exec rm -rf -- {} +
}

replace_source
cp -a "${SOURCE_ROOT}/." "${INSTALL_ROOT}/"

echo "Installing the background service..."
if ! bash "${INSTALL_ROOT}/deploy.sh"; then
  echo "Deployment failed." >&2
  if [[ "${HAD_PREVIOUS_INSTALLATION}" == true ]]; then
    echo "Restoring the previous source..." >&2
    replace_source
    tar -xzf "${BACKUP_PATH}" -C "${INSTALL_ROOT}"
    bash "${INSTALL_ROOT}/deploy.sh" || \
      echo "The previous source was restored, but its service could not be restarted." >&2
  fi
  exit 1
fi

echo "Server Monitor installation completed."
echo "Installation directory: ${INSTALL_ROOT}"
echo "Uninstall command: bash ${INSTALL_ROOT}/uninstall.sh"
if [[ -n "${BACKUP_PATH}" ]]; then
  echo "Previous source backup: ${BACKUP_PATH}"
fi
