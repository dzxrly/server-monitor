<div align="center">

# Server Monitor 后端

</div>

<div align="center">

![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Fbackend%2Finfo.json&query=%24.version&prefix=V&style=flat-square&label=Version)

</div>

<div align="center">

这是Server Monitor的后端。请在需要监控硬件状态的服务器上部署该后端，默认状态下后端使用`6543`端口，请确保防火墙放行该端口！

</div>

<div align="center">

[简体中文](../../docs/zh-CN/README.md) | [繁體中文](../../docs/zh-TW/README.md) | [English](../../README.md)

</div>

> [!CAUTION]
>
> 完成后端部署后需要部署[前端网站](https://github.com/dzxrly/server-monitor/blob/frontend/docs/zh-CN/README.md)
> 以监控服务器硬件状态！

## 后端部署

### 使用一键部署脚本（推荐）

1. 使用`git clone`拉取后端源码

   ```bash
   git clone -b backend https://github.com/dzxrly/server-monitor.git
   ```

2. 进入源码目录

   ```bash
   cd server-monitor
   ```

3.
    - 对于**Linux**

      ```bash
      # 授予脚本可执行权限
      chmod +x deploy.sh
      # 运行部署脚本
      ./deploy.sh
      ```

    - 对于**Windows**

      ```bash
      # 直接运行以下命令
      ./deploy.bat
      ```

### 手动构建

1. 使用`git clone`拉取后端源码

   ```bash
   git clone -b backend https://github.com/dzxrly/server-monitor.git
   ```

2. 进入源码目录

   ```bash
   cd server-monitor
   ```

3. 创建虚拟环境（此处使用`conda`举例，并非一定要使用该虚拟环境管理器）

   ```bash
   conda create -n server-monitor
   ```

4. 切换至步骤1创建的虚拟环境

   ```bash
   conda activate server-monitor
   ```

5. 安装依赖库

   ```bash
   pip install -r requirements.txt
   ```

6. 运行`server.py`开启后端服务器

   ```bash
   python server.py
   ```

7. 完成部署后在网站输入`你的服务器IP:端口号`即可

## 配置文件设置

配置文件位于`./server_config.py`中，其中字段均为`waitress`的`serve`函数可接受字段，默认仅设置了`host`与`port`
，具体配置请参考：[waitress serve arguments docs](https://docs.pylonsproject.org/projects/waitress/en/latest/arguments.html#arguments)。

---

<div align="center">

[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/eggtargaryen)

</div>

<div align="center">

by Egg Targaryen

</div>
