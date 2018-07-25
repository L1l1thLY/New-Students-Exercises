# Docker笔记：介绍、安装、卸载、更新
## Docker 版本介绍
目前Docker提供两种版本，Community版本和企业版本。
其区别如下：

| 功能 |  Community Edition | Enterprise Edition Basic | Enterprise Edition Standard | Enterprise Edition Advanced |
| --- | --- | --- | --- | --- |
| 容器引擎；内置的编排功能（built in orchestration，在集群上部署多容器应用）；网络功能；安全功能； | √ | √ | √ | √ |
| 认证的基础架构；插件和ISV容器 | | √ | √ | √ |
| 镜像管理（私有的docker registry，caching）| | | √ | √|
| 容器应用管理数据中心 | | | √ | √|
| 镜像安全扫描 | | | | √ |
## Community 版本介绍
CE支持多种系统平台，详情参考：[支持系统](https://docs.docker.com/install/#supported-platforms)。

## 安装
安装说明文档：[Ubuntu安装说明](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
### 卸载旧版本的Docker
老版本的Docker直接命名为`docker`或`docker-engine`。如果系统安装了老版本，应该首先删除掉。

```
$sudo apt-get remove docker docker-engine docker.io
```

尝试运行这条指令，如果系统提示这些软件没有被安装，则可进行下一步。
已经存在于`/var/lib/docker/`的内容会被留下，包括镜像、容器、卷和网络。目前新的Community版本Docker名字为`docker-ce`。
### 支持的存储驱动
Ubuntu的CE版本支持`overlay2`和`aufs`存储驱动。  

- 版本4以上的kernel，`overlay2`优先级高于`aufs`
- 版本3的内核仅仅支持`aufs`

### 安装Docker CE
多种方式可以安装Docker CE：

- 大多数用户会使用添加Docker的repository安装，这简化了安装和更新的过程。推荐使用这种方式安装。
- 也可以下载DEB包然后手动安装，并且手动配置更新。当你在一个air-gapped系统（不通过任何方式连接互联网的系统）里安装Docker的时候这种方式会比较有用。
- 在测试和开发环境中，也有用户使用自动脚本安装Docker。

#### 使用repository安装
初次安装Docker CE需要设置Docker的repository，然后就可以通过repository进行安装了。
##### 设置repository
-  升级`apt`包目录

```
$ sudo apt-get update
```

- 安装组件使`apt`支持HTTPS repository：

```
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
```

- 添加Docker官方的GPG公钥

```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

添加后确定已经添加过指纹为`9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88`的公钥。

```
$ sudo apt-key fingerprint 0EBFCD88

pub   4096R/0EBFCD88 2017-02-22
      Key fingerprint = 9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
uid                  Docker Release (CE deb) <docker@docker.com>
sub   4096R/F273FCD8 2017-02-22
```

- 设置`stable`repository。

```
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

- 安装

```
$ sudo apt-get update
$ sudo apt-get install docker-ce
```

安装特定版本的命令如下：

```
//查看repo中可用的版本
$ apt-cache madison docker-ce

docker-ce | 18.03.0~ce-0~ubuntu | https://download.docker.com/linux/ubuntu xenial/stable amd64 Packages

//输入完整的包名来安装特定版本的docker
//例子：docker-ce=18.03.0~ce-0~ubuntu
$ sudo apt-get install docker-ce=<VERSION>
```

- 确定安装成功：

```
$ sudo docker run hello-world
```

这个命令会下载一个测试镜像并运行在一个容器中，容器运行时打印一个消息后退出。

### 更新
更新`apt`后选择安装最新版本的docker即可。

```
$sudo apt-get update
```

### 卸载Docker

卸载Docker CE包：

```
$ sudo apt-get purge docker-ce
```

删除镜像，容器，卷以及其他配置文件：

```
$ sudo rm -rf /var/lib/docker
```

