## Scoket与Select

### Socket

我觉得python的socket编程是一个相当有意思的话题。

至于一些非常初级的知识我就不说了，例如什么叫做套接字，什么是TCP,UDP，网络模型什么的。

#### 新建套接字

新建立一个套接字需要这样：

`my_socket = socket.socket(address_family, socket_type, protocol=0)`

第一个参数叫做`地址家族`，不同的地址家族指定了套接字的地址类型，早期的套接字是一种IPC即进程间通信工具，之后又在其基础上构建出了网络通信工具，因此套接字的类型大体上可以分为面向文件的和面向网络的，前者用于IPC，后者用于实现网络功能，这种类型的套接字在python里面称之`AF_UNIX`，换句话说他的地址家族就是`AF_UNIX`，当然也有些平台上使用了新的名字`AF_LOCAL`，但python没有改。

面向网络的套接字的地址家族常用的是`AF_INET`，据说所有细分种类的套接字中99%以上都是这种类型的，但是其实还有很多类型，例如应用于IPV6的`AF_INET6`，除此之外还有很多，有些是非常专业的，有些是非常罕见的，有些是未实现的。总之，也就是说基本上用`AF_INET`就够了。

接下来另一个参数是套接字的类型(注意前者是地址类型)，这里最最常用的是`TCP和UDP`分别对应的类型是`socket.SOCK_STREAM和socket.SOCK_DGRAM`，他们最常用，具体的细节就不说了，但是我最感兴趣的其实是`socket.SOCK_RAW`即原始套接字

最后一个参数`protocol`，

#### 网络模型

网络模型分为`ISO/OSI`七层模型和`TCP/IP`四层模型自不必言，但是现实中真正用上的是`TCP/IP`四层模型自然也不必说，这四层模型从低到高分别是网络接口层，然后是网际层，运输层，应用层。

实际上具体细节我已经忘得差不多了，但是暂时我也不太想补全。

我现在的感觉基本上可以这样说，网络接口层基本上就差不多算是硬件层了，这里面负责了数据该怎么传输，每一帧是怎么样的等等，这些东西现阶段我觉得吧，可能控制不了，也没办法控制。

所以说最有意思的，最好玩的实际是高三层，而我们前述的`TCP和UDP`是属于传输层的，然后应用层就是在这两者之上搭建的，例如我曾经自己实现的http极简服务器，就是使用了应用层协议HTTP协议。

应用层基本上就是随便搞了，基本上想怎么玩怎么玩，协议可以自己定，需要和浏览器交互自然需要HTTP协议，但是例如我自己写的文件传输就是自定义的传输格式，但是都是架构在TCP之上的。

这些东西的确很有意思，但是都不太爽，受到了相当的限制。

有意思的是网际层，这一层也有很多耳熟的协议，`IP, IGMP, ICMP, ARP, RARP`等等。

使用了`ICMP`的最有名的工具是`ping`，然后`ICMP`协议又是基于`IP`协议，另外一个我比较感兴趣的是`ARP`协议，但是`ARP`协议并不基于`IP`协议，而是直接架构在网络接口层之上

如果想要搞些花招，那么首要的问题就是要搞清这些协议，以及他们是干什么的，怎么工作的。这里我的重点对象就是`TCP, IP, ARP, ICMP`，搞定了这些之后，下一步就是搞清楚怎么在python里面拿到这些控制权，例如已经知道了怎么样配置地址家族和套接字类型可以使用`TCP或者UDP`协议，那么怎么才能使用`IP、ICMP、ARP`协议呢？这就是问题所在。



#### 回到socket

至于上面提到的两个问题中的第一个，即这些协议，我基本上不会详细描述。

这里插播一句，不同的`OS`上对功能的支持是不一样的，例如windows就不支持很强的`epoll`，甚至不支持`poll`，只支持`select`，通过pythonista可以知道在`iOS`上至少苹果不会提供`epoll`，只有`select和poll`。总之，我想说的是有必要知道当前平台上python支持的地址家族，套接字类型，协议。

这个其实很简单

~~~python
import socket

address_family = [i for i in dir(socket) if "AF_" in i]
socket_type = [i for i in dir(socket) if "SOCK_" in i]
protocol = [i for i in dir(socket) if "IPPROTO_" in i]

