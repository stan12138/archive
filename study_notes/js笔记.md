## JavaScript笔记

> --by stan 17.7.19

&lt;font color='red'>最佳参考书为JavaScript高级程序设计（第三版）&lt;/font>

### 概念

首先澄清几个概念，ECMAScript就是标准化的Js,事实上现在人们通常认为二者是同义词，但是呢，更严格地讲，Js的范围要更广一些，他应该包含基本的Js,DOM（文档对象模型），BOM（浏览器对象模型）
DOM似乎是完成了js和html,css的接口，甚至是一些鼠标事件

### 数据类型

下面写的很混乱，在这里重新声明一下，js的数据类型大概可以分为5种：Undefined,Null,Bool,Number,String.还有一个复杂的数据类型，叫做Object,Object本质上是一组无序的键值对，类似于python里面的字典

### 变量与类型

*   变量统一使用var声明，使用动态类型，与python一致

*   区分大小写，html不区分大小写，但是它的标签和属性在js中必须写成小写。

*   注释使用//和/**/，与C语言一致

*   分号不是必须的，但注意保持风格一致，但是在某些位置句尾还是必须要分号的，介于我还不是老手，所以建议每个句尾都加分号

#### 数字

数字同样不分类，十六进制使用0x或0X的前缀，不是所有的标准都支持直接写八进制，支持的使用0开头，所以建议不要用
浮点数支持e或E的用法
四则运算为+-*/，取余%，似乎其他复杂运算都要调用库，Math库，留待后述
溢出不报错，定义了Infinity。另外还用一个NaN。
注意不要去试探她的浮点数的精度，譬如0.3-0.2并不等于0.2-0.1  

#### 时间

js里面特别提供了一个日期或时间类型，它提供了一些方法，可以让我们快速进行计算，例如快速计算两个事件之间的毫秒数，可以直接使用减法。  

#### 字符串

js的默认编码为utf-16
单引号和双引号都可以，与python一致
可以拆分为多行，但行尾必须使用\续行
转义字符一致，暂不叙述
字符串支持加法，另外还有很多的属性和方法，例如length属性
支持索引[]
自带支持正则表达式，正则表达式使用两条/包围，第二条的后面还可以跟一个或多个修饰的字母  

#### 布尔值

保留字true,false

#### 缺失值

null,undefined
前值为空，后者就是未定义的意思  

#### 全局对象

？？？

#### 类型转换

这里的类型转换似乎要灵活得多，暂且略过，只保留字符串与数字
数字有一个toString()方法，并接受一个参数指定基数，还有更高级的toFixed,toExponential,toPrecision等方法，暂不详述。
将字符串转换为数字有parseInt(),parseFloat()等函数，很智能很高级，暂不详述
总之类型转换很灵活，很复杂，东西很多还没说  

#### 作用域

在局部作用域里面可以访问其相对全局作用域的变量，并且可以直接更改，不需要特别声明，这一点和python不同。
函数是一个局部作用域，这一点和类C语言一致，但是js中不存在块级作用域，例如在C中，当你在一个for语句，if语句内部声明了一个变量，那么你将可以在花括号内部访问该变量，但是在花括号结束时，该变量就被销毁了，但js不存在这一个作用域，for等的内部声明的变量，在外部依旧存在

### 全局对象

有一个很奇特的叫全局对象的东西，指的是一份js代码文件，也可以使用this自我引用，文件里面所有的全局变量都是this的一个属性，不使用var声明的可以使用delete删除，等等，暂不需了解太多  

### 表达式运算符

*   创建一个对象要使用new关键字
*   ++ -- += -= *= /=
*   `+ - * /`

*   == ! &amp;&amp; ||  &lt; &gt; &lt;= &lt;=
  均类似于C语言
*   还有一个什么鬼的`===`是恒等的意思，`！==`恒不等,暂时也用不上，就不深究了
*   in和instanceof暂时略过
*   还有一个神奇的eval()函数，可以直接运行字符串形式的源代码，暂不表
*   有三目运算符?:
*   typeof运算符，测量类型，如 typeof x；关于返回值的情况暂时略过
*   delete运算符，删除一个对象的属性或者一个元素
*   void运算符，可以强制去掉返回值

### 语句

#### if

~~~c
if(expression)
{
}
else if(expression)
{
}
~~~

#### switch

我没有用过switch,所以暂时不写

#### while

~~~c
while(expression)
{
}
~~~

#### do while

~~~c
do
{
}
while(expression)
~~~

#### for

~~~c
for(init;test;update)
{}
~~~

#### for/in

~~~c
for(variable in object)
{}
~~~

#### 另有

跳转部分的标签，break，continue，return等

#### 异常处理

throw try/catch/finally等，暂不表

#### 其他语句

with  debugger  "use strict"暂不说  

### 数组

js里面的数组更类似于python里面的列表，元素类型不限。
可以随意增长，只需要对后面的索引赋值即可，总之其索引方式异常灵活。
稀疏数组，略过
数组都有一个length属性  

*   向尾部增添一至多个元素，调用push方法*   删除用delete操作符，但是并不会改变length，而是让数组变成了稀疏数组。

*   因为稀疏数组的存在，让遍历显得略微复杂，暂不提*   数字的方法也暂时略过

