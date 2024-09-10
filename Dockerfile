FROM node:latest AS builder

WORKDIR /src
COPY ./ /src

RUN rm -rf /src/dist

RUN npm i -g @quasar/cli \
    && npm install \
    && quasar build

FROM nginx:latest

RUN mkdir /usr/share/nginx/front \
    && mkdir /usr/share/nginx/front/dist \
    && rm -rf /etc/nginx/nginx.conf

COPY --from=builder /src/nginx.conf /etc/nginx/nginx.conf

COPY --from=builder /src/dist/spa /usr/share/nginx/front/dist

EXPOSE 80