#获取到的协议为['IPPROTO_ICMP', 'IPPROTO_IP', 'IPPROTO_RAW', 'IPPROTO_TCP', 'IPPROTO_UDP']
~~~

当然了，可能不准确，不完整啊，我猜测应该是这样

其中，已经知道的是第三个参数协议，默认值是0，而0代表的实际是`socket.IPPROTO_IP`，也就是ip协议



ok，据我现在搜索到的知识，利用python在windows系统下，可以使用IP协议，但是却不能控制以太网的协议，然后ARP就是直接架构在以太网协议上的，这也就意味着是无法直接利用python发送arp的，但是ICMP和伪造TCP，HTTP还是可以的。

在Linux上面，python提供了一个地址家族，叫做`AF_PACKET`，可以直接控制以太网帧。

但是呢，现在我再次陷入了焦虑，每次一处理windows下的这些东西，我就头疼，所以，暂时标记一下参考资料，等想做的时候再继续。





绑定的地址，是一个元组`(host, port)`，host明显是字符串，而port应该是整数

阻塞，socket.socket对象具有setblocking方法，可以设置为阻塞的或者非阻塞的，它实际上是settimeout方法的速记形式

`setblocking(True)等价于settimeout(None)`而`setblocking(False)等价于settimeout(0.0)`

对于timeout而言，一个非0数值意味着，如果后续对于这个socket的任意某操作未能在该时间内完成就会触发一个error，如果给的数值是0，那么意味着这个socket处于非阻塞模式，如果给了None那么意味着是阻塞模式。换句话说settimeout这个方法是多功能的

因此一个socket对象可以出在三种状态，阻塞，非阻塞，timeout。缺省情况下都是阻塞状态。

阻塞状态下，操作会阻塞，直至操作完成，或者触发错误

非阻塞模式下，如果操作不能立马完成就会触发错误，并且操作会失败，返回一个错误，但是这个错误具体是什么依赖于平台，这种情形下，使用select

timeout模式就很简单了

要注意connect方法也有一个timeout参数，一般推荐先写settimeout然后才使用connect方法

accept方法也会返回一个socket对象，一般而言，如果原socket是阻塞模式或者timeout，那么返回的将是阻塞模式

如果是非阻塞，那么具体会返回什么类型依赖于平台。

python官网上的指导这么说，对于非阻塞模式，主要的不同在于，send,recv,connect,accept可以在啥也没干的情况下返回，这个时候，你可以使用各种措施执行完成检查，确定情况，但是绝大多数情形下，如果你选择手动来做，结果将是被累死。因此正确的方法就是使用select，换句话说，非阻塞模式就应该与select合作





接下来再说一下阻塞与非阻塞的问题，阻塞就是持续等待，例如TCP的监听端口会堵塞在accept的位置，直至接到新的连接，然后，考虑到同时为多个用户提供服务的情况下，单进程单线称加阻塞必然是不可能实现的，那么多进程和多线程呢？可以做，但是问题在于每来一个链接就开一个新的进程，那么开不了多少，电脑就崩了，线程稍微好一点，毕竟占的空间比进程少，但是太多也顶不住。于是就可以考虑协程。

如果使用协程的话，例如gevent，就是在单进程单线称下完成同时为多个用户提供服务的做法，那么gevent是怎么实现的？实际上它是把套接字设置为非阻塞的，然后不停的检查，检查到一个服务，就提供服务，然后再检查。

所以，抛弃gevent，自己也是可以实现的。

使用协程自然是比较强的，因为占用的资源相当少，那么还能不能更快呢？可以。一些服务器就可以做到更强，例如Nginx，他是怎么做的呢？使用系统的服务。

这里就是`select, poll, epoll`了，下面说了这三者的区别。

但其实三者有更加本质的区别，select和poll的做法实际上和前面讲的思路一致，基于轮询，只是执行轮询任务的不再是python而是操作系统，自然要快。

那么Nginx是怎么做的？Nginx更快，它利用了epoll，epoll在linux上可用，它的不同之处在于，不再基于轮询，而是基于事件系统，不再逐个查询，而是要求每个端口在触发事件的时候主动报告。这个自然要快得多，尤其是连接数比较多的时候。但是epoll的实现自然要比前两者复杂的多得多。