###  函数

~~~c
function test(a,b)
{
	var c = a+b;
	return c;
}
~~~

##### 函数的参数

函数的参数的行为很有意思，无论你在函数的定义中写了几个形参，函数调用时从来不在意你传入了几个参数，传入也行，不传也行，数目与形参一致可以，不一致也行。这一切都是因为参数在内部是通过一个数组表示的，函数只是接受了这个数组，从不在意数组的值。在函数内部是可以通过arguments这个对象来访问所有的参数，通常情况下我们会使用arguments.length这个属性来得到参数的数目，通过[]索引来获取每一个参数。另外特别需要注意的就是，arguments与参数永远保持同步，换句话说arguments[1]永远与第二个实参保持一致，两者的改动也会保持一致，虽然两者对应的并不是同一块内存。

~~~c
function test(num1,num2)
{
	if(arguments.length==1)
	{
		alert(num1);
	}
	else if(arguments.length==2)
	{
		arguments[1] = 10;
		alert(num1+num2);
	}
}
~~~

这个函数的行为表现为传入一个参数的时候会输出这个值，传入两个参数的时候会输出第一个参数加10的结果，因为通过arguments[1]可以直接修改num2的值



### 内存管理

js内部也有自动的垃圾收集机制，但是事实上os分配给浏览器的内存数量比桌面程序要少，因而当你不再使用一个数据的时候，最后可以通过手动解除引用将其内存释放一下，方法为将变量的值设置为null  


### 引用类型

所谓引用类型与我一直以来所说的构造类型一样，之所以要特别声明这个类型就是在于复制时的表现，如果一个变量是基本类型，那么在执行a=b这样的操作时它们分别指向两块内存，改变一个值不会引起另一个值的改变，但是如果一个一个变量是引用类型，那么执行复制操作的时候，两个变量事实上指向了同一块内存，改变一个会引起另一个的改变。向函数传参的时候的表现也是这样的.  


    <font color='red'>靠！！！！刚才写的几百字竟然丢了，一直很谨慎，竟然还是中招了</font>
##### Object类型

object类型会是一个常用的引用类型，创建的方法有两种：
1、使用关键字new,`var person = new Object();`，然后直接定义属性
2、使用字面值直接定义：

~~~c
var person = {
  name = 'stan',
  age = 29
};
~~~

当使用第二种方式创建时，属性名字可以是变量名也可以是字符串，如果是数字，则会被自动转换为字符串

另外这种对象也是向函数传递不定数量的大量参数的一种很好的方式  

索引属性的方式有两种，一种是`.`，另一种是[]索引，后者必须使用字符串进行索引，第二种方式可以实现一些特殊属性名的索引，例如包含空格的名字，除此之外实质上是建议使用第一种索引的

##### Array类型

所谓Array类型实际上就是数组，之前已有部分说明，这里再详细记录一次。
创建方式和Object一样，也是两种：
1、var l = new Array();可以传入参数，当传入一个数值时，代表数组的长度，也可以传入项
2、var l = [1,2,3]; 不要企图使用多余的`,`来增加数组的长度，不同的浏览器解释方式不同  

*   索引同样使用[0~n],当设置索引不存在的项的时候会自动增加

*   数组具有length属性，不仅可读，还可写，如果将其写长，会增加undefined值，如果缩短会把后面原有的值变成undefined

*   检测对象是不是数组很重要，使用Array.isArray(value)来检测

###### 栈与队列

数组同时也实现了站和队列的操作，实现的方式为提供了几个方法，`person.push()`可以接受1~n个参数，把这些量依次加到数组的末端，`person.pop()`可以弹出数组的最后一个值，并缩短数组长度，`person.shift()`可以弹出数组的第一个值，并缩短长度。额外的又提供了另外一个特殊的方法，`person.unshift()`接收多个参数，可以把它们依次加入数组的首部，同时增加长度

###### 排序

数组也集成了排序，数组提供了两个方法进行排序，`reverse`和`sort`,前者可以将数组反序，后者默认将数组升序排列，但是后者是通过将数组项转换为字符串，然后对字符串按位升序得到的，所以他会认为5大于15。因此我们需要传入一个比较函数，sort方法将会使用这个比较函数对每两个值进行比较，进而排序。比较函数需要满足的要求是：当第一个参数小于第二个时，返回负数，相等返回0，大于返回正数。如果比较函数满足这个要求，sort会将数组升序排列。因而降序也有两种方法，一是在比较函数上做手脚，一个是先升序排列，再reverse。这里提供两个样例：

~~~javascript
function compare(value1,value2)
{
  if(value1>value2) return -1;
  else if(value1==value2) return 0;
  else return 1;
}

function compare(value1,value2)
{
  return value2-value1;
}

a = [1,10,5,15];
a.sort(compare);  //没有返回值，直接将a降序排列
~~~

###### 其他方法

