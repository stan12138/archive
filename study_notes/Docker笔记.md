## Docker笔记

这里记录一下今天远程教学学到的docker的知识，省得忘了。

当然，可能很多地方我说的不对，或者不严谨。总之，记录一下先。



如果想要认真的学习一下`Docker`, 那么我的推荐参考书是：[第一本Docker书](https://book.douban.com/subject/26285268/)



### 环境

我并没有自己装docker，这一块是同学给我整好的，就先跳过。

欧科，其实到目前为止，我并没有搞懂安装docker是个怎么样的流程，以及为什么要这么做。似乎还有什么docker-ce和docker-ee我也并不知道是什么。

但是，目前的WSL已经很不错了，我可以在上面装docker，安装的方法[参考这里](https://www.runoob.com/docker/ubuntu-docker-install.html), 防止失效，这里摘录，做个备份：

> **Ubuntu 18.04 安装 Docker-ce**
>
> 1.更换国内软件源，推荐中国科技大学的源，稳定速度快（可选）
>
> ```
> sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
> sudo sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
> sudo apt update
> ```
>
> 2.安装需要的包
>
> ```
> sudo apt install apt-transport-https ca-certificates software-properties-common curl
> ```
>
> 3.添加 GPG 密钥，并添加 Docker-ce 软件源，这里还是以中国科技大学的 Docker-ce 源为例
>
> ```
> curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
> sudo add-apt-repository "deb [arch=amd64] https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu \
> $(lsb_release -cs) stable"
> ```
>
> 4.添加成功后更新软件包缓存
>
> ```
> sudo apt update
> ```
>
> 5.安装 Docker-ce
>
> ```
> sudo apt install docker-ce
> ```
>
> 6.设置开机自启动并启动 Docker-ce（安装成功后默认已设置并启动，可忽略）
>
> ```
> sudo systemctl enable docker
> sudo systemctl start docker
> ```
>
> 7.测试运行
>
> ```
> sudo docker run hello-world
> ```
>
> 8.添加当前用户到 docker 用户组，可以不用 sudo 运行 docker（可选）
>
> ```
> sudo groupadd docker
> sudo usermod -aG docker $USER
> ```
>
> 9.测试添加用户组（可选）
>
> ```
> docker run hello-world
> ```

经过我的测试，是可以的，只是因为WSL2本身也是虚拟机，所以第6步以后我都没有做。

此时如果运行`sudo docker images `大概是无法执行的，因为docker并没有在运行。

执行`sudo service docker start` 即可运行docker，然后上述测试命令就可以使用了，环境布置到此完成。



### 基本概念

我现在认为，docker就是虚拟机，但是是一个功能强大，使用方便，资源占用很少，启动相当快速的虚拟机。

docker里面有容器和镜像两个概念。容器就是虚拟机，每跑起来一个容器就跑起来了一个虚拟机。

镜像是一个虚拟机在某一个状态的快照，也就是某个时刻这个虚拟机全部环境和状态的打包。

如果我们在一个容器里面跑某一个镜像，那么我们就获得了一个运行某一个镜像的虚拟机。

假设，我首先搞一个最基本，最核心的Ubuntu的镜像，然后把它跑起来，然后在这里面装一下python，此时创建一个镜像，那么我就获取了一个装了python3的ubuntu，新开一个容器跑这个镜像，我就有了一台装了python3的虚拟机。如果把这个镜像转移到其他位置，就可以在其他机器上跑起来。

### 简单用法

~~~bash
sudo docker images #列出当前拥有的镜像
sudo docker run -itd --name stan -p 5000:5000 ubuntu
#运行一个容器，在后台运行，同时将容器的5000端口映射出来到5000端口，容器内运行的镜像是ubuntu，并将这个容器命名为stan
sudo docker ps -a
#列出存在的所有容器，无论是否正在运行
sudo docker stop stan #停止stan容器的运行
sudo docker start stan  #开始
sudo docker restart stan #重启

sudo docker exec -it stan
sudo docker exec -it stan bash
sudo docker attach stan

sudo docker commit stan ubuntu_python3  #对stan容器现在的状态创建一个ubuntu_python3的镜像

sudo docker rmi ubuntu_python3  #删除镜像

sudo docker rm stan  #删除容器

sudo docker rm -f stan  #强制删除容器，即使在运行

sudo docker run -it --name test ubuntu_python3 python3

sudo docker pull redis   #从官方的镜像仓库获取redis镜像

sudo docker run --name stan_redis -d redis

sudo docker inspect stan_redis  #查看stan_redis容器的信息

sudo docker pull mysql

sudo docker run --name stan_mysql -e MYSQL_ROOT_PASSWORD=xxxxxx -p 3306:3306 -d mysql
~~~



如前面的redis和mysql的镜像，这都是官方配置好的，这个镜像就可以顺利的运行起这两个服务器，官方仓库在[这里]([https://hub.docker.com](https://hub.docker.com/))，可以搜索。凡是官方认证的镜像都是不带任何前缀的，用户也可以上传镜像，一般都会带用户名前缀。

例如可以搜索mysql的，点击去可以看到说明，尤其是`how to use `那一部分比较重要



另外就是前面查看容器信息的一块，在结果的最后可以看到一个IP地址的字段，这是容器的ip地址

docker会把同一台机器上运行的所有容器放进一个子网内，容器与容器由于都在这个子网内，所以可以通过对方容器的ip地址访问彼此。但是本机想要访问容器就不行，因为本机并不在容器子网中。本机要访问容器，就必须通过之前的-p参数把容器的端口映射出来。



欧科，基本上就这么多了，有些东西我忘了，就先不说了。

假设我们要做一个小项目，要用python，数据库什么的，那么一般的工作方式是什么呢？数据库需要单开一个容器，然后python3开一个容器，然后进行访问。

最后再说一点，所谓镜像，其实就是当前环境的完全打包。所以说我们获取一个mysql的镜像，其实是要比我们单独下一个mysql要大，因为还包含了一点其他东西，但是一般不会大太多。





### 关于穿透

但我的几台服务器在一个局域网内，想要访问，那么至少要通过frpc将ssh穿透出来。

然后服务器上运行了docker，如果一个容器的端口需要穿透，首先要把容器的端口映射到本机，接下来是否需要frpc再把本机映射出内网呢？

当然可以这么做。其实也可以不用。

SSH也提供了一个映射功能，可以把SSH目标主机上的某个端口映射到这台机器上。

所以，例如服务器A处于局域网，上面开了一个docker，其中某个容器内运行了jupyterlab，在8888端口。首先可以通过docker将容器的8888映射到A上，但是A的访问是命令行，也用不了浏览器，所以可以通过frpc再把A的8888映射出来，这样就能访问jupyterlab了，也可以通过在我们的电脑上直接使用`ssh -p 60005 -NL 8888:localhost:8888 xxxxxx`，这样可以将A上面的8888映射到本机的8888，这样通过本机的`127.0.0.1:8888`就可以访问jupyterlab了。

这里，还要说一下，上述命令是在win的powershell运行的。是的powershell是可以直接使用ssh的。也就是说一些简单的连接就不需要再借助软件了，用powershell就可以，只是不能保存而已。





### 基本操作

关于容器和镜像是什么就不说了。

启动第一个`ubuntu` 容器

`sudo docker run --name XXXXXX -i -t ubuntu /bin/bash `

上述命令，将创建一个新的容器，并且运行，这个容器执行的是ubuntu，名字是`XXXXXX`，参数`-i` 开启了容器的标准输入，而`-t` 参数为容器分配了一个伪tty终端，这样在这两个参数的作用下，容器就能提供一个交互式shell。

如果不给容器命名，那么将会产生一个随机的名字，使用起来略麻烦。

假设，之前我们已经创建了一个容器，并且未命名，我们也可以为之修改名字，命令为：

`sudo docker oldname newname`

当我们执行前述命令，应该就能进入到ubuntu的交互shell，此时可以像普通shell和系统一样执行我们想要的操作，如果要退出这个shell，只需要执行`exit` 即可，但此时也就退出了这个容器，容器停止了执行