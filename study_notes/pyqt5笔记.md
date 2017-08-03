### PyQt5
---



<font color="red">入门参考书为PyQt5 tutorial</font>

将`ui`文件转换为`.py`文件，使用命令行，命令如下：

	pyuic5 -o my_ui.py my_ui.ui


遇到的困难远比我想象的要多，以下做一个记录 ：


文本显示问题：


尝试过这么几个控件：

1、`QLabel`, 
 
2、`QLineEdit`,

3、`QTextEdit`，

4、`QTextBrowser`，

大概就是这些吧。
第一个是一个可以是多行的，但是不支持滚动（至少现在据我所知是这样的），过长的文本就无法显示了，所以多行文本就不用考虑它了，除此之外，对齐之类的，他都做得到

第二个只能显示一行，支持对齐

第三个可以显示多行，经过寻找，找到了工作状况良好的代码，可以让它以我所想要的方式工作，第一点：文本对齐，代码如下：
	self.msg_box.append("hi it's me")
        
    cursor = self.msg_box.textCursor()
    textBlockFormat = cursor.blockFormat()
    textBlockFormat.setAlignment(QtCore.Qt.AlignCenter)
    cursor.mergeBlockFormat(textBlockFormat)
    self.msg_box.setTextCursor(cursor) 


	self.msg_box = QtWidgets.QTextEdit（）
	#这一句仅用来表明msg_box是一个QTextEdit

换句话说，呃，以前我在`QTextEdit`中增加文本的方式是事先用一个字符串记录，每次增长字符串，然后直接设置`QTextEdit`的`Text`为这个字符串，从以上的代码来看，这种方式以后要被舍弃了，因为他十分之不灵活，换用上面的代码后，先`append`相当于只是将文字存入了缓存区，具体文字如何显示，有接下来的代码决定，应该是设置了光标什么的，暂时还看不懂，也就是说，这种方式下，我可以任意设置每一行的对齐方式


要求完成的第二个要求是：虽然`QTextEdit`支持滚动，但是文本过长时，他默认显示的是文本头部，而不是尾部，我们想要的是显示最后一行，这个已通过下面一行代码实现：

	self.msg_box.moveCursor(QtGui.QTextCursor.End)

也是设置了光标

虽然`QTextEdit`有一个设置对齐的方法，但是不要尝试了，它并不会生效。


至于最后一个，我认为没有太多的必要使用。


---

####接下来是要完成一个合适的驱动方式

---
记住，直接在`sys.exit(app.exec_())`之前写一个过程性的代码，会崩溃，在之后写则根本不会运行到，所以要考虑一个合适的驱动方式



过程比我想得要漫长，电脑端的UI已经写了一天了，还只是完成到了一半。。。。


再记录一点：

	self.setFixedSize(self.width(),self.height())

这一句应该可以阻止窗口大小的调整，当然里面的参数可以直接改成数字，应该把。。。



一边是ui界面在工作，另一边tcp在尝试通信，而ui有自己的主循环，tcp的延迟又无法确定，所以，我认为无法融合两者，唯一的解决方式，也许就是多线程，暂时，似乎要选择Qt自带的多线程，而不用python的多线程，因为涉及到信号触发问题，所以，应该是这样的。。。

解决方法已经找到，代码如下：

	class my_tread(QtCore.QThread) :
    	signal = QtCore.pyqtSignal()
    
    	def __init__(self) :
        	super().__init__()
 
    	def run(self) :
        	for i in range(50) :
            	sleep(3)
            	print("i am running",i)
            	if i==10 :
                	self.signal.emit()


	class my_ui(QWidget) :
    	def __init__(self) :
        	super().__init__()
        
        	self.tre = my_tread()
        	self.tre.signal.connect(self.edit)
        	self.tre.start()
        	self.setui()
                

首先创建一个新的类，继承自`QtCore.QThread`，这个类需要写一个初始化方法，同时必须创建一个`run`方法，用来覆盖`QtCore.QThread`的`run`方法，在`run`方法里面写业务代码，换句话说，线程开始后，所执行的代码就是`run`方法里面的。

接下来，需要在主线程的初始化方法中实例化自行创建的线程类，然后调用这个实例的`start()`方法，这样就完成了在主线程之外新开一个线程的任务。


---

接下来，需要注意的另外一个问题就是自行产生信号。


我们需要在辅助线程中创建一个信号，特定情况下，这个信号触发，然后这个信号会传递给主线程中的一个特定函数，对UI做出某些行为。

下面代码实现这样的信号的 ：

	class my_tread(QtCore.QThread) :
    
    	signal = QtCore.pyqtSignal()
    
    	def __init__(self) :
        	super().__init__()
        
        
        
    	def run(self) :
        	for i in range(50) :
            	sleep(3)
            	print("i am running",i)
            	if i==10 :
                	self.signal.emit()

	class my_ui(QWidget) :
    	def __init__(self) :
        	super().__init__()
        
        	self.tre = my_tread()
        	self.tre.signal.connect(self.edit)
        	self.tre.start()
        	self.setui()

    	def edit(self) :
        	self.msgwindow.setText("emit success!!!!!")


以上的代码，是一个大概的示例，但是明显里面我写了大量的冗余代码，他们是没有必要存在的，我写上只是因为懒得清理，解释一下，在辅助线程里面实例化`QtCore.pyqtSignal()`类，这就是一个信号对象，此处必须注意，实例化必须卸载类的第一行代码，不在任何方法内部，否则就会报错，说信号对象没有`connect()`方法，接下来是信号触发的方法，很明显，只用调用一个函数`self.signal.emit()`

我们需要在主线程里面调用辅助线程的信号，然后使用`self.tre.signal.connect(self.edit)`函数将这个信号链接到一个方法上。

大概就是这样。所有条件应该已经准备结束了。        

###PyQt4与5的区别

- 模块被重新组织了，有一些被抛弃了，如QtScript，一些被分裂了，如QtGui,QtWebKit

- 新加入了一些模块，如QtBluetooth,QtPositioning,Enginio

- 只支持新式的信号和槽处理，SIGNAL()或SLOT()不再支持

- 在Qt5.0中被标记为废弃的API不再支持

###PyQt5的整体架构

主要包含了15个模块，当然还有一些其他的模块



1.  QtCore

-  QtGui

- QtWidgets

- QtMultimedia

- QtBuletooth

- QtNetwork

- QtPositioning

- Enginio

- QtWebSockets

- QtWebKit

- QtWebKitWidgets

- QtXml

- QtSvg

- QtSql

- QtTest

比较明显的是大概4~15早期的时候都不需要做太多的学习，他们大多提供了一些特殊的功能。下面逐一对其大概的功能做一下介绍。

QtCore明显是核心，包含了time,files,directories,各种数据类型，流，URLs，mime types，线程，进程等  

QtGui包含了针对窗口系统集成，事件处理，2D图形，图像，字体，文本的类  

QtWidgets包含的是一系列的部件  

多媒体包含了可以处理多媒体内容的类，同时提供了相机，无线电等的接口，蓝牙就不说了。  
网络模块提供的是网络编程功能，它提供了构建一个TCP,UDP服务的东西  
QtPositioning它通过各种方式提供定位服务  
Enginio提供了Qt云端服务的客户端  
Websockets包含了网络套接字协议  
剩下的几个没什么好说的，要么暂时没用，要么名字就很明显