-   concat(),用于利用本数组创建一个新数组，以返回值的形式给出，如果不传入参数则是创建一个不同内存块的相同数值的数组，如果传入参数则会将这些项添加到新数组的尾部，如果传入一至多个数组，会自动解包，然后逐项添加。
-   slice()，用于使用本数组中的几个项创建一个新数组，参数为1或2个，一个参数时是从该项到最后一项，两个参数的话分别代表首尾，包含起始项，不包含尾部。如果传入参数是负数，那么实际上代表的是数组长度加上该值的项。
-   splice(),这个据说是最为强大的方法，接受2~n个参数，如果只有两个参数，代表从v1开始，删除数组中的v2项。如果将删除的项数设置为0，同时传入更多的参数，将会将第3至n个参数插入数组，从位置v1开始。如果同时指定了删除的项数，那么相当于替换。需要注意的是插入项不能是数组形式，他不会自动解包。
-   indexOf(),lastIndexOf(),这是两个查找方法，他们均可以接受两个参数，第一个是要查找的项，第二个是查找的起点，第二个参数可选。两者不同之处在于前者从头开始查找，后者从尾开始。同样的查完或者查到第一个结束，不会找到所有的位置。查找失败返回-1。需要特别注意的是，这里的查找是全等，也即同一块内存，因而自行构建的两个看起来一样的引用对象是查不到的。
-   迭代方法，数组定义了5个迭代方法，每个方法都接受两个参数，第一个是要在每一项上运行的函数，第二项是运行该函数的作用域对象**不明白啥意思**。其中传入的函数接受三个参数：数组项的值，位置，数组对象本身。函数的返回值对于不同的迭代方法有不同的要求。
    -   every(),如果对每一项函数的返回值都是true,则该方法返回true
    -   filter(),返回一个数组，数组中的项是函数返回值为true的项
    -   forEach(),只是运行函数，没有返回值,类似于一个for循环，所以有啥用？
    -   map(),返回一个由函数返回值组成的数组
    -   some(),如果有至少一项的函数返回值为true，则返回true
-   归并方法，提供了两个归并方法，reduce(),reduceRight(),两个方法均会逐个迭代数组里的所有值，区别在于前者从前往后，后者从右开始。均接受两个参数，第一项是要在每个项上执行的函数，第二个是归并基础的值，可选。函数接受四个参数：前一个值，当前值，位置，数组对象。这个函数的返回值会作为下一项执行函数的第一个参数。如果只给方法提供了一个参数，那么方法会自动从数组的第二项开始执行，并把第一项作为迭代函数的第一个参数传入。如果提供了两个参数，则会从第一项开始执行，并把第二个参数作为迭代函数的第一项传入。

##### Date类型

使用`new Date()`可以创建一个时间类型，不传入参数创建的是当前时间，支持传入一个微秒数，以创建一个特定的时间，时间基点为1970.1.1 00：00：00.  

为了简化又特意提供了两个方法，其中的Date.parse()接受特定格式的日期字符串，然后返回微秒数，但是标准中并未规定字符串的格式，因地区而异，因而我觉得这并不是一个好的方法。

Date.UTC(),该方法接受一系列的参数，分别代表：年，基于0的月份（0是1月），天（1~31），小时（0~23），分钟，秒，毫秒。参数中年月必需，天默认是1，其他默认0.

日了狗了，在chrome中测试，UTC方法的默认时区是格林尼治时间。

绕了一圈才发现实例化的时候竟然支持与UTC一致的参数传入，而且时区会设置为本地时区。

-   Date.now()，返回调用这个方法时的毫秒数

###### 继承的方法

Date类型重载了几个方法，分别是toLocaleString(),toString(),valueOf()，分别是转换为本地格式的日期字符串，带时区信息的字符串，毫秒数。似乎没啥太多用处

###### 日期格式化

大概有那么5个方法，大多输出格式因浏览器而异，所以没太大用处

除了上面说的之外，还有很多方法，不再提及

##### RegExp类型

RegExp是用于支持正则表达式的

这里使用的正则表达式的格式类Perl:`var expression = /pattern/flage;`

其中的pattern即正则表达式，flage是一些行为标志，支持三种：

-   g,全局模式，匹配所有的，即全局模式，而非在发现第一个时停止。
-   i,不区分大小写。
-   m，多行模式，会继续查找下一行，不因行的结束而停止

例如：var pattern = /.[bc]at/gi;

###### 属性

有几个用来查看实例属性的属性：

-   global,是否设置了g
-   ignoreCase,是否设置了i
-   multiline,是否设置了m
-   lastIndex
-   source

这些都没有实用价值

###### 方法

重要方法有两个，

-   exec(),接收一个要应用模式的字符串为参数，返回第一个匹配项的数组信息，无匹配返回null。返回值是一个特别的数组，有两个特殊属性，index,input，前者代表匹配项在数组中的位置，后者就是exec的参数。exec每次只会返回一个匹配项，返回值数组的第一项是匹配到的字符串，如果模式中有捕获分组，则数组的其他项是捕获组，没有捕获的话只有一个。如果正则表达式开启了全局模式，则每次调用exec会匹配下一个位置，如果没开，每次调用匹配的是同一个位置。
-   test(),接收被应用的字符串，返回值代表匹配到与否

注意，这似乎是一个状态机之类的，如果开了全局模式，然后先调用了一次test,然后再调用exec，他也会把第一个跳过

###### 其他属性

还有大概6个被称作构造函数属性的属性，每个属性有两个名字，一个长属性名，一个短属性名，大概暂时用不到，我也不再详细记录了

