# Docker 笔记：Dockerfile 基础
## 一个 Dockerfile 文件的简单模式
首先是类似于`.gitignore` 文件的`.dockerignore`文件。此文件会使 Dockerfile 不再管理一些文件：

```
.git
node_modules
npm-debug.log
```

## Dockerfile
Docker 可以根据`Dockerfile`，自动生成镜像。这个是一个文本文档包括一些用来用来组装镜像的。
### 用法
`docker build` 通过 `Dockerfile` 及其附属内容来创造一个镜像。所谓的附属内容是一个文件集合，位于 `PATH` 或 `URL` 规定的位置。`PATH` 是一个你本地文件系统的目录，`URL` 是 Git 仓库地址。

对于附属内容的操作是递归完成的，所以一个`PATH`包括子目录，`URL` 也包括其仓库和子模块。下面这个例子表示一个`build`命令使用当前目录作为附属内容：

```
$ docker build .
Sending build context to Docker daemon  6.51 MB
...
```

`build`命令是由 Docker 守护程序执行的，而不是命令行。`build`过程第一件事情就是把所有的附属内容递归地发送给守护程序。在大多数情况下，最好用一个空文件夹作为附属内容，并且把 Dockerfile 放在这个文件夹里。

> 注意： 不要使用根目录`/`作为`PATH`，因为这会使`build`把整个硬盘内容发送给 Docker 守护程序。

为了使用位于附属内容中的文件，`Dockerfile`使用一些命令来操作这些文件，举个例子，一个`COPY`命令。为了提高 `build` 的性能，在附属内容中编写一个 `.dockerignore` 文件来排除一些没用的文件。

一般大多数人都会把 Dockerfile 文件起名叫 `Dockerfile`，放在附属内容的根目录。在使用`docker build`命令的时候，添加 `-f` 参数来指定文件系统里任何一个 Dockerfile。

```
$ docker build -f /path/to/a/Dockerfile .
```

你可以标记一个仓库来储存 `build` 出来的新的镜像：

```
$ docker build -t shykes/myapp .
```

可以把同一个镜像标记为多个仓库，只需要添加多个 `-t`：

```
$ docker build -t shykes/myapp:1.0.2 -t shykes/myapp:latest .
```

在 Docker 守护程序运行 `Dockerfile` 里面的指令之前，它会对里面的指令进行语法检查，如果有语法错误会报错：

```
$ docker build -t test/myapp .
Sending build context to Docker daemon 2.048 kB
Error response from daemon: Unknown instruction: RUNCMD
```

Docker 守护程序会逐个运行指令，并且必要的时候每步都生成一个新镜像（缓存），最终输出新镜像的 ID。Docker 守护程序会自动清理发送给守护程序的附属内容。

注意，每个指令都是独立的。所以 `RUN cd /tmp` 对下一条指令没有任何作用。

Docker 有可能会为了加速构建反复使用中间生成的镜像（缓存），如果使用了会在终端上打印`Using cache`：

```
$ docker build -t svendowideit/ambassador .
Sending build context to Docker daemon 15.36 kB
Step 1/4 : FROM alpine:3.2
 ---> 31f630c65071
Step 2/4 : MAINTAINER SvenDowideit@home.org.au
 ---> Using cache
 ---> 2a1c91448f5f
Step 3/4 : RUN apk update &&      apk add socat &&        rm -r /var/cache/
 ---> Using cache
 ---> 21ed6e7fbb73
Step 4/4 : CMD env | grep _TCP= | (sed 's/.*_PORT_\([0-9]*\)_TCP=tcp:\/\/\(.*\):\(.*\)/socat -t 100000000 TCP4-LISTEN:\1,fork,reuseaddr TCP4:\2:\3 \&/' && echo wait) | sh
 ---> Using cache
 ---> 7ea8aef582cc
Successfully built 7ea8aef582cc
```

构建中产生的缓存只会用于那些使用本地继承链的镜像——这意味着这些镜像是之前构建的或者整个经项链都是使用`docker load`载入的。希望使用某个特定镜像的缓存，可以使用`--cache-from`选项。使用这个命令指定的镜像不需要一个继承链并且可能是从其他目录拉取得。

### 格式
一个 Dockerfile 的格式：

```
# Comment
INSTRUCTION arguments
```

虽然指令大小写不敏感，但是一般来说都用大写，这样比较清晰。

