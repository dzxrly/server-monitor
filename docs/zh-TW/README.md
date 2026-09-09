<div align="center">

# Server Monitor 前端

</div>

<div align="center">

![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.version&prefix=V&style=flat-square&label=Version) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.dependencies.vue&style=flat-square&logo=vuedotjs&label=Vue&color=41a172) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.dependencies.quasar&style=flat-square&logo=quasar&label=Quasar&color=2fb6fd)

</div>

<div align="center">

基於 Vue 3 與 Quasar 的多伺服器監控面板，可同時監控 Windows 和 Linux 主機。目前前端使用後端統一的 API v1 指標快照，並完整支援明亮與暗黑主題。

</div>

<div align="center">

[简体中文](../../docs/zh-CN/README.md) | [繁體中文](../../docs/zh-TW/README.md) | [English](../../README.md)

</div>

> [!CAUTION]
>
> 使用前端監控伺服器狀態前，需要在每台受監控主機上部署[後端服務](https://github.com/dzxrly/server-monitor/blob/backend/docs/zh-TW/README.md)！

## 主要功能

- 緊湊且自適應的伺服器卡片，可在同一畫面顯示更多主機。
- 頁面、對話框、表格、控制項、載入和錯誤狀態均支援明亮與暗黑主題。
- 顯示 CPU、記憶體、NVIDIA GPU、溫度、所有掛載磁碟區、硬碟 I/O、所有網路介面和即時傳輸速率。
- 顯示每個邏輯核心的 CPU 佔用與頻率，使用純色背景，不使用模糊效果或填充動畫。
- 可設定 CPU、記憶體和 GPU 各自納入的高佔用程序數量，合併至一張可排序表格，預設依 CPU 佔用降冪排列。
- 提供緊湊、標準和詳細三種儀表板密度。
- 可設定更新週期、容量單位、溫度單位、使用率閾值和三種介面語言。
- 每台伺服器的每個更新週期只請求一次 `GET /api/v1/metrics`。

前端要求後端支援 API v1，未帶版本號的舊介面不再相容。

## 環境需求

- Node.js 24 或更新版本。
- npm 11 或更新版本。
- 每台受監控主機均已部署 [Server Monitor 後端](https://github.com/dzxrly/server-monitor/tree/backend)。

## 本機開發

```bash
git clone -b frontend https://github.com/dzxrly/server-monitor.git
cd server-monitor
npm ci
npm run dev
```

開發伺服器會輸出本機網址。在介面中新增後端基礎 URL，例如 `http://192.168.1.10:6543`；前端會自動附加 `/api/v1/metrics`。

## 正式環境建置

```bash
npm ci
npm run typecheck
npm test
npm run build
```

靜態 SPA 會輸出至 `dist/spa`。隨附的 Nginx 設定已包含 history 模式回退，直接開啟伺服器詳細資料 URL 也能正常載入。

## Docker 部署

```bash
docker build -t server-monitor-frontend .
docker run --rm -p 80:80 server-monitor-frontend
```

開啟 `http://localhost`，然後新增一個或多個後端基礎 URL。

## 設定與相容性

- 「每類資源納入程序表的數量」會控制 `processLimit` 查詢參數，允許範圍為 `1`–`50`。
- 可以遷移舊版前端匯出的設定；舊 GPU 類型欄位僅為匯入相容而保留，API v1 會自動辨識 NVIDIA 硬體。
- 設定和伺服器清單儲存在瀏覽器本機儲存空間，並可匯入或匯出為 JSON。
- 在伺服器詳細資料頁選單中可編輯名稱、基礎 URL、標籤顏色和儲存的 GPU 類型。儲存時保留原 UUID，修改 URL 後會立即請求新位址；若已暫停更新，則在恢復更新後請求。
- 瀏覽器會阻擋混合內容。HTTPS 前端無法直接請求 HTTP 後端，請統一通訊協定或使用反向代理。
- 使用者瀏覽器必須能路由到每個後端位址。將前端部署至公網並不會讓公網使用者自動存取內網後端。

## 品質檢查

```bash
npm run lint
npm run typecheck
npm test
npm run format:check
npm audit
```

---

<div align="center">

[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/eggtargaryen)

</div>

<div align="center">

by [Egg Targaryen](https://eggtargaryen.com)

</div>
