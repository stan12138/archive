## Socket TCP模块使用说明

这是我新设计的模块化socket tcp模块的使用说明。

整个模块一共包含3份文件：

~~~
lib.py   协议模块
server.py  服务器基类
client.py  客户端基类
~~~

### 基本约定

基本约定包含了，服务器如何表示客户端，服务器如何处理来自客户端的消息，消息协议是什么

#### 通信协议

在这里，一个消息的完整结构是header+content，其中的header是基本类型的字典，键是字符串，值是字符串形式的整数或者字符串，content是二进制信息。其中header是必选的，content是可选的。当然特殊情况下，header也可以是空字典。

发送一条消息可以简单地使用header表示，也可以使用header或者content表示，但是content必须是二进制内容。特别的注意，当content不为空的时候，不需要在header里面设置content长度，协议模块会自动完成这部分任务。

#### 表示方式

除了服务器使用socket描述符直接表示之外，一般情况下，所有的连接统统使用Messenger实例表示，Messenger实例可以访问到具体的描述符，地址，收到的信息等

Client类和Server实例都会维持一个messengers列表，列表中包含所有连接。也就是说Server和Client都可以支持和维护多个连接，连接的管理方法是使用selector。只支持读事件的管理。



### Server

`Server`基类，可以供调用和重载的属性与方法如下：

`Server(ip, port)`，构建

`Server.addr`, (ip, port)形式的服务器地址

`Server.server`，服务器的监听socket

`Server.messengers`，服务器的全部客户端的Messenger列表

`Server._lock`，服务器的客户端操作锁，一般不调用

方法：

`Server._listen()`，持续监听方法，死循环，可调用，不可重载。会自动处理接受连接，加入监控队列，自动处理消息接收

`Server.stop()`，关闭服务器

`Server._close_client(messenger, need_lock=True)`，关闭一个客户端，可以设置关闭过程是否需要锁，只有当明确确定之前已经获取锁的情况下可以设置不需要锁，否则建议使用锁

`Server.broadcast(header, content=None)`，向全体客户端发送广播消息，失败将自动关闭连接

`Server.send(client, header, content=None, close_when_fail=True, need_lock=True)`， 向某一个客户端发送信息，可以指定发送失败是否自动关闭连接，关闭连接是否需要lock

`Server.multicast(clients, header, content=None)`，多播，失败将自动关闭连接

一系列重要事件的处理都是用`callback`来处理，使用的时候通过继承并重载这些callback来实现对于这些事件的处理，这些事件包括：

~~~python
Server.new_connect_callback(client)       #获取了一个新链接，client是新连接的Messenger实例    
Server.client_close_callback(client, alive_client_num) #断开了一个链接，client是断开的连接的Messenger实例，alive_client_num是剩余的连接的数量
Server.receive_callback(client)  #获取了新的信息，client是发送了信息的连接的Messenger
~~~





### Client

`Client`基类用户构建客户端

`Client()`， 构建一个实例

`Client._addr`，服务器的地址

`Client.messengers`，所有连接的Messenger实例列表

`Client._lock`，同服务端

`Client._listen()`，死循环监听消息，可调用，不可重载

`Client.stop()`，关闭所有连接

`Client.add_connection(ip, port)`，新增一个连接

`Client._close_client(messenger, need_lock=True)`，关闭一个连接，可以设置关闭过程是否需要锁，只有当明确确定之前已经获取锁的情况下可以设置不需要锁，否则建议使用锁

`Client.broadcast(header, content=None)`，向全体连接发送广播消息，失败将自动关闭连接

`Client.send(client, header, content=None, close_when_fail=True, need_lock=True)`， 向某一个连接发送信息，可以指定发送失败是否自动关闭连接，关闭连接是否需要lock

`Client.multicast(clients, header, content=None)`，多播，失败将自动关闭连接

一系列重要事件的处理都是用`callback`来处理，使用的时候通过继承并重载这些callback来实现对于这些事件的处理，这些事件包括：

```python
Client.connect_fail_callback(client)       #新链接连接失败，client是新连接的Messenger实例 
Client.connect_success_callback(client)       #新链接成功，client是新连接的Messenger实例    
Client.client_close_callback(client, alive_client_num) #断开了一个链接，client是断开的连接的Messenger实例，alive_client_num是剩余的连接的数量
Client.receive_callback(client)  #获取了新的信息，client是发送了信息的连接的Messenger
```





### lib.py

在lib.py里面主要定义了信使类，同时也定义了一些错误

#### Messenger

信使类，socket tcp模块的使用者不需要，也不建议自行生成Messenger的任何实例

`Messenger(selector, fileobj, addr, default_recv_length=4069)`，生成一个实例，并不希望用户直接调用生成任何实例

`Messenger.socket`，信使代表的socket描述符

`Messenger.addr`， 地址，永远都是服务器的地址，所以对于服务器是自己的地址，对于客户端是连接的服务器的地址

`self.id`， `ip:port`组成的字符串的哈希值

`self.recv_time`， 最新一次收到消息的时间

`self.send_time`，最近一次发送消息的时间

`self.header`，最新收到的消息的header

`self.body`，最新收到的消息的body

`self.read()`，读取消息，不需要自行调用，Server和Client已经调用过了

`self.send(header, content=None)`，发送信息到socket



### 总结

当需要发送消息的时候，调用send方法

对于Client除了重写读消息方法，常调用`_listent`

对于Messenger，一般查看addr,socket，header和body，并使用send发送信息

在使用过程中，都需要使用线程，一个线程负责listen，其他线程用来处理想要的事情



## 示例

上述说明只是一些简单的描述，具体如何使用，都是需要继承两个类，然后重载定义需要的方法。我表述能力太差，在example里面提供了一些样例，可以根据样例使用。

~~~python
client_example.py
server_example.py
~~~

上述两个样例可以使用命令行完成一系列任务，管理多个连接，发送消息，广播等

~~~python
ip_server.py
filer_client.py
~~~

上述两个例子是新的filer，其中的ip_server可以管理所有连接，接收汇报，同时定时发送广播

`filer_client`是命令行版本的filer客户端，可以完成定时汇报，连接到其他客户端，接受其他客户端的连接，完成消息发送，广播等功能，只是现在暂时未完成文件传输功能。