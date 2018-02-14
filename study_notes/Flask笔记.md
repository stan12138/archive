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





## 新旅途

我重新启动flask，这一次大有不同，我购买了树莓派，我准备搭建一个包含了合格的生产服务器的完整的网页。

据网上的说法，nginx是一个不错的服务器选择，相比apache，nginx虽然有一些劣势，但是它完美的解决了c10k的问题，虽然现在这个对我而言毫无意义，但是很牛呀，他足够轻量级，只有几兆而已。可谓完美，对于树莓派而言。

在服务器和框架之间，我们需要一个过渡件，一个wsgi接口，我看到呼声最高的是`uwsgi`和`gunicorn`，这两者都只在`linux`上面可用，两者都是python的模块，据我的切身体验和初步尝试，以及风评来看，大家似乎说对于`Django`而言，前者似乎还挺好的，但是对于`flask`而言，后者的体验更好。



然后，基本确定了`nginx-gunicorn-flask`的架构。

至于数据库什么的再说吧。



一直以来我都有点排斥python的虚拟环境，但是继上一次系统被我搞坏之后，我觉得虚拟环境还是挺好的。



### 过程与环境构建

首先cd到一个你想要在这里折腾的文件夹，例如`/home/pi/flask_test`，然后在这里执行`python3 -m venv server_test`，这条命令将在当前文件夹里面构建一个虚拟环境，所有的东西地方在`server_test`文件夹内，例如`bin include lib share`等文件夹

构建虚拟环境的工具似乎很多，但是我选择这个，似乎他并不需要什么额外的模块支持吧，应该，如果需要的话可能是`virtualenv`？执行以下`pip3 install virtualenv`即可

接下来需要启动虚拟环境，首先要保证自己在`/home/pi/flask_test/server_test`文件夹下，然后执行`source ./bin/activate`

再次声明，这些所有都是在linux上面执行的，windows下面并不可行



如果成功的启动了虚拟环境你会看到命令行提示符最前面是`(server_test)`这样的



在虚拟环境下你就可以执行正常的python命令了

安装flask，`pip3 install flask`，安装gunicorn，`pip3 install gunicorn`



接下来可以做一些测试：

`vim first.py`，然后编写一个基本的flask应用：

例如：

~~~python
from flask import Falsk

app = Flask(__name__)

@app.route("/")
def hello() :
    return "hello"

if __name__ == "__main__" :
    app.run(host="0.0.0.0",port=8000)
~~~

这个文件将会保存在当前文件夹下，也即`/home/pi/flask_test/server_test`

然后可以运行一下`python3 first.py`

注意在linux上面，必须要写host为这个值，否则的话其他机器无法访问

通过gunicorn运行，不使用上述命令运行，取而代之是`gunicorn --bind 0.0.0.0:8000 first:app`

观察一下就知道，前一个是py文件的名字，后一个是里面的`app`的名字

使用`ctrl-c`就可以结束



退出虚拟环境`deactivate`





下面要安装Nginx

执行`sudo apt-get install nginx`

它将生成`/etc/nginx`，存于里面



### 运行过程

终止环境构建的部分，我要讲一下到目前为止的，我对运行过程的理解，这很有必要。但是要声明，这里面很多只是推测，并不是确切的从书上看到的，但是我对这些推测持有相当高的信心。



据以前的知识，我知道flask自带一个测试服务器，当使用python命令直接运行的时候，flask就是运行在这个服务器上面，但是，也很明确的知道这些常见的服务器框架都是运行在相同的协议上面，就是wsgi，这个协议表明了服务器应该以什么样的格式把数据交给网络框架，我们可以使用任何服务器，只要他能够完成以wsgi协议，将数据传递给flask的一个app即可。

对于nginx，它可以处理各种那个繁琐的事务，包括如何接收断开和客户端的链接，接收发送报文等一系列的工作，最最重要的一点是nginx通过它的配置文件可以配置一个`proxy_pass`参数，这个参数表明了它可以把自己接收到的报文转发给某个对象，一般是一个套接字，具有现实意义的是这个套接字是`127.0.0.1:port`，那么他就可以转发给本机的指定端口。

这时gunicorn上场了，它可以监听指定的套接字，当host指定为`0.0.0.0`的时候它可以接受以ip地址访问的请求，但是如果套接字被指定为了`127.0.0.1:8000`这样的时候，它将只监听本机8000端口的请求，注意到奇妙的链接了吗？我们只需要让nginx把请求发送到gunicorn监听的端口就好了。

最后一个步骤，gunicorn将会把报文解析，转换为wsgi格式交给他所绑定的app。于是一系列的周转完成了。



所以，明显，我们要配置nginx，然后让它运行起来，然后再使用gunicorn运行flask，两者之间自然会转发完成交互。总之，需要同时运行两个程序。