然后，python在windows下只能提供垃圾的select



### select介绍

我们知道的应该是`select`,`poll`和`epoll`三个才对

select最早出现，用于监视文件描述符，唯一的优点在于良好的跨平台支持，select单进程只能监视有限数量的描述符

poll的优点在于没有数量限制，其他颇为类似，也是比较广泛被支持

epoll是最优秀的，具有了所有的优点，但是只有Linux支持



我搞出了第一个原型

现在需要注意的是，第一，writeable列表一直可用，第二，recv不是直接请求的，你不调用不代表就无法接受数据，其实只要对方发送，就已经收过了，放在缓存区，recv是从缓存区读的

等我一会详细写。



select的工作模式是这样的，假设我们试图让socket服务器端，同时可以服务于多个客户端，自然我们要listen(n)，但是关键问题在于，我们该如何检测多个客户端的连接与收发，以往我们在单线程下，往往只会应对一个客户端，处理方式是while True循环检测，明显这种方式对于多个客户端并不行，或者说很资源浪费。select就是为此而生。它可以处理读写，错误监测。

`readable, writeable, errors = select.select(read_list, write_list, error_list)`

上面就是原型，其中的`read_list`是要检测可读的列表，例如`accept,recv`这些都是可读的，`write_list`是可写列表，`error_list`是错误检测，当这些列表中出现了对应事件的时候，这个函数就会返回，分别将可读，可写，错误的描述符放入对应列表中，我们只需要逐个检查列表，根据情况做对应处理即可。

~~~python
import select, socket, sys
from queue import Queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)

server.bind(('',5000))
server.listen(5)

input_list = [server]
output_list = []

while input_list :
	read_list, write_list, error_list = select.select(input_list, output_list, input_list)

	for s in read_list :
		if s is server :
			client, client_address = s.accept()
			print("get connect from",client_address)
			client.setblocking(False)
			input_list.append(client)

		else :
			data = s.recv(4096)
			if data :
				print("get message from",client_address, "content is :",data)
			else :
				input_list.remove(s)
				s.close()
                
	for s in error_list :
		input_list.remove(s)
		s.close()
~~~

上面就是一个简单的例子，可以看到其中的逻辑，一开始我们只把服务器放入可读检测列表中，只要出现了有客户端连接，就会返回，我们只需要accept即可，然后把客户的socket连接也放入可读检测中，之后根据判断决定执行accept或者recv。

乍一看，似乎用处很一般，但是相信我，这绝对是大大减少了我们的循环检测任务，要注意的是每个socket都必须设置为非阻塞模式。

这里，要注意，我并未使用可写列表，因为每一个客户端socket时刻都是可写的，所以select将会不停的返回，一直要求我们写点什么。总而言之，我觉得可写列表完全没有使用的必要。



这样大概就可以了。



### 局域网文件传输工具

下面是在使用socket构建局域网文件传输工具的时候得到的种种经验。

构架方面，将设置一个第三方服务器，这个服务器使用socket和select搭建，只负责一个任务，检测有几个客户端试图加入通信队列，获取它们的ip地址，和提供的通信端口，以及标识ID，然后通知每个客户端可用设备的列表，并在设备下线的时候，实时向各个设备更新设备列表。

说起来挺复杂的，实现起来也算不上很简单，但其实任务很简单，就是为了免除在文件传输过程中各个客户端要输入IP地址。



然后，下一步是大体积文件的传输方式，与注意事项，这里采用的通信方式是TCP，协议是服务器将首先向客户端发送文件的名字，体积，预计通信次数的相关信息。当获得客户端的确认之后，开始无反馈的传输，测试比较好的每次传输的块体积是32KB，要注意客户端结束接受的标志应该是收到了预计体积的内容，而非达到了协商好的次数。注意此时因为发送不是立即就能完成的，所以socket不能是非阻塞模式，也就不能再使用select了。



下一步的测试是，如何在通信客户端之间建立连接，考虑到之前的单客户端与服务器设计的问题比较复杂，例如如何协商谁来做服务器，谁来做客户端，并且通信必须步调协调，属于半双工模式，因而，我决定利用多线程，每个设备都构建两个线程，分别做一个服务器，再做一个客户端，服务器只负责发送，客户端只负责接收，这样就不存在协商问题了，同时也变成了全双工的通信。

