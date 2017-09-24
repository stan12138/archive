## MongoDB笔记

我安装了mongodb

###环境配置

官网下载community的Windows Server 2008 R2 64-bit and later, with SSL support x64即可，安装，选择custom可以定制文件夹，很快就可以安装结束

之后的过程说实话我也很模糊

我做了很多尝试，但多以失败告终，所以我也不敢确定哪些是有用的

大概应该是这样的:

1.  我们需要一个目录作为db数据的目录，可惜这个目录并不会自动创建，我们可以自己建一个data/db
2.  cd进入mongodb的目录下的bin文件夹，然后执行`mongod --dpath d:\data\db`，此时你应该可以看到db下出现了很多文件，并且命令行也输出了很多信息
3.  加入环境变量，方便使用。在系统环境变量里新建一个，名字自定，如:`MONGODB_HOME`，值是mongodb的目录一直到bin的上一层，例如`D:\ProgramFile\MongoDB\Server\3.4`，然后编辑系统的path，在后面添加`%MONGODB_HOME%\bin;`，注意path的每一个值都是用；分割的，最后一个也要使用;所以万一前面一个少了;你要记得自己加上，你应该能看出来吧，MONGODB_HOME就是被当作了一个变量，然后使用%标识等等
4.  加入windows服务，这一步我执行了，但是我在服务中并没有找到mongodb，但是至少我的确成功设置了日志文件。我们应该在data下再新建一个dbConf的文件夹，并在里面新建一个空白文件，叫mongodb.log。接下来在管理员命令行输入：`mongod.exe --bind_ip 127.0.0.1 --logpath "D:\ProgramFile\data\dbConf\mongodb.log" --logappend --dbpath "D:\ProgramFile\data\db" --port 27017 --directoryperdb --serviceName MongoDB -install`注意改一下该改的目录。他们说接下来输入services.msc就可以看到弹出来的服务中就有mongodb但是，我并未发现
5.  我们该如何启动mongodb，打开管理员命令行，输入`net start MongoDB`，自己看一下，信息正常就说明应该是开启成功了。
6.  我们打开一个新的命令行，输入`mongo`，应该就会连接成功，这时我们就可以在这里操作了,例如输入2+2，会给出4，例如db，一般输出test
7.  想要关闭db，网上给了很多方法，但有些看不懂，有些不成功。我成功的就是在上面的操作界面输入`use admin`切换到管理员，然后输入`db.shutdownServer();`即可，这时使用`ctrl-c`可以退出操作界面，然后再mongo，应该会发现连接失败，说明已经退出成功了。先要开启，还要在管理员命令行界面输入net start MongoDB
8.  怎么证明你的确是设置成功了dbpath呢？去之前设置的目录，打开日志文件，应该就能找到。