大概就是这样，但是我的确有一些疑问，例如nginx的确可以通过异步等完成高级的c10k等问题，但是它通过转发和gunicorn的交互依旧是串行的，单线交互，所以后者难道不会导致优势消耗殆尽吗？这样的话nginx的存在就完全没必要了，甚至是累赘了。

这些我还不懂，甚至也不需要懂。



### 环境续

前面讲到安装结束nginx，此时我们需要对它进行配置，他的默认启动配置文件是'/etc/nginx/sites-available/default'，两种做法，简单的，直接在这个文件上下手，复杂的在合适的文件夹下创建一个新的配置文件，然后通过链接处理，让nginx从自己写的配置启动。后者不说了，[看这里](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04)



对于前者，我们也使用要备份一下原始配置文件，说不定哪天就用上了，执行命令`sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak`

备份就是带有`.bak`后缀的那个，我们修改前者：`sudo vim /etc/nginx/sites-available/default`

前面那个链接给出的配置文件是：

~~~
server {
    listen 80;
    server_name server_domain_or_IP;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/user/myproject/myproject.sock;
    }
}
~~~

稍微解释一下，listen指定的是监听哪个端口，`server_name`是域名或者ip地址.

我没改这么多，直接保留了原文件里面的listen和`server_name`

然后删掉这两项和location之间的所有内容，location里面的内容可以直接写成上面写的那样，只是把`proxy_pass`修改成`http://127.0.0.1:8000`，意思是啥很明显的吧。

保存即可。



然后应该运行起来nginx，命令为`sudo /etc/init.d/nginx start`

停止的话直接`sudo nginx -s stop`即可



然后只需要回到虚拟环境，重新执行`gunicorn --bind 127.0.0.1:8000 first_app:app`即可



基本的使用到此就结束了，当然后面就该测试所有的细节内容了，包括静态文件，模板，等等。很有可能还是需要修改nginx的配置，但是最重要的入门一步到此就结束了。



哎呀，已经三个小时了，差不多。入门是入了，可是原计划的学习却完全被耽误了，感觉今天的学术计划要泡汤。。。





如果对静态文件的修改无法及时在浏览器中显示，那是因为浏览器的缓存问题，可以使用`ctr-F5`刷新缓存















### 关于flask使用的一些技术

为了使用editor.md，我需要用flask模拟很多响应过程，这里面用到的技巧有：

1.  如何在url的响应中指定MIME类型，同时，我们的返回内容可以是字符串，也可以是二进制的：

~~~python
from flask import Flask,render_template,request,Response

app = Flask(__name__)

@app.route('/fonts/editormd-logo.woff',methods=['GET','POST'])
def t1() :
	with open('static/editormd-logo.woff','rb') as fi :
		rep = fi.read()
	return Response(rep,mimetype='application/font-woff')


@app.route('/fonts/fontawesome-webfont.woff2',methods=['GET','POST'])
def t2() :
	with open('static/fontawesome-webfont.woff','rb') as fi :
		rep = fi.read()
	return Response(rep,mimetype='application/font-woff2')

@app.route('/fonts/editormd-logo.ttf',methods=['GET','POST'])
def t3() :
	with open('static/editormd-logo.ttf','rb') as fi :
		rep = fi.read()
	return Response(rep,mimetype='application/x-font-ttf')
~~~

在这里看到的几个响应明显是静态的字体或者相应的文件，为什么我会手动处理？原因是这几个请求的发出不受我的控制，它们是由众多js中的某一个动态构建的，我无法控制，因而只能接受，只能响应。并且要注意，类型与文件必须对应。

2.  第二个问题是，`http://127.0.0.1:8000/fonts/fontawesome-webfont.woff2?v=4.3.0`这种形式的url是个什么情况

其实前面那段代码中的大多数请求都是这种样子的，`?`后面的内容应该是参数，如何指定这种url的视图函数呢？方法就是像上面的代码一样，直接抛弃掉`?`及后面的部分，flask会帮我们进行这样的映射。



3.  你知道的，校园网是一个局域网，这就意味着外界无法访问，但是神奇的在于，我们是支持了ipv6的，也就是说，如果校园网外的某个人如果接入了ipv6，那么他就可以访问我了，ipv6没有局域网。我只需要开启一个ipv6的服务器就可以，而让flask接收ipv6的连接方法很简单，只需要指定`host='::'`，而浏览器以ip地址+端口号的形式就可访问，与ipv4一致，但是因为ipv6的地址里面有`:`，所以写法与ipv4不同，ipv4为`127.0.0.1:8000`，而ipv6为`http://[2001:da8:215:501:1010:f98e:a051:b4de]:8000/`，方括号内为主机ipv6地址
4.  我在web编辑器的路径上面被搞得头晕，但是很多情况下，请求的路径又在js文件中，我无法渲染，定位到根目录，所以，如果我们可以知道`url_for`函数是干嘛的就好了，经过验证，发现这个页面的路径和linux下面的路径规则是一致的，如果我们想从根路径开始，那么只需要`/abc`这就是根目录下的abc文件夹，这意味着我们不再需要`url_for`函数了，可以直接写




