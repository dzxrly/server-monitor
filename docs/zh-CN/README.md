<div align="center">

# Server Monitor 后端

</div>

<div align="center">

![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Fbackend%2Finfo.json&query=%24.version&prefix=V&style=flat-square&label=Version)

</div>

<div align="center">

Server Monitor 后端通过一个带版本号的统一 API 提供 CPU、内存、NVIDIA GPU、温度、硬盘、网络、操作系统和高占用进程指标。Windows 与 Linux 均可在普通用户权限下运行。

</div>

<div align="center">

[简体中文](../../docs/zh-CN/README.md) | [繁體中文](../../docs/zh-TW/README.md) | [English](../../README.md)

</div>

> [!CAUTION]
>
> 完成后端部署后，需要部署[前端网站](https://github.com/dzxrly/server-monitor/blob/frontend/docs/zh-CN/README.md)以查看和管理服务器指标！

## 主要功能

- 使用单一 `GET /api/v1/metrics` 返回同一采样时刻的完整快照，不再调用多个旧接口。
- 读取所有可见挂载卷、物理硬盘 I/O、网络接口及各接口实时速率。
- 可指定 CPU、内存和 NVIDIA GPU 高占用进程的返回数量。
- 通过 NVML 读取 NVIDIA 设备和进程指标。
- Linux 通过 `psutil` 读取温度；Windows 通过 LibreHardwareMonitor 读取温度。
- 后台定时采样，HTTP 请求不会现场阻塞采集。
- Linux 使用 systemd 用户服务，Windows 使用当前用户的受限计划任务自动启动。

未带版本号的旧 API 已删除，前端必须支持 API v1。

## 环境要求

- Python 3.9 或更高版本。运行和开发依赖均固定为支持 Python 3.9 的版本。
- 使用随附的后台部署方案时，Linux 需要 systemd。
- 如需 NVIDIA 指标，需要安装 NVIDIA 驱动。

## 推荐部署方式

普通用户可通过一行命令完成首次安装或更新：

```bash
curl -fsSL https://raw.githubusercontent.com/dzxrly/server-monitor/backend/install.sh | SERVER_MONITOR_REF=backend bash
```

引导脚本会将 `backend` 源码下载至 `~/server-monitor`，备份已有源码，保留原有 `venv` 和日志，然后安装服务。若已经拉取了源码，也可以在仓库中执行：

```bash
git clone -b backend https://github.com/dzxrly/server-monitor.git
cd server-monitor
```

### Linux：systemd 用户服务

请以最终运行服务的普通用户执行，不要使用 `sudo`：

```bash
bash deploy.sh
```

安装器会创建项目内的 `./venv`、安装 `requirements.txt`、生成 `~/.config/systemd/user/server-monitor.service`，随后启用并立即启动服务。如果发行版未安装 `ensurepip`/`python3-venv`，脚本会从 PyPI 下载固定版本且经过 SHA-256 校验的 pip wheel，无需 root 即可完成隔离环境。常用命令：

```bash
systemctl --user status server-monitor.service
systemctl --user restart server-monitor.service
journalctl --user -u server-monitor.service -f
bash uninstall.sh
```

若要在用户首次登录前启动，并在退出登录后继续运行，需要为该用户启用 systemd lingering。安装器会自动尝试；若系统策略拒绝，则管理员只需执行一次：

```bash
sudo loginctl enable-linger 用户名
```

服务进程本身仍以普通用户运行，并启用了 `NoNewPrivileges=true`。

### Windows：当前用户计划任务

在普通权限的命令提示符或 PowerShell 中执行：

```powershell
deploy.bat
```

安装器会创建 `./venv`、安装依赖、下载并校验 LibreHardwareMonitor 0.9.6，并为当前用户注册受限权限的 `Server Monitor` 计划任务。任务会在用户开机登录后于后台启动，并在异常退出后自动重启。

管理命令：

```powershell
powershell -ExecutionPolicy Bypass -File deploy/windows/start.ps1
powershell -ExecutionPolicy Bypass -File deploy/windows/stop.ps1
uninstall.bat
```

LibreHardwareMonitor 来自官方 GitHub Release，并使用 [`vendor/librehardwaremonitor/README.md`](../../vendor/librehardwaremonitor/README.md) 中记录的 SHA-256 校验。部分传感器是否可见取决于硬件、驱动和 LibreHardwareMonitor 的权限要求；普通用户无法读取时会正常降级，不会影响其他指标或后端运行。

## 手动运行

部署脚本保持原有的项目内 `venv` 运行逻辑。手动安装与其等价：

```bash
python3 -m venv venv
./venv/bin/python -m pip install -r requirements.txt
./venv/bin/python server.py
```

Windows 请将最后两条命令中的解释器替换为 `venv\Scripts\python.exe`。

## API v1

| 接口 | 用途 |
| --- | --- |
| `GET /api/v1/health` | 服务及后台采样器健康状态 |
| `GET /api/v1/capabilities` | 当前平台和采集器能力 |
| `GET /api/v1/metrics?processLimit=5` | 完整指标快照 |

`processLimit` 必须位于 `1` 和 `SERVER_MONITOR_MAX_PROCESS_LIMIT` 之间，后者默认为 `50`。可选采集器不可用时，对应区域会返回 `available: false` 和原因，其他指标仍会正常返回。

## 环境变量

无需修改源码配置文件，直接使用环境变量：

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `SERVER_MONITOR_HOST` | `0.0.0.0` | 监听地址 |
| `SERVER_MONITOR_PORT` | `6543` | 监听端口 |
| `SERVER_MONITOR_SAMPLE_INTERVAL` | `2` | 后台采样周期，单位为秒 |
| `SERVER_MONITOR_PROCESS_LIMIT` | `5` | 默认高占用进程数量 |
| `SERVER_MONITOR_MAX_PROCESS_LIMIT` | `50` | API 允许的最大进程数量 |
| `SERVER_MONITOR_CORS_ORIGINS` | `*` | 允许的前端来源，多个值以逗号分隔 |
| `SERVER_MONITOR_ENABLE_LHM` | `true` | 是否启用 Windows LibreHardwareMonitor |
| `SERVER_MONITOR_LHM_PATH` | 内置 vendor 路径 | 自定义 LibreHardwareMonitor DLL 路径 |
| `SERVER_MONITOR_LOG_DIR` | `./log` | 日志目录 |

## Docker

```bash
docker build -t server-monitor-backend .
docker run --rm -p 6543:6543 server-monitor-backend
```

镜像以非 root 用户运行。容器命名空间可能隐藏或虚拟化宿主机的硬盘、网卡、进程和传感器；如需完整宿主机指标，推荐原生部署。

## 开发验证

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
python -m ruff check .
```

API 本身不包含鉴权。请仅向可信网络开放 `6543` 端口，或在公网部署时使用带鉴权的反向代理。

---

<div align="center">

[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/eggtargaryen)

</div>

<div align="center">

by Egg Targaryen

</div>
