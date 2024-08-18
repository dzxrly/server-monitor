<div align="center">

# Server Monitor Backend

</div>

<div align="center">

![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Fbackend%2Finfo.json&query=%24.version&prefix=V&style=flat-square&label=Version)

</div>

<div align="center">

This is the backend of Server Monitor. Please deploy this backend on the servers where hardware status needs to be
monitored. By default, the backend uses port `6543`. Please ensure that this port is allowed through the firewall!

</div>

<div align="center">

[简体中文](./docs/zh-CN/README.md) | [繁體中文](./docs/zh-TW/README.md) | [English](./README.md)

</div>

> [!CAUTION]
>
> After completing the backend deployment, you need to deploy
> the [Frontend Website](https://github.com/dzxrly/server-monitor/blob/frontend/README.md) to monitor the hardware status
> of the server !

## Deployment

### Use deployment script (Recommend)

1. Run `git clone` to pull the source code

   ```bash
   git clone -b backend https://github.com/dzxrly/server-monitor.git
   ```

2. Enter the source code root

   ```bash
   cd server-monitor
   ```

3.
   - For **Linux**

      ```bash
      # Add executable permission
      chmod +x deploy.sh
      # Run deployment script
      ./deploy.sh
      ```

   - For **Windows**

     ```bash
     # Run the command below
     ./deploy.bat
     ```

### Run as Python program

1. Run `git clone` to pull the source code

   ```bash
   git clone -b backend https://github.com/dzxrly/server-monitor.git
   ```

2. Enter the source code root

   ```bash
   cd server-monitor
   ```

3. Create Python virtual environment (In this case, using `conda` as venv manager)

   ```bash
   conda create -n server-monitor
   ```

4. Change to the venv created in Step.1

   ```bash
   conda activate server-monitor
   ```

5. Install dependences

   ```bash
   pip install -r requirements.txt
   ```

6. Run `server.py`

   ```bash
   python server.py
   ```

7. Input `<your server IP>:<port>` in Serve Monitor website

## Config File

Config file is in the `./server_config.py`, all arguments are from the `serve` of `waitress`. Only
setting `host` & `port` by default. More config file info
in [waitress serve arguments docs](https://docs.pylonsproject.org/projects/waitress/en/latest/arguments.html#arguments).

---

<div align="center">

[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/eggtargaryen)

</div>

<div align="center">

by Egg Targaryen

</div>