-   input  $_
-   lastMatch  $&
-   lastParen  $+
-   leftContext  $`
-   multiline   $*
-   rightContext  $'

##### Function类型

函数事实上是对象，既有属性又有方法，函数名只是一个指向函数对象的指针。

正因为函数是对象，我们也可以使用实例化Function类来创建一个函数，虽然这种方式极不推荐。

解析器有一个叫做函数声明提升的过程，这样即便函数写在调用之后，也还是可以工作，但不推荐这样做，函数声明和函数表达式不一样，如果以函数表达式创建一个函数，就绝对不能写在调用之后。

1.  函数的内部对象

    一个内部对象是前面所说的类数组参数对象arguments,不再多说，补充一下，arguments有一个callee属性，它是一个只想拥有该arguments对象的函数，这在某些时候有些用处。

    另一个是this,指向拥有该函数的对象。

2.  函数的属性

    -   length,代表函数希望接受的参数的数量
    -   prototype,暂时我也不太懂，也似乎对我还没啥用

3.  函数的方法

    -   apply()
    -   call()
    -   bind()

    说是这几个方法都是用来扩充函数的作用域或类似作用的，暂时也没啥用

##### 基本包装类型

布尔类型，数字，字符串，如前所述是基本类型，但是它们的确可以访问一些特殊的方法和属性，这是因为实际上在创建的时候解释器自动进行了一个创建对象并销毁的过程。

因而存在Boolean(),Number(),String()对象，但是，对于前两者而言，基本上不建议使用，没啥用，有时还会造成误解。

###### String类型

我觉得暂时没必要写很多字符串的方法，反正也记不住，跳过吧



##### 单体内置对象

大多数所谓单体内置对象都已经介绍过了，就是内置类型，这里再介绍两个

###### Global对象

似乎并没有太多适合现在研究学习的，只有一个前面提到过的eval方法

window对象，全局作用域里面的所有变量和函数都是window对象的属性

###### Math对象

提供数学计算

-   属性

    这里提供了很多常用的常数，例如Math.E,Math.PIdeng

-   方法

    -   min(),max().特别的如果想要找到数组的最值，不能简单的传入，需要这样Math.max.apply(Math,array)
    -   舍入，ceil(),向上舍入，floor(),向下，round()四舍五入
    -   random(),[0,1)之间的随机数
    -   其他的数学函数，如abs,exp,log,pow,sqrt,sin,atan2等，不多说

    ​

### 面向对象

书中在原型模式创建类，继承这两个部分花费了很多笔墨，也相对而言比较难懂，我也暂时用不上这么深入的东西，因而暂不记录。

-   考虑如何创建一个对象。

~~~javascript
//实例添加
var person = new Object();
person.name = 'stan';
person.age = 23;
person.sayname = function(){
  alert(this.name);
};

//字面值
var person = {
  name : 'stan',
  age : 23;
  sayname : function()
  {
    alert(this.name);
  }
};

//如何创造一个可供实例化的对象呢？
//
//工厂模式
function Person(name,age)
{
  var o = new Object();
  o.name = name;
  o.age = age;
  o.sayname = function()
  {
    alert(this.name);
  };
  return o;
}

//构造函数
function Person(name,age)
{
  this.name = name;
  this.age = age;
  this.sayname = function()
  {
    alert(this.name);
  }
}
~~~

总而言之，你只是想构建一个特殊的结构体，那么推荐前两种，如果是想创建一个类，那么推荐最后一种。

-   属性设置

    -   对象的每个属性都可以设置4种数据属性，用来控制某个属性的行为特征，这四个属性是：`Configurable 可否delete并重新设置`,`Enumerable 可否通过for-in循环返回属性`,`Writable 可否修改属性的值`,`Value 包含这个属性的值`

        这四个属性的前三个默认值为true,最后一个默认undefined。

        如果想要修改某个属性的默认值，必须使用一个特殊的设置函数`Object.defineProperty()`这个方法接收三个参数：属性所在的对象，属性的名字，一个描述符对象。

        ~~~javascript
        var person = {};

        Object.defineProperty(person,'name',{writable:false,value:'stan'});
        ~~~

        经过上述设置，person.name将只能读，无法再修改了。

        值得注意的是，按照书上所说，属性是可以通过上述方法反复修改的，但是，如果把configurable设置为false之后就会受到约束。但是我暂时实验反复修改会抛出错误，所以，暂时只是知道就好了，具体行为有待继续研究。

    -   另外属性还可以设置四个访问器属性，这四个属性控制其被访问时的特征（这里具体的属性数量我还不确定，四个里为啥有两个重复的），先说两个：

        这两个同样需要通过Object.defineProperty()来设置，分别是get和set,设置方法如下所示：

        ~~~javascript
        var book = {
          _year : 2004,
          edition : 1
        };

        Object.defineProperty(book,'year',{
          get:function(){
            return this._year;
          },
          set:function(value){
            if(value>2004){
              this._year = value;
              this.edition += value-2004;
            }
          }
        })
        ~~~

        这时当你访问book.year时，get就会起作用，当你试图设置book.year时，set函数就会起作用。

    大概属性设置就是这样，甚至暂时根本用不上。

    ​

面向对象的更深入的部分暂时不再继续了

### 函数表达式

常用的函数创建方式叫做函数声明，还有一种创建方式叫做函数表达式。

常用的函数表达式的形式为：

~~~javascript
var functionname = function(args){
  //函数体
}
~~~

这是创建的函数也叫匿名函数。

我讨厌递归，跳过

#### 闭包

所谓闭包，就是指一个函数，它可以访问其他函数的局部作用域的变量。

书中做了大量的解释，包含作用域的作用域链机制，我并未深入研究。

暂时到这。

#### 块级作用域

呃，有点不知所云

#### 私有变量

这里有点意思，前面一直在强调，函数也是对象，这句话是什么意思？对象的特征是什么？所谓对象，最明显的特征是具有属性和方法，所以这意味着可以为一个函数再创建一个方法，这个时候函数就颇类似于一个类了，也可以实例化：

~~~javascript
function Person(name)
{
  this.get = function()
  {
    return name;
  };
  this.set = function(name1)
  {
    name = name1;
  };
}

var person = Person('stan');
alert(person.get());
person.set('nats');
~~~

##### 模块模式

没搞懂。。。。。



---

>   开始新的一部分



## BOM

Bom是用于访问浏览器的功能的。

### window对象

window对象既是用于访问浏览器窗口的接口，同时也是js的全局对象，这意味着js中的所有全局变量和函数都是window的属性和方法。

html5已经废除了框架，所以暂时在这里就不再介绍关于框架的操作。

==截止到这一部分，我必须要同时使用html进行测试了，所以先一笔带过在html中外链js的做法==

`<script src='test.js'></script>`

==这里需要绝对注意的是，文档加载的问题，例如我把外链js写在head里面了，那么js几乎是无法获取到body里面的标签的，因为代码执行的时候body还没加载出来，所以，暂时需要把script放在后面==

==现在，我对BOM的意义及作用很困惑，感觉并没有太多的用处==

-   setInterval()与clearInterval()方法，前者可以以制定的时间间隔循环运行函数，后者可以停止这个函数的运行。

    ~~~javascript
    var func_id = window.setInterval(func,time);
    window.clearInterval(func_id);
    //time的单位是毫秒
    ~~~

-   setTimeout()与clearTimeout()方法，他们可以在指定时间之后调用函数

    ~~~javascript
    var func_id = window.setTimeout(func,time);
    window.clearTimeout(func_id);
    ~~~

需要注意的一个点就是，如果要循环执行一个函数，函数需要执行200毫秒，却把间隔设置成100毫秒，就会出问题，所以比较好的替代方案是利用setTimeout()

~~~javascript
function work()
{
  //do something
  window.setTimeout(work,100);
}
var func_id = window.setTimeout(work,100);
window.clearTimeout(func_id);
~~~

==这个方法会不会产生大量的id的吧==，怎么办

没有可以一次清除所有工作的内置方法，一个思路是id是一个整数，所以循环清除大量的整数就可以了。

我觉得并不好。

呃，书上说，clearTimeout是用来处理超时未调用的情况的，所以，其实，其重要性远低于clearInterval



==靠，连写个html做一些小的验证都出错，写不出来，学的没有忘得快，什么时候才能结束==

##### 窗口位置，大小

根据测试，是无法修改当前窗口的位置和大小的，能起作用的只有使用window.open打开的新窗口

根据不同的浏览器，可能会提供这么几种属性拿到窗口的位置，screenLeft,screenTop,screenX,screenY

这四个属性对浏览器依赖很严重，所以如果要用，需要仔细再研究。

跨浏览器确定窗口大小也不容易，可能会使用的四个属性是：innerWidth,innerHeight,outerWidth,outerHeight。在Chrome等浏览器里document.documentElement.clientWidth,document.documentElement.clientHeight也提供了页面信息

除了上面这些之外，还有：

-   window.moveTo(x,y),将窗口移动到x,y
-   window.moveBy(dx,dy),将窗口移动dx,dy
-   window.resizeTo(x,y),将窗口尺寸变为x,y
-   window.resizeBy(dx,dy),将窗口尺寸变化dx,dy

如上面所言，这四个改变窗口的方法必须对程序自己打开的窗口才有效，反正Chrome里面是这样

所以：

-window.open(),这个方法接受四个参数，但通常使用的都是前三个，第四个是关于历史记录什么的，感兴趣自己看。第一个是URL，可以是空字符串，第二个是target,如果是一个已存在的窗口，就会替换内容，如果不是则会新打开一个，第三个参数是一个特性字符串，用以设置新窗口的位置，大小，菜单栏，状态栏，工具栏等等，这里只记录一下关于尺寸位置的，示例：`top=100,left=100,width=800,height=600'`

