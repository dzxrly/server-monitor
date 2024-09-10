<div align="center">

# Server Monitor 前端

</div>

<div align="center">

![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.version&prefix=V&style=flat-square&label=Version) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.dependencies.vue&style=flat-square&logo=vuedotjs&label=Vue&color=41a172) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.dependencies.quasar&style=flat-square&logo=quasar&label=Quasar&color=2fb6fd)

</div>

<div align="center">

這是 Server Monitor 的前端部分，可以透過`docker`構建與部署。

</div>

<div align="center">

[简体中文](../../docs/zh-CN/README.md) | [繁體中文](../../docs/zh-TW/README.md) | [English](../../README.md)

</div>

> [!CAUTION]
>
> 在前端監控伺服器狀態需要在每台被監控的伺服器上部署[後端服務](https://github.com/dzxrly/server-monitor/blob/backend/docs/zh-TW/README.md)！

## 部署

### 從 Docker 構建（推薦）

1. 拉取前端部分原始碼

   ```bash
   git clone -b frontend https://github.com/dzxrly/server-monitor.git
   ```

2. 進入原始碼根目錄

   ```bash
   cd server-monitor
   ```

3. 使用`docker buildx`構建鏡像

   ```bash
   docker buildx build --no-cache -t eggtargaryen/server-monitor .
   ```

4. 運行該鏡像

   ```bash
   docker run -p 80:80 eggtargaryen/server-monitor
   ```

### 從原始碼手動構建

1. 拉取前端部分原始碼

   ```bash
   git clone -b frontend https://github.com/dzxrly/server-monitor.git
   ```

2. 進入原始碼根目錄

   ```bash
   cd server-monitor
   ```

3. 安裝`quasar/cli`

   ```bash
   npm install -g @quasar/cli
   ```

4. 安裝其他依賴庫

   ```bash
   npm install
   ```

5. 使用`quasar/cli`構建

   ```bash
   quasar build
   ```

6. 入口文件`index.html`位於`./dist/spa`目錄下

## 注意事項

- 受限於瀏覽器安全設置，請確保前端與後端均採用同一協議，例如前端與後端均為`http`或均為`https`，混用協議可能導致請求被瀏覽器攔截。
- 同樣受限於瀏覽器安全設置，如果前端部署於公網網段，而後端部署於內網網段，則無法正常建立通信。

---

<div align="center">

[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/eggtargaryen)

</div>

<div align="center">

by [Egg Targaryen](https://eggtargaryen.com)

</div>
