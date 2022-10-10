FROM klakegg/hugo:0.101.0-busybox as builder

WORKDIR /src
COPY . .

RUN hugo

FROM nginx
COPY --from=builder /src/public /usr/share/nginx/html
