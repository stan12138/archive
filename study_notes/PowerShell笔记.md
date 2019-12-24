## PowerShell笔记

我还是蛮喜欢powershell的，尤其是在windows terminal搭配下的。那些非常非常简单的操作自然都是会的，运行个程序，cd和ls之类的，都是常规操作，但是我还是有一些想学的东西的。例如能不能写一个powershell的脚本，能不能让一个代码在后代运行之类的，总而言之，我觉得可以尝试学习一下powershell的使用。

参考书：windows powershell实战指南(第二版)



### 版本

现在，我想也许，我的参考书选的不怎么样。这本书使用的powershell版本是V3，但是我现在win10上面的版本似乎是V5.1了都。

如何查看powershell版本信息

~~~powershell
$PSVersionTable
~~~



有第三版的书，但是我找不到电子版。



powershell不区分大小写

powershell的可执行命令包含很多种不同类型，有的叫作cmdlet，有的叫函数，还有的叫作工作流

powershell的自动补全还是蛮厉害的，无论是参数名,cmdlet名字都可以

### 帮助

~~~powershell
help Get-service
~~~

获取`get-service`的帮助

~~~powershell
help *log*
~~~

查找名字里包含了log的命令

~~~powershell
help get-eventlog -full  /*查看完整形式*/
help get-eventlog -example /*给出一个例子*/
~~~

~~~powershell
update-help
~~~

更新帮助。也许需要管理员

### 命令与参数

但help一个cmdlet的时候，可以看到他的语法，例如：

~~~powershell
Get-EventLog [-LogName] <string> [[-InstanceId] <long[]>]  [<CommonParameters>]
~~~

参数分为这么几种，可选参数，必选参数，定位参数。前两者很容易理解，原则上命令调用的时候，应该例如这样：

~~~powershell
Get-EventLog -LogName 'test'
~~~

类似的，也就是说传参的时候，前面应该写参数名字，空格，再写参数值，而参数名字总是以`-`开头。

但是有些参数可以是定位参数，此时不需要写参数的名字。

那么怎么区分呢？

`[]`代表的意思是可选，那么前面的这个命令，可以看到`[-LogName]`带方括号，意味着它是可选的，但是又可以看到它的值`<string>`并没有放入方括号，这意味着这个参数是必选的，但是参数名可选，这意味着这个参数是一个定位参数，可以不写参数名，但是必须传值。如`Get-EventLog 'test'`

再看`[[-InstanceId] <long[]>]`，这个参数的参数名有方括号，意味着可以是一个定位参数，同时最外层还有一个方括号，这意味着是一个可选参数。

再例如，如果有这样的参数`[-Before <DateTime>]`，这意味着这个参数可选，但是如果使用了，就必须带参数名。

还有一些参数叫做开关参数，长这样`[-AsString]`，详细的语法长这样`-AsString [<SwitchParameter>]`，后面的`[<SwitchParameter>]`指明了这是一个开关参数，输入参数名就代表使用这个参数，不需要给值。

参数的类型使用`<>`给出

我们可以看到`string, Int, Int32 Int64, DateTime`等等不同的参数类型

以字符串为例，如果参数是字符串，一般不需要引号，当参数中包含空格就需要引号，单双引号都行，最好使用单引号

也有观察到数组对吧，也叫列表

例如`[-ComputerName <string>[]]`，那么这个参数可以接受多个string参数，多个参数怎么传递呢？

`-computername name1, name2, name3`，也就是说多个参数使用逗号分隔。



还有一种提供列表或者数组值的方法，可以将每个参数一个值一行存在文本文件中，然后使用`Get-Content`来读取文件内容，但是明显需要用圆括号指定一下操作顺序对吧，例如：

~~~powershell
Get-Eventlog Application -computername (get-content names.txt)
~~~



### 命令再述

#### 命令别名

前面可以观测到，命令还是蛮规范的，总是以一个动词开头接着一个`-`然后是功能

缺陷是可能很长，别名所以重要。

~~~powershell
Get-Alias -Definition "Get-Service"

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           gsv -> Get-Service

~~~

这样就能查看到`get-service`的别名是`gsv`

知道别名，可以用`help gsv`查看含义



所以，可以看到别名都是内置，通用的。也可以使用`new-alias`自定义，但是生命周期只到这个shell结束，可以用`export-alias`导出，然后下次再导入，但明显很麻烦，所以不要自定义



#### 参数别名

参数也有别名，说是你可以输入参数名的几个字母，只要能唯一确定一个参数名就行，但是我想何必呢，这样自动补全一下就好了呀。

怎么查看参数别名就不说了，我觉得没用，命令还很长



