# Docker 笔记：在 macOS 上 Docker Toolbox 与 Docker
## Docker Toolbox 环境
Docker Toolbox 安装`docker`，`docker-compose`和`docker-machine`在 Mac 的`usr/local/bin`路径下。此外，它还安装 VirtualBox。安装的时候，`docker-machine`会创造一个 VM 虚拟机并命名为 `defalut`，此虚拟机运行`boot2docker` linux 发行版。此发行版带有认证过的 Docker Engine。此发行版位于`$HOME/.docker/machine/machines/default`。

> `boot2docker`是基于 Tiny Core Linux 的轻量级 Linux 发行版，专为Docker 准备，完全运行于内存中，只有24M 大小，启动只需要5-6秒。

在 Mac 上使用`docker`和`docker-compose`之前，一般会使用`eval $(docker-machine env default)`设置环境变量，这样`docker`和`docker-compose`才能知道如何和在 VirtualBox 上运行的 Docker Engine 联络。

其结构如下图所示：

![](media/15331965268710/15331972596535.png)

## Docker for Mac 环境
Docker for Mac 环境属于原生的 Mac 应用，是安装在/Applications里的。安装的时候，它创建了位于`/usr/local/bin`的软连接：`docker`和`docker-compose`等等……实际上这些东西是软件包里的，位于`/Applications/Docker.app/Contents/Resources/bin`。  

有一些关键点是必须要知道的：  

- Docker for Mac 使用 HyperKit而不是 Virtual Box，它是 Mac 下的轻量级虚拟化技术，它基于优胜美地之后系统版本上的 Hypervisor.framework。
- 安装Docker for Mac，使用 Docker Machine 创造的虚拟机并不会受到影响。
- Docker for Mac 并不使用`docker-machine`来支持它的虚拟机。Docker Engine 的 API 是直接暴露在 Mac 的可使用的套接字上，其位于`/var/run/docker.sock`。当 Docker 和 Docker Compose 客户端连接 Docker 守护程序时，会默认访问这个位置。因此，只可以使用`docker`和`docker-compose`两个命令。

结构如下图所示：

![](media/15331965268710/15331981506060.png)

使用 Docker for Mac，你只有（并且只需要）一个虚拟机，这个虚拟机由 Docker for Mac 管理。Docker for Mac 会自动更新可用的 Docker 更新（包括客户端和守护程序）。  

如果你需要多个虚拟机，比如说需要测试多节点集群的时候，你可以继续使用 Docker Machine，它运行于Docker for Mac之外。为了达到这个目的，应该参考[使 Docker Toolbox 与 Docker for Mac 共存](https://docs.docker.com/docker-for-mac/docker-toolbox/#docker-toolbox-and-docker-for-mac-coexistence)。

### 设置使用 Docker for Mac
1.检查 ToolBox DOCKER 环境变量是否设置了：

```
 $ env | grep DOCKER
 DOCKER_HOST=tcp://192.168.99.100:2376
 DOCKER_MACHINE_NAME=default
 DOCKER_TLS_VERIFY=1
 DOCKER_CERT_PATH=/Users/<your_username>/.docker/machine/machines/default
```

如果什么输出都没有，那当前使用的就是 Docker for Mac，跳过第二步。  

如果输出像上面展示的那样，需要删除`DOCKER`环境变量使客户端连接 Docker for Mac Engine。如下步所示。

2.使用`unset`命令来删除环境变量。

```
 unset DOCKER_TLS_VERIFY
 unset DOCKER_CERT_PATH
 unset DOCKER_MACHINE_NAME
 unset DOCKER_HOST
```

> 注意：有些人用一个一打开命令窗就会设置`DOCKER`环境变量的脚本。那想用 Docker for Mac 就得每次都得删除这些环境变量。
> 如果在安装 Docker Toolbox 之后才安装了 Docker for Mac，那么后者会把`/usr/local/bin`下面的`docker`和`docker-compose`替换成自己的版本（指向`/Applications/Docker.app/Contents/Resources/bin`路径下命令的软连接）。

## Docker Toolbox 与 Docker for Mac 共存
同一台机子上两者可以共存，当你想用后者，只需要删除环境变量。当你想要使用一个或多个 Virtual Box 虚拟机，只需要运行`eval $(docker-machine env default)` (或者目标虚拟机的名字）。这会切换当前的命令行连接至特定的 ToolBox 虚拟机。  

如下图所示：

![](media/15331965268710/15331992152291.png)

## 使用不同的 Docker Tools 版本
只有 Virtual Box 虚拟机和 Docker for Mac 运行的是同一个版本的引擎才能使用共存的安装模式。如果你需要使用虚拟机来安装老版本的 Docker 引擎，那么需要使用 Docker Version Manager 来管理多个 Docker 客户端。

### 检查组件版本

理想化状态下，Docker 的命令行客户端和 Docker 引擎应该是同一个版本。如果版本号不同，可能会导致一些问题（客户端无法连接服务器或宿主机）。  

如果你已经安装了 Docker Toolbox，又安装了 Docker for Mac，你可能会得到一个更高版本的 Docker 客户端。使用`docker version`检查客户端和服务器的版本。

```
$ docker version
Client:
Version:      1.11.1
...

Server:
Version:      1.11.0
...
```

同样的，如果你使用 Toolbox 系列安装了 Docker Machine 接着安装了或更新了 Docker for Max，你可以会有一个虚拟机使用不同的

...

## 从 Docker Toolbox 继承到 Docker for Mac
## 卸载 Docker Toolbox

