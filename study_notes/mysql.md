## MySQL笔记



还是使用命令行吧，去软件列表里找到，打开


如果无法连接，说明MySQL未打开，在运行里输入：services.msc回车，找到MySQL，右键运行





### 数据类型：

- 整数： int, bit
- 小数： decimal
- 字符串： varchar(长度可变), char(长度固定),text存储大文本，大于4000个字符
- 日期时间： date, time, datetime
- 枚举：enum

这一部分可以参见[这个博客](https://blog.csdn.net/anxpp/article/details/51284106)



### 数据库操作

- 连接数据库

    ~~~
    mysql -uroot -p；
    mysql -uroot -ppassword;
    ~~~

- 退出数据库

    ~~~
    exit;
    quit;
    ctrl-d;
    ~~~

- 查看数据库版本 `select version();`

- 查看当前时间 `select now();`



- 查看数据库 `show databases;`
- 创建数据库 `create database name;`, 同时指定编码`create database name charset=utf8;`

- 查看创建某个数据库时执行的详细指令 `show create database name;`

- 删除某个数据库 `drop database name;` 当name中包含了一些特殊字符如连字符需要使用反引号引起name



- 查询当前使用的数据库 `select database();`

- 使用某一个数据库 `use name;`

- 查看当前数据库内所有的表 `show tables;`

- 创建一个表

~~~mysql
-- auto_increment 自动增长
-- not null 不能为空
-- primary key 主键
-- default 默认值
-- create table name (字段 类型 约束[, 字段 类型 约束]);

create table stan (id int primary key not null auto_increment, name varchar(30));

-- 支持换行
create table name (
	id int primary key not null auto_increment,
    name varchar(30)
)
~~~

- 查看数据表的结构 `desc name;`

- 无符号类型 `int unsigned`

一个示例:

~~~mysql
create table students (
	id int unsigned primary key not null auto_increment,
    name varchar(30),
    age tinyint unsigned default 0,
    high decimal(5, 2),
    gender enum("girl", "boy", "secrete"),
    cls_id int unsigned
);
~~~

- 显示详细的创建table的语句 `show create table name;`



- 修改表， 添加一个字段    `alter table name add colname 类型 约束;`

- 修改表， 修改一个字段，但是不重命名这个字段 `alter table name modify colname 类型与约束;`
- 修改表， 修改一个字段，并重命名 `alter table name change oldname newname 类型与约束;`
- 修改表， 删除一个字段， `alter table name drop colname;`



- 删除表， `drop table name;`

