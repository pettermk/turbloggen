FROM debian:bookworm-slim as gpx-processor

# Copy uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /src
COPY . .

# Downsample large GPX files
RUN chmod +x scripts/downsample_large_gpx.sh && \
    scripts/downsample_large_gpx.sh 300000 10

FROM floryn90/hugo:0.121.2-busybox as builder

WORKDIR /src
COPY --from=gpx-processor /src .

RUN hugo

FROM nginx
COPY --from=builder /src/public /usr/share/nginx/html