### 登陆、Cookie与session

我现在需要登录了，或者说用户状态追踪。

flask里面的这一块一如其他部分，十分之友好方便，简单到令人发指。并且实现表现的形式正如我所想要的。

首先要明白的是，一般情况下，当我们需要追踪用户状态的时候，我们的解决方法其实就是cookie，那么这种情况下的使用逻辑是，当用户请求的时候，在响应里面设置一个cookie, 等用户登录成功之后，我们设置cookie里面的某个字段，以后需要检查的时候，就根据这个字段来判断用户是否登陆成功了。

逻辑很清晰，flask里面也的确有这种设置cookie的方法，但是稍微想一下就知道，这种方式很容易被用户猜出服务器是根据什么判断登陆的，然后篡改即可，如何解决？其实并没有什么高端的方法，无非就是加密而已，我加密cookie，用户拿到了也不知道内容，但是服务器这边通过简单的解析即可得到cookie内容，在flask里面实现了这个的功能叫做session就是会话。

这里，直接给出一个例子：

~~~python
from flask import Flask,render_template,request,Response, session, make_response, escape

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home() :
	if 'state' in session and escape(session['state'])=='login' :
		res = make_response(render_template('homepage.html',user="stan"))
	else :
		res = make_response(render_template('homepage.html',user="stranger"))
	return res

@app.route('/login',methods=['GET','POST'])
def blog() :
	if request.method == "POST" :
		if request.form['user'] == "stan" :
			session['state'] = "login"
	return render_template('login.html',user="stranger")

@app.route('/logout',methods=['GET','POST'])
def log() :
	if 'state' in session and escape(session['state'])=='login' :
		session['state'] = "logout"
	return render_template('login.html',user="stranger")


@app.route("/favicon.ico")
def icon() :
	with open("static/images/stan.ico",'rb') as fi :
		rep = fi.read()
	return Response(rep,mimetype='image/x-icon')

app.secret_key = '12345'

if __name__ == '__main__' :

	app.run(host="0.0.0.0",debug=True,port=8000)
~~~

从代码里面看，我们使用session的对外的接口就类似于一个字典，我们可以通过键值访问，适当的时候我们设置，适当的时候修改，适当的时候检查就可，需要注意的是首先使用之前必须设置密码，应该很复杂才对。

然后你可能很奇怪的是，代码里面根本没有展示我们什么时候把session加入了响应中，难道session就只是一个服务器上面的字典吗？从未发出，那简直太傻了吧，根本不可能实现追踪不同的用户，一人登陆大家登陆。其实完全不必担心，session的确被加入了响应中，只是是由flask默默完成了，完全不必担心，检查一下浏览器，你就会发现真的有cookie，但是是一个被加密过的乱码，根本认不出来。

总而言之，session的确是通过cookie实现的，并且感觉上比cookie更加易用，更加安全，完全可以实现用户追踪。



### 数据库与分页

我并不想做一个多么正式的东西，只要对我而言够用即可，只要功能能实现就好，鉴于树莓派至今因为系统是32位的，无法安装mongodb的原因，现在我的选择是，使用sqlite3作为数据库。

数据库只是为了存储文章和用户，所以需求十分简单。

我需要一个表来存储文章总数n，其实和文章记录存到一起也未尝不可，虽然有点浪费空间，但毕竟还是那句话需求很简单，又不对外开放。

然后对于每一篇文章记录的结构是`ID 即序号 title auth date content path`，序号记录这是第几篇文章，从1开始，越新序号越靠后，文章是md文件，并不存与数据库中，而是存在一个其他文件夹中，路径由path给出，content其实还没考虑好，原本打算直接是预览部分的html代码，这样动态页面生成的时候就方便了，或者只是预览部分的内容摘要，然后结合title，作者，时间等来动态生成。

假设文章总数为n，当前请求的页面页码为p，每页最多m篇文章，那么总页数mp是int((n+m-1)/m)，如果当前页是`[1,mp)`，那么需要的文章预览条目是id为`[n-10p+1，n-10(p-1)]`，如果是最后一页，那么条目是`[1,n-m(p-1)]`

这样的话，基本上问题就解决了

剩余的是数据库操作的问题。

sqlite3是关系型数据库，它的数据库已经被简化为了一个`.db`文件，数据库内有表，表的每一行是一个记录，每一列是一个键，我需要知道的最基本操作无非增删改查。

~~~python
import sqlite3

