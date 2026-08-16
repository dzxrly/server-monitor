<div align="center">

# Server Monitor Backend

</div>

<div align="center">

![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Fbackend%2Finfo.json&query=%24.version&prefix=V&style=flat-square&label=Version)

</div>

<div align="center">

The Server Monitor backend exposes one versioned API for CPU, memory, NVIDIA GPU, temperature, disk, network, operating-system, and top-process metrics. It runs on Windows and Linux without administrator/root privileges.

</div>

<div align="center">

[简体中文](./docs/zh-CN/README.md) | [繁體中文](./docs/zh-TW/README.md) | [English](./README.md)

</div>

> [!CAUTION]
>
> After deploying the backend, deploy the [Frontend Website](https://github.com/dzxrly/server-monitor/blob/frontend/README.md) to view and manage server metrics.

## Highlights

- One coherent `GET /api/v1/metrics` snapshot instead of separate legacy endpoints.
- All visible mounted volumes, physical-disk I/O rates, network interfaces, and per-interface transfer rates.
- Configurable top CPU, memory, and NVIDIA GPU process lists.
- NVIDIA device and process metrics through NVML.
- Linux temperatures through `psutil`; Windows temperatures through LibreHardwareMonitor.
- Background sampling keeps HTTP requests fast and avoids blocking per request.
- Current-user auto-start: a systemd user service on Linux and a limited scheduled task on Windows.

The old unversioned API has been removed. The frontend must support API v1.

## Requirements

- Python 3.9 or newer. Runtime and development dependencies are pinned to versions that support Python 3.9.
- Windows or a systemd-based Linux distribution for the supplied background-service installers.
- NVIDIA drivers when NVIDIA metrics are required.

## Recommended deployment

For a fresh installation or an update, run the one-line bootstrap as the ordinary user that should own the service:

```bash
curl -fsSL https://raw.githubusercontent.com/dzxrly/server-monitor/backend/install.sh | SERVER_MONITOR_REF=backend bash
```

The bootstrap downloads the `backend` source into `~/server-monitor`, backs up an existing source tree, preserves its `venv` and logs, and runs the service installer. To deploy from an existing checkout instead:

```bash
git clone -b backend https://github.com/dzxrly/server-monitor.git
cd server-monitor
```

### Linux: systemd user service

Run the installer as the ordinary user that should own the service—do not use `sudo`:

```bash
bash deploy.sh
```

The installer creates `./venv`, installs `requirements.txt`, writes `~/.config/systemd/user/server-monitor.service`, enables it, and starts it immediately. If the distribution omits `ensurepip`/`python3-venv`, it securely bootstraps pip from a pinned, SHA-256-verified PyPI wheel without requiring root. Useful commands:

```bash
systemctl --user status server-monitor.service
systemctl --user restart server-monitor.service
journalctl --user -u server-monitor.service -f
bash uninstall.sh
```

To run before the first login and remain active after logout, the user must have systemd lingering enabled. The installer attempts this automatically. If local policy blocks it, an administrator needs to run this once:

```bash
sudo loginctl enable-linger YOUR_USER
```

The service process itself still runs as the ordinary user with `NoNewPrivileges=true`.

### Windows: current-user scheduled task

From Command Prompt or PowerShell, without elevation:

```powershell
deploy.bat
```

The installer creates `./venv`, installs dependencies, downloads and verifies LibreHardwareMonitor 0.9.6, and registers a limited `Server Monitor` scheduled task for the current user. It starts in the background at sign-in and restarts after failures.

Management commands:

```powershell
powershell -ExecutionPolicy Bypass -File deploy/windows/start.ps1
powershell -ExecutionPolicy Bypass -File deploy/windows/stop.ps1
uninstall.bat
```

LibreHardwareMonitor is downloaded from its official GitHub release and checked against the SHA-256 recorded in [`vendor/librehardwaremonitor/README.md`](./vendor/librehardwaremonitor/README.md). Some sensors depend on hardware/driver support and may only be exposed by LibreHardwareMonitor when elevated; unavailable sensors degrade cleanly and do not prevent the backend from running as an ordinary user.

## Manual run

The deployment scripts intentionally use a project-local `venv`. A manual installation is equivalent:

```bash
python3 -m venv venv
./venv/bin/python -m pip install -r requirements.txt
./venv/bin/python server.py
```

On Windows, use `venv\Scripts\python.exe` in the last two commands.

## API v1

| Endpoint | Purpose |
| --- | --- |
| `GET /api/v1/health` | Service and sampler health |
| `GET /api/v1/capabilities` | Platform/provider availability |
| `GET /api/v1/metrics?processLimit=5` | Complete metrics snapshot |

`processLimit` must be between `1` and `SERVER_MONITOR_MAX_PROCESS_LIMIT` (default `50`). The response is still useful when an optional provider is unavailable: the affected section reports `available: false` and a reason, while other collectors continue.

## Configuration

Configuration is supplied through environment variables; no source file needs editing.

| Variable | Default | Meaning |
| --- | --- | --- |
| `SERVER_MONITOR_HOST` | `0.0.0.0` | Listen address |
| `SERVER_MONITOR_PORT` | `6543` | Listen port |
| `SERVER_MONITOR_SAMPLE_INTERVAL` | `2` | Background sampling interval in seconds |
| `SERVER_MONITOR_PROCESS_LIMIT` | `5` | Default top-process count |
| `SERVER_MONITOR_MAX_PROCESS_LIMIT` | `50` | Maximum API process count |
| `SERVER_MONITOR_CORS_ORIGINS` | `*` | Comma-separated allowed frontend origins |
| `SERVER_MONITOR_ENABLE_LHM` | `true` | Enable Windows LibreHardwareMonitor support |
| `SERVER_MONITOR_LHM_PATH` | bundled vendor path | Override the LibreHardwareMonitor DLL path |
| `SERVER_MONITOR_LOG_DIR` | `./log` | Log directory |

## Docker

```bash
docker build -t server-monitor-backend .
docker run --rm -p 6543:6543 server-monitor-backend
```

The image runs as a non-root user. Container namespaces can hide or virtualize host disks, interfaces, processes, and sensors, so native deployment is recommended when complete host metrics are required.

## Development checks

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
python -m ruff check .
```

The API has no built-in authentication. Restrict port `6543` to trusted networks or place it behind an authenticated reverse proxy before exposing it publicly.

---

<div align="center">

[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/eggtargaryen)

</div>

<div align="center">

by Egg Targaryen

</div>
