### 工具

写大的代码文件，一般使用spyder

但是在平时做一些简单的交互式测试的时候，一般使用jupyter notebook

在做网络编程的时候，常用的是sublime text3+cmd

#### jupyter notebook

打开一个命令行，输入jupyter notebook，即可运行起来notebook

最基本的，我需要设置字体，因为原本的字体实在太难看了，打开anaconda下面的Lib/site-packages/notebook/static/custom/custom.css，在里面添加这样的css`.CodeMirror pre {font-family: 'Source Code Pro';}`即可

呃，还有结果输出的样式：`div.output_area pre {font-family: 'Source Code Pro';}`

然后，运行的快捷键是shift-enter



### 有很多模块包的网站

[下载python模块的网站](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame)

1，查看所有的模块列表，使用help('modules')

2、 urllib可以制作爬虫

3、如何存储文件到指定文件夹，关键在于获取路径，下面就是pythonista的文件路径:
'/private/var/mobile/Containers/Shared/AppGroup/1E6396A6-FB23-4A10-B1BB-B5F1F35BE42E/Pythonista3/Documents/picture/%s.png'%x

4、另一种方法，导入sys,使用sys.executable,可以获得pythonista3的路径

9,文件a已经导入了x模块，文件b导入了文件a，那么b就也间接导入了x模块

### 关于列表的拷贝技术：

列表是可变对象，直接传入，或者直接使用=进行拷贝，在改变时都会造成原列表的改变，因而，常用的列表拷贝技术是：a=b[:]
但是，这种方法并不安全，对于简单的一维列表，这种方式是有效的，但是对于结构复杂的列表这种方式在某些情况下往往会失效（并不是所有的情况下都会失效，甚至有一定的不确定性，我只隐约观察到了一点规律，并不确定），虽然使用id()去观察会看到两个变量是不同的物理地址，总而言之，对于复杂的列表，可靠的拷贝技术为：

~~~python
from copy import deepcopy

a = deepcopy(b)
~~~


这种方法是绝对安全的。此外，本方法用处很广，例如，类也是可变对象，传入函数是怎么办？怎么进行拷贝？deepcopy可以

==以后尽量少用import *==





## python包的经验


>这是一个关于python模块的重新说明，
>
>事实上这只是一个十分局限的说明，关于包
>
>2017/4/24 14:58:55 --stan

#### 为什么使用包？

大概也就是为了可以在常用的代码文件夹下创建一个已完成代码的文件夹，然后把不太会修改的代码放进去。

#### 要求与用法


- 首先，放置这些文件夹的上级或说更高级的目录必须是一个已经在搜索路径里面的目录
- 然后，记住python的import里面是使用`.`来代替`/`的
- 这条路径上的所有文件夹里面必须包含一个`__init.py`文件，这个文件可以是一个空文件，当然这个文件也可以写一些代码，当导入发生时，这个文件里面的代码会首先默认执行，例如我们可以在这里面控制`import*`时会发生什么


#### 相对导入

例如文件夹的目录结构如下所示：

目录树画不出来了，直接描述吧

相对导入存在的意义就在于：解决导入路径的模糊性，例如当前文件所在目录有一个文件，恰好他的名字和默认路径上的某个文件名字一样，或者和某个内置模块的名字相同，那么，怎么确定导入的是哪一个呢？

关于语法，以当前文件所在路径为标准，一个点号回到该文件的父目录，两个点号回到父目录的父目录，使用方法如下： 

文件夹A下有两个文件夹：B和C，B下面有D和E，当前文件夹为E，则执行`from . import D`会导入文件D，执行命令`from .. import C`会导入文件C 

总而言之，相对导入存在的目的就在于让导入的路径更加精准，如果你可以确认不会因为路径不准确而发生任何错误，则不用考虑

#### 关于导出的内容的控制

假如有一个文件`imagetools.py`,我打算使用这个文件作为一个模块使用，但是我想防止当用户使用`from imagetools import *`时导出了太多的东西，我应该怎么办?
解决的方法就是在该文件中写一个列表，`__all__=[]`，在列表中使用字符串列出所有希望导出的变量的名字，那么当使用`import *`时将只会导出列表中列出来的变量





### 关于命令行的pip install

我使用

`pip install IPython --upgrade`
时出现了如下错误

`Cannot remove entries from nonexistent file d:\anaconda3\lib\site-packages\easy-install.pth`
此时需要使用如下命令：

