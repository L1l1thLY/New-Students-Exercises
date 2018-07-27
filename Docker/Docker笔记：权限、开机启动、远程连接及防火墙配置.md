# Docker笔记：权限、开机启动、远程连接及防火墙配置
## 权限设置
`docker`的守护进程是绑定在 Unix 套接字上的而并非使用 TCP 端口。Unix 套接字默认是 root 拥有的，普通用户只能使用`sudo`才能使用。`docker`的守护进程一般是作为`root`用户运行的。  
如果你不想在使用`docker`命令的时候频繁输入`sudo`，创建一个叫做`docker`的 Unix 用户组，并且添加用户。等`docker`守护进程开始运行时，可以使`docker`用户组的用户可以自由读写 Unix 套接字。

> Warning: The docker group grants privileges equivalent to the root user. For details on how this impacts security in your system, see [Docker Daemon Attack Surface.](https://docs.docker.com/engine/security/security/#docker-daemon-attack-surface)

- 创建`docker`用户组：

```
$sudo groupadd docker
```

- 添加用户：

```
$sudo usermod -aG docker $USER
# -a|--append  把用户追加到某些组中，仅与-G选项一起使用 
# -G|--groups  把用户追加到某些组中，仅与-a选项一起使用 
```

> -a|--append  ##把用户追加到某些组中，仅与-G选项一起使用 
-c|--comment ##修改/etc/passwd文件第五段comment 
-d|--home    ##修改用户的家目录通常和-m选项一起使用 
-e|--expiredate  ##指定用户帐号禁用的日期，格式YY-MM-DD 
-f|--inactive    ##用户密码过期多少天后采用就禁用该帐号，0表示密码已过期就禁用帐号，-1表示禁用此功能，默认值是-1 
-g|--gid     ##修改用户的gid，改组一定存在
-G|--groups  ##把用户追加到某些组中，仅与-a选项一起使用 
-l|--login   ##修改用户的登录名称 
-L|--lock    ##锁定用户的密码 
-m|--move-home   ##修改用户的家目录通常和-d选项一起使用 
-s|--shell   ##修改用户的shell 
-u|--uid     ##修改用户的uid，该uid必须唯一 
-U|--unlock  ##解锁用户的密码 

- `logout`后重新登入使群组设置生效。虚拟机需要重新启动使设置生效。
- 确定你可以不使用`sudo`命令使用`docker`

```
$ docker run hello-world
```

如果在增加用户组之前就使用命令行运行`docker`，并且是加了`sudo`的，那么可能会造成下面的错误。

```
WARNING: Error loading config file: /home/user/.docker/config.json -
stat /home/user/.docker/config.json: permission denied
```

这是因为创建`~/.docker/`的时候使用了`sudo`以至于使权限出错。想要解决这个问题，可以直接删除这个文件夹（但会丢失个人设置）。或者更改它的权限：

```
$ sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
$ sudo chmod g+rwx "/home/$USER/.docker" -R
```

## 开机启动
RHEL, CentOS, Fedora, Ubuntu 16.04 以及更高版本使`systemd`管理开机启动服务。Ubuntu 14.10以下版本使用`upstart`（无需设置，自动开机启动）。

```
$ sudo systemctl enable docker
$ sudo systemctl disable docker
```

## 更改 Docker 监听位置
默认 Docker 只通过 Unix 套接字监听本地的客户端。可以设置 Docker 监听某个 IP 的某个端口或者其他系统的 Unix 套接字，详细参阅：[Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/dockerd/)。  
设置 Docker 接受远程连接，可以使用`docker.service`，这是一个 systemd 组件（只在支持此组件上的系统上使用）。不支持此组件的西永，可以使用`deamon.json`。

### systemd
- `sudo systemctl edit docker.service`打开配置文件。
- 增加或修改以下行：

```
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://127.0.0.1:2375
```

- 保存
- 重新载入`systemctl`配置：

```
$ sudo systemctl daemon-reload
```

- 重启 Docker

```
$ sudo systemctl restart docker.service
```

- 检查更改是否生效：

```
$ sudo netstat -lntp | grep dockerd
tcp        0      0 127.0.0.1:2375          0.0.0.0:*    
```
## 防火墙配置
如果 Docker 运行的主机上运行有防火墙，并且需要被远程连接，需要设置防火墙的准入。一般加密端口是`2376`，非加密端口是`2375`。

### UFW
乌班图一般使用此防火墙，设置`DEFAULT_FORWARD_POLICY="ACCEPT"`即可。
### firewalld
增加规则：

```
<direct>
  [ <rule ipv="ipv6" table="filter" chain="FORWARD_direct" priority="0"> -i zt0 -j ACCEPT </rule> ]
  [ <rule ipv="ipv6" table="filter" chain="FORWARD_direct" priority="0"> -o zt0 -j ACCEPT </rule> ]
</direct>
```

## 其他配置
[更改存储驱动](https://docs.docker.com/engine/userguide/storagedriver/imagesandcontainers/)
[启动 IPv6 ](https://docs.docker.com/config/daemon/ipv6/)
[内核兼容性、配置 DNS等](https://docs.docker.com/install/linux/linux-postinstall/#troubleshooting)

