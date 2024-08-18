<div align="center">

# Server Monitor 後端

</div>

<div align="center">

![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Fbackend%2Finfo.json&query=%24.version&prefix=V&style=flat-square&label=Version)

</div>

<div align="center">

這是Server Monitor的後端。請在需要監控硬體狀態的伺服器上部署該後端，預設狀態下後端使用`6543`端口，請確保防火牆放行該端口！

</div>

<div align="center">

[简体中文](../../docs/zh-CN/README.md) | [繁體中文](../../docs/zh-TW/README.md) | [English](../../README.md)

</div>

> [!CAUTION]
>
> 完成後端部署後需要部署[前端網站](https://github.com/dzxrly/server-monitor/blob/frontend/docs/zh-TW/README.md)
> 以監控伺服器硬體狀態！

## 後端部署

### 使用一鍵部署腳本（推薦）

1. 使用`git clone`拉取後端源碼

   ```bash
   git clone -b backend https://github.com/dzxrly/server-monitor.git
   ```

2. 進入源碼目錄

   ```bash
   cd server-monitor
   ```

3.
    - 對於**Linux**

      ```bash
      # 授予腳本可執行權限
      chmod +x deploy.sh
      # 運行部署腳本
      ./deploy.sh
      ```

    - 對於**Windows**

      ```bash
      # 直接運行以下命令
      ./deploy.bat
      ```

### 手動構建

1. 使用`git clone`拉取後端源碼

   ```bash
   git clone -b backend https://github.com/dzxrly/server-monitor.git
   ```

2. 進入源碼目錄

   ```bash
   cd server-monitor
   ```

3. 創建虛擬環境（此處使用`conda`舉例，並非一定要使用該虛擬環境管理器）

   ```bash
   conda create -n server-monitor
   ```

4. 切換至步驟1創建的虛擬環境

   ```bash
   conda activate server-monitor
   ```

5. 安裝依賴庫

   ```bash
   pip install -r requirements.txt
   ```

6. 運行`server.py`開啟後端伺服器

   ```bash
   python server.py
   ```

7. 完成部署後在網站輸入`你的伺服器IP:端口號`即可

## 配置文件設置

配置文件位於`./server_config.py`中，其中字段均為`waitress`的`serve`函數可接受字段，預設僅設置了`host`與`port`
，具體配置請參考：[waitress serve arguments docs](https://docs.pylonsproject.org/projects/waitress/en/latest/arguments.html#arguments)。

---

<div align="center">

[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/eggtargaryen)

</div>

<div align="center">

by Egg Targaryen

</div>
