## pythonista上的UI模块的用法

> 关于ui模块的用法的说明

> --stan


### 基本
---

一般使用两个文件，一个`.pyui`文件，一个`.py`文件，前者是ui设计文件，后者相当于后台文件,两者的文件名字没有必要的要求。

以下以`core`代表后台文件，以`front`代表ui设计文件。

	v = ui.load_view('front')
	v.present('sheet')  #另外还有几个模式，'popover','fullscreen'


动作函数要定义在`load_view`之前

ui设计界面里，例如按键这些元素会有一个`action`属性，填写触发的动作函数的名字

动作函数只会有一个默认的传入参数，sender，这个代表被触发的部件

另外，对于不同的部件还有一些各自独特的参数，例如`slider`具有一个`value`，等等，具体的可以看手册


### 其他的一些
---

其实要说的东西也不是特别多了

例如之前我们使用`v = load_view('front')`拿到了主view，这个时候我们可以认为v是一个字典，可以使用键来访问其中的部件，在设计文件的界面可以为每一个部件设置名字，在v中就可以使用具体的某个部件的名字作为键来访问这个部件，并设置其相关属性

另外我们可以使用`v.subviews`拿到v的所有子部件，得到的是一个元组
我们可以使用某个部件的`superview`属性得到部件的`父view`，例如在被触发的动作函数中，我们可以使用`v = sender.superview`得到`sender`的`父view`

至于其他的详细的细节，自己看手册

### ImageView
---

特别介绍一下`imageview`

例如，vim是一个`imageview`，那么我们可以使用`vim.image = a`来设置显示的图片，其中的a必须是一个ui.Image，简单化的，我们可以使用`a = ui.Image.named('mou.png')`得到

然后如果这是一张经过PIL处理的图片，那么可以使用以前提到的首先将图片保存到一个`io.BytesIO()`容器的技术传入，具体细节看另一份经验记录

如果这是一张来自`matplotlib`的图片，那么同样的，也是可以先使用`savefig`保存到`io.BytesIO()`,然后传入到`ui.Image`