client = sqlite3.connect('test.db')

cursor = client.cursor()

cursor.execute()
client.execute()

result = client.execute()

res = [i for i in result]


f = open('test.sql')
fi = f.read()
f.close()
client.executescript(fi)
~~~

这是一个最简单的实例，光标和连接都可以通过execute执行sql代码，第一句中，如果没有test.db这个数据库，就会生成。

假设我们是做了查询，返回值result是一个数据库中的表，用type检查的话是一个光标对象，但是我们可以迭代，于是我一般选择先用迭代器将其转换为一个列表，列表的每一个元素都是一个元组，每一个元组就是一条记录，这样我们就可以很方便地使用了。

最后那个是执行脚本的方法，想要执行脚本我们需要自己读取，然后将读到的内容交给这个方法。

脚本就是.sql脚本，例如这样的

~~~sql
drop table blog;
create table blog(
	id int primary key,
	title text,
	auth text,
	c_date text,
	content text
);

insert into blog values(1, "test1", "stan", "17.12.13", "<article>haha</article>");
insert into blog values(2, "test1", "stan", "17.12.14", "<article>haha</article>");
insert into blog values(3, "test1", "stan", "17.12.15", "<article>haha</article>");
insert into blog values(4, "test1", "stan", "17.12.16", "<article>haha</article>");
insert into blog values(5, "test1", "stan", "17.12.17", "<article>haha</article>");
insert into blog values(6, "test1", "stan", "17.12.18", "<article>haha</article>");	
insert into blog values(7, "test1", "stan", "17.12.19", "<article>haha</article>");

delete from blog where id=4 ;

update blog set id=id-1 where id>4 ;
~~~



下面的其实是sqlite3的使用方法，这里要说的话估计要写很多，但其实没啥必要，去网上看一看教程就够了，例如[这个](http://www.runoob.com/sqlite/sqlite-create-database.html)

不用看那么细，知道怎么创建表，怎么插入数据，insert update select delete即可

对于我们的要求而言，其实要掌握的很少，只需最基本的操作。

最重要的问题是怎么删除一个记录，其实上面我最后的两个语句就完成这个任务了，我感觉这样就地修改正在遍历的键并不好，但是这的确很方便，也的确有效。

就这样，我们的最重要的原理就搞定了。就差写出来了。

还有就是模板，秉承够用就好的理念，我决定也不深入学习jinja2了，够用就行。



### 闪现

我又得到了一个很好的特性

来自于bootstrap的alert，和flask的闪现







### 题外杂记1

按照我以前的开发流程，我构建了很多虚拟环境，然后在里面安装gunicorn等等，都很顺利，但是现在我想不要虚拟环境，直接安装gunicorn，然后运行

但是bash给出了反馈`-bash:gunicorn:未找到命令`

这个问题实际上十分之明显，就是这个命令未被添加到环境变量中，在windows下面我见的多了，至于为什么会出现这种问题，就不是我需要考虑的了。

所以问题的关键在于，要么我们找到这个命令对应的bash脚本所在，然后把这个目录添加到树莓派的环境变量里面去，要么我们通过某些神奇的重新安装等等，来实现自动修复。

我搜索了google和百度，看到了来自stackoverflow等多个地方的各种解决方案，要么很不优雅，要么实现不了，在此过程中，我也付出了很大的代价，例如，我因为不停的误用python2，所以一怒之下利用`sudo apt-get remove python2.7`卸载了python2，然后我的树莓派上损失了很多很多东西，例如wolfram，我的世界等等，虽然我几乎不会碰他们，但是我很后悔。

然后中间也接触到了一些东西，例如如何使用pip卸载模块，不使用缓存安装模块，更新模块等，自己搜一下，很容易得到结果。

这些就不说了，我决心完成的是把命令添加到环境变量中，问题的关机在于第一怎么找到脚本所在，第二怎么添加到环境变量。

对于前者，我很机智的借用了原来的虚拟环境，进入启动虚拟环境之后，利用which guicorn命令找到了脚本所在，那么，明显在本机环境中gunicorn也应该存储在对应目录中，最终搜查一下，得到是`/home/pi/.local/bin/gunicorn`，当然，对于其他人可能不是这里，线索是`/home/pi/.local/lib/python3.5`是python3.5的目录

然后我们只需要把`/home/pi/.local/bin/`加入到环境变量即可

怎么修改树莓派环境变量，搜索一下网上有

`sudo vim /etc/profile`

在PATH的最后添加`:/home/pi/.local/bin/`保存即可

此时再使用`which gunicorn`即可发现，的确可以使用了，哈哈哈

作为备忘，网上有人说，可能gunicorn可能没有自动安装一些必须库，我们需要自己安装，我的确手动装了一个`sphinx`，也许有用，也许没用。

总之就是这样