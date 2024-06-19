<div align="center">

# Server Monitor 前端

</div>

<div align="center">

![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.version&prefix=V&style=flat-square&label=Version) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.dependencies.vue&style=flat-square&logo=vuedotjs&label=Vue&color=41a172) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdzxrly%2Fserver-monitor%2Ffrontend%2Fpackage.json&query=%24.dependencies.quasar&style=flat-square&logo=quasar&label=Quasar&color=2fb6fd)

</div>

<div align="center">

这是一个在线服务器硬件状态监控网站的前端部分，可以通过`docker`构建与部署。

</div>

## 部署

1. 拉取前端部分源码

   ```bash
   git clone -b frontend https://github.com/dzxrly/server-monitor.git
   ```

2. 进入源码根目录

   ```bash
   cd server-monitor
   ```

3. 使用`docker buildx`构建镜像

   ```bash
   docker buildx build -t eggtargaryen/server-monitor .
   ```

4. 运行该镜像

   ```bash
   docker run -p 80:80 eggtargaryen/server-monitor
   ```

## 从源码手动构建（可选）

1. 拉取前端部分源码

   ```bash
   git clone -b frontend https://github.com/dzxrly/server-monitor.git
   ```

2. 进入源码根目录

   ```bash
   cd server-monitor
   ```

3. 安装`quasar/cli`

   ```bash
   npm install -g @quasar/cli
   ```

4. 安装其他依赖库

   ```bash
   npm install
   ```

5. 使用`quasar/cli`构建

   ```bash
   quasar build
   ```

6. 入口文件`index.html`位于`./dist/spa`目录下

## 注意事项

- 受限于浏览器安全设置，请确保前端与后端均采用同一协议，例如前端与后端均为`http`或均为`https`，混用协议可能导致请求被浏览器拦截
- 同样受限于浏览器安全设置，如果前端部署于公网网段，而后端部署于内网网段，则无法正常建立通信

## i18n

| 语言代码 | 支持情况 |                文本文件位置                 |
| :------: | :------: | :-----------------------------------------: |
|  zh-CN   |    ✅    | [zh-CN/index.ts](./src/i18n/zh-CN/index.ts) |
|  en-US   |    ✅    | [en-US/index.ts](./src/i18n/en-US/index.ts) |

---

<div align="center">

[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/eggtargaryen)

</div>

<div align="center">

by Egg Targaryen

</div>
