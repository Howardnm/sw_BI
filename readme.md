# 构建docker容器

```shell
docker build -t sw_bi . -f Dockerfile --no-cache
```

```shell
docker run -d \
--name sw_bi \
--network op_network \
-p 13003:80 \
-e DJANGO_ALLOWED_HOSTS="bueess.top" \
-e DJANGO_CSRF_TRUSTED_ORIGINS="http://bueess.top:13003" \
-e DEBUG=False \
-e DJANGO_LOGLEVEL="info" \
-e MY_SQL_HOST="mysql_8.0.40" \
-e MY_SQL_PORT=3306 \
-e MY_SQL_PASSWORD="xxx" \
howardnm/sw_bi:latest
```