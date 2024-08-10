<div align="center">

# Server Monitor 后端

</div>

<div align="center">

![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Fbackend%2Finfo.json&query=%24.version&prefix=V&style=flat-square&label=Version)

</div>

<div align="center">

这是一个在线多服务器硬件状态监控网站的轻量化后端。请在需要监控硬件状态的服务器上部署该后端，默认状态下后端使用`6543`
端口，请确保防火墙放行该端口！

</div>

> [!CAUTION]
>
> 完成后端部署后需要部署[前端网站](https://github.com/dzxrly/server-monitor/blob/frontend/README.md)以监控服务器硬件状态！

## 操作系统支持

<div align="center">

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

</div>

## 后端部署

### 使用一键部署脚本

1. 使用`git clone`拉取后端源码

   ```bash
   git clone -b backend https://github.com/dzxrly/server-monitor.git
   ```

2. 进入源码目录

   ```bash
   cd server-monitor
   ```

3.
    - 对于**Linux系统**

      ```bash
      # 授予脚本可执行权限
      chmod +x deploy.sh
      # 运行部署脚本
      ./deploy.sh
      ```

    - 对于**Windows系统**

      ```bash
      # 直接运行以下命令
      ./deploy.bat
      ```

### 手动构建（可选）

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

配置文件位于`./server_config.py`中，其中字段均为`waitress`的`serve`
函数可接受字段，默认仅设置了`host`与`port`
，具体配置请参考：[waitress serve arguments docs](https://docs.pylonsproject.org/projects/waitress/en/latest/arguments.html#arguments)。

---

<div align="center">

[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/eggtargaryen)

</div>

<div align="center">

by Egg Targaryen

</div>