#### 作弊：图形化命令编辑器

提供了一个图形界面，让你填写一个命令的参数，然后点击复制就可以得到命令：

~~~powershell
show-command get-eventlog
~~~



### 使用提供程序

提供程序？很诡异。它是一种程序，叫做`PSProvider`

~~~powershell
get-psprovider
~~~

可以获取当前拥有的提供程序



#### FileSystem

这是提供程序之一，自然是针对文件系统的

文件系统三层次：驱动器，文件夹，文件，文件是最小单元。

powershell使用一个术语，叫做item，即项，文件和文件夹都叫做项。

。。。。。

sorry，我现在根本没看懂他在说什么

~~~powershell
set-location -path
~~~

切换路径,cd也行

`New-Item testfolder`， 建立一个新的项，名字叫做testfolder，按说上说会让你输入type来决定这个项是一个文件夹还是什么，但是新版改了。。。。

mkdir就可以创建文件夹



#### 通配符

`*`代表0到多个字符，`?`代表单个字符



#### 使用提供程序查看和修改注册表

~~~powershell
cd hkcu:
cd software
cd microsoft/windows
set-itemproperty -path dwm -pspropert enablewindowcolorization -value 0
~~~

所以注册表也是类似文件系统一样的使用方式，最后一个修改值我并未测试



### 管道

管道符，对吧，Linux里面就知道，是啥就不说了，powershell也支持



~~~powershell
Get-Process(别名：ps)
~~~

~~~powershell
ps | Export-csv procs.csv
~~~

~~~powershell
ps | ConvertTo-Html | Out-File process.html
~~~



`stop-process`的别名叫做`kill`



### 扩展命令

这是扩展？呃，感觉用不上，跳过先。



### 对象与数据

powershell的数据使用对象表示，例如`get-process`产生的数据每一行代表一个进程，每一列代表一种属性，Get-member可以获取所有的属性和方法，别名gm

~~~powershell
get-process | gm
~~~

就可以获知都有哪些列，自然这里面包含了属性和方法

~~~powershell
get-process | sort-object -property VM
~~~

按照vm属性排序

sort-object的别名 sort



~~~powershell
get-process | select-object -property Name, ID, VM, CPU
~~~

select-object 别名select  property是定位参数



所以，对于我们获取的数据，可以首先使用gm知道它的属性，然后用sort和select进行选择处理



### 管道进阶

不想看，也还没看懂



### 格式化





### 远程处理

powershell的远程处理类似telnet和ssh，但是通信协议不一样，powershell用的协议叫做ws-man，针对管理的web服务，基于http/https。基于windows远程服务组件，即WinRM

说实话，我现在并未搞懂这个远程处理的细节，但是，现在我参照各种教程和指南，应该是成功的，刚才也借助了frp完成了内网穿透，当然还有很多东西并未完成，所以，现在只是大概能用的。

在一对一模式下，powershell远程管理功能自然分成了服务端和客户端，在服务端的话，需要在管理员powershell下执行：

~~~powershell
Get-Service winrm
Enable-PSRemoting -Force
Disable-PSRemoting -Force
~~~

第一条命令用来查看winrm服务的状态，应该是stopped的，然后第二条命令可以开启ps的远程管理功能，同时会帮忙开启winrm，当不再使用时，第三条命令可以关闭ps远程管理。

客户端的话，我用了太多命令都有点记不清了，大概是：

~~~powershell
Enable-PSRemoting -Force
Set-Item -Path WSMan:\localhost\client\trustedhosts -Value * -Force
Disable-PSRemoting -force
~~~

第一条也是开启ps远程管理，然后第二步是把任意主机加入信任列表，这样我们的电脑才能连到服务端。

也许服务端也需要这个？我也不知道，反正我在服务端也输过。

最后一个命令就是在不用的时候关闭的。



初期设置应该到此已经搞定，接下来当客户端要连接服务端的时候，直接使用：

~~~powershell
Enter-PSSession -ComputerName 10.210.68.195 -Credential Stan
~~~

这样类似的命令就行了，然后就能连接到powershell了。



服务使用的端口有两种http用5895，https用5896，我测试实际上用的是5895



所以，我的frpc.ini做了如下配置：

~~~ini
[common]
server_addr = xxxxxxxx
server_port = 12345

[stan]
type = tcp
local_ip = 127.0.0.1
local_port = 5985
remote_port = 60009
.custom_domains = xxxxxxxx
~~~

就是用服务器的60009代理了5985端口，然后客户端这边，可以使用`-Port`参数指定服务端的端口号，如下：

~~~powershell
Enter-PSSession -ComputerName xxxxxxx -Credential Stan -Port 60009
~~~

