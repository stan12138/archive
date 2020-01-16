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

在这里，一个消息的完整结构是header+content，其中的header是基本类型的字典，键是字符串，值是整数或者字符串，content是二进制信息。其中header是必选的，content是可选的。当然特殊情况下，header也可以是空字典。

发送一条消息可以简单地使用header表示，也可以使用header或者content表示，但是content必须是二进制内容。特别的注意，当content不为空的时候，不需要在header里面设置content长度，协议模块会自动完成这部分任务。

#### 表示方式

除了服务器使用socket描述符直接表示之外，一般情况下，所有的客户端和连接统统使用Messenger实例表示，Messenger实例可以访问到具体的描述符，地址，收到的信息等

### Server

`Server`基类，可以供调用和重载的属性与方法如下：

`Server(ip, port)`，构建

`Server.addr`, (ip, port)形式的服务器地址

`Server.server`，服务器监听socket

`Server.messenger`，服务器的全部客户端的Messenger列表

`Server._lock`，服务器的客户端操作锁，一般不调用

方法：

`Server._listen()`，持续监听方法，死循环，可调用，不可重载。会自动处理接受连接，加入监控队列，自动处理消息接收

`Server._close_client(messenger, need_lock=True)`，关闭一个客户端，可以设置关闭过程是否需要锁，只有当明确确定之前已经获取锁的情况下可以设置不需要锁，否则建议使用锁

`Server._broadcast(header, content=None)`，向全体客户端发送广播消息

`Server.process_read(messenger)`， 用户通过重载这个方法确定如何处理来自客户端的消息



### Client

`Client`基类用户构建客户端

`Client(ip, port)`， 构建一个连接到指定服务器的客户端

`Client._addr`，服务器的地址

`Client._client`，本客户端的socket描述符

`Client.messenger`，本客户端的Messenger实例

`Client._lock`，同服务端

`Client._listen()`，死循环监听消息，可调用，不可重载

`Client.process_read(messenger)`， 用户通过重载这个方法实现对于接收到的消息的处理



### lib.py

在lib.py里面主要定义了信使类，同时也定义了一些错误

#### Messenger

信使类，socket tcp模块的使用者不需要，也不建议自行生成Messenger的任何实例

`Messenger(selector, fileobj, addr, default_recv_length=4069)`，生成一个实例，并不希望用户直接调用生成任何实例

`Messenger.socket`，信使代表的socket描述符

`Messenger.addr`， 地址，永远都是服务器的地址，所以对于服务器是自己的地址，对于客户端是连接的服务器的地址

`self.recv_time`， 最新一次收到消息的时间

`self.send_time`，最近一次发送消息的时间

`self.header`，最新收到的消息的header

`self.body`，最新收到的消息的body

`self.read()`，读取消息，不需要自行调用，Server和Client已经调用过了

`self.send(header, content=None)`，发送信息到socket



### 总结

总之，一般情况下，我们只需要重写Server和Client的`process_read`方法，此外，对于Server也会常常调用`_broadcast`方法，和`_listen`方法，偶尔可能会使用`_close_client`方法

当需要发送消息的时候，会使用对应Messenger的send方法

对于Client除了重写读消息方法，常调用`_listent`

对于Messenger，一般查看addr,socket，header和body，并使用send发送信息

