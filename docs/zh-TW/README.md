# Server Monitor 後端

Server Monitor 後端透過一個具版本號的統一 API 提供 CPU、記憶體、NVIDIA GPU、溫度、硬碟、網路、作業系統和高佔用程序指標。Windows 與 Linux 均可在一般使用者權限下執行。

[简体中文](../zh-CN/README.md) | [繁體中文](./README.md) | [English](../../README.md)

## 主要功能

- 使用單一 `GET /api/v1/metrics` 回傳同一採樣時刻的完整快照，不再呼叫多個舊介面。
- 讀取所有可見掛載磁碟區、實體硬碟 I/O、網路介面及各介面即時速率。
- 可指定 CPU、記憶體和 NVIDIA GPU 高佔用程序的回傳數量。
- 透過 NVML 讀取 NVIDIA 裝置和程序指標。
- Linux 透過 `psutil` 讀取溫度；Windows 透過 LibreHardwareMonitor 讀取溫度。
- 背景定時採樣，HTTP 請求不會現場阻塞採集。
- Linux 使用 systemd 使用者服務，Windows 使用目前使用者的受限排程工作自動啟動。

未帶版本號的舊 API 已移除，前端必須支援 API v1。

## 環境需求

- Python 3.9 或更新版本。執行和開發相依套件均固定為支援 Python 3.9 的版本。
- 使用隨附的背景部署方案時，Linux 需要 systemd。
- 如需 NVIDIA 指標，需要安裝 NVIDIA 驅動程式。

## 建議部署方式

一般使用者可透過一行指令完成首次安裝或更新：

```bash
curl -fsSL https://raw.githubusercontent.com/dzxrly/server-monitor/backend-dev/install.sh | bash
```

引導腳本會將 `backend-dev` 原始碼下載至 `~/server-monitor`，備份既有原始碼，保留原有 `venv` 和日誌，然後安裝服務。若已經拉取原始碼，也可以在儲存庫中執行：

```bash
git clone -b backend-dev https://github.com/dzxrly/server-monitor.git
cd server-monitor
```

### Linux：systemd 使用者服務

請以最終執行服務的一般使用者執行，不要使用 `sudo`：

```bash
bash deploy.sh
```

安裝程式會建立專案內的 `./venv`、安裝 `requirements.txt`、產生 `~/.config/systemd/user/server-monitor.service`，隨後啟用並立即啟動服務。如果發行版未安裝 `ensurepip`/`python3-venv`，腳本會從 PyPI 下載固定版本且經過 SHA-256 驗證的 pip wheel，不需要 root 即可完成隔離環境。常用命令：

```bash
systemctl --user status server-monitor.service
systemctl --user restart server-monitor.service
journalctl --user -u server-monitor.service -f
bash uninstall.sh
```

若要在使用者首次登入前啟動，並在登出後繼續執行，需要為該使用者啟用 systemd lingering。安裝程式會自動嘗試；若系統原則拒絕，管理員只需執行一次：

```bash
sudo loginctl enable-linger 使用者名稱
```

服務程序本身仍以一般使用者執行，並啟用了 `NoNewPrivileges=true`。

### Windows：目前使用者排程工作

在一般權限的命令提示字元或 PowerShell 中執行：

```powershell
deploy.bat
```

安裝程式會建立 `./venv`、安裝相依套件、下載並驗證 LibreHardwareMonitor 0.9.6，並為目前使用者註冊受限權限的 `Server Monitor` 排程工作。工作會在使用者開機登入後於背景啟動，並在異常結束後自動重新啟動。

管理命令：

```powershell
powershell -ExecutionPolicy Bypass -File deploy/windows/start.ps1
powershell -ExecutionPolicy Bypass -File deploy/windows/stop.ps1
uninstall.bat
```

LibreHardwareMonitor 來自官方 GitHub Release，並使用 [`vendor/librehardwaremonitor/README.md`](../../vendor/librehardwaremonitor/README.md) 中記錄的 SHA-256 驗證。部分感測器是否可見取決於硬體、驅動程式和 LibreHardwareMonitor 的權限需求；一般使用者無法讀取時會正常降級，不會影響其他指標或後端執行。

## 手動執行

部署腳本保留原有的專案內 `venv` 執行邏輯。手動安裝與其等價：

```bash
python3 -m venv venv
./venv/bin/python -m pip install -r requirements.txt
./venv/bin/python server.py
```

Windows 請將最後兩條命令中的直譯器替換為 `venv\Scripts\python.exe`。

## API v1

| 介面 | 用途 |
| --- | --- |
| `GET /api/v1/health` | 服務及背景採樣器健康狀態 |
| `GET /api/v1/capabilities` | 目前平台和採集器能力 |
| `GET /api/v1/metrics?processLimit=5` | 完整指標快照 |

`processLimit` 必須位於 `1` 和 `SERVER_MONITOR_MAX_PROCESS_LIMIT` 之間，後者預設為 `50`。選用採集器不可用時，對應區域會回傳 `available: false` 和原因，其他指標仍會正常回傳。

## 環境變數

不需要修改原始碼設定檔，直接使用環境變數：

| 變數 | 預設值 | 說明 |
| --- | --- | --- |
| `SERVER_MONITOR_HOST` | `0.0.0.0` | 監聽位址 |
| `SERVER_MONITOR_PORT` | `6543` | 監聽連接埠 |
| `SERVER_MONITOR_SAMPLE_INTERVAL` | `2` | 背景採樣週期，單位為秒 |
| `SERVER_MONITOR_PROCESS_LIMIT` | `5` | 預設高佔用程序數量 |
| `SERVER_MONITOR_MAX_PROCESS_LIMIT` | `50` | API 允許的最大程序數量 |
| `SERVER_MONITOR_CORS_ORIGINS` | `*` | 允許的前端來源，多個值以逗號分隔 |
| `SERVER_MONITOR_ENABLE_LHM` | `true` | 是否啟用 Windows LibreHardwareMonitor |
| `SERVER_MONITOR_LHM_PATH` | 內建 vendor 路徑 | 自訂 LibreHardwareMonitor DLL 路徑 |
| `SERVER_MONITOR_LOG_DIR` | `./log` | 日誌目錄 |

## Docker

```bash
docker build -t server-monitor-backend .
docker run --rm -p 6543:6543 server-monitor-backend
```

映像以非 root 使用者執行。容器命名空間可能隱藏或虛擬化主機的硬碟、網路卡、程序和感測器；如需完整主機指標，建議使用原生部署。

## 開發驗證

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
python -m ruff check .
```

API 本身不包含驗證。請僅向可信任網路開放 `6543` 連接埠，或在公網部署時使用具驗證功能的反向代理。
