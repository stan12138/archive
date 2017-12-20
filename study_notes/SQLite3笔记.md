## SQLite3笔记

我需要数据库了，现在。我大概会优先选择MongoDB，但是因为我想在树莓派上运行，但是现在树莓派官方依旧只提供32位OS，而32位系统上无法安装MongoDB，没办法，我又的确不太想用MySQL，又考虑到现在并不是要做什么很正式的应用，所以简单的python自带的简单的SQLite3也就够用了。这里的笔记是针对python里面的操作的。



###建立连接与表格

~~~python
import sqlite3

client = sqlite3.connect("data.db")

client.execute()
~~~

上述是连接数据库，若不存在，会自动创建，使用下面的语句执行SQL代码，如果执行了插入或删除操作，必须执行`client.commit()`提交，最后需要关闭`client.close()`

所以下面的部分主要就是SQL语句了。

~~~sql
CREATE TABLE table_name(
   column1 datatype  PRIMARY KEY,
   column2 datatype,
   column3 datatype,
   .....
   columnN datatype,
);
~~~

我实在搞不懂它的数据类型，但是我常用的就是`int text`

并且我习惯上使用小写的语句，在某些极个别的情况下是必须使用大写的，但我暂时用不上。



删除表格`drop table tablename;`

注意，语句必须使用分号结尾



### 插入数据

有两种基本使用方法：

~~~sql
INSERT INTO TABLE_NAME (column1, column2, column3,...columnN)  VALUES (value1, value2, value3,...valueN);
~~~

这个是插入部分列，而不是所有列

如果插入所有列，就不需要列名了

`INSERT INTO TABLE_NAME VALUES (value1,value2,value3,...valueN);`



### 选择数据

我们可以选择指定列，也可以选择所有列

语法是：

~~~sql
SELECT column1, column2, columnN FROM table_name;
SELECT * FROM table_name;
~~~

在python里面，执行这个语句，返回的是一个光标对象，可以使用list()转换为列表，列表每一项是一个数据条目，元组的形式，元组的每一项是该条目的一列



### 更新数据

我们可以更新条目的列

`update tablename set col1=value1, col2=value2 where condition;`

这里面，明显是可以更新任何列的，只要在中间增加这里列即可，最后还有一个条件子句，可以不带，这样就是更新所有，如果使用了condition则只更新满足条件的。

选择，更新，删除都可以使用条件语句，后面会详细描述。



### 删除数据

删除指的是删除一个或多个条目

`delete from tablename where condition;`

不加条件语句的话，会删除所有记录。



### 条件

按照计划，这个将是最后一部分，不会再继续深入了，这一部分功能最为强大，东西也最为繁杂，主要的会说明一下表达式，运算符，逻辑运算，where子句，like子句，GLOB子句，limit子句等



#### 运算符与逻辑运算

这里的运算符除了常规的加减乘除，`%`是取余

然后在这里`==和=`都可以用于判断相等，并且我看到的它们在条件中都用的是`=`

不等也有两个`<>和!=`

至于大于小于，大于等于，小于等于，都与一般别无二致

另外还有`!<`和`!>`



除此之外的逻辑运算都是用关键字而不是符号，如`and or not`

还有相当多的逻辑运算符，我在这里只挑出那些我可能用得上的，并且比较难以由已知语句组合而成的

`in`可以搜索在范围内的，如`select * from user where name in ("stan", "han"); `

`not in`

别的我都不太用得上:joy:

至于`like GLOB`我要单独摘出来写



#### where子句

where很常用

用法也是极其简单的，所以就不说了



#### like子句

like适用于匹配特定模式的的文本，若匹配将返回真，否是假

与之配合的常有两个通配符，`%和_`

百分号代表n个数字或字符，n可以是任意值，下划线代表一个字符或数字

例如`select * from tablename where name like %123%;`代表选择名字中任意位置包含123的

`select * from tablename where name like 123%;`名字以123开头的

`select * from tablename where name like _123_;`名字必须是5位，中间三位是123



#### GLOB子句

这个也是通配符，但是要注意，我之前有说在语法中，大多时间是不分大小写的，但是GLOB要分，所以当使用这个语句时必须写为`GLOB`,小写的意义是不同的

它的通配符是`*和？`星号是n个，问号是一个

所以，它和like有什么区别呢？不知道，那就算了吧，怪费劲的



### 更多的内容

我现在感觉上面的内容应该就可以满足我的需要了，还有一些其他的内容，我只是稍微提一下，以备不时之需

`Limit`可以限制返回的条目数量，也可以配合`offset`设置偏移

`order by`可以按照要求对返回的条目排序

`group by`和`having`不知所以

`distinct`可以筛出重复的条目





### 规划

[这一篇文章](http://www.jianshu.com/p/0c88017f9b46)讲述了一些数据库接口的东西

我现在的打算就是写一个类，对数据库的操作做一些包装，让操作简单一点，类似于ORM



