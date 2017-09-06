## Flask学习笔记

>事实上，我并没有太大的学习需求，只是感觉好玩，这里只是一个简单的要点记录
>---stan

### 简单的开始

下面就是一个可以工作的例程：

~~~python
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index() :
    return render_template('hello.html')

if __name__ == '__main__' :
    app.run()
~~~

这里大概就是最初要知道的事情，如何创建一个app，如何写一个url处理函数，如何给出返回结果，以及如何运行。

经过尝试，通过threading和signal加强ctr-c退出的尝试并不成功

#### 静态文件

我总是卡死在静态文件的地方，Django就是死在这里，写完了自己的垃圾服务器之后大概也有感觉了吧，静态文件的路径问题的确相对而言要比一个普通的程序文件的路径要复杂一些，更不要提这还是要通过jinja2进行模板解析的了，下面进入正题，如何加载静态文件。 

如果你不使用模板进行渲染，那么可以直接在代码中使用with读出html文档的字符串，直接在视图函数中返回即可，这个时候html文档放在哪里就无所谓了

但是如果你要使用模板进行渲染，那么要在程序目录下新建一个名字叫templates的文件夹，html就放在这里面，jinja2会默认找到这个文件夹，去里面加载的。如果不行，删掉重建，关机重启都可以试试，因为我遇到过，大概是代码抽风了。

然后就是css,图片,js什么的了，这些文件必须要在程序目录下再建一个static目录，然后把它们放在里面，当然你想更细致的分出来css的目录，可以再建一个子文件夹，但是必须要在static下面。html里面的link可以直接写相对路径，如：`static/mycss.css`，也可以使用模板提供的地址，如下：

```html
<!DOCTYPE html>
<html>
	<head>
		<title>this is stan</title>
		<link rel="stylesheet" type="text/css" href="{{url_for('static',filename='mycss.css')}}">
	</head>

	<body>
		<h1>Stan!</h1>
	</body>
</html>
```

但是，我现在并不清楚为什么，即便我使用相对地址，即便我已经写了statics这个名字，还是不行，静态文件的文件夹的名字必须是static,不知道它的实现方式，应该找源码看一下。

说实话，我很讨厌静态文件的地址要写得那么复杂，恶心至极。



#### 动态路由

```python
@app.route('/user/<name>')
def index(name) :
	return '<h1>Hello,%s</h1>'%name
```

<>中包含的即为可变部分，同时装饰器可以识别并把这个参数传入路由函数



### 动态模板（jinja2的使用）

#### 渲染模板

jinja2使用render_template函数来渲染模板，接受的第一个参数是文档的名字，引擎会自动去templates文件夹下寻找，其他参数都是关键字参数，关键字即模板中的变量名

#### 变量

使用{{name}}这样的形式表示一个变量

变量不仅可以是一个单值，也可以是复杂的形式，例如字典，列表

同时可以使用过滤器对变量进行一些修改和定制，形式为{{name|过滤器}}。

常用过滤器包括：safe,capitalize,lower,upper,title,trim,striptags。

他们实现的功能包含了，控制转义，大小写转换，空格等格式控制，标签清除等



#### 控制结构

这里所说的控制结构就是程序中的流程控制。可以使用流程控制语句来对模板进行大量的修改，如条件控制语句，循环语句（产生一组类似的结构），语句中的语句部分都使用{%xxxxxx%}包裹起来，支持宏，支持模板继承等。

##### 条件语句

~~~html
{% if user %}
	hello,{{user}}!
{% else %}
	hello,stranger!
{% endif %}
~~~

##### for循环

常常使用for循环产生一组相似元素，例如列表：

~~~html
<ul>
  {% for comment in comments %}
  	<li>{{comment}}</li>
  {% endfor %}
</ul>
~~~

##### 宏

宏类似于函数

~~~html
{% macro render(com) %}
	<li>{{com}}</li>
{% endmacro %}

<ul>
  {% for comment in comments %}
  	{{render(comment)}}
  {% endfor %}
</ul>
~~~

从上面可以看出，宏类似于函数，但是，它似乎是一种就地生成的东西，不需要写返回值，大概的感觉吧

###### 宏文件

可以将一些反复使用的宏保存为文件，类似于模块包，导入的语法是这样的：

~~~html
{% import 'macros.html' as macros %}

<ul>
  {% for comment in comments %}
  	{{macros.render(comment)}}
  {% endfor %}
</ul>
~~~

不在说太细了，自己体味一下

##### 模板复用

书上只提了一下`{% include 'test.html' %}`，其他的并没多提

##### 模板继承

你需要首先创建一个.html模板文档,里面可被定制化的部分是block

然后在新的文档里面只需要使用`{% extend 'base.html' %}`包含，然后修改block即可，大概不太用得上吧。



### 插件

我很讨厌这样做，bootstarp插件，表单插件等等，什么都要用插件，很恶心。就不能直接用吗？



### 自定义错误页面

例如为404和500自定义错误页面

~~~python
@app.errorhandler(404)
def page(e) :
	with open('templates/wrong.html') as fi :
		rep = fi.read()
	return rep,404
~~~



### 链接

url_for()，啥？



呃，到这里，我似乎明白了一点东西，但是并说不太清，这是关于静态文件为什么要使用url_for的。

我感觉这应该是flask的框架，或者测试服务器处理的问题，现象是：

当故意输入一个错误的url，如`127.0.0.1:5000/templates/hello.html`，因为它没有视图函数，所以，会引发一个404，因而前面写的404处理的视图函数就会返回wrong.html，但是即便我在wrong.html里面写了去static/wrong.css里面寻找css文件，但是服务器寻找的路径却是`templates/static/wrong.css`，因而无法加载出css文件，但是当做完必要的修改，使用url_for和模板渲染之后，就一切正常了，据书上的解释，url_for会把路由映射到根目录，blabla，暂做记录如此



### 本地化时间与日期

又是插件，滚吧



### 表单



