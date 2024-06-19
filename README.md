# Server Monitor

<div align="center">

![Static Badge](https://img.shields.io/badge/Verison-V0.0.1-2a82c0?style=flat-square)

</div>

在线多服务器硬件状态监控网站轻量化后端。

请在需要监控硬件状态的服务器上部署该后端，默认状态下后端使用`6543`端口，请确保防火墙放行该端口！

## 操作系统支持

- Windows
- Linux

## 服务器部署

1. 使用`git clone`拉取后端源码

   `git clone -b backend https://github.com/dzxrly/server-monitor.git`

2. 进入源码目录

   `cd server-monitor`

3. 创建虚拟环境（此处使用`conda`举例，并非一定要使用该虚拟环境管理器）

   `conda create -n server-monitor`

4. 切换至步骤1创建的虚拟环境

   `conda activate server-monitor`

5. 安装依赖库

   `pip install -r requirements.txt`

6.
    - Linux系统部署

        - 授予部署脚本权限

          `chmod +x deploy.sh`

        - 运行部署脚本

          `./deploy.sh`

    - Windows系统部署

        - 运行`.bat`脚本

          `./deploy.bat`

7. 完成部署后在网站输入`你的服务器IP:端口号`即可

## 配置文件设置

配置文件位于`./server_config.py`中，其中字段均为`waitress`的`serve`
函数可接受字段，具体配置请参考：[waitress serve arguments docs](https://docs.pylonsproject.org/projects/waitress/en/latest/arguments.html#arguments)。
