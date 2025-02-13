# 构建docker容器

```shell
docker build -t sw_BI .
```

```shell
docker run -d --name sw_bi --net=bridge -p 8000:8000 django-docker:latest
```