##### 对话框

-   alert(),常用的
-   prompt(),接受的第一个参数是提示文本，第二个参数是默认输入文本，这个方法会给出一个文本输入框，然后把用户输入的字符串返回
-   window.print(),显示打印对话框
-   window.find(),显示查找对话框

##### location对象

这个对象提供了很对关于url，host等等的属性，似乎对我暂时没啥用

##### navigator对象

这个似乎常用来检测浏览器也能检查插件，也暂时没用

##### screen与history对象

跳过

### 客户端检测

跳过？





到了DOM了

## DOM

### 关于节点

html就是document的一个子节点，接下来html又有head,body两个子节点，这两个子节点互为兄弟节点，就这样整篇文档构成一个家谱关系

-   节点类型，所有类型的节点都继承自Node类型，共享相同的属性和方法，每个节点都有一个nodeType属性，节点类型一共有12种，任意节点必属其一，这十二种类型都有两个名字，一个是一个常数值，另一个是Node的属性名

    -   Node.ElEMENT_NODE    1
    -   Node.ATTRIBUTE_NODE  2
    -   Node.TEXT_NODE       3
    -   Node.CDATA_SECTION_NODE  4

    .....

    其余的就不做记录了

    推荐使用数值进行比较，例如：`someNode.nodeType==1`

    常用的节点是元素和文本

