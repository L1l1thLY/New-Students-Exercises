# Docker笔记：安装 TensorFlow
## 前言
按照以下步骤通过 Docker 安装 TensorFlow：

1. [按照 Docker 文档中的说明在计算机上安装 Docker](https://blog.csdn.net/sangreallilith/article/details/81195045)。
2. （可选）[创建一个名为 docker 的 Linux 组](https://blog.csdn.net/sangreallilith/article/details/81254602)，以支持启动不带 sudo 的容器（如 Docker 文档中所述）。（如果不执行此步骤，则每次调用 Docker 时都必须使用 sudo。）
3. 要安装支持 GPU 的 TensorFlow 版本，您必须先安装 nvidia-docker（存储在 github 中）。
4. 启动包含某个 TensorFlow 二进制映像的 Docker 容器。
 
##  仅支持 CPU 
要启动仅支持 CPU（即不支持 GPU）的 Docker 容器，请输入以下格式的命令：

```
$ docker run -it -p hostPort:containerPort TensorFlowCPUImage
```

其中：

- `-p hostPort:containerPort` 是可选项。如果您想从 `shell` 运行 TensorFlow 程序，请省略此选项。如果您想从 `Jupiter` 笔记本运行 TensorFlow 程序，请将 `hostPort` 和 `containerPort` 设置为 `8888`。如果您想在容器内部运行 `TensorBoard`，请再添加一个 -p 标记，并将 `hostPort` 和 `containerPort` 设置为 `6006`。
- `TensorFlowCPUImage` 是必填项。它表示 Docker 容器。请指定如下某个值：
    1. `tensorflow/tensorflow`：TensorFlow CPU 二进制映像。
    2. `tensorflow/tensorflow:latest-devel`：最新的 TensorFlow CPU 二进制映像以及源代码。
    3. `tensorflow/tensorflow:version`：指定的 TensorFlow CPU 二进制映像版本（如 1.1.0rc1）。
    4. `tensorflow/tensorflow:version-devel`：指定的 TensorFlow GPU 二进制映像版本（如 1.1.0rc1）以及源代码。

例如，以下命令会在 Docker 容器中启动最新的 TensorFlow CPU 二进制映像，您可以通过该容器在 shell 中运行 TensorFlow 程序：

```
$docker run -it tensorflow/tensorflow bash
```

以下命令也可在 Docker 容器中启动最新的 TensorFlow CPU 二进制映像。但是，在这个 Docker 容器里，您可以通过 Jupyter Notebook 运行 TensorFlow 程序：

```
$ docker run -it -p 8888:8888 tensorflow/tensorflow
```

Docker 将在您第一次启动 TensorFlow 二进制映像时下载该映像。

## GPU支持
在安装支持 GPU 的 TensorFlow 之前，请确保您的系统满足所有 [NVIDIA 软件要求](https://www.tensorflow.org/install/install_linux#NVIDIARequirements)。要启动支持 Nvidia GPU 的 Docker 容器，请输入以下格式的命令：

```
$ nvidia-docker run -it -p hostPort:containerPort TensorFlowGPUImage
```

其中：

-p hostPort:containerPort 是可选项。如果您想从 shell 运行 TensorFlow 程序，请省略此选项。如果您想从 Jupiter 笔记本运行 TensorFlow 程序，请将 hostPort 和 containerPort 设置为 8888。
- TensorFlowGPUImage 用于指定 Docker 容器。您必须指定如下某个值：
    1. tensorflow/tensorflow:latest-gpu：最新的 TensorFlow GPU 二进制映像。
    2. tensorflow/tensorflow:latest-devel-gpu：最新的 TensorFlow GPU 二进制映像以及源代码。
    3. tensorflow/tensorflow:version-gpu：指定的 TensorFlow GPU 二进制映像版本（如 0.12.1）。
    4. tensorflow/tensorflow:version-devel-gpu：指定的 TensorFlow GPU 二进制映像版本（如 0.12.1）以及源代码。

我们建议安装最新 (latest) 的某个版本。例如，以下命令会在 Docker 容器中启动最新的 TensorFlow GPU 二进制映像，您可以通过该容器在 shell 中运行 TensorFlow 程序：

```
Usage: docker run [OPTIONS] IMAGE [COMMAND] [ARG...]  
 
  -d, --detach=false         指定容器运行于前台还是后台，默认为false   
  -i, --interactive=false   打开STDIN，用于控制台交互  
  -t, --tty=false            分配tty设备，该可以支持终端登录，默认为false  
  -u, --user=""              指定容器的用户  
  -a, --attach=[]            登录容器（必须是以docker run -d启动的容器）
  -w, --workdir=""           指定容器的工作目录 
  -c, --cpu-shares=0        设置容器CPU权重，在CPU共享场景使用  
  -e, --env=[]               指定环境变量，容器中可以使用该环境变量  
  -m, --memory=""            指定容器的内存上限  
  -P, --publish-all=false    指定容器暴露的端口  
  -p, --publish=[]           指定容器暴露的端口 
  -h, --hostname=""          指定容器的主机名  
  -v, --volume=[]            给容器挂载存储卷，挂载到容器的某个目录  
  --volumes-from=[]          给容器挂载其他容器上的卷，挂载到容器的某个目录
  --cap-add=[]               添加权限，权限清单详见：http://linux.die.net/man/7/capabilities  
  --cap-drop=[]              删除权限，权限清单详见：http://linux.die.net/man/7/capabilities  
  --cidfile=""               运行容器后，在指定文件中写入容器PID值，一种典型的监控系统用法  
  --cpuset=""                设置容器可以使用哪些CPU，此参数可以用来容器独占CPU  
  --device=[]                添加主机设备给容器，相当于设备直通  
  --dns=[]                   指定容器的dns服务器  
  --dns-search=[]            指定容器的dns搜索域名，写入到容器的/etc/resolv.conf文件  
  --entrypoint=""            覆盖image的入口点  
  --env-file=[]              指定环境变量文件，文件格式为每行一个环境变量  
  --expose=[]                指定容器暴露的端口，即修改镜像的暴露端口  
  --link=[]                  指定容器间的关联，使用其他容器的IP、env等信息  
  --lxc-conf=[]              指定容器的配置文件，只有在指定--exec-driver=lxc时使用  
  --name=""                  指定容器名字，后续可以通过名字进行容器管理，links特性需要使用名字  
  --net="bridge"             容器网络设置:
				                bridge 使用docker daemon指定的网桥     
				                host 	//容器使用主机的网络  
				                container:NAME_or_ID  >//使用其他容器的网路，共享IP和PORT等网络资源  
				                none 容器使用自己的网络（类似--net=bridge），但是不进行配置 
  --privileged=false         指定容器是否为特权容器，特权容器拥有所有的capabilities  
  --restart="no"             指定容器停止后的重启策略:
				                no：容器退出时不重启  
				                on-failure：容器故障退出（返回值非零）时重启 
				                always：容器退出时总是重启  
  --rm=false                 指定容器停止后自动删除容器(不支持以docker run -d启动的容器)  
  --sig-proxy=true           设置由代理接受并处理信号，但是SIGCHLD、SIGSTOP和SIGKILL不能被代理  
```


```
$ nvidia-docker run -it tensorflow/tensorflow:latest-gpu bash
```

以下命令也可在 Docker 容器中启动最新的 TensorFlow GPU 二进制映像。在这个 Docker 容器里，您可以通过 Jupyter Notebook 运行 TensorFlow 程序：

```
$ nvidia-docker run -it -p 8888:8888 tensorflow/tensorflow:latest-gpu
```

以下命令会安装旧版 TensorFlow (0.12.1)：

```
$ nvidia-docker run -it -p 8888:8888 tensorflow/tensorflow:0.12.1-gpu
```

## 验证安装
要验证您的 TensorFlow 安装，请执行以下操作：
1. 确保您的环境已准备好运行 TensorFlow 程序。
2. 运行一个简短的 TensorFlow 程序。

### 启动 Docker 容器以运行bash

```
$ docker run -it tensorflow/tensorflow bash
```

### 运行一个简短的 TensorFlow 程序
从 shell 中调用 Python，如下所示：

```
$ python
```

在 Python 交互式 shell 中输入以下几行简短的程序代码：

```
# Python
import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
```

如果系统输出以下内容，说明您可以开始编写 TensorFlow 程序了：

```
Hello, TensorFlow!
```




