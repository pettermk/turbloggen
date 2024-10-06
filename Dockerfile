FROM floryn90/hugo:0.121.2-busybox as builder

WORKDIR /src
COPY . .

RUN hugo

FROM nginx
COPY --from=builder /src/public /usr/share/nginx/html
