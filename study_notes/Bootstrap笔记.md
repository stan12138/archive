## 笔记

### 基础

#### 文件结构

我现在使用的是直接从github上面下载bootstrap的压缩包，解压之后，我们需要的大概就是里面的dist文件夹，也许不叫这个名字，但总之就是一个包含了css,fonts,js三个子文件夹的一个文件夹。把这个文件夹取出来，可也改一下名字叫做bootstrap

在css和js两个文件夹里面都包含了两套文件，一套是正常后缀的，另一套的后缀之前还有.min，这两套文件完全一致，后者是被压缩过的，为了提高加载速度，用于生产环境，学习的时候推荐使用前者。

#### 如何使用

并不需要做太多的东西，bootstrap包含了css和js，如果只使用css的话，很简单，只需要把css文件包含进去即可，但是由于js依赖于jQuery，所以必须额外包含jQuery，另外由于所谓移动先行的宗旨，还有一个meta标签，似乎不要也行，但是，规范起见，还是带上吧

~~~html
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<meta name='viewport' content="width=device-width,initial-scal=1">
		<title>test Bootstrap</title>
		<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
	</head>

	<body>

	</body>
</html>
~~~

### CSS布局

#### 基础排版

##### 标题

bootstrap特别调整了h1~h6的样式，另外还额外定义了6个类，也是` h1~h6`,但是他们的表现并不与标题完全一致

另外还可以在标题里面使用small元素，这里面也特意定制了它们的样式

##### 页面主题

bootstrap定制了全局的字体，字号，间距等，并且为p元素定义了边距

如果我们想突出一个段落，可以使用lead类，效果是改变字号，粗细，行间距，边距

##### 强调文本

四个元素：small,strong,em,cite

四种对齐方式对应的类，text-left,text-center,text-right,text-justify

##### 缩略语

实现在abbr元素上面，当鼠标移动到上面的时候会显示title属性

##### 地址

实现在address元素上面，只需要每行以br元素结尾

##### 引用

blockquote元素，里面可以使用任何元素，但推荐使用p

可以使用small和cite元素注明出处

~~~html
		<blockquote>
			<p>祸莫僭于欲利，痛莫过于伤心</p>
			<small>from <cite title="史记 司马迁">史记</cite></small>
		</blockquote>
~~~

另外提供了一个右对齐，只需要将blockquote定义为pull-right类即可

~~~html
		<blockquote class="pull-right">
			<p>祸莫僭于欲利，痛莫过于伤心</p>
			<small>from <cite title="史记 司马迁">史记</cite></small>
		</blockquote>

~~~

##### 列表

提供了6种列表，分别是普通列表，有序，去点，内联，描述，水平描述

###### 普通列表

只做了一些细微的优化

和原来用法一样

~~~html
		<ul>
			<li>stan</li>
			<li>hanyi</li>
			<li>who
				<ul>
					<li>stan</li>
					<li>me</li>
				</ul>
			</li>
			<li>this is test</li>
		</ul>
~~~

###### 有序列表

也只是做了一些微调

~~~html
		<ol>
			<li>stan</li>
			<li>hanyi</li>
			<li>who
				<ol>
					<li>stan</li>
					<li>me</li>
				</ol>
			</li>
			<li>this is test</li>
		</ol>
~~~

###### 去点列表

这种列表去除了默认样式前面的圆点

其实看起来并没有那么爽

只需定义一个list-unstyled类即可，只对本层有效，不会被继承

~~~html
		<ul class="list-unstyled">
			<li>stan</li>
			<li>hanyi</li>
			<li>who
				<ul>
					<li>stan</li>
					<li>me</li>
				</ul>
			</li>
			<li>this is test</li>
		</ul>
~~~

###### 定义列表

也是一些微调

~~~html
		<dl>
			<dt>first class</dt>
			<dd>stan</dd>
			<dd>asimo</dd>
			
			<dt>second class</dt>
			<dd>this</dd>
			<dd>that</dd>
		</dl>
~~~

不知道为什么chrome里面没有缩进，看起来怪怪的

###### 水平定义列表

只需要把dl元素上应用dl-horizontal类即可，列表的表头和项将会水平排列，自己试试就知道了

~~~html
		<dl class="dl-horizontal">
			<dt>first class</dt>
			<dd>stan</dd>
			<dd>asimo</dd>

			<dt>second class</dt>
			<dd>this</dd>
			<dd>that</dd>
		</dl>
~~~

这个又莫名其妙缩进了比较多

#### 代码

##### 内联代码

使用code元素即可，做了一些样式，有一些背景，文字是深红色

##### 用户输入代码

kbd元素，不明白啥意思，效果是深黑色背景，白色字

##### 多行代码块

使用pre元素，控制了背景

#### 表格

##### 基础样式

只需要在table上面应用table类

~~~html
		<table class="table">
			<tr>
				<td>first</td>
				<td>second</td>
				<td>thied</td>
			</tr>

			<tr>
				<td>frist</td>
				<td>secod</td>
				<td>thord</td>
			</tr>

			<tr>
				<td>frist</td>
				<td>secod</td>
				<td>thord</td>
			</tr>
		</table>
~~~

##### 背景条纹

只需要在追加table-striped类即可

~~~html
		<table class="table table-striped">
			<tr>
				<td>first</td>
				<td>second</td>
				<td>thied</td>
			</tr>

			<tr>
				<td>frist</td>
				<td>secod</td>
				<td>thord</td>
			</tr>

			<tr>
				<td>frist</td>
				<td>secod</td>
				<td>thord</td>
			</tr>
		</table>
~~~

##### 边框

追加table-bordered类

##### 鼠标悬停高亮

追加table-hover

##### 紧凑型表格

追加table-condensed

##### 行样式

特意为tr增加了五种额外样式，控制背景颜色，分别为以下5类：

-   active,表示当前活动
-   success，表示成功或正确
-   info，表示中立的信息
-   waring,警告
-   danger,危险错误

##### 响应式表格

只需将表格包含在一个div中即可，div声明为table-responsive类

这主要是应对小屏幕，出现滚动条



#### 表单





### CSS组件

组建共有21种

#### 小图标

小图标应用于内联元素，只需要在内联元素上加上两个类即可：

`class='glyphicon glyphicon-serach'`

后面的类名的后半部分指明了是哪个图标



#### 下拉菜单

啊啊啊



#### 按钮组



#### 按钮下拉菜单



#### 输入框组



#### 导航



#### 导航条



#### 面包屑导航



#### 分页导航



#### 标签

#### 徽章



#### 大屏幕展播



#### 页面标题

####缩略图

#### 警告框



#### 进度条



#### 媒体对象



#### 列表组



#### 面板



#### 洼地



#### 主题

