<div align="center">

# Server Monitor Frontend

</div>

<div align="center">

![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.version&prefix=V&style=flat-square&label=Version) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.dependencies.vue&style=flat-square&logo=vuedotjs&label=Vue&color=41a172) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.dependencies.quasar&style=flat-square&logo=quasar&label=Quasar&color=2fb6fd)

</div>

<div align="center">

A Vue 3 and Quasar dashboard for monitoring multiple Windows and Linux servers. The current frontend uses the backend's single API v1 metrics snapshot and supports complete light and dark themes.

</div>

<div align="center">

[简体中文](./docs/zh-CN/README.md) | [繁體中文](./docs/zh-TW/README.md) | [English](./README.md)

</div>

> [!CAUTION]
>
> To monitor server status from the frontend, deploy the [Backend Service](https://github.com/dzxrly/server-monitor/blob/backend/README.md) on every monitored host.

## Highlights

- Compact responsive server cards for displaying more hosts on one screen.
- Light and dark themes across pages, dialogs, tables, controls, and loading/error states.
- CPU, memory, NVIDIA GPU, temperature, every mounted volume, disk I/O, every network interface, and transfer-rate panels.
- Configurable top CPU, memory, and GPU process counts merged into one sortable table, ordered by CPU usage by default.
- Compact, standard, and detailed dashboard density settings.
- Configurable refresh interval, byte units, temperature units, thresholds, and three UI languages.
- One `GET /api/v1/metrics` request per server per refresh cycle.

The frontend requires an API v1 backend. Legacy unversioned endpoints are no longer supported.

## Requirements

- Node.js 24 or newer.
- npm 11 or newer.
- A deployed [Server Monitor backend](https://github.com/dzxrly/server-monitor/tree/backend) on each monitored host.

## Local development

```bash
git clone -b frontend https://github.com/dzxrly/server-monitor.git
cd server-monitor
npm ci
npm run dev
```

The development server prints its local URL. Add a server in the UI using the backend base URL, for example `http://192.168.1.10:6543`; the frontend appends `/api/v1/metrics` itself.

## Production build

```bash
npm ci
npm run typecheck
npm test
npm run build
```

The static SPA is written to `dist/spa`. The included Nginx configuration has history-mode fallback for direct detail-page navigation.

## Docker deployment

```bash
docker build -t server-monitor-frontend .
docker run --rm -p 80:80 server-monitor-frontend
```

Open `http://localhost` and add one or more backend base URLs.

## Settings and compatibility

- `Processes per resource included in the table` controls the `processLimit` query parameter and accepts `1`–`50`.
- Existing configuration exported by the previous frontend is migrated; the old GPU type field is retained only for import compatibility because API v1 auto-detects NVIDIA hardware.
- Settings and server entries are stored in browser local storage and can be exported/imported as JSON.
- Browsers block mixed content. An HTTPS frontend cannot directly request an HTTP backend; use matching protocols or a reverse proxy.
- A user's browser must be able to route to every backend URL. A public frontend URL does not make private backend addresses reachable from outside that private network.

## Quality checks

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
