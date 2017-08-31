# tornado学习笔记

>   呃，tornado应该是包含了服务器和网络框架吧，但愿没搞错
>
>   --by stan 17.8.28

### 第一个示例

~~~python
import tornado.ioloop
import tornado.web

class mainhandler(tornado.web.RequestHandler):
	"""docstring for mainhandler"""
	def get(self) :
		with open('static_file/first.html') as fi :
			rep = fi.read()

		self.write(rep)
		
def app() :
	return tornado.web.Application([('/',mainhandler),])

if __name__ == '__main__' :
	my_app = app() 
	my_app.listen(8000)
	tornado.ioloop.IOLoop.current().start()
~~~

可以工作，注意一下一些特性，这里同样要创建一个application的实例，然后url是直接在创建实例的时候传入的，url的处理函数也是一个实例，大概get和post方法都是重写的，所以get和post都是通过重写方法实现的，然后内容不需要是二进制的，普通的字符串就行，关于content-type和status code等都不需要手动实现，绑定端口后是使用的app的listen方法，然后就可以运行，运行之后没有任何的信息输出，同时也不支持ctr-c退出，所以，这完全只是一个示例。

## 用户文档

### 介绍

tornado可以分为四块：

-   一个网络框架，包含RequestHandler和其他支撑性的类
-   HTTP客户端和服务器实现，HTTPServer,AsyncHTTPClient
-   一个异步网络库，包含IOLoop,IOStream
-   一个协程库，tornado.gen，可以以一种更直接的方式写异步代码

### 异步与非阻塞IO

传统服务器使用一个线程服务一个用户，十分消耗资源，这里tornado使用单线程，这意味着每个时刻只有一个用户出于活跃状态，所以，每个用户都必须是异步和非阻塞的，虽然异步和非阻塞二者常常交换使用，但二者并不一样



==这这这，还是看不了，因为这里用了太多异步，协程之类的东西了，而我依旧不太了解。==



