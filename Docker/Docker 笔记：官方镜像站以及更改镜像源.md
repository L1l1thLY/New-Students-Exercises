# Docker 笔记：官方镜像站以及更改镜像源
Docker 通过镜像来创造容器，镜像的官方仓库地址为[Docker Hub](https://hub.docker.com)。

## 更改镜像源
通过 Docker 官方镜像加速，中国区用户能够快速访问最流行的 Docker 镜像。该镜像托管于中国大陆，本地用户现在将会享受到更快的下载速度和更强的稳定性，从而能够更敏捷地开发和交付 Docker 化应用。

Docker 中国官方镜像加速可通过 registry.docker-cn.com 访问。该镜像库只包含流行的公有镜像。私有镜像仍需要从美国镜像库中拉取。

可以使用以下命令直接从该镜像加速地址进行拉取：

```
docker pull registry.docker-cn.com/myname/myrepo:mytag
```

可以配置默认使用国内镜像加速：

修改 /etc/docker/daemon.json 文件并添加上 registry-mirrors 键值。

```
{
  "registry-mirrors": ["https://registry.docker-cn.com"]
}
```

重启 Docker 服务：

```
$ sudo service docker restart
```

测试镜像：

```
$ docker pull busybox
```

输出结果如下则成功：

```
Using default tag: latest
latest: Pulling from library/busybox
75a0e65efd51: Pull complete 
Digest: sha256:d21b79794850b4b15d8d332b451d95351d14c951542942a816eea69c9e04b240
Status: Downloaded newer image for busybox:latest
```