`pip install IPython --upgrade --ignore-installed`

### 关于IPython

简直了，默认情况下，ipython中matplotlib的图像显示的方法是inline也就是嵌入式的，此时如果是动画就无法更新，所以我最喜欢的还是弹出式显示，但是我使用了网上给出的所有方法进行设置，我尝试过：
~~~python
	%matplotlib qt
	%gui qt
	%gui qt5
	switch_backend("Qt5Agg")
~~~
等等，各种方法，均无效，甚至导致无法显示图片
最后我终于解决了，直接在spyder的设置里面找到IPython的设置，然后设置graphic..里面的backend为自动，总之不要是inline就行，确认，重启spyder即可
不知道为啥以命令的形式设置就不行呢?

### functools

functools模块提供了一些用于函数的工具，例如偏函数

#### 偏函数

对于一个函数，也许有很多参数，或者说可以设置很多参数，对于一个特定的需求我们可能每次调用都要设置一次某个参数，很麻烦，但是偏函数可以帮我们把某个函数的某个参数设置为我们想要的默认参数，并返回设置后的一个新函数：
~~~python
	int('10',base=2)
	//这个可以把int函数设置为二进制转换，但是每次都需要为base设置为2，不然就是10进制的默认参数
	int2 = functools.partial(int, base=2)
	int2就是新的函数
~~~
若不加关键字，将会自动设置为最左边的参数

### 很牛叉的代码中运行代码

实现的效果是怎么样的呢？我可以写一个GUI或者Web页面，自制一个编辑器，接收收入的字符串，然后写入到一个.py文件中，然后使用代码运行这个文件，并接受输出结果，然后再放回到GUI中。 
~~~python
	import sys
	import subprocess
	
	a = subprocess.check_output([sys.executable,filepath],stderr=subprocess.STDOUT, timeout=5)
~~~
a就是filepath指的代码的运行输出结果，但是是一个二进制字符串，怎么解析就不必说了吧。  
稍微解释一下，check_output似乎是一个可以执行命令的函数，并给出返回值，第一个参数是一个列表，列表的第一个值sys.executable是一个字符串，它是本电脑上面python解释器的exe文件的路径，filepath是要执行的文件的目录，stderr是一个固定参数，用来处理错误的，换句话说如果运行出错会返回错误信息，timeout设定最长运行时间。

差不多就是这样了，再多的细节我也不太清楚。  

你如果很感兴趣的话，廖雪峰给了一个完整的网络代码编辑器的实现，见网址[python运行助手](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432523496782e0946b0f454549c0888d05959b99860f000)



### 关于目录和文件的操作

主要使用的模块是os和shutil

-   os.getcwd(),获取当前脚本的工作目录
-   os.listdir()，返回指定目录下的文件和目录名字
-   os.rename(old,new)，重命名
-   os.mkdir(dirname)，创建一个单级目录，可以指定完整路径名字，从而在其他磁盘创建
-   os.remove(filename)，删除文件
-   os.removedirs(dirname),删除目录,只能删除空目录
-   shutil.rmtree(dirname)，删除任意目录
-   shutil.copyfile(oldfilename,newfilename)
-   shutil.copytree(olddir,newdir)，将一个目录复制，newdir必须不存在
-   shutil.move(old,new)，移动


### 关于time

和time有关的有time和datetime两个模块，这里只简单的记录一两个函数

-   time.time(),时间戳，单位是秒，用来做计时还不错，无论windows还是Unix
-   time.sleep(),暂停，单位是秒，支持小数
-   time.clock()，在win上面第一次调用的返回值没啥用，但是之后每次调用都会返回与第一次调用的时间间隔，单位秒，还算可以，但是在Unix上面返回值一直都很诡异，还是别用了

### 关于signal

我现在了解的真的都很少，并没有细读任何东西，下面只讲一点

我们可以设置一个捕捉特定信号的处理函数，但是只能捕捉某些信号，

总而言之，它可以完成使用ctr-C结束多进程等的任务

~~~python
import signal,time

stop = False

def handler(a,b) :
    global stop
    stop = True
    print('get stop')
    
    
signal.signal(signal.SIGINT,handler) 

start = time.time()

while True :
    if not stop :
        if time.time()-start>2:
            print('2 seconds past....')
            start = time.time()
    else :
        print('I stop')
        break
~~~

就像上面所示，常规的使用方法是在信号处理函数中设置一个用于全局停止的变量，这里设置的signal.SIGINT可以捕捉ctr-C