-   类型属性

    -   与节点类型相关的三个属性
        -   someNode.nodeType,前面写过，查看属于12种的哪一种
        -   someNode.nodeName,查看标签名，Tag Name
        -   someNode.nodeValue，最废物的属性，值永远是null

    -   家谱关系索引的相关属性

        -   someNode.hasChildNodes,确定节点是否有子节点的很好的属性

        -   someNode.childNodes,这个属性保存着一张NodeList列表，其中是所有的子节点，是一个动态变化的类数组结构，有length属性，也支持[]索引，也可以使用item方法进行索引

            ~~~javascript
            someNode.childNodes[0];
            someNode.childNodes.item(0);
            someNode.childNodes.length;
            ~~~

        -   someNode.firstChild,someNode.lastChild,为了便捷的firstChild和lastChild属性，分别指向childNodes列表的第一个和最后一个元素

        -   someNode.parentNode

        -   someNode.previousSibling,someNode.nextSibling，如果不存在就是null

        -   someNode.ownerDocument,直接访问指向整篇文档的文档节点

-   方法与节点操作

    -   appendChild(),insertBefore(),replaceChild(),removeChild(),我并不认为这种改变文档树结构的方法会经常使用，详细用法自己看，==注意，这些都是针对父节点的子节点的操作==
    -   cloneNode(),细节不记录
    -   normalize(),处理文本节点

### Document

document表示整个html页面，nodeType是9，nodeName是`#document`,没有parent,没有ownerDocument

-   document.documentElement,该属性指向html元素
-   document.body,该属性指向body属性
-   具有childNodes,firstChild,lastChild等属性

#### 文档信息

-   document.title,可以读写，但是即便写了也不会反映到浏览器上
-   document.URL,documnet.domaim,document.referrer.大概现在也用不上

==靠！！！！弄了一个小时，Sublime Text3上面的Js智能提示也没弄好，这些插件都像屎一样难用==

#### 查找元素

-   document.getElementById()
-   document.getElementByTagName(),接受标签名，返回值同样是一个动态集合，支持[]索引，具有length属性和item方法，如果标签有name，还支持直接使用[]的类似字典的索引方式，或者将名字传入namedItem方法
-   document.getElementByName(),这是html页面独有的方法
-   特殊集合
    -   document.anchors,所有带name属性的`<a>`元素
    -   document.forms，所有form元素
    -   document.images
    -   document.links,所有包含href属性的a元素


#### 文档写入

主要指`document.write(),document.writeln(),document.open(),document.close()`这四个方法，你可以使用前两个往页面内写入html代码，至于后两个，书中并未说明

需要注意的是浏览器对于嵌入式代码的解析规则，它是自上而下进行解析的，所以如果你在嵌入的js代码中无论以任何形式写了`</script>`的话，浏览器不会管什么匹配规则，直接就会结束script，从而出现错误。解决这个问题的办法就是把这个标签转义一下`<\/script>`

### Element

1.  使用nodeName属性查看标签名，其实还有一个tagName，两者一致

    需要注意的是查到的名字往往都是大写形式

2.  所有的html元素均继承自HTMLElement,而HTMLElement直接继承自Element，然后增加了一些属性。

    -   id,获取一个元素的id
    -   title,如果元素具有title属性，获取title的值
    -   className,获取元素的class,之所以不叫class，因为那是关键字
    -   dir lang，这两个前者是文本的方向，后者是语言，都极少用

    上述属性都是可修改的，并且修改会起作用，例如html关联了css，那么对id或class的修改会立刻使样式变化，再如对dir的修改会立刻使文本位置改变

3.  几乎所有的元素的特性都可以使用属性来访问，但是对于自定义的特性是无法通过属性来访问的,这时可以使用元素的getAttribute()方法，建议是除了要获取自定义特性之外，其它的特性统一使用属性的方式获取

    值得注意的是,有两类特殊的特性利用属性和getAttribute方法得到的返回值不同：

    -   style,属性会返回一个对象，方法会返回一个css文本
    -   onclick等事件处理程序，属性会返回一个对应的js函数，方法则会返回函数的代码字符串

    总而言之，尽量避免使用getAttribute()

4.  与getAttribute对应的是setAttribute,但是两者的待遇差很多，对于设置特性而言，推荐使用setAttribute,这里的特点是这样的：针对chrome，直接使用属性的方式去设置特性是无效的，并不会产生什么结果，唯一的结果是再使用属性的方式去访问时，可以得到修改后的结果，但是使用setAttribute却可以使修改真正生效，例如让css起效等，但是如果是使用setAttribut进行修改的话，使用属性的方式去访问却无法得到结果，此时必须使用getAttribute才能得到修改结果，很恶心是不是。



