

> 大概零零碎碎的记录一些


### 图片尺寸与保存

如何设置图片的大小
此时需要使用figure产生一个图片，然后就能设置大小，figure(figsize=(a,b))

在matplotlib中，如何准确的设置画布的大小，首先先生成figure(figsize=(100,100),dpi=264)

figsize的单位是英寸，dpi即分辨率，也即每英寸像素点的个数，这样在显示的时候大概是绝对准确的


> 华硕R409JF的屏幕尺寸为1366*768，DPI大概是112
> ipad4的屏幕尺寸为2048*1536，DPI为264



但是如果直接保存：svaefig('a.png')，你大概依旧会发现像素不对，这是因为在保存的时候还要再写一下dpi，它并不会自动把显示的dpi调整到与保存时的一致，所以正确的保存写法应该是这样的：savefig('a.png',dpi=264)





### 类别
使用`a.__class__.__name__`可以查看a的类别


乱七八糟做一点记录，目前的知识对于构造树大概是够了的。
我需要了解的是在它的系统里，`Figure`是一个类，这个类的一个实例就是一个`figure`对象，大概相当于一个画板，然后在这个画板上可以创建一个坐标图，就是绘制图像的图。使用`pyplo`t里的`figure()`函数可以创建一个这样的对象。使用最上面的属性设置可以改变整个画板的大小。
然后在画板上可以创建一个坐标系，用术语说就是一个`Axes类`，然后呢，利用pyplot里面的`axes`和`subplot`都可以创建一个`Axes对象`，两者的区别在于前者可以任意改变它在画板中的位置，和大小，比较随意；后者比较规整，整齐，但自由性也比较小，经实验，使用前者也可以在一个画板中创建多个Axes但是由于某些原因，大概效果很不好，所以总结而言，如果你想创建一个可以自由调整大小和位置的***对象在画板中，那么使用前者，如果你想创建多个，那么使用后者。

一段关于基础上用的代码在pythonista里面有简单示例。
总而言之，如果利用上述方法已经创建了一个Figure和Axes对象，那么就可以任意设置相关属性.

ax = Axes
下面就可以使用ax.text，ax.annotate创建文本或者注释,详情参见matplotlib技术手册或者等我继续。


text()可以用于添加文本
一个简化版的text是这样的，text(x,y,str),即只有坐标和字符串
复杂版的里面一个较常用的参数的列表包括：alpha,color,position,rotation,ha,va,size,weight,bbox
只解释其中的几个，ha,va代表对齐属性，相当于设置锚点，但是只能设置，'left','right','center'
size也可以用fontsize
bbox代表一个文本框，bbox是一个字典，一种可行的写法是：
bo = dict(   ),bbox = bo
dict里面的参数常用的包含boxstyle,fc(facecolor),ec(edgecolor),lw(linewidth)
比较简单的就不多解释了，只说明boxstyle,类型包含larrow,rarrow,round,round4,roundtooth,sawtooth,square,每一个都可以设置pad即大小。
一个例子：

	bo = dict(boxstyle='round,pad=0.3',fc='r',ec='b',lw=10)
	text(x,y,str,color='r',rotation=45,ha='center',va='center',size=12,bbox=bo)

特别介绍，关于颜色的问题，fc,ec,color的值：
简化版的是类似于matlab的'r','b'等等
同时也支持#hex格式和rgb,pythonista上面设置比较简单，一个例子：
fc = '#df96ff'
fc = (0.88,0.59,1.0)



这里就是大概的文本的设置，接下来将介绍注释，annotate


关于怎么添加图片在`tree.py`中大概有一个示例

### 关于中文
---
大概，不能显示中文就是因为没有中文字体，下面即修改方法：
1、在`anaconda\Lib\site-packages\matplotlib\mpl-data`文件夹下可以找到一个名为`matplotlibrc`的配置文件，打开，可以找到`font.serif:.....blablabla`这样一行，把注释去掉，同时因为`-`也大概无法正常显示，所以，顺便把下面的`axes.unicode_minus:False`的注释去掉，同时该`False`为·`True`

2、搞一个中文字体的`ttf`文件，例如微软雅黑，然后将其改名为matplotlib里面的字体名，例如`Vera.ttf`，然后将其拷贝到`mpl-data\fonts\ttf`文件夹下，替换即可。

因为pythonista不允许修改内置文件夹，所以这个方法大概无法在上面实现了。

中文依旧十分之诡异，尚未完全解决

一种方式是直接替换文件夹里面的字体,现在感觉这个方式并不好，因为会导致全局字体的改变

另一种方式是：

	matplotlib.rcParams['font.family'] = 'SimHei'

这种方式可以起效，但会修改本程序的全局字体

还有一种方式就是在使用时，修改fontproperties变量：

	plt.xlabel('时间',fontproperties='SimHei')

根据视频上给出的列表，我看到了以下几种字体：

	SimHei
	Kaiti
	LiSu
	FangSong
	YouYuan
	STSong

所以这几种大概都是可以起效的，但是


