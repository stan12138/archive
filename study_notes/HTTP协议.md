##HTTP协议学习笔记

> --stan


####常见方法
常见方法有5种：  
GET  
PUT  
DELETE  
POST  
HEAD



####http报文的结构
报文的第一行是起始行，包含的东西不必多说了  
第二行之后包含了0~n个行，称之首部字段，根据现在的情况，首部字段至少会有一行，用来说明类型，首部字段的每一行都包含一个名字和一个值，使用`:`分割，但是根据现有经验，更确切的是使用`: `进行分割的,首部字段以一个空行结束，也就是说起始行与首部之间没有空行，但是主体与首部之间有一个空行  
第三部分是主体，主体未必存在，例如很多GET报文中不包含主体。  

#####注意
请求报文的语法：

	<method> <request-URL> <version>
	<headers>

	<entity-body>

响应报文语法：

	<version> <status> <reason-phrase>
	<headers>

	<entity-body>

两者只有起始行有区别  
状态短语只是为人类阅读方便而提供的，机器只认状态码  
首部字段中的Content-Length字段的意思是主体的长度












####spider
spider要伪装自己要实现基本的首部字段，一般包含User-Agent,Accept,Host等


  