这里要注意的唯一一个问题就是之前也遇到过的，如果客户端在服务器之前启动的话，那么基本上客户端是无法连接上服务器的，即便使用了 



### 补充

毫无疑问，更好的选择应该是epoll而不是select，epoll的使用也非常的简单，这里我并不打算详细的说些什么。

我已经写过了一个整合的类，叫做SEpoll，它可以根据平台自动选择使用上述哪一个，然后提供相同的接口。这个类现在放在ToDo这个仓库里面的server中，文件名是`select_epoll.py`



### 内网穿透

这一段时间有稍微重新大略的复习了一下计算机网络，作为一个练习，我试着完成了一下内网穿透。

首先描述一下问题。

已知，使用了私有地址的局域网，其中的设备本身都不具备公网IP，当设备需要访问外网的时候，必须经过NAT设备，NAT会自动完成一个叫做端口映射的过程，具体的就是将设备的端口映射到本局域网对外的IP的一个端口上，这样的话实际上对于访问外网这个过程NAT的存在是透明的。

但是如果想让另外一个局域网的设备访问本局域网内的设备该怎么办呢？做法就是内网穿透，也就是在NAT上面打一个洞。

问题的麻烦之处在于NAT设备也是动了手脚的，即便短期内它为局域网内的某一台设备建立了一个端口映射，它也并不会老老实实的让所有的数据包通过这个端口，他会做筛选。这个造成的结果就是有些根本无法实现内网穿透。

唉，得了，我的表达能力实在是捉急，反正这一段的重点并不是这些，网上的很多文章的介绍是很详细的，随便去看看好了。

总之，直接说结论，我现在能做到的只有UDP下的内网穿透，而且也不是所有的局域网都可以，例如4G网络就不能穿透。下面直接说方法：

#### 要求

首先必须要有至少两个局域网，以及分别位于两个局域网内的设备A,B。然后还必须具有同一台公网设备服务器S。当然S可以是其中一个局域网内的设备，只不过通过了一个固定的端口映射，让它可以通过公网访问。

#### 过程

首先在A,B上建立一个UDP的socket，它们都是客户端，S上面运行一个UDP服务端

A，B分别向S发送任意短消息，让S直到它们暴露在公网的ip和端口，然后S将这些`(ip, port)`地址对分发给A,B，这样AB都获取了对方的地址。

接下来，B需要首先向A发送一个短消息，此时A是不可能收到这一个短消息的，因为A的NAT会发现这是一个全新的来源，他不会接受。但是这个过程会让B的NAT设备将A的地址写入可接受信息的表中，也就是说B的NAT至此已经可以接受A的短消息了。

这时B可以向S报告自己准备好了，然后S告诉A可以开始发送消息(当然这一步很随便，规划好时间的话，不经过S插手也是可以的)

接下来A向B发送短消息，这个步骤有两个意义，首先让A自己的NAT知道下一次可以接受B的消息，另外就是B已经可以收到这条消息了。

如果上面的一步失败了，可以多发几条试试，如果还是收不到，那说明B的内网不可穿透。

如果B收到了消息，那说明A到B的通信已经建立，B的内网已被穿透。接下来B也要向A发一条消息，建立B到A的通路。如果A也收到了。至此内网穿透就搞定了。

接下里AB之间必须保持一定的收发频率，如果长时间不进行通信，端口可能就会被NAT回收，那么打出来的洞就会再次关闭。



至于代码就很简单了，这里就不写了，只要严格遵守上述过程就可以。现在已知的是4G的网络似乎是不能穿透的。但是我们学校的校园网是可以穿透的。回家后可以试一下家里的局域网。





### 续

