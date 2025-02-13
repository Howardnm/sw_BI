# 构建docker容器

```shell
docker build -t sw_bi .
```

```shell
docker run -d \
--name sw_bi \
--net=bridge \
-p 13003:8000 \
-e DJANGO_ALLOWED_HOSTS="bueess.top" \
-e DEBUG="True" \
-e DJANGO_LOGLEVEL="info" \
sw_bi:latest
```