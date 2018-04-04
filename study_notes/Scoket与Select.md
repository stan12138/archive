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



### select介绍

我们知道的应该是`select`,`poll`和`epoll`三个才对

select最早出现，用于监视文件描述符，唯一的优点在于良好的跨平台支持，select单进程只能监视有限数量的描述符

poll的优点在于没有数量限制，其他颇为类似，也是比较广泛被支持

epoll是最优秀的，具有了所有的优点，但是只有Linux支持



