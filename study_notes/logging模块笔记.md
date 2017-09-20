## logging模块笔记

因为在写服务器，总是使用print显得有点low，并且有些信息输出的样式不太好，因此我决定学习logging



可以认为logging里面包含了5个常用级别：

-   logging.DEBUG
-   logging.INFO
-   logging.WARNING
-   logging.ERROR
-   logging.CRITICAL

级别依次增加，这里面是有了一个level的，低于这个级别的将不会被记录，包括打印和输出到文件，默认的level是WARNING

不做任何设置的时候，我们可以使用logging.debug(message),logging.info(message),logging.warning(message),logging.error(message),logging.critical(message)来进行屏幕的输出，必须注意低于level的不会被输出



然后我们可以对输出的格式进行设置，使用logging.basicConfig()来设置，参数有很多：

-   filename，设置日志文件的名字，后缀也要自己写，一般是.log，例如：filename = 'stan.log'

-   filemode，'w'或'a'

-   level，指定级别，例如logging.DEBUG

-   format，这是最复杂的参数，里面可以包含很多信息：

    -   %(levelno)s，输出日志级别的数值
    -   %(levelname)s，级别名字
    -   %(pathname)s，当前程序的路径
    -   %(filename)s，当前程序名字
    -   %(funcName)s，当前函数名字
    -   %(lineno)d，当前行号
    -   %(asctime)s，时间
    -   %(thread)d，线程ID
    -   %(threadName)s，线程名字
    -   %(process)d，进程ID
    -   %(message)s,日志信息

    你每给出一项，就会输出一项的信息，并严格按照给定的次序和格式，例如：

    `format='[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s : %(message)s'`

    这样的格式将会输出：

    `[时间] 文件名[line:序号] 级别：信息`

-   datefmt，指定时间的格式，这也是一个字符串，是time.strftime()

    -   %a，星期几，简称
    -   %A，全称
    -   %b，月，简称
    -   %B，全称
    -   %c，
    -   %d，一月的第几天[01,31]
    -   %H，小时，24小时
    -   %I，12小时
    -   %j，一年的第几天[001,366]
    -   %m，月,[01,12]
    -   %M，分钟,[00,59]
    -   %p，AM,PM
    -   %S，秒,[00,61]
    -   %U，一年的第几周
    -   %w，周几,[0(周日),6]
    -   %W，和%U一样，但是两者的起点不一样
    -   %x，本地格式的日期格式
    -   %X，本地格式的时间格式
    -   %y，一个世纪里的第几年
    -   %Y，完整年份
    -   %z，时区
    -   %Z，时区名字
    -   %%，%

    例如我们可以这样设置：

    `datefmt='%d/%m/%Y, %H:%M:%S'`

-   stream，指定日志输出到哪，默认sys.stderr，当你设置了filename的时候，这个参数将被忽略，所以本质上没啥意义



如果我们已经指定了将日志输出到文件，那么想要同时输出到屏幕就必须做一些比较复杂的操作：

我们需要定义一个StreamHandler：

~~~python
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
~~~

可以看得出，上面的配置是比较复杂的，我们可以使用配置文件来代替这种配置：

配置文件的后缀并没有特殊要求，可以自定，一般是conf什么的

一般而言配置文件是这样的：

~~~python
[loggers]
keys=root,first,second

[logger_root]
something

[logger_first]
something

[logger_second]
something



[handlers]
keys=handle1,handle2

[handler_handle1]
something

[handler_handle2]
something



[formatters]
keys=form1,form2

[formatter_form1]
something

[formatter_form2]
something

~~~

大概的规律还是可以看出来的吧，分为三块loggers，handlers，formatters

举个栗子，如果我们要同时输出日志文件，屏幕，那么我们应该需要三个logger，两个handler，两个format

三个logger是因为要写一个root，我不知道为啥，然后handler是处理类，format是格式

针对loggers，首先列出keys，然后以logger_keyname设置每一个，一般我们应该设置level，handlers，propagate，qualname。第一个是级别，第二个是它对应那个handler，第三个是传播等级，设置为0吧先，第三个控制着外部程序如何引用这个logger

然后是handlers，对于每个handler我们应该设置class，level，formatter，args.当我们要输出到屏幕class就是StreamHandler，文件的话就是FileHandler，控制文件备份的是handlers.RotatingFileHandler，不必怀疑为什么这个有handlers.，规定就是这样；level级别，所以，大概logger不设置就好；formatter设置对应哪个格式，args设置参数，例如对于屏幕输出args=(sys.stdout,)，对于文件args=('stan.log','a')这样的

最后是formatters，我们可以设置format和datefmt，这两个就是baseConfig里面的那两个参数

最后的最后我们应该导入logging.config，然后读入文件：

~~~python
import logging
import logging.config

logging.config.fileConfig("logger.cong")
logger = logging.getLogger('first')

logger.debug(message)
logger.info(message)
~~~

大概的总体就是这样的，下面给出一个真实的例子，细节从里面自行获取

stan.conf

~~~python
[loggers]
keys=root,first,second

[logger_root]
level=DEBUG
handlers=hand1

[logger_first]
handlers=hand1
propagate=0
qualname=first

[logger_second]
handlers=hand2
propagate=0
qualname=second


[handlers]
keys=hand1,hand2

[handler_hand1]
class=StreamHandler
level=DEBUG
formatter=format1
args=(sys.stdout,)

[handler_hand2]
class=FileHandler
level=DEBUG
formatter=format1
args=('stan.log','a')



[formatters]
keys=format1

[formatter_format1]
format=[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s : %(message)s
datafmt=%d/%m/%Y, %H:%M:%S
~~~

test.py

~~~python
import logging
import logging.config

logging.config.fileConfig('stan.conf')
f_log = logging.getLogger('second')
s_log = logging.getLogger('first')


f_log.info('this is stan test')
s_log.info('this is stan test')

f_log.warning('this is warning test')
s_log.warning('this is warning test')

f_log.error('this is error test')
s_log.error('this is error test')
~~~

