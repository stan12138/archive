## Docker笔记

这里记录一下今天远程教学学到的docker的知识，省得忘了。

当然，可能很多地方我说的不对，或者不严谨。总之，记录一下先。

### 环境

我并没有自己装docker，这一块是同学给我整好的，就先跳过。

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



这样吧先。

下雨了。

独自在办公室坐了两三个小时，学术的事情依旧没有任何进展。忽然听到窗外传来阵阵雷声，猛然抬头，才发现天已经完全暗了下来，树木摇摆，雨如帘。下雨了。

打开窗，凉风裹着细碎的雨雾扑面而来，早晨的沉闷燥热终于一扫而空，我好喜欢这个雨天，喜欢这冷风，喜欢这雨，还有轰隆隆的雷声，偶尔的闪电以及昏暗的天色。

如果没有论文要做的话，我应该会很开心。



办公室终于来了一个同学，当闪电刚过，我跟他说：好像很久没有下雨了。说着这些话，我却突然有了一些很怪异的想法，似乎雨突然变得有些神奇，好像并不是一种常见的天气现象，我在想会不会有一个星球，那里有迥然不同的天气现象，那里的雨会是怎么样的，又会是怎么样一个意义。我想去一个不同的地方，去感受一下那里的雨。