使用方式就是使用signal.signal()设置信号的处理函数

需要注意的是，这个函数必须在主线程设置。



### 装饰器

这里只讲基本的装饰器函数。

~~~python
def t(func) :
	def t2(a) :
		print('this is stan')
		return func(a)
	return t2

@t
def test(a) :
	print('stan')
~~~

这里你要写一个函数，接受一个函数作为参数，然后当你使用@语法之后，实际上得到的是：

test = t(test)

接下来只需要分析t函数就可以了，t(test)的返回值是t2，所以test实际上变成了t2，当你调用test的时候就会先print('this is stan')，然后返回原本的test函数的返回值，实际上这里是没有返回值的，只是会运行一下test函数，但是，当有返回值的时候返回就有作用了

接下来要更进一步：

如果想让装饰器接收参数，如@t('stan')，那就必须为其再增加一层包装，因为t('stan')已经在执行一个函数了

~~~python
def t(b) :
	def t2(func) :
		def t3(a) :
			print('this is stan')
			return func(a)
		return t3
	return t2

@t('stan')
def test(a) :
	print('stan')
~~~

其实是蛮容易理解的吧

这里再给出一个flask里面用来设置url的装饰器，他的目的只是关联url和相应的处理函数，并把处理函数收集起来，所以它的装饰器原型是这样的

~~~python
	def set_url(self,url,method='GET') :
		def second(func) :
			if method=='GET' :
				self.get_handle_func[url] = func
			elif method=='POST' :
				self.post_handle_func[url] = func
			return func
		return second
~~~

使用的时候：

~~~python
@ap.set_url('/')
def index() :
	with open("static_file/homepage.html",'rb') as fi :
		rep = fi.read()
	#print('got html file')
	return rep
~~~

稍微分析一下，set_url是第一层包装，只是用来让装饰器可以接收参数的，然后才会返回一个基础版的装饰器即second，当使用这个装饰器的时候，就相当于在做，index = second(index)，于是我们就成功的收集到了index，这是只需要把他和url一起存入字典即可，至于return func，实际上并没有什么用，这是写一写

装饰器就讲这么多

### 生成器

这里讲的生成器指的是生成器函数，而不是表达式

基础的形式只有两种：yield value和value = yield

#### yield value

这种形式的生成器函数配合next()函数使用，它每次都运行到yield语句，然后当调用next()函数的时候，会返回value，然后继续运行，直至下一个yield

~~~python
def gen() :
	a = 1
	while True :
		yield a
		a = a+2

s = gen()
next(x)

~~~

每次调用next就会返回一个a的值，然后运行a=a+2，然后再次断在yield语句处

#### value = yield

这种形式的生成器函数配合send方法使用，同样每次到会运行到yield语句，然后等待从send里面获取一个值，然后继续运行，直至下一个yield

~~~python
def gen() :
	while True :
		a = yield
		print('I got ',a)

s = gen()
next(x)
s.send(1)

~~~

这里只是要注意，我们在调用send方法之前，必须确保生成器运行到了yield语句处，方法就是先调用一下next,这是规范化的一步，叫做预激协程

总而言之，首先使用next预激协程，使用send使协程工作，然后还可以调用close关闭协程，另外close也是可以捕捉的

当协程退出时，他会收到一个GeneratorExit异常，只要捕捉这个异常就好

#### 运行状态

事实上，一个使用生成器函数定义的协程有四个状态：GEN_CREATED,GEN_RUNNING,GEN_SUSPENDED,GEN_CLOSED

其中第一个状态是协程未启动状态，前面的value = yield，当只是执行了s=gen()之后，就出在这个状态，这个时候如果你调用send就会收到一条错误消息，消息很清楚地表示了生成器的状态，这是必须执行预激活

当解释器处在运行中，就是第二种状态

在yield处暂停是第三种状态



#### 复合语句

我们可以把`value = yield`和`yield value`两种语句结合在一起

~~~python
def gen3() :
	a = 2
	while True :
		b = yield a
		print('I got ',b)
s = gen3() #1
next(s)    #2
s.send(3)  #3

~~~

这里，我暂时无法做一些解释，我只能描述他工作的方式

注意，首先我们从前面可以观察到yield value也是会暂停的，当使用next时才会继续运行

然后a = yield也会暂停，需要执行一次send

所以，可以按照这个分析一下上面的代码怎么运行：

