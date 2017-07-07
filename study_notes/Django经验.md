## Django

推荐使用python的虚拟环境，不要问太多，直接来就得了

1、虚拟环境 ：
	
打开命令行，不需要使用管理员模式，进入到想要安装虚拟环境的目录，然后运行命令 ：

	python -m venv name
将name替换为想要的名字，然后启动虚拟环境，使用如下命令：

	cd Scripts
	activate.bat
此时你可以观察到命令行中目录的最前面有`(name)`，这说明已经进入了虚拟环境

2、安装Django :

防止因为不知道版本而安装错误，可以使用pip，在虚拟环境下使用命令如下 ：

	pip install django

然后等待即可

如果网速太慢，可以下载合适版本的安装包，Django-xxxx.tar.gz文件，无须解压，直接放在`name`文件夹下，使用如下命令：

	pip install Django-1.9.6.tar.gz(即文件全名)

3、一个检查方法 ：

可以使用如下命令检查本虚拟环境下安装的模块，前提必须要已经进入了虚拟环境 ：

	pip freeze

4、建立一个django工程 ：

要使用命令行建立一个django的工程，使用了之后，django会帮你建立一个工程的初始模板，帮你构建所有的必要的初始文件，所以说这个是必须的
，在虚拟环境的根目录下运行运行如下命令：

	D:\django_test\Scripts\django-admin startproject projectname

将`projectname`替换为你想构建的第一个工程的名字，以下将以`pn`代替


以上工作完成后，你会在虚拟环境的目录下发现一个`pn`名字的文件夹，打开后里面还会有一个`pn`的文件夹和一个名为`manage.py`的文件

5、初次运行 ：

在虚拟环境的根目录下，使用cd进入工程的根目录，然后使用如下命令即可初次运行 ：

	python manage.py runserver

输入给出的url即可打开一个初始的页面： `http://127.0.0.1:8000/`


6、构建第一个app :

一个app相当于是一个功能，我们也需要使用命令行构建一个app,在虚拟环境下，在当前工程目录下：

	python manage.py startapp firstappname

使用想要的app的名字替代`firstappname`,例如一下将以`blog`代替