Docker 按照次序运行 `Dockerfile` 里面的指令。一个 `Dockerfile`必须以一个`FROM`指令开始。这个指令指定了一个 [基镜像](https://docs.docker.com/engine/reference/glossary/#base-image) ，一个新镜像都是基于一个基镜像来修改生成的。在`FROM`指令之前只能插入`ARG`指令，这个指令声明了一些`FROM`行需要用的声明。

`#` 用于表示注释，但有时也表示词法处理器指令（类似预处理命令）。也可作为普通字符放在一个文字声明里。

```
# Comment
RUN echo 'we are running some # of cool things'
```

注释不支持分行符。

### 词法处理器指令
词法处理器指令是可选的，影响其后的`Dockerfile`行是如何被处理的。词法处理器指令并不是镜像构建过程的一部分，所以不会展示为构建的一部分。词法处理器指令看起来是一种特殊的注释，形式为：`# directive=value`，一个单独的词法处理器指令只会使用一次。

一旦一个注释、空行或者一个构建命令已经被执行了，Docker 就不在寻找词法处理器指令了，就算后面有词法处理器指令，也是没有卵用。因此所有的词法处理器指令**必须顶格在顶部**。

词法处理器指令同样不区分大小写，习惯上是小写。一般格式如此：

```
# directive=value1
# directive=value2

FROM ImageName
```

只要不换行，空格是可以随意添加的：

```
#directive=value
# directive =value
#	directive= value
# directive = value
#	  dIrEcTiVe=value
```

下面的词法处理器指令是有效的：

```
# escape=\
```

或者

```
# escape= `  
```

这个指令设置某个符号作为转义符号和分行符。如果没有设置，默认是`\`。

把转义符号设置为点在 `Windows`下很有用，因为 Windows的目录分隔符是反斜杠。

### 环境替换
使用`ENV`声明的环境变量，可以作为一种变量给其他指令引用（类似 C 语言中 define 字符串替换）。同样转义符号也可以将这个替换功能暂时取消，将这种语法形式变成字符串本身。

在`Dockerfile`里面，环境变量用两种模式来引用，一种是`$variable_name`，一种是`${variable_name}`，效果一样。一般来说，不带空格的变量用带花括号的模式，比如`${foo}_bar`。  

同时，带花括号的模式还支持一些`bash`修饰符：

- `${variable:-word}` 意思是如果这个变量已经被设置了，那么得到的结果会是这个值。如果没有被设置，那么得到的结果会是`word`
- `${variable:+word}` 意思是如果这个变量已经被设置了，那么会得到`word`这个结果。如果这个变量没被设置，那么得到的结果会是一个空字符串。

上面两种情况里面，`word`都可以是任何字符串，其中可以包括一些环境变量。

可以在这些变量前面增加转义符，比如`\$foo`或者`\${foo}`，这就使得转义符后面的东西是文字值本身。

举个例子：

```
FROM busybox
ENV foo /bar        #                   声明了一个含有 /bar 字符串的变量
WORKDIR ${foo}      # WORKDIR /bar
ADD . $foo          # ADD . /bar        效果和上方相同
COPY \$foo /quux    # COPY $foo /quux   由于转义符号，变量引用并没有被转换
```

支持这种引用的指令有：

- ADD
- COPY
- ENV
- EXPOSE
- FROM
- LABEL
- STOPSIGNAL
- USER
- VOLUME
- WORKDIR

以及：

- `ONBUILD`（仅在和上方的某个指令一起使用的时候）

这种环境变量的替换，单行指令中的引用被替换为什么，取决于这个变量在此指令之前被赋值时的值。

```
ENV abc = hello
ENV abc = bye def = $abc
ENV ghi = $abc
```

最后会使得，`def` 的值为 `hello`，而不是 `bye`。然而，`ghi` 的值为 `bye` ，因为对 `ghi` 的赋值过程，已经是对 `abc` 赋值为 `bye` 的那一行的后一条指令了。

### .dockerignore 文件
一般在附属内容的根目录，都有一个 `.dockerignore` 文件。它禁止一些不必要的或者敏感的文件被发送到 `docker` 守护程序。从而这些文件都会被 `ADD` 和 `COPY` 指令忽略。  

命令行视 `.dockerignore` 为一个类似 glob （最早是出现在类Unix系统的命令行中, 是用来匹配文件路径的）的列表文件。为了匹配路径，附属内容的根目录被同时看做工作目录和根目录。举个例子来说，`/foo/bar` 和 `foo/bar` 都会排除一个在 `foo` 文件夹里面的一个叫做 `bar` 的文件夹。这个 `foo` 文件夹可能是 `PATH` 规定的根目录，或者一个 git 库（位于 `URL` ）。  

单行注释用 `#` 标记（注意前面不能有空格）。

例子：

``` 
# comment
*/temp*
*/*/temp*
temp?
```


| 规则 | 解释 |
| --- | --- |
| # comment | 注释 |
| */temp* | 对于直接位于根目录下的所有文件夹，去除其中以 `temp` 开头的文件夹和文件 |
| */*/temp* | 若直接位于根目录下的所有文件夹为集合 A，对直接位于 A 里面的所有文件夹集合 B 进行操作，去除其中以 `temp` 开头的文件和文件夹。 |
| temp? | 去除直接在根目录下面的、名字为 `temp` 加任意一个字符的文件夹或文件夹， |

匹配规则和 Go 语言的 [filepath.Match](http://golang.org/pkg/path/filepath#Match) 规则相同。在这之前还有一步预处理操作：使用 Go 语言的 [filepath.Clean](http://golang.org/pkg/path/filepath/#Clean) 去除前后的空格，并且把相对路径计算为绝对路径。所以空行都会被排除。

除了 Go 本身的匹配规则，Docker 还支持一个特殊的通配符 `**`，这个通配符匹配任何文件夹。比如 `**/*.go` 会排除掉包括根目录在内的所有 `.go` 结尾的文件。

如果在规则中有个别文件不想排除，那就用 `!` 来标注。

```
*.md
!README.md
```

所有的 MD 文件都会被排除，但是 `README.md` 会留下。

`.dockerignore` 和 `Dockerfile` 也可以被排除。虽然构建过程还是会读取这两个文件，但是 `COPY` 和 `ADD` 会忽略这两个文件。

所以如果要排除的文件反而占大多数，一行用 `*` ，后一行用 `!` 是一种通用办法。

> 由于一些历史原因，不能匹配 `.`

### FROM

`FROM` 的用法为：

```
FROM <image> [AS <name>]
```

或

```
FROM <image>[:<tag>] [AS <name>]
```

或

```
FROM <image>[@<digest>] [AS <name>]
```

`FROM` 指令用来初始化一个新的构建平台，然后设置一个[基镜像](https://docs.docker.com/engine/reference/glossary/#base-image)。一个合法的 `Dockerfile` 开头必然是 `FROM` 指令。这个镜像可以是任何一个合法的镜像，尤其是那些从官方仓库拉去的镜像，更加方便。  

- `ARG` 是唯一一个可能存在于 `FROM` 之前的指令。
- 同一个`Dockerfile`里面，`FROM` 可以出现多次。这样可以创造多个镜像，或者使用一个构建平台作为另一个构建平台的依赖。 
- 可以给新的构建平台取名。即添加 `AS <name>` 字段。这样就可以用 `FROM` 和 `COPY --from=<name|index>` 来引用一些在这个构建平台里的镜像了。
- `tag` 和 `digest` 是可选的。如果没填，那默认就是 `latest` 标签。如果找不到这个标签，那会报错。

#### ARG 和 FROM 的关系
`FROM` 支持一些由 `ARG` 已经声明过的变量。

```
ARG  CODE_VERSION=latest
FROM base:${CODE_VERSION}
CMD  /code/run-app

FROM extras:${CODE_VERSION}
CMD  /code/run-extras
```

一个在 `FROM` 之前声明的 `ARG` 实际上是不在构建平台里的，所以在 `FROM` 之后的其他指令都不能用。比如：

```
ARG VERSION=latest
FROM busybox:$VERSION
ARG VERSION
RUN echo $VERSION > image_version
```

### RUN

`RUN` 有两种形式：
- `RUN <command>` （**shell 形式**，这个指令会运行在 shell 里，linux里默认是运行的 shell 是 `/bin/sh -c`。在 Windows 上默认是 `cmd /S /C`。
- `RUN ["executable", "param1", "param2"]` **exec 形式**。

`RUN` 指令在当前的镜像的顶层（layer）运行任意命令，并且提交（commit）运行后的结果。这个提交后的结果镜像会用于`Dockerfile`的下一步行为。

这种层面化 `RUN` 加上提交结果的形式遵从了 Docker 的核心概念：提交是成本极低的并且镜像可以生成于历史记录的任何一个节点，就像版本控制一样。  

使用 `exec` 形式的 `RUN` 指令可以避开整理 shell 字符串参数，并且在基镜像上运行这个命令（基镜像可以不包含特定的可运行的 shell 命令） 。

可以使用 `SHELL` 指令来更改运行 shell 命令的默认 shell 软件。

在 shell 形式中可以使用反斜线来拆分单个命令。

```
RUN /bin/bash -c 'source $HOME/.bashrc; \
echo $HOME'
```

> - 想要使用不同的 shell 而不是 `/bin/sh` 可以使用 exec 形式的指令调用想要的 shell。`RUN ["/bin/bash", "-c", "echo hello"]`。
> - exec 形式的指令是按照 JSON 来解析的，所以每个量两边要用双引号。

> - exec 形式的指令并不会调用一个命令行 shell。也就是说，普通的 shell 过程并不起效果。举个例子，`RUN [ "echo", "$HOME" ]` 并不会替换环境变量 `$HOME` 代表的值。如果想要使用 exec 形式正常执行一个 shell 过程，可以这样写：`RUN [ "sh", "-c", "echo $HOME" ]`，这样就直接运行了一个 shell。当直接运行了一个 shell 的时候，就和 shell 形式类似了，是 shell 在执行这个环境变量替换的命令而不是 docker。

> - 在JSON格式里，要明确避开使用反斜线。特别是在 Windows 这种反斜线表示路径分割符的系统，比如下面这条指令就被判定为不合法的 JSON 格式 `RUN ["c:\windows\system32\tasklist.exe"]`。正确的写法应该是这样的：`RUN ["c:\\windows\\system32\\tasklist.exe"]`

每一条`RUN`产生的缓存在下一次构建中并不会被自动作废，这些缓存都会被下一次构建重用。可以使用 `--no-cache` 参数来来作废`RUN` 指令产生的缓存：`build --no-cache`

但使用`ADD`指令，会作废`RUN`指令产生的缓存。

### CMD
`CMD` 指令有三种形式：

- `CMD ["executable","param1","param2"]` exec 形式，推荐使用。
- `CMD ["param1","param2"]` 给`ENTRYPOINT` 提供默认参数。
- `CMD command param1 param2` shell 形式。

一个 `Dockerfile` 里面只能有一个 `CMD`。如果写了超过一个的此指令，只有最后一个有效。

**`CMD`的功能是给运行容器提供默认值**。这些默认值可以包含一个可执行文件，或者删除一个可执行文件。若要删除一个可执行文件，那么还要设定一个`ENTRTPOINT`指令。

> - 如果`CMD`用于给`ENTRYPOINT`指令提供默认参数，那么两者都必须使用 JSON 数组格式。
> - exec 形式的指令是按照 JSON 来解析的，所以每个量两边要用双引号。
> - exec 形式的指令并不会调用一个命令行 shell。也就是说，普通的 shell 过程并不起效果。举个例子，`RUN [ "echo", "$HOME" ]` 并不会替换环境变量 `$HOME` 代表的值。如果想要使用 exec 形式正常执行一个 shell 过程，可以这样写：`RUN [ "sh", "-c", "echo $HOME" ]`，这样就直接运行了一个 shell。当直接运行了一个 shell 的时候，就和 shell 形式类似了，是 shell 在执行这个环境变量替换的命令而不是 docker。

当使用 shell 或者 exec 形式的`CMD`，它设定了当镜像开始运行的时候执行的命令。

如果使用 shell 形式的 `CMD`，命令会在会执行在`/bin/sh -c`：

``
FROM ubuntu
CMD echo "This is a test." | wc -
``

如果想要不使用 shell 来运行命令，应该使用 JSON 数组，并且提供可执行文件的完整路径。任何可选的参数都应该独立地置于 JSON 数组中：

```
FROM ubuntu
CMD ["/usr/bin/wc","--help"]
``` 

如果用户使用了`docker run` 命令并规定了参数，那么会覆盖掉 `CMD` 规定的默认值。

> `RUN` 和 `CMD`完全不同：前者是运行一条命令并且提交命令导致的结果；后者并不会在构建阶段运行任何的命令，但是却规定了镜像预期的命令。
> 

### LABEL
```
LABEL <key>=<value> <key>=<value> <key>=<value> ...
```

`LABEL` 指令为镜像添加元数据。这种 `LABEL` 是键值对形式的。如果想要在`LABEL`值里面增加空格，应该使用引号和反斜杠：

```
LABEL "com.example.vendor"="ACME Incorporated"
LABEL com.example.label-with-value="foo"
LABEL version="1.0"
LABEL description="This text illustrates \
that label-values can span multiple lines."
```

一个镜像可以包含多个`LABEL`。在单行里面也可以设置多个标签。从前的版本，这种写法可以减小镜像的大小，不过现在这已经不是问题了，两种写法可以随便选：

```
LABEL multi.label1="value1" multi.label2="value2" other="value3"

LABEL multi.label1="value1" \
      multi.label2="value2" \
      other="value3"
```

在基镜像和父镜像中定义的标签，会被子镜像继承。如果一个标签已经存在并且被重复定义了，那么新定义的会覆盖老定义的值。

想要查看一个镜像的标签，使用`docker inspect`命令。

```
"Labels": {
    "com.example.vendor": "ACME Incorporated"
    "com.example.label-with-value": "foo",
    "version": "1.0",
    "description": "This text illustrates that label-values can span multiple lines.",
    "multi.label1": "value1",
    "multi.label2": "value2",
    "other": "value3"
},
```

### MAINTAINER （不建议使用）
```
MAINTAINER <name>
```

设置镜像的创建者信息。最好用`LABEL`指令来代替这个指令：

```
LABEL maintainer="SvenDowideit@home.org.au"
```

### EXPOSE

```
EXPOSE <port> [<port>/<protocol>...]
```

通知 Docker 开放一些在容器运行时需要监听的网络端口。可以规定这些端口是监听 TCP 还是 UDP ，默认是 TCP。  

这个`EXPOSE`指令并不会真正公开这些端口。它实际的作用更像是一种镜像构建者给使用者的一个文档，说明哪个端口将要被公开。真正公开端口的方式是运行容器的时候添加`-p`参数来公开端口并映射端口。或者添加`-P`参数来公开所有已经`EXPOSE`了的端口，并把这些端口映射到 high-order 端口。  

默认是，`EXPOSE`默认使用 TCP 端口，可以定制为 UDP：

```
EXPOSE 80/udp
```

想要同时公开 TCP 和 UDP 的时候，应该写两行：

```
EXPOSE 80/tcp
EXPOSE 80/udp
```

在这种情况下，如果使用`-P`参数，端口会为 TCP 公开一次再为 UDP 公开一次。`-P`会使用短暂的`high-ordered`宿主机端口在宿主机上，所以 TCP 和 UDP 的端口并不会相同。

如果使用`-p`参数可以重载`EXPOSE`指令的规定：

```
docker run -p 80:80/tcp -p 80:80/udp ...
```

想要设置宿主系统上的端口重定向，查看[using the -P flag](https://docs.docker.com/engine/reference/run/#expose-incoming-ports)。`docker network` 命令支持在容器间重建用于通讯的网络，并且不需要 expose 或公开特定的端口。这是因为连接到网络的容器可以通过任何的端口相互联系，更多信息：[overview of this feature](https://docs.docker.com/engine/userguide/networking/)

### ENV
```
ENV <key> <value>
ENV <key>=<value> ...
```

`ENV`指令设置环境变量`<key>`其变量值为`<value>`。这个值会一直存在于环境中，对于其后每个在构建平台上的指令都有效，并根据环境变量进行替换（参见前文环境变量替换）。  

`ENV`指令有两种形式。第一种形式`ENV <key> <value>`设置单个变量给单个值，在第一个空格之后的整个字符串都会被看做值——包括空格。这个值会为其他环境变量而解析，所以没有被转义的引号会被移除。

第二种形式`ENV <key>=<value>`，可以一次设置多个环境变量。可以使用反斜杠来加入空格：

```
ENV myName="John Doe" myDog=Rex\ The\ Dog \
    myCat=fluffy
```

和：

```
ENV myName John Doe
ENV myDog Rex The Dog
ENV myCat fluffy
```

结果完全相同。

使用此指令设置的环境变量会一直存在，甚至在容器运行的时候。可以使用`docker inspect`来查看这些值，并且可以使用`docker run --env <key>=<value>`来修改。  

> 环境变量的一直存在会导致一些副作用。比如说，设置`ENV DEBIAN_FRONTEND noninteractive`会让 apt 使用者在使用 Debian 基础上的镜像产生遇上问题。为了给一个单独的命令设置环境变量，需要使用`RUN <key>=<value> <command>`


### ADD
`ADD`指令拥有两种形式：

```
ADD [--chown=<user>:<group>] <src>... <dest>
ADD [--chown=<user>:<group>] ["<src>",... "<dest>"]
```

> `--chown`特性只在 Linux 容器上才支持。因为用户和组的概念在 Linux 和 Windows 平台上并不通用，想使用`etc/passwd` 和 `etc/group` 来将组和用户名名称转换为 ID，也只能在 Linux 容器上。




## Dockerfile instruction
## FROM
一般定制的镜像都继承自官方镜像。Docker 官方建议一个极小（5 MB）但完整的 Linux 发行版[Alpine image](https://hub.docker.com/_/alpine/)。

## LABEL
为了记录许可证信息、自动化帮助信息或者其他原因，可以给镜像添加标签。每个标签以`LABEL`标注开始