1、第一步必须执行next(s)，预激活，然后程序会执行到yield a，返回a，然后等待

2、第二步应该执行send,程序继续运行，到yield a之前

接下来每执行一次next,返回一个值，再执行一次send接收一个值

当然可以连续执行两次next，那么就会收到一个None

天衣无缝是不是？但是，事实并非如此

事实上的常规运行是：预激活，然后不停调用send就行了，程序只会在b=yield处产生断点，yield a则会自动执行，并不需要调用next，如果调用了next则相当于send(None)

~~~python
def gen3() :
	a = 2
	while True :
		b = yield a
		print('I got ',b)
        
        
s1 = gen3()
next(s1)
out :2
s1.send(5)
out: I got 5
out: 2
next(s1)
out: I got None
out: 2
~~~

如上所示

总而言之，断点只有b = yield，而yield a会自动执行，除了预激活之外不需要使用next

我知道很诡异

#### 预激活装饰器

如果忘记预激活了，就很麻烦，所以可以使用一个装饰器，自动完成预激活

~~~python
from functools import wraps

def coroutine(func) :
	@wraps(func)
	def primer(*args,**kwargs) :
		gen = func()
		next(gen)
		return gen
	return primer

@coroutine
def test() :
	total = 0.0
	count = 0
	av = None
	while True :
		term = yield av
		total += term
		count += 1
		av = total/count

b = test()
b.send(2)
~~~

用法完全一致，只不过可以少了预激活

前面的wrap装饰器可以直接忽略掉，因为他只是用来弥补装饰器的缺陷的，因为是用完了装饰器之后func的`__name__`等属性会改变，wrap只是把它改回来

#### 终止协程与异常处理

截止到目前为止，如果向协程send了不合乎要求的值，将会直接导致抛出异常，协程也将终止，并且无法使用send再次激活

这实际上说明了可以使用这种方式终止协程

生成器提供了两个方法，throw和close

后者可以直接关闭生成器，前者可以向生成器传入一个异常，如果想在关闭时做一些操作，则需要使用try...finally

~~~python
def test() :
	total = 0.0
	count = 0
	av = None
	try :
		while True :
			term = yield av
			total += term
			count += 1
			av = total/count
	finally :
		print('stop')
  
~~~

#### 生成器的返回值

如果想要通过return拿到生成器的值比较麻烦，因为生成器的停止一定会抛出异常，返回值将以异常的value的形式给出，所以，我们必须这样：

~~~python
def gen3() :
    a = 2
    while True :
        b = yield a
        if b==1 :
            break
        print('got ',b)
    return 10
s = gen3()
next(s)
try :
    s.send(1)
except StopIteration as t :
    ret = t.value
~~~

ret就是返回值



#### yield from

这是一个新增的语法，我认为它存在的目的就是为了解决如何在一个生成器中调用另一个生成器，如果你想要尝试一下手工实现这个目的，并完整的实现输出，传递数据，处理异常，各种方法调用，你就会知道，这也是一个比较麻烦的问题，yield from解决了这所有的问题，如此。

假设函数A是：`yield from B()`

B()会返回一个可迭代对象（或者生成器），A也会返回一个生成器，分别称之b,a

那么，借用一个博客上面的记录：

>   1.  b迭代产生的每个值都直接传递给a的调用者。
>   2.  所有通过`send`方法发送到a的值都被直接传递给b. 如果发送的 值是`None`，则调用b的`__next__()`方法，否则调用b的`send` 方法。如果对b的方法调用产生`StopIteration`异常，a会继续 执行`yield from`后面的语句，而其他异常则会传播到a中，导 致a在执行`yield from`的时候抛出异常。
>   3.  如果有除`GeneratorExit`以外的异常被throw到a中的话，该异常 会被直接throw到b中。如果b的`throw`方法抛出`StopIteration`， a会继续执行；其他异常则会导致a也抛出异常。
>   4.  如果一个`GeneratorExit`异常被throw到a中，或者a的`close` 方法被调用了，并且b也有`close`方法的话，b的`close`方法也 会被调用。如果b的这个方法抛出了异常，则会导致a也抛出异常。 反之，如果b成功close掉了，a也会抛出异常，但是是特定的 `GeneratorExit`异常。
>   5.  a中`yield from`表达式的求值结果是b迭代结束时抛出的 `StopIteration`异常的第一个参数。
>   6.  b中的`return <expr>`语句实际上会抛出`StopIteration(<expr>)` 异常，所以b中return的值会成为a中`yield from`表达式的返回值。

