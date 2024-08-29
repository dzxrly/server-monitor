<div align="center">

# Server Monitor Frontend

</div>

<div align="center">

![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.version&prefix=V&style=flat-square&label=Version) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.dependencies.vue&style=flat-square&logo=vuedotjs&label=Vue&color=41a172) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.dependencies.quasar&style=flat-square&logo=quasar&label=Quasar&color=2fb6fd)

</div>

<div align="center">

This is the frontend of Server Monitor, which can be built and deployed using `docker`.

</div>

<div align="center">

[简体中文](./docs/zh-CN/README.md) | [繁體中文](./docs/zh-TW/README.md) | [English](./README.md)

</div>

> [!CAUTION]
>
> To monitor the server status on the frontend, the [Backend Service](https://github.com/dzxrly/server-monitor/blob/backend/README.md) needs to be deployed on each monitored server.！

## Deployment

### Build from Docker (Recommend)

1. Pull the frontend source code

   ```bash
   git clone -b frontend https://github.com/dzxrly/server-monitor.git
   ```

2. Enter the root directory of the source code

   ```bash
   cd server-monitor
   ```

3. Run `docker buildx` to build container

   ```bash
   docker buildx build --no-chache -t eggtargaryen/server-monitor .
   ```

4. Run the container

   ```bash
   docker run -p 80:80 eggtargaryen/server-monitor
   ```

### Build from the source code

1. Pull the frontend source code

   ```bash
   git clone -b frontend https://github.com/dzxrly/server-monitor.git
   ```

2. Enter the root directory of the source code

   ```bash
   cd server-monitor
   ```

3. Install `quasar/cli`

   ```bash
   npm install -g @quasar/cli
   ```

4. Install other dependences

   ```bash
   npm install
   ```

5. Build by `quasar/cli`

   ```bash
   quasar build
   ```

6. Entry file `index.html` is in the `./dist/spa`

## Notes

- Due to browser security settings, please ensure that both the frontend and backend use the same protocol, such as both using http or both using https. Mixing protocols may cause requests to be blocked by the browser.
- Similarly, due to browser security settings, if the frontend is deployed in a public network segment while the backend is deployed in a private network segment, communication cannot be established properly.

---

<div align="center">

[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/eggtargaryen)

</div>

<div align="center">

by [Egg Targaryen](https://eggtargaryen.com)

</div>
