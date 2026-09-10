<div align="center">

# Server Monitor 前端

</div>

<div align="center">

![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.version&prefix=V&style=flat-square&label=Version) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.dependencies.vue&style=flat-square&logo=vuedotjs&label=Vue&color=41a172) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.dependencies.quasar&style=flat-square&logo=quasar&label=Quasar&color=2fb6fd)

</div>

<div align="center">

基于 Vue 3 与 Quasar 的多服务器监控面板，可同时监控 Windows 和 Linux 主机。当前前端使用后端统一的 API v1 指标快照，并完整支持明亮与暗黑主题。

</div>

<div align="center">

[简体中文](../../docs/zh-CN/README.md) | [繁體中文](../../docs/zh-TW/README.md) | [English](../../README.md)

</div>

> [!CAUTION]
>
> 使用前端监控服务器状态前，需要在每台被监控主机上部署[后端服务](https://github.com/dzxrly/server-monitor/blob/backend/docs/zh-CN/README.md)！

## 主要功能

- 紧凑且自适应的服务器卡片，可在同一屏幕展示更多主机。
- 页面、对话框、表格、控件、加载和错误状态均支持明亮与暗黑主题。
- 展示 CPU、内存、NVIDIA GPU、温度、所有挂载卷、硬盘 I/O、所有网卡和网络实时速率。
- 展示每个逻辑核心的 CPU 占用和频率，使用纯色背景和流畅的占用过渡动画，并遵循系统的减少动态效果设置。
- 同时展示内存和 Swap 的使用率、已用/总容量，以及可用内存和剩余 Swap 容量。
- 首页存储摘要优先展示 Linux 的 `/` 或 Windows 的 `C:`；未上报系统卷时，显示已上报卷中占用率最高的一项。
- 硬盘详情按总容量从大到小排列挂载卷，容量相同时按挂载路径排序。
- 硬盘容量按数值大小自动选择 B、KB、MB、GB、TB、PB 或 EB；内存、Swap 和显存使用设置中的单位，可选范围为 B 到 EB。
- 可设置 CPU、内存和 GPU 各自纳入的高占用进程数量，合并至一张可排序表格，默认按 CPU 占用降序排列。
- 提供紧凑、标准和详细三种仪表盘密度。
- 可配置刷新周期、容量单位、温度单位、使用率阈值和三种界面语言。
- 每台服务器的每个刷新周期只请求一次 `GET /api/v1/metrics`。

前端要求后端支持 API v1，未带版本号的旧接口不再兼容。

## 环境要求

- Node.js 24 或更高版本。
- npm 11 或更高版本。
- 每台被监控主机均已部署 [Server Monitor 后端](https://github.com/dzxrly/server-monitor/tree/backend)。

## 本地开发

```bash
git clone -b frontend https://github.com/dzxrly/server-monitor.git
cd server-monitor
npm ci
npm run dev
```

开发服务器会输出本地访问地址。在界面中添加后端基础 URL，例如 `http://192.168.1.10:6543`；前端会自动追加 `/api/v1/metrics`。

## 生产构建

```bash
npm ci
npm run typecheck
npm test
npm run build
```

静态 SPA 输出到 `dist/spa`。随附的 Nginx 配置已包含 history 模式回退，直接打开服务器详情 URL 也能正常加载。

## Docker 部署

```bash
docker build -t server-monitor-frontend .
docker run --rm -p 80:80 server-monitor-frontend
```

打开 `http://localhost`，随后添加一个或多个后端基础 URL。

## 设置与兼容性

- “每类资源纳入进程表的数量”会控制 `processLimit` 查询参数，允许范围为 `1`–`50`。
- 可以迁移旧版前端导出的配置；旧 GPU 类型字段仅为导入兼容而保留，API v1 会自动识别 NVIDIA 硬件。
- 设置和服务器列表保存在浏览器本地存储中，并可导入或导出为 JSON。
- 在服务器详情页菜单中可编辑名称、基础 URL、标签颜色和保存的 GPU 类型。保存时保留原 UUID，修改 URL 后会立即请求新地址；若已暂停刷新，则在恢复刷新后请求。
- 浏览器会拦截混合内容。HTTPS 前端不能直接请求 HTTP 后端，请统一协议或使用反向代理。
- 用户浏览器必须能够路由到每个后端地址。将前端部署在公网并不会让公网用户自动访问到内网后端。

## 质量检查

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