但是，试一下你就知道根本连不上，这是为什么呢？

观察一下错误信息，基本可以发现是在说无法解析computername，这是因为我在这里使用了服务器的域名作为computername。然后尝试ping一下服务器，找到服务器的ip地址，然后把computername替换为ip地址，就成功连上了。

真坑。

当我们连上远端的powershell之后，输入`exit`就可以断开连接。

我现在还不知道怎么编辑文件，传输文件，所以还是一个问题.

然后，我看到了很多资料，说powershell的远程管理功能现在不仅仅可以基于winrm了，也可以使用ssh，如果使用ssh会带来多少便利呢？我也不知道，至于配置方式，我也没有尝试。



### 后台任务

后台任务很重要。按照参考书上说的，使用`Start-Job`执行后台任务，但是在我实际的测试中，并没用，任务总是立即被结束。

现在我找到了一个新的方法，使用`Start-Process`命令：

~~~powershell
Start-Process [-FilePath] <string> [[-ArgumentList] <string[]>]  [<CommonParameters>]
~~~

更加完整的格式可以去看微软官网的说明。

给出一个例子：

~~~powershell
Start-Process -FilePath ".\background.exe" -RedirectStandardOutput "out.txt" -WindowStyle Hidden
~~~

`-FilePath`参数给出了我们要执行的exe程序的名字，如果需要带参数，可以通过`-ArgumentList`以字符串的形式给出参数，可以重定向标准输入输出到文件，并且通过窗口样式参数指定无窗口运行，这样就可以完成后台执行命令了。

上例中，`background.c`源码如下：

~~~c
#include<stdio.h>
#include<Windows.h>


int main(int argc, char *args[])
{
	int times = 50;

	while(times>0)
	{
		printf("%d\n", times);
		Sleep(2000);
		times--;
	}

	printf("part 1 done!");

	while(times<50)
	{
		printf("%d\n", times);
		Sleep(2000);
		times++;
	}

	return 0;
}
~~~



既然如此，那么其实关于执行python之类的，就很简单了，执行pyhon文件的命令是`python test.py`，这里明显`python`是一个exe， 而文件名字是参数，所以很容易就可以做到。

也知道的吧，python自己也提供了另一种后台执行方法，就是用`pythonnw.exe`替代`python.exe`

关于上述命令，唯一一个我很不满意的问题就是，标准输出被重定向之后，输出内容不能及时刷新到文件中，在`background`测试中，直到程序完全执行结束，结果才会被一次性刷新进入重定向输出文件。



### 开机自动执行脚本

对于某些电脑，我需要它开机执行一些常驻程序。举例，我需要让电脑自动执行一个校园网登录脚本，然后使用邮件将IP地址发送给我。这些是短时的代码，会快速执行完毕。另外还需要自动启动一些常驻后台的程序，例如自动启动frp内网穿透程序，以及循环检测校园网登陆状态的代码。

总而言之，我需要开机自动启动，以及后台程序。

首先来说一下，我所面临的问题，我之前做过利用批处理脚本，放在C盘的启动目录中，来实现开机启动的功能，工作状况良好。但是现在因为要执行powershell的后台命令，所以，我想把批处理换成ps1脚本，但是也许是我电脑的问题，我好像搞错了打开方式，然后也莫名其妙的无法重新设定，总之我的ps1脚本的默认打开方式变成了用sublime打开，这就造成了极其尴尬的ps1脚本执行时是打开.......

所以我现在的妥协方式是搞一个批处理，然后用批处理启动powershell，来执行ps1脚本。

我想多找几种开机启动的方式，然后从里面选择最好的。根据我查到的资料，主要包括以下几种方法：

1. 启动目录，可以将脚本放入下述两个目录中任意一个：
    - C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup
    - C:\Users\xxxxxx\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

2. [这个网站](https://www.itprotoday.com/windows-8/powershell-script-run-certain-service)，给出了一个通过组策略的方式，但是我测试了一下，好像不太行？不过我使用ps1测试的，也许批处理会可以，我没试，重启好多次了，好麻烦呀。
3. [这里](https://www.cnblogs.com/tinysun/p/6732973.html)，给出了一个使用注册表的方式，我没试。

呃，想一下，还有其他方法没，噢，对了，我还看到了一个使用计划任务来做的，也没测试。

反正吧，我现在找到的就是这些方式。我觉得还是方式1比较简单。。。。。但是似乎系统执行重大更新会被清除？也许是升级。



需要注意的另一个问题是，我在测试时，发现似乎方式一启动的exe，并未在任务管理器中找到，但是根据输出结果看，它似乎又的确在运行。

先到这里吧。