我持续在socket编程上遇到麻烦，各种Exception会导致服务器崩溃。现在参考来自[real python](https://realpython.com/python-sockets/)的socket教程，我重新学习一下，记录一下我学到的新知。

#### types.SimpleNamespace

这是types模块里面的一个类，他提供的功能如下：

~~~python
data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
print(data.addr, data.intb, data.outb)
~~~

也就是以具名参数的形式传入参数，就可以像属性一样访问，算是对数据的一个包装。

#### selectors模块

它是对于select的高级封装。鼓励使用selectors.DefaultSelector，它会自动根据平台帮我们选择最合适的实现。

它的`register`方法接受三个参数：

~~~python
register(fileobj, events, data=None)
~~~

也就是说，我们可以在注册一个描述符的同时携带上一定的数据

其中的events就是`selectors.EVENT_READ`还有`selectors.EVENT_WRITE`等，使用上是这样的：

~~~python
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
~~~

注册完了之后，使用select方法阻塞的等待结果，然后返回值是key和mask，其中的key的fileobj属性是文件描述符，data是携带的data，mask是events。



需要注意，如果我们注册了write事件，这个事件基本就会被一直触发



## socket模块

使用socket进行网络编程，对我来说一直都是个问题，到目前为止，每次要做socket编程，我依旧十分头疼。

我几乎每次尝试重新做一个新的项目的时候，都会想要重新设计一个应用层协议，而每一次，TCP服务器的设计都让我感觉很头疼。无数的异常，很难让服务器不会因为各种问题而中断运行。我都不知道当时怎么让Filer的IP服务器做到不间断运行的。

现在我决定参考[real python](https://realpython.com/python-sockets/)上面的socket编程的项目设计一个比较通用一点的TCP服务器和客户端模块，然后我也意识到，其实我并不需要每次重新设计应用层协议，只需要制定一个通用协议，然后隐藏在模块之中，自动完成协议的构建和解析就可以了。



### 特点

这里，同样使用select来完成多连接的服务器设计，同时考虑到服务器的终止和广播功能的设计，也应用了多线程。

和以前的不同在于，这一次我终于注意到了标准库里面的selectors模块，这样就不用使用我写的垃圾SEpoll了。

### 协议

这里，我重新制定了一个应用层协议，以后我都会使用这个协议进行编程，这个协议基本上就是HTTP和real python的混合修改版，我做了一些小幅度的调整。如下：

~~~
2B            <----开头是2B的数字，小端存储，无符号，代表了header的长度
CL:123;TYPE:message    <----header是键值对的形式，使用UTF8编码，数字也是直接转换为字符串，每个键值对之间使用分号进行分割，最后一个不用分号，键值对没有特殊要求，可以完全自定义，唯一要求的是必须要一个CL代表content-length，在我的模块设计里面，这一个字段会被隐藏起来，由模块负责添加解析。
content         <-----content是内容，类似于http的body，要求是二进制格式，模块只负责读取，不负责解析。
~~~

现在，这个协议的设计方案就是这样的，所以可以负载数据的是header部分和content部分，content自然是可以为空的。

给出一个符合上述格式的报文：

~~~
b'\x11\x00CL:7;type:messagecwsdwed'
~~~

明显，这个报文的`b'\x11\x00'`是header长度，header包含`CL和type`两个字段，content的内容是`b'cwsdwed'`

### 模块设计

这里我不会太过于详尽的说明这个模块的每一个部分，而是着重说明各种我原本就不知道的事情，和各种遇到的异常。

a是一个字符串，len(a)，代表了这个字符串中包含了多少个字符，但是并不能代表这个字符串占据了多少空间即字节数，将一个字符串encode可以得到在某种编码下的二进制内容，返回值是bytes对象，对于bytes对象做len操作，得到的是字节数。

前面有提到过，selectors模块里面的注册的每个socket都是可以携带data的。

当发生了可读事件的时候，执行socket.recv，如果什么都没有读到，说明对方关闭了socket，或者在关闭中

当send的时候，send不能保证已经将全部数据发送出去，返回值是发送出去的字节数，如果有信息要发送，但是返回值是0，代表连接已经被破坏了。

这两点在socket的文档里面并未提及，而是在python的socket programing HOWTO里面的。

在send和recv中都有可能会发生BlockingIOError错误，这是因为socket暂时被阻塞了，这种异常只需要直接pass了就可以。

已经观测到send的时候可能发生ConnectionResetError，这也是对方关闭了socket

还有send的ConnectionAbortedError，原因同上。

还有

当对于一个非阻塞的tcp客户端进行连接的时候，使用connect_ex方法，如果连接失败的话，selector会直接返回一个recv事件，并且在接收数据的时候会抛出ConnectionRefusedError异常



我现在开始了重新完善socket模块的工作，今天做了一些，但是没有搞定，明天会继续，然后推送