从外在表现上面看，你会感觉到，你对a的操作完全就是在直接操作b，没有任何区别，因此一系列表现与上面讲的生成器没有区别。



#### 一些关于输出的小把戏

我主要感兴趣的就是原地显示和颜色控制

##### 原地显示

所谓原地显示指的是覆盖上一个字符，始终在原处显示，主要为了表现一种等待的状态，这里主要使用的是转义字符，据我所知控制输出位置的字符有两个`\r`和`\b`，前者的表现是将输出位置转移到本行的最前端，然后当你继续输出的时候就会依次覆盖前面的字符，后者的表现是输出位置前移1个位置，也就是说会覆盖前一个

借助`\b`，我们可以实现一个原地旋转的`\`，当然要配合一下time.sleep，关于sys.stdout.write和print的区别我就不必多说了吧，总之前者是无格式输出

这里给一个样例：

~~~python
import time
import sys

def test() :
    a = ['\b-','\b\\','\b|','\b/','\b-','\b\\','\b|']
    print('this is test e',end='')
    for i in range(5) :
        for j in a :
            sys.stdout.write(j)
            time.sleep(0.4)

test()
~~~

这个，在普通输出的时候的确工作的蛮好的，那么在windows命令行下的表现如何呢？你以为就这样就ok，那你想的就太简单了，在命令行下如果你运行这样的代码，你会发现输出会卡死。

怎么解决？很可悲，百度似乎并找不到结果，google了之后找到了一个答案，答案是输出是存在缓存的，所以结果并不会立即展示，所以我们需要手动刷新，方法很简单只需要在每一个time.sleep下面加一行sys.stdout.flush()就好

##### 颜色控制

颜色控制来自系统，与语言无关，他是一串转义序列，我们可以将其嵌入到字符串中，下面给出这个特殊转义序列的书写格式：

`\033[显示方式;前景色;背景色m`

我们只需要将这串序列嵌入到字符串中，就可以使接下来的输出全部以指定的颜色显示，直至我们做了新的更改。其中的显示方式是使用数字标识的：

-   0,终端默认设置
-   1，高亮
-   4，下划线
-   5，闪烁
-   7，反显
-   8，不可见
-   22，非粗体
-   24，非下划线
-   25，非闪烁
-   27，非反显

前景色和背景色也是用数字表示，前景色是30-37，背景色是40-47，对应的数字颜色是一致的

-   x0，黑
-   x1，红
-   x2，绿
-   x3，黄
-   x4，蓝
-   x5，紫红
-   x6，青蓝
-   x7，白

系统默认的样式是`\033[0m`

举一个栗子：

~~~python
print('\033[1;31m')
print('this is stan test')
print('\033[0m')

print('\033[1;31mthis is stan test\033[0m')
~~~

但是你以为这么就结束了吗？naive。

这种代码是无法直接使用在logging的format里面的，至少在使用配置文件和命令行的情况下是不行的。

即便只是单单的命令行，也是无法使用的。

换句话说，在windows命令行中这种代码是无法使用的。想要在命令行使用，我们必须调用win的设置，使用ctypes：

~~~python
import ctypes

std_out_handle = ctypes.windll.kernel32.GetStdHandle(-11)

def set_color(color,handle=std_out_handle) :
	ctypes.windll.kernel32.SetConsoleTextAttribute(handle,color)
def reset() :
	set_color(0xf0)

black = 0xf0
red = 0xfc
yellow = 0xfe
~~~

这里面的获取handle的部分，-11是标准输出的代码，-10是输入，-12是标准错误

然后在颜色设置的时候，需要使用两位十六进制代码，其中的高位代表背景色设置，低位代表前景色，对应的色彩是一致的：

0-f分别为：

| 代码   | 颜色   |
| ---- | ---- |
| 0    | 黑    |
| 1    | 暗蓝   |
| 2    | 暗绿   |
| 3    | 暗天空蓝 |
| 4    | 暗红   |
| 5    | 暗粉   |
| 6    | 暗黄   |
| 7    | 暗白   |
| 8    | 暗灰   |
| 9    | 蓝    |
| a    | 绿    |
| b    | 天空蓝  |
| c    | 红    |
| d    | 粉    |
| e    | 黄    |
| f    | 白    |

我们每个输出最好先设置色彩，然后reset