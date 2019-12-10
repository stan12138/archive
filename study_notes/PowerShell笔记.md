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

