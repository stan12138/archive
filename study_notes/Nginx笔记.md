# Nginx笔记

对于windows，去官网下载即可，然后直接解压，然后cd到文件夹中，在命令行输入`start nginx`即可运行，在任务管理器就可以发现有两个进程在运行。打开浏览器`127.0.0.1`即可看到欢迎页面。

但是也许你会运行失败，那么十之八九是因为默认的端口80被占用了，此时需要打开conf文件夹，找到`nginx.conf`文件，修改listen的端口号即可。

关闭服务器，可以使用`nginx -s stop`

~~~python
nginx -s stop // 停止nginx
nginx -s reload // 重新加载配置文件
nginx -s quit // 退出nginx
~~~

