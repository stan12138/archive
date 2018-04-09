## Scoket与Select

我暂时并不打算十分详细的写这两个话题，只是暂时准备在我学习select做一点笔记，至于完整的话题，大概以后才会认真写一下

### Socket

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