#!/usr/bin/env bash
set -euo pipefail

SERVICE_PATH="${HOME}/.config/systemd/user/server-monitor.service"
systemctl --user disable --now server-monitor.service 2>/dev/null || true
if [[ -f "${SERVICE_PATH}" ]]; then
  rm -- "${SERVICE_PATH}"
fi
systemctl --user daemon-reload
echo "Server Monitor user service removed. The venv and logs were preserved."
