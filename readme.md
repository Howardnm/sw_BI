# 构建docker容器

```shell
docker build -t sw_bi . -f Dockerfile --no-cache
```

```shell
docker run -d \
--name sw_bi \
--net=bridge \
-p 13003:80 \
-e DJANGO_ALLOWED_HOSTS="bueess.top" \
-e DJANGO_CSRF_TRUSTED_ORIGINS="http://bueess.top:13003" \
-e DEBUG=False \
-e DJANGO_LOGLEVEL="info" \
howardnm/sw_bi:latest
```