##Flask学习笔记
>事实上，我并没有太大的学习需求，只是感觉好玩，这里只是一个简单的要点记录
>---stan


####简单的开始
下面就是一个可以工作的例程：

	from flask import Flask,render_template

	app = Flask(__name__)
	
	@app.route('/')
	def index() :
	    return render_template('hello.html')
	
	if __name__ == '__main__' :
	    app.run()

这里大概就是最初要知道的事情，如何创建一个app，如何写一个url处理函数，如何给出返回结果，以及如何运行。

####静态文件
我总是卡死在静态文件的地方，Django就是死在这里，写完了自己的垃圾服务器之后大概也有感觉了吧，静态文件的路径问题的确相对而言要比一个普通的程序文件的路径要复杂一些，更不要提这还是要通过jinja2进行模板解析的了，下面进入正题，如何加载静态文件。  
首先html文件要在程序目录下新建一个名字叫templates的文件夹，html就放在这里面，jinja2会默认找到这个文件夹，去里面加载的。如果不行，删掉重建，关机重启都可以试试，因为我遇到过，大概是代码抽风了。然后要返回html的时候，必须经过jinja2的渲染，无论你想不想，就是调用上述代码中的函数。  
然后就是css,图片,js什么的了，这些文件必须要在程序目录下再建一个static目录，然后把它们放在里面，当然你想更细致的分出来css的目录，可以再建一个子文件夹，但是必须要在static下面。这还不算完，html里面的link也必须要改，如下：

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

css文件本身就没什么要特别对待的了。

好吧我错了，css未必需要url_for来指定，直接使用相对路径好像也行。好像。

####动态路由

	@app.route('/user/<name>')
	def index(name) :
		return '<h1>Hello,%s</h1>'%name

<>中包含的即为可变部分，同时装饰器可以识别并把这个参数传入路由函数




####动态模板（jinja2的使用）
jinja2使用render_template函数来渲染模板  


使用{{name}}这样的形式表示一个变量，支持字典，列表等多种形式的变量，同时可以使用过滤器对变量进行一些修改和定制，形式为{{name|过滤器}},过滤器有可以改变大小写的，等等。  


控制结构，可以使用流程控制语句来对模板进行大量的修改，如条件控制语句，循环语句（产生一组类似的结构），语句中的语句部分都使用{%xxxxxx%}包裹起来，支持宏，支持模板继承等。
