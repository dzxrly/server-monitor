FROM node:24-alpine AS builder

WORKDIR /src
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /src/dist/spa /usr/share/nginx/html

EXPOSE 80
