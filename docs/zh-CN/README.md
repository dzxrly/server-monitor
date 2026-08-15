# Server Monitor 前端

基于 Vue 3 与 Quasar 的多服务器监控面板，可同时监控 Windows 和 Linux 主机。当前前端使用后端统一的 API v1 指标快照，并完整支持明亮与暗黑主题。

[简体中文](./README.md) | [繁體中文](../zh-TW/README.md) | [English](../../README.md)

## 主要功能

- 紧凑且自适应的服务器卡片，可在同一屏幕展示更多主机。
- 页面、对话框、表格、控件、加载和错误状态均支持明亮与暗黑主题。
- 展示 CPU、内存、NVIDIA GPU、温度、所有挂载卷、硬盘 I/O、所有网卡和网络实时速率。
- 可设置 CPU、内存和 GPU 各自显示的高占用进程数量，并在对应资源面板下展示。
- 提供紧凑、标准和详细三种仪表盘密度。
- 可配置刷新周期、容量单位、温度单位、使用率阈值和三种界面语言。
- 每台服务器的每个刷新周期只请求一次 `GET /api/v1/metrics`。

前端要求后端支持 API v1，未带版本号的旧接口不再兼容。

## 环境要求

- Node.js 24 或更高版本。
- npm 11 或更高版本。
- 每台被监控主机均已部署 [Server Monitor 后端](https://github.com/dzxrly/server-monitor/tree/backend-dev)。

## 本地开发

```bash
git clone -b frontend-dev https://github.com/dzxrly/server-monitor.git
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

- “每类资源显示的高占用进程数”会控制 `processLimit` 查询参数，允许范围为 `1`–`50`。
- 可以迁移旧版前端导出的配置；旧 GPU 类型字段仅为导入兼容而保留，API v1 会自动识别 NVIDIA 硬件。
- 设置和服务器列表保存在浏览器本地存储中，并可导入或导出为 JSON。
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
