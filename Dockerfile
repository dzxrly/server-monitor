# 使用 Node.js 作为基础镜像
FROM node:20.14

# 设置工作目录
WORKDIR /src

# 复制项目文件到容器
COPY ./ /src

# 安装全局 Quasar CLI
RUN npm install -g @quasar/cli

# 安装项目依赖
RUN npm install

# 构建项目
RUN quasar build

# 安装 Nginx
RUN apt-get update && apt-get install -y nginx

# 移动构建后的文件到 Nginx 静态文件目录
RUN mkdir -p /usr/share/nginx/html && \
    cp -r /src/dist/spa/* /usr/share/nginx/html/

# 删除默认的 Nginx 配置文件并复制自定义配置
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/nginx.conf

# 暴露端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
