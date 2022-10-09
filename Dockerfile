FROM klakegg/hugo:0.101.0-busybox

WORKDIR /src
COPY . .

EXPOSE 1313