5.  最后是删除属性的方法removeAttribute()
6.  元素还有一个attributes属性，它的表现类似于childNodes，同样是以动态列表的形式给出所有的特性，同样可以做索引等操作，但是这个方法并没有上述方式用起来方便，所以只会在做遍历的时候使用。

#### 创建元素

==fuck,发现自己很没有条理，各种标题，部分标的一塌糊涂==

使用document.createElement()方法可以创建一个新的标签，同时会返回这个标签的引用，然后可以为这个标签设置各种特性，例如：

~~~javascript
var div = document.createElement('div');
div.setAttribute('id','stan');
~~~

然后，如果要使这个标签发挥作用，必须将其添加到文档树中，可以使用document.body的appendChild,insertBefore,replaceChild等方法

#### 子节点

元素也有getElementByTagName的方法，跟document的这个方法不同的是，元素的方法搜索的是元素的子节点

#### Text类型

例如div标签中包含的文本，p标签中的文本等等，都是Text元素，它们的nodeType等于3，可以通过nodeValue或者data属性访问它们的值。

可以直接通过给data赋值进行修改，但是他也提供了一些方法：

-   appendData()
-   deleteData()
-   insertData()
-   replaceData()
-   splitText()
-   substringData()

同时，无论nodeValue还是data都提供了一个length属性

##### 创建文本节点

使用document.createTextNode(text)来创建一个新的文本节点，然后使用元素的appendChild()方法，把新建的文本节点加入元素，最后使用doucument.body的appendChild()方法把元素加入文档树

但是，值得注意的是，如果分多次给一个元素加入了多个文本节点，那么虽然视觉上与一个文本节点无异，但是逻辑上是多个节点，然后只需要对这些文本节点的父节点调用normalize()方法，就可以合并为一个。使用上述文本节点的splitText()方法也可以将一个文本节点分为多个。

#### 可能用得上的两个类型

##### DocumentFragment

这个类型存在的意义就是作为一个轻量级的文档片段仓库，例如要为一个ul添加多个li条目，那么如果逐个添加会导致浏览器多次渲染，可以使用document.createDocumentFragment()创建一个文档片段，然后暂时把这些条目加入片段，最后再把片段加入ul

##### Attr类型

这个类型其实就是元素的特性，可以通过创建一个完整的特性节点，然后添加到元素中，其实没有太大的必要，我觉得很多余

#### 其他的一些类型

comment类型是注释，CDATASection是针对XML的类型，DocumentType支持的浏览器不多，包含的是文档的doctype相关信息

### DOM操作技术

书中讲了很多关于动态js和动态样式表的内容，实际上说的就是利用js动态创建一个外链js或者css的标签，不细说了

##### 操作表格

直接使用核心DOM创建一个表格十分之繁复，所以为了方便，特意提供了一些属性和方法：

呃，暂时用不上吧，不想写了

## DOM扩展

### 新的选择器

这些js扩展的目的就是改进元素的选择方法，不使用蹩脚的getElementById等方法，而是直接使用与css的选择器一致的方法，这里的两个核心方法是document.querySelector()和document.querySelectorAll()

-   querySelector(),该方法接受一个css选择符，返回第一个匹配的元素或者null,示例：

~~~javascript
var body = document.querySelector('body');
var mydiv = document.querySelector('#mydiv');
var selected = document.querySelector('#.selected');
var img = document.querySelector('img.button');
~~~

-   querySelectorAll(),这个方法的返回值永远都是一个NodeList，如果没有，列表就是空的

上述两个方法，document类型和Element类型都有，不同之处在于，前者会搜索整篇文档，后者之后搜索元素的所有后代元素

### 元素遍历

核心的DOM中，只有childeNode等访问子节点的属性或方法，但是节点意义广泛，如果只是想访问子元素，就必须再自行做检查，新的API中，直接定义了一组新的访问元素的属性：

-   childElementCount,子元素个数
-   firstElementChild
-   lastElementChild
-   previousElementSibling
-   nextElementSibling

### 关于HTML5的改变和专有扩展

除了新增了一个getElementByClassName()方法之外，其它的都有些莫名其妙，略过

## DOM2和DOM3

==what?==

==我不想写了，最后再学一个canvas，就暂时终止js的学习==



## Canvas

canvas可以说是分为2D和3D两种，所谓3D指的就是WebGL，2D和3D的区分是通过在canvas上获得的绘图context实现的

首先需要在html中设置一个canvas标签，同时指定绘图区域的宽和高，与之前一样的是我们可以通过js修改宽和高，同时也可以用css修改其样式，但是，如果完全不做任何绘制，也不指定样式canvas在页面上是不可见的。

Ps.<u>我前面似乎做过一些记录，说修改元素的特性直接使用属性是不会起效的，需要使用setAttribute()，当时对于元素的class的修改实验的确是这样的，但是现在发现对于canvas直接利用属性来修改它的尺寸是可以的，所以，这个问题依旧没有完全搞定。</u>

首先，明显要先通过各种手段获得canvas的引用，如:`var ca = document.getElementById('drawing');`

