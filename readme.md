# 构建docker容器

```shell
docker build -t sw_bi .
```

```shell
docker run -d --name sw_bi --net=bridge -p 13003:8000 sw_bi:latest
```