然后，获取ca的绘图context，这一步也是决定2D还是3D，如:`var con = ca.getContext('2d');`

之后就可以利用context进行各种绘制操作了

### 2D context

画布的坐标系原点是左上角

#### 填充与描边

两种基本的绘制类型是填充和描边，含义很明显，这两种操作的特性通过context的fillStyle和strokeStyle两个属性来设置，默认两个都是'#000000'，即黑色，支持设置为颜色字符串，渐变对象，模式对象等，颜色字符串则支持名字，16进制，rgb，rgba，hsl，hsla，如：'red','#ffffff','rgba(0,255,255,0.5)'等

#### 绘制矩形

矩形的绘制有三种，fillRect(),strokeRect(),clearRect()，前两个都很明显，最后一个是用来清空一部分画布的，这三个函数都接受4个参数，矩形左上角的x,y坐标，矩形的宽和高

另外可以通过设置context的一些属性来设置描边的特征，例如lineWidth控制线宽，可设置任意整数;lineCap控制线条末端的形状，是平头，圆头，还是方头，对应：'butt','round','square';lineJoin属性控制线条相交的方式，圆交，斜交还是斜接，对应：'round','bevel','miter'

#### 绘制路径

首先，必须调用context的beginPath()方法，然后调用各种路径绘制方法进行绘制：

-   arc(x,y,radius,startangle,endangle,counterclockwise)，x,y为弧线的圆心，radius是半径，最后一个参数为true代表逆时针绘制，反之为顺时针
-   arcTo(x1,y1,x2,y2,radius)，从当前点开始经过x1,y1绘制一条以radius为半径的弧线到x2,y2
-   bezierCurveTo(c1x,c1y,c2x,c2y,x,y),从当前位置以c1x,c1y,c2x,c2y两个点为控制点绘制一条贝塞尔曲线到x,y
-   lineTo(x,y),从当前位置绘制一条直线到x,y
-   moveTo(x,y)，把画笔移动到x,y
-   quadraticCurveTo(cx,cy,x,y),以cx,cy为控制点，从当前位置绘制一条二次曲线到x,y
-   rect(x,y,width,height),以x,y为左上点，绘制一个指定宽高的矩形路径

当路径完成之后，需要调用fill方法填充，或者调用stroke()方法描边



#### 绘制文本

绘制文本可以使用三个属性对文本的绘制进行设置，这三个属性分别是font,textAlign,textBaseline，其中的font可以指定文本的样式，大小，字体，使用的是CSS字体样式，如'bold 14px Arial'或'10px Arial'等，至于textAlign,textBaseline类似于锚点的设置，其中的textAlign可能的值为'start','end','center','left','right'，建议不要使用'right'和'left'，因为他们的意思比较含糊不清，textBaseline的可能的值为'top','middle','bottom','hanging','alphabetic','ideographic'，其中前三者的意思很明显，后三者是比较特别的基准线。很明显textAlign指定横向锚点，textBaseline指定纵向锚点

chrome默认值是左下角是锚点

上述三个属性都有默认值

设置或者使用默认设置之后，绘制工作使用的是context的两个方法，filltext()和strokeText()，含义也很明显，均接受四个参数：文本字符串，x,y，第四个参数可选，代表最大像素宽度

#### 变换

设置一些变换之后，之后的绘制工作都会经过这个变换再进行绘制

有以下几种变换的方法：

-   rotate(angle),绕原点旋转

-   scale(ax,ay),分别指定了x,y方向上的缩放因子

-   translate(x,y)，将整个坐标系统的坐标原点移动到x,y

-   transform(m11,m12,m21,m22,dx,dy),直接修改变换的矩阵，在当前变换矩阵的基础上再乘上

    m11 m12 dx

    m21 m22 dy

    0   0   1

-   setTransform(m11,m12,m21,m22,dx,dy),首先将变换矩阵重置为初始状态，然后再使用给定的参数调用transform()方法


其实，从上面的一系列过程可以看出，对于context的设置是一个状态机，一旦设置了，就很难回到初始状态，现在提供了两个方法，save()和restore()，这两个方法提供了一个栈，使用save()可以记录现在的状态到栈内，使用restore()返回栈顶的状态


#### 绘制图像

在html5中，img有两个属性，分别是naturaHeight,naturaWidth,可以获得图片的原始尺寸

想要绘制，首先要获取一张图片，书上给出的方式是拿到一个html的img标签，然后把这个标签传入到context的drawImage()方法就可以

这个方法可以接受三个，五个，或九个参数，三个参数分别是img，左上角坐标x,y。五个参数再增加要绘制成的图片的宽高。九个参数，是可以截取图片的某一部分，增加的四个参数是截取区域的左上坐标，宽高。

#### 阴影

通过设置context的下述几个属性，可以设置阴影的效果：

-   shadowColor,接收的是CSS格式的颜色
-   shadowOffsetX,x方向的阴影偏移量，默认0
-   shadowOffsetY
-   shadowBlur,模糊的像素数，默认0

不同浏览器对阴影的支持效果不同



==余下的几个，感觉并不是很有趣，先跳过了，至于WebGL，呵呵，先留着吧==





#### 渐变



#### 模式



#### 使用图像数据



#### 合成





### WebGL

