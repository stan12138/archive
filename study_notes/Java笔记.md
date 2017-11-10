# Java笔记



参考书为Java疯狂讲义，或者Head First Java

### 准备工作

#### 开发环境

-   首先我们必须在电脑上安装JDK，去oracle官网，在菜单找开发者，开发者资源，向下翻找到java，然后查看所有，找到download里面的java SE，然后去下载页面找到JDK，找到合适的版本，下载，安装即可。安装过程中不需要做太多的更改，只需要改一下想要安装的文件夹即可

-   安装完成，我们还需要配置环境变量

    首先找到控制面板-系统-高级系统设置-高级-环境变量，然后再系统环境变量里面点新建，名字为`JAVA_HOME`，值为你的JDK的安装目录，例如：`C:\Program Files\Java\jdk1.8.0_92`

    然后继续新建，名字为`CLASSPATH`，值为`.;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar;`

    接下来找到系统环境变量里面的Path，点编辑，在最后添加`;%JAVA_HOME%\bin`，确定，配置完成

-   验证，我们只需要打开命令行，输入`java -version`，如果输出正常版本信息即说明完成

-   我们只需要到eclipse官网下载合适版本的软件，解压安装即可，也许你会注意到上面写着forjava EE，但是不必担心，无所谓的

前两天发布了最新版的JDK9，我准备直接在电脑上安装，一切按步骤走，结果当Eclipse安装之后，发现打不开，总是报错，什么one error has occur，让去看.log，我试了无数方法，JDK,Eclipse卸了装，装了卸，试了n次，几乎花了近三个小时，百度，谷歌，stackoverflow，甚至是youtube，还有官方交流组，我是了所有能找到的方法，而一无所获，最后我几乎要放弃了，决定直接使用sublime和命令行进行开发。但我最后决定再尝试一次，我卸载了JDK9，重装了JDK8，然后，我成功了。。。。靠！

#### 一点说明

安装JDK的同时就会安装JRE，当你安装完了jdk之后，你大概会在目录下发现jdk和jre，前者是开发环境，后者是运行环境，运行环境包含了各种API和虚拟机，开发环境主要包含了编译器

关于版本，之前可能看到过Java EE，Java SE，Java ME之类的东西，这其实是Java的三个版本，最初在JDK1.2的时候产生了分化，分为J2ME,J2SE,J2EE，第一个是面向移动设备和家电的控制的，第二个是整个JAVA的核心和基础，也是1，3的基础，也是我们主要学习的，第三个是java中应用最广的，主要面向企业应用开发。这三个版本一直存在，直到2004年将这三个改成了最前面我们见到的三个名字

#### 创建项目和运行

我使用Eclipse进行学习。

首先我们要在file->new->java project，然后输入项目名字即可，不需要更改默认设置，点击Finish即可。

接下来就会在package explore出现这个项目的文件夹，点开，里面有一个src目录，在该目录右键new->class，输入类名即可，一般与项目名称一致，不需更改默认设置，完成即可。

此时编辑器就会出现这个文件的编辑页面，输入以下代码：

~~~java
public class HelloWorld {  
    
    public static void main(String[] args) {
        System.out.println("Hello this is stan");
    }
    
}
~~~

需要注意，这里的类名必须与.java文件的名字一致

接下来就是运行，运行有两种方法：

-   在Eclipse里面保存之后，直接在编辑页面右键，run as 选择java application点击即可

-   找到.java文件所在的文件夹，在该文件夹打开命令行，然后输入`javac HelloWorld.java`，注意文件名是你的文件，这一步将源文件编译为class字节码文件，产生了一个.class文件，然后再输入`java HelloWorld`

    即运行了。

除了上面使用Eclipse开发之外，我们可以直接使用文本编辑器写代码文件，然后编译运行即可



### 基本规则

java纯粹面向对象，程序因此必须以类的形式存在

源码的后缀必须是.java，通常情况下文件名是不做要求的，但是如果源码中定义了一个public类，那么文件名必须与该public类保持一致，也正因如此，一个文件至多只能有一个public类，但是可以包含多个类

上面算是硬性要求，但是为了规范和增强可读性，常有以下建议：

-   一个源文件只包含一个类，不同类放在不同文件中
-   每个文件中单独定义的类都定义为public，然后文件名与该类一致

#### 关于输入输出

java的运行入口是main方法，如果我们要运行一个类，则必须要写一个mian方法，然后这个方法必须使用public static修饰，这两个修饰符位置可互换，返回值必须是void类型，接受的参数也是固定的，必须是字符串数组。总而言之main推荐是这样的形式：

~~~java
public static void mian(String[] args) 
{
    
}
~~~



java里面的输出主要有两个函数：`System.out.print()`和`System.out.println()`



#### 关于注释

java有三种注释：单行注释，多行注释，文档注释

单行注释使用`//`，多行注释使用`/*  */`

文档注释是这样的形式：`/**注释*/`



### 数据类型与运算符

java的关键字全是小写

是一种强类型语言

#### 基本数据类型

基本数据类型包含整型，字符类型，浮点，布尔四大类

其中的整型包含byte 1字节，short 2，int 4，long 8

字符类型只有char 2

浮点型包含了float 4和double 8

布尔类型 boolean 1位 true false

字符串类型不是基本数据类型，而是一个类

#### 零星介绍

字符类型必须使用单引号，String使用双引号

运算符只支持+-*/，%，++,--

更多的乘方等必须依赖java.lang.Math

扩展运算符还包含了+=,-=，*=，/=等等

比较运算符包含了：>,<,==,>=,<=,!=

逻辑运算符包含&&,||,!

还有一个三目运算符



### 语句

if语句还是一般的样式，长的只能使用else if

switch我依旧很少使用

while也别无二致

do while也很少用

for循环也一样，for(init;test;interation)

同样也有break,continue,return



### 数组

#### 定义与初始

数组的定义使用:

type[] name;

type name[];

推荐使用前者，并且定义数组的时候不能指定长度

定义之后，还必须在使用之前再初始化，初始化分为静态和动态，前者直接给出每个元素，系统决定长度，后者只指定长度，系统赋初值

静态

~~~java
int[] a;
a = new int[]{1,2,3,4,5};
//简单起见，其实还是有定义和初始化一起的
int[] a={1,2,3,4,5};
~~~

动态

~~~java
int[] price = new int[5];
~~~

关于初始值，整型默认0，浮点型0.0，字符型是'\u0000'，布尔型false，引用型null

不要在指定初始值的同时指定长度

#### 使用

索引方式也是[]，下标自0开始

每个数组都有一个length属性，标明长度

对于迭代类型，现在有提供了一种便捷的访问

~~~java
int[] a={1,2,3,4,5};
for(int i : a)
{
    System.out.println(i);
}
~~~

要注意这种便捷访问只能用来访问，不要用以改变数组的值

并且，这里的i必须是本代码块的局部变量。



怎么说呢，数组变量只要类型相同，即便长度不一致，也是可以互相赋值的，例如int[] a={1,2,3};int[] b=new int[4];b=a;

这个时候只是让b重新指向了a的内存，所以看起来是长度可变的。

实际上还是我说的，这种复合类型都是直接和内存相关的

#### 多维数组

严格上说java是没有多维数组的，但是我们可以使用

定义和初始化方法有这些：

~~~java
//1
int[][] a;
a = new int[3][];
a[0] = new int[2];

//2
int[][] b=new int[3][4];

//3
int[][] b=new int[][]{new int[3],new int[4]};
~~~

最自然的还是第二种

有一个Array类，提供了很多操作数组的方法，这里暂时不再说明



### 类（上）

所有的类都是引用类型

定义一个类是以下结构 ：

~~~java
修饰符 class name
{
    构造器
    属性
    方法
}
~~~

类的修饰符可以是`public final`二者之一，或者没有

类的成员有三种，构造器，属性，方法。构造器控制如何产生实例，如果没有则无法产生实例，默认系统会提供一个

成员之间不分先后，可以互相调用，但是static修饰的成员不能调用没有static修饰的成员

#### 属性

属性必须指定类型，可以在前面加修饰符，可以不加，修饰符的范围是`public protected private static final`

前三者只能选一个，后二者互不冲突

#### 方法

方法与普通函数的定义没区别，最前面也可以加修饰符，修饰符的范围是`public protected private static final abstract`，前三者只能选一个，后两者只能选一个，static和abstract也不能同时对方法使用。



static这个关键字表示这是属于类共有的，而不是一个类的单个实例。有static修饰的属性和方法称为类属性，类方法。没有的称为实例属性，实例方法

或者称前者为静态属性方法，后者非静态属性方法，静态成员的不能直接访问非静态成员



#### 构造器

构造器是一个特殊方法，可以加修饰符`public protected private`三者之一，没有返回值相关字段，可以带参数，名字必须与所在类保持一致



#### 使用

例如已经创建了一个Hello类，然后使用Hello a = new Hello();创建一个实例



#### this

与python里面的self一样，但是因为在一个对象内调用自己的成员十分常见，所以在java里面实际上我们可以省略this。

然后还是要特别注意，还是之前所说的static修饰的方法不能直接调用没有static修饰的成员（属性和方法）

本质上当你直接调用的时候，系统相当于使用了this

并且static修饰的方法是不能使用this的，换句话说，你永远不能在main里面使用this

如果你必须在静态方法中访问普通方法，那么必须创建一个新的对象，例如前面有个fun()普通方法，在main中调用它，则必须这样：

new StaticAccessNonStatic().fun();

还有一些情况必须使用this进行解决，例如在方法内有一个局部变量和属性同名。



#### 方法的参数传递

书中特意指出，参数传递的时候是值传递，也就是说传的只是副本，我以为即便是构造类型例如数组也是如此，但是并不是，经过测试，构造类型一如我之前所说依然是传引用。所以这里特意提出的值传递与其他语言中的基本类型的值传递别无二致。

##### 形参长度可变

可以支持长度可变的形参，但是有相当的限制：长度可变的形参只能位于参数列表的最后，换句话说只能有一个，然后这些可变参数必须是相同类型。

`void test(int a,String... books)`

如上所示，只需要在最后一个参数的类型后面紧跟三个.即可，这时如果传入了多个String类型的参数，这些参数将以数组的形式存在books中。

#### 递归

我讨厌递归



#### 方法重载

如果同一个类里面有两个名字一致的方法，但是他们的形参列表不同，那么调用方法的时候系统将自动匹配，调用不同的方法。

记清楚要求，同一个类，方法名字一致，参数列表不同，至于修饰符，返回值什么的完全没有要求

然后还要注意一个可变长度的形参的问题，例如有两个方法，一个的形参是一个String，另一个是一个长度可变的String，那么当你传入一个String的时候，系统将优先调用形参是一个String的方法。虽然这样也是可以的，但是严重不推荐使用参数长度可变的方法重载，尤其是形参列表除了长度不同别无二致的。

#### 关于static

static到底有什么用？

我们来考虑一下，程序的唯一入口是修饰符为static的main方法，而static不能调用非static成员，这意味着，如果你如果把一个成员标记为非static，那么在类的本体内，我们将永远无法直接运行，使用这个变量，要想使用，我们必须创建一个实例，所以书上的说法十分准确，static代表这是一个类成员，没有static则是实例成员

但是仅仅如此吗？static还有静态的意思，这意味着如果一个成员如果被标记为static，那么任何一个实例对该成员的修改将直接映射，影响到类的本体，以后创建的任何新的实例都会受到影响。

举例来说，如果类的定义里面有一个`static int x = 10;`，这时，我们创建一个实例`test`，那么当我们做这样的操作之后`test.x = 100;`，以后再创建新的实例如`t2`，那么`t2.x`的初始值就将被改变为`100`

不仅如此，static的影响力更大，从内存的角度来讲，同一个类的不同实例的非static成员在内存中处于不同的位置，而同一个类的不同实例的static成员与类本体共同在内存里占有相同的一块位置，换句话说一个实例的修改会扩散到所有实例，无论是之前还是之后创建的。

但是非static类型的就不会这样，实例对非静态成员的修改将不对类本体产生任何影响

#### 作用域

据我现在的观察，java真的很个性，在python和c++里面，作用域都是有一个先后高低之分的，例如

#### 局部变量

在java里面，局部变量的作用域将被控制在代码块中，例如你将一段代码使用{}括起来，那么这就是一个代码块，出了代码块就不能访问内部的局部变量；一如既往for循环也是一个代码块`for(int nats=1;nats<5;nats++)`这里面的nats出了for就没了

我们该怎么使用变量呢？明显可以观察出类属性范围最大，其次是方法的局部变量，然后是代码块局部变量，我们应该尽量缩小变量的作用域，换句话说，我们应该尽量使用代码块局部变量。





#### 封装与隐藏

总之，想要控制外界对于类的访问，使用，权限

##### 访问控制符

访问控制符有三个：`private protected public`，事实上我们可以不加控制符，那么其实可以称作default，所以可以说是一共有四个访问控制级别

-   private，如果一个类成员被private修饰，那么这个成员只能在类内部被访问
-   default，可以被包内的其他类可以访问
-   protected，即可以被同一个包访问，也可以被不同包内的子类访问，一般而言，使用protected修饰的方法，是希望子类重写的
-   public，可以被任何类访问，无论在不在一个包内，无论是不是子类，这是最宽松的访问控制

注意这里所说的访问指的就是调用，例如private不能在类外被访问，指的就是在类外，你使用常规手段是无法调用这个成员的

你只能在类里面提供public的修改方法，访问方法



#### 包，导入，路径与目录管理

说句实话，我觉得这里的包与路径目录管理十分之恶心，我相当讨厌，花费了大概1个小时，反复试验才大概得到了一点结论，并未彻底满意

首先，我们考虑一下一个项目的合理目录，要我说的话，我也知道如果把源码和class文件分离会比较好，尤其是class文件是一些包的时候。

那么，按照书上给出的建议，我们应该在根目录下建立两个文件夹，例如一个叫classes，一个叫src，前者专门存包文件，后者专门存储源码，然后两个文件夹下应该同时维持着相同名字的项目名，例如名字叫做stan的项目，然后在下面分别存放.class文件和.java文件，所以路径应该是`some path/classes/stan/test.class`和`some path/src/stan/test.java`，但是现在的问题是，这样的路径会给我工作造成极大的困扰和麻烦

##### 创建一个包

我们要如何生成一个包文件（包里面放的是class），它需要满足两点：首选产生这个class的java文件的第一个非注释行必须是这样的`package name`，其次这个class文件实际所处的目录必须与上面写的一致。

这里，我选择了使用命令行来编译和运行java文件，因为Eclipse里面似乎也很麻烦。

例如我们现在在`D://java_script`打开了命令行，位于`D://javascript/src/stan`有一个P.java文件，它是我们打算用来生成包文件的源文件。

我们打算在`D://java_script/class_file/stan`下存储P.class，那么我们的P.java应该是这样的：

~~~java
package class_file.stan;

public class P
{
	public void fun()
	{
		System.out.println("this is class.stan.Test");
	}
}
~~~

然后在命令行输入`javac -d . src/stan/P.class`即可，这里要注意第一个坑，书上面极其坑爹的把顶级包目录的名字取为了class，也就是说他的第一行是这样的`package class.stan`，但是这样并不行，class是关键字

接下来我们成功的将P.class放进了制定的地方，但是接下来我们要在T.java里面引用这个文件，语法为：

`import class_file.stan.P;`

这样我们就可以获取P这个类，但是，只要你的文件不是在`D://java_script`下，你是不可能运行的，因为他会找不到包文件，这时我们必须新建一个环境变量，名字为`CLASSPATH`，注意这个可能已经存在了，那么只需要在其后添加`D://java_script;`即可

但是你以为这样就行了吗？naive，我们必须在T.java所在的目录下打开命令行，使用javac编译产生class文件，然后在class文件所处的目录运行java才行，这就是因为java命令不能指定class文件所在目录，只能运行自己目录下的文件



总之，我已经完全被搞蒙了，书上面说的挺好，清晰划分，结构更准确，但是，我觉得运行更困难，Fuck You！！！这一点东西已经花费了两个小时了，两小时前我就应该休息的。

总之一切问题的所在是，搜寻包的方法不智能，必须要在classpath指定，然后运行的命令也不智能，只能在自己的目录下运行。所以你可能需要不断切换目录，靠！

学艺不精

更新一下，我前一段时间重新处理了python的模块与包管理的部分，总而言之，之后我觉得java的做法没有什么不合理的。

如果你只是想创建一个新的文件，那么只需要把它放在和顶层文件（就是你要真正运行的程序）同一目录下就好，如果你写出了一个不再轻易更改的包，那么就可以把这个包放在一个统一的包路径下，为了告诉java去哪里搜索包，我们需要在CLASSPATH这个环境变量里面设置。没有什么不合理的。并没有可以在顶层文件中提供相对目录穿梭的方法，python也没有。



#### 构造器

前面已经介绍过怎么写一个构造器了，构造器其实就是初始化方法，别的没有什么需要多说的。只提一点：构造器也是可以重载的。并且我们可以在一个构造器里面调用另一个构造器，调用的时候，并不需要使用名字，只需要直接使用this()即可，系统会根据参数数量自动选择使用哪个构造器。

暂时查到的结果是，构造器可以使用任何类型的访问控制修饰符但是不能使用其他修饰符，如static final abstract



#### 继承

集成的关键字是extends，例如一个新的类继承一个父类：

`修饰符 class subclass extends superclass{}`

java规定，一个子类只能有一个直接父类

我们该怎样在子类里面使用父类的成员呢？直接使用就好，不需要创建新类也不需要使用this

##### 重写方法

重写父类的方法需要满足名字相同，参数相同，子类返回值小于等于父类？？抛出的异常也应该小于等于父类，而子类的方位权限应该大于等于父类。

特别的，你重写的方法必须同时是static或者同时不是。

我们可以使用super获得父类的引用，也就可以获得父类的被覆盖方法，但是super和this一样，不能在static方法中使用。

还记得重载吗？我们只要控制参数数量就可以实现方法重载，即使是父类的方法。







##### 调用父类构造器

子类会继承父类的方法，属性。包括构造器，我不知道说构造器被继承了是不是合理，但从运行上面来说，子类如果继承了父类，那么在子类使用过程中，父类的构造器总会最先运行，所以，如果父类有一个无参数构造器，那么子类不需要做太多的操作，可是如果父类的构造器是有参数的，那么之类就必须显式的调用父类的构造器，并且调用的位置应该是子类构造器的第一行。

总而言之，如果父类只有有参数构造器，那么之类就必须也有构造器，而且在自己构造器的第一行显式调用父类构造器，调用的方式是：`super(args);`

关键，我们还是要理解程序的运行过程，正如在初始块那一部分说的：当有继承的时候，最先调用的总是静态初始块，所以，首先应该是父类静态初始块，然后是子类静态初始块，然后是父类的普通初始块和构造器，然后是之类的普通初始块和构造器。



#### 多态

多态十分之诡异，我并没有看出他有什么用，所以几乎就是跳过了。

总之，如果你定义一个父类类型的变量，然后赋给他一个子类的值，那么就会出现多态。



#### 继承与组合

呃，我不知道该怎么说，这是一个很重要的问题，也大概是很容易忽略的问题，书中有说子类不能获得父类的构造器，但是当你在创建一个子类的时候，会首先执行父类的构造器。这个矛盾吗？或者说前面一句话指的是我们不能通过方法名直接调用父类的构造器？

忽略这些，说一个必须注意的点，如果父类的构造器会执行他自己的一个方法，然后这个方法又被子类重写了，那么，当你在子类里创建一个子类的实例的时候，他会首先调用父类的构造器，但是这个构造器调用的方法将不再是父类的方法，而是被子类重写的方法。这在警示我们，==不要在父类的构造方法中调用可能会被子类重写的方法。==

但是，并不用担心，如你所想，如果你是直接创建了一个父类，那么并不会受到影响。



鉴于集成的这种破坏性，我们可以选择使用组合的方法来复用代码

##### 组合复用

来考虑一下如何组合，首先你要明白，并没有新的关键字来完成这一个任务

哈哈哈，起这么高级的名字，简直就是搞笑，其实就是在新的类里面定义一个属性，这个属性就是原来的类



#### 初始化代码块

初始化块很神奇，他其实是类的第四种成员，并且他和构造器的类型一致，也是初始化操作，并且系统会优先执行初始块，然后才是构造器，可以有多个初始块，系统会按顺序执行

初始块的结构是这样的

~~~java
修饰符 {
  初始块代码
}
~~~

修饰符可以没有，有的话只能是static

里面的代码可以是任何代码

我们无法在其他地方调用初始块，拥有调用权限的只有初始的时候自动调用

##### 考虑一下

对于一个类，我们在方法之外为他定义一个属性，并赋值，那么我们可以直接使用，这意味着这些位于方法外的属性也有类似于初始块的性质，于是两者就会有一些冲突，例如初始块和方法外属性同时设置了一个属性的值，那么最终是谁起作用呢？答案是方法外属性，应为初始块总是会被首先执行的，因此被覆盖了。



##### 与构造器对比

其实呢，从上面也可以看出，如果初始化代码不需要参数的话，代码块必构造器更好用，更安全



##### 关于静态初始块与运行特点

如果用static修饰初始块，那么初始块将不能调用非静态属性

并且静态初始块会绝对优先执行，当类被加载到内存的时候就会执行，与之对比普通初始块只有在实例化的时候才会被执行。并且静态初始块只有被加载到内存的时候才会被执行，换句话说只有一次，之后的实例化的时候不会再被执行，而普通的每次实例化都执行一次

并且呢，继承的时候所有的初始化内容都是自顶向下执行的，在多重继承的前提下，第一次实例化，将会显示父类的父类的静态初始化，然后是父类静态，然后是子类静态，紧接着是父类的父类普通和构造器，父类的普通与构造器，子类的普通与构造器

以后再实例化，就没有静态的那一段了



### 类（下）

#### 基本数据类型与包装类

说是存在这样的情况（反正我没见过），方法要求我们提供一个类的类型的变量，但需要的值却是基本类型。这时我们面临的问题其实是在这样一个纯粹的面向对象的语言中却存在着不是类的基本类型的问题，因而java里面提供了一种叫做包装类的东西，每个基本数据类型都对应了一个自己的包装类，并且除了int和char之外，其余6个基本类型对应的包装类都是首字母大写即可：

| 基本数据类型 | 包装类       |
| ------ | --------- |
| byte   | Byte      |
| short  | Short     |
| int    | Integer   |
| long   | Long      |
| float  | Float     |
| double | Double    |
| boolea | Boolean   |
| char   | Character |

如何使用？

~~~java
int a = 10;
Integer aa = new Integer(a);

int b = aa.intValue();
~~~

总之包装为包装类，利用的是构造器，从包装类里取出基本数据类型利用的是xxxValue()方法，这里的xxx就是基本类型名字

##### 新方法

在JDK1.5之后，为了简化上述繁琐步骤，提供了称之为自动装箱，自动拆箱的功能，现在包装不需要构造器，可以直接赋值，拆包装也不需要调用方法，也可以直接赋值

~~~java
Integer A = 10;
int a = A;
~~~

##### 与字符串的转换

如果不是应用的话，我其实很讨厌这个。我现在也用不上，只是稍微记一下吧

将特定类型的字符串解析为相应的基本类型使用包装类的parseXxx()方法，Xxx是基本类型的首字母大写产生的（没有特例）

~~~java
String s = "123";
int t = Integer.parseInt(s);
String ss = String.valueOf(t);
~~~

将基本类型转化为字符串，要使用String的valueOf方法，其实并用不着，更简单的方法就是直接使用+就行了，如`String ss = 10 + "";`



#### 对象的处理

##### 打印

在java里面最基本的类是Object，所有的类都是它的子类，Object类提供了一个叫做toString()的方法，这个方法控制了如何将类描述为一个字符串，当一切需要的时候，系统便会自动调用这个方法，这个默认的方法的返回值是：`类名@hashCode`

考虑一下python的语法，你可以明白这个方法意味着什么？它意味着我们可以直接打印一个类，也可以把它和一个字符串做连接运算。

~~~java
father x = new father();
String xx = x + "haha";
System.out.println(x);
System.out.println(xx);
/**
father@15db9742
father@15db9742haha
**/
~~~

是的你没有想错，我们完全可以重写这个方法，实现定制的自我描述，这个就不再多说了（修饰符是public，返回值String，没有参数）

##### 相等

在java里面，判断相等有两个方法，`==`或者`equals()`方法，`==`要求十分严格，对于基本数据类型，只要值相等即可，并不要求类型一直，但是对于类，两个变量相等必须指向同一个对象或者说是实例才会认定为相等。但是equals()方法不一样，这里不要多想，equals方法与`==`并不挂钩。

equals()方法来自于Object类，对于String，它定制了这个方法，只要字符串的值一样，就会认定相等。对于其他的类，我们可以任意定制。

equals方法修饰符为public，返回值boolean，接收的参数为Object类型的一个变量



#### 类成员

还是之前说的，如果一个成员使用了static修饰，那么这个成员将成为类成员，否则叫做实例成员，所谓类成员即只占有一块内存，类本体和所有的实例的该成员都指向相同的地址，一个的改变会影响到整体。实例成员则是每个实例的成员指向不同的内存。所以说，实际上python中的oop，默认所有的都是实例成员。

实际上java的类可以有6种成员，初始化块，构造器，属性，方法，内部类，枚举类，我们已经介绍过前4种，在所有的6种之中，只有构造器不能被static修饰，也即无法成为类成员

##### 单例类

之前我们看到的所有构造器的访问控制符都使用了public，如果你不写构造器，系统会自动提供一个。所以可以想象，如果我们写一个空的构造器，并且将其设置为private，那么这将意味着永远无法使用构造器创建一个实例。

这样也意味着，我们可以自行写一个方法，通过这个方法来创建实例，然后我们就可以具有超级大的控制权，产生我们想要的效果。例如所谓单例类，也即永远只能存在至多一个该类的实例。

那么该怎么实现呢？我们只需要在类内部创建一个属性，存储我们实例，然后根据条件决定是创建这个实例，还是返回这个实例：

~~~java


public class Learn
{  
	static int a = 10;
	{
		this.a = 50;
	}
    public static void main(String[] args) 
    {
    	father a = father.creat();
    	father b = father.creat();
    	System.out.println(a == b);
  	
    }
    
}

class father
{
	private father(){}
	
	private static father only_one;
	
	public static father creat()
	{
		if(only_one==null)
		{
			only_one = new father();
		}
		return only_one;
	}
}
~~~

注意这里面的修饰符等细节



#### final修饰符

final可以用来修饰类，变量（不单是属性），方法

final修饰意味着不可改变

##### 修饰变量

变量也可以分为两种，属性或者局部变量

当修饰属性的时候可以分为类属性或者实例属性，再综合一下静态初始块，普通初始块，构造器，方法外属性初始化，然后考虑到final不可更改初始值的特点，以及上面几个东西的运行特点，我们可以说：

对于使用final修饰的类属性，我们要么在方法外初始化的时候就设定初始值，要么在静态初始块中初始化，除此之外都不行

对于实例属性，我们可以选择普通初始块，构造器，或者方法外



修饰局部变量的时候一样，只能赋值一次，可以不显式初始化，例如作为形参

##### 修饰类型

一样的，不能重新赋值，但是对于构造类型如数组，或者引用类型如类，我们可以改变其成员，例如更改某一个数组元素的值，或者更改类的某个属性，但是我们不能直接改变整体



##### 修饰方法

关于方法，我们要认真考虑一下，对于一个方法，其操作有访问，重写，重载这么几种

如果我们使用访问控制符修饰，例如private，那么意味着子类将无法访问这个方法，但是这并不能阻止我们重写这个方法

而final可以阻值子类重写方法，如果有final修饰，那么将无法重写，编译会报错

但是接下来就神奇了，final的确不能重写，但是如果父类的方法同时被private修饰了的话，我们就可以继续重写了。使用我上面的解释方法是无法解释的。

正确的说法是，除了我说的这几种方法的操作，应该说还有一种叫新建，private意味着不能访问，也就不存在重写了，你做的实际是新建，如果有private和final的话，这意味着二者作用相互覆盖，final让我们不能重写，private让子类根本无法见到这个方法，于是你再写就会被认为是新建。

##### final类

如果用final来修饰类，那么类将无法具有子类，保证类不会被继承

##### 不可变类

所谓不可变类指的是创建类的实例之后，市里的属性不可改变。这里我们主要使用private final修饰属性

其他的其实里面的细节很复杂，需要仔细考虑，小心设计和包装，才能保证类不会被改变。这里就不再详谈了。

还有用于储存的缓存池，也不再说了。



#### 抽象类

怎么说呢？这种类想要实现的是这样的效果：父类定义了一系列的方法，但是都没有实现，留给子类来实现。

一个抽象类可以没有抽象方法，但是一旦具有一个抽象方法，这个类就必须被定义为抽象类。

抽象类只需要使用abstract修饰即可，而抽象方法也是使用这个进行修饰，并且方法体必须为空，花括号之外还要加分号

如果我们将一个类定义为抽象类，那么意味着这个类只有一种用法：被继承。他是无法使用new来创建实例的。

但是抽象类可以包含所有6种类型的成员。我们前面已经说过继承时，代码的运行特点了，首先各父类的初始块会运行，之后是构造器，所以抽象类的初始块，构造器对于子类还是有用的。

如果一个子类继承了抽象类，但是没有把它的所有抽象方法都实现的话，那么这个子类将也必须被定义为抽象类。

想成为普通类，就必须实现所有抽象方法。

final与abstract是冲突的，因为前者不能重写。

同时static和final也不能同时修饰方法

private和abstract也不能同时使用



#### 更彻底的抽象：接口

抽象类是一个模板，但是他可以包含非抽象方法。

接口类不一样，他的所有方法都是抽象方法。

##### 定义

接口使用一个新的关键字取代class，即：interface

~~~java
修饰符 interface Name extends 父接口1,父接口2....
{
    
}
~~~

接口的修饰符只能选择public或者没有，也就是说只能控制包访问权限

接口和类不同，可以继承多个父接口，但是他只能继承接口，不能继承类

接口内部不能包含初始块，构造器，可以包含其它的。

因为接口成员本来就是为了继承的，所以成员的访问控制符只能选择没有或者public

接口内部的属性将被默认定义为static final，这意味着是常量。

而接口内部的方法将全都是抽象方法，无论你是否写abstract，并且默认public，也因此不能是static

##### 使用

接口无法创建实例，只能通过继承工作。

特别的一个类也可以继承多个接口，但是这个继承不是使用extends，而是implements，可以同时继承类和接口

同样的类继承了接口之后，就必须实现所有接口的抽象方法，否则只能定义为抽象类。

##### 面向接口编程

很高级的样子，我似乎暂时也用不上，就先跳过吧



#### 内部类

第五种成员

内部类创建在类的内部，嵌套。内部类封装的更好。

具有一些特点，其他的类是无权访问内部类的。外部类也不能访问内部类的属性（这里的外部类指的就是包装内部类的那个类），但是内部类对于外部类来说类似于成员，是可以访问外部类的数据的。



内部类有蛮多分类的：因为内部类可以被定义在类的任何位置，所以当然也可以定义在方法内，如果是这样将成为局部内部类，在方法外的话就是成员内部类，我们常见的就是成员内部类。此外还有一个匿名内部类，暂时不说。

对于成员内部类，根据是否使用static修饰可以分为静态内部类和非静态内部类。

##### 非静态内部类

对于非静态内部类，在内部类里，可以正常使用外部类的属性和方法。但在内部类内访问一个变量的时候将会首先从自己的局部变量找起，然后是自己的属性，然后是外部类的属性，然后是报错。

但是，如果遇到同名的情况下，我们可以指定，name是访问局部，this.name访问自己的属性，OutClassName.this.name是访问外部类的属性

并且因为内部类是成员般的存在，所以也可以访问外部类的private成员

但是外部类想访问内部类的成员，就必须通过创建实例来实现。

这里静态不能访问非静态的规则依然存在，所以外部类的静态成员完全无法访问非静态内部类。

另外java规定非静态内部类内不能有任何静态成员。

这里要考虑一下规则，细心一点：静态无法访问非静态，那么如何才能突破这个限制呢？难道外部类的静态成员就无法访问非静态内部类了？我们还有实例化这一工具，有了实例化，一切都可以通过调用实例方法，属性实现。

##### 静态内部类

还是静态不可以访问非静态在起作用，如果内部类被定义为静态类，那么他将不能访问外部类的非静态成员。

即便静态类内部的非静态方法也依旧不能访问外部类的非静态成员。

外部类可以通过类名调用静态内部类的成员，再不济实例化总是可以的。

##### 使用

只要内部类不被定义为private，那么我们就可以在外部类的外部以外部类的成员的身份，访问内部类。

但是这一段真的极其绕。

###### 在外部类的外部使用静态内部类

例如，我们要在外部类的外部创建一个静态内部类的实例，那么我们要解决两个问题：类型怎么写？实例怎么得到？

首先创建一个静态内部类类型的变量：OutClass.InnerClass name;

然后拿到一个实例，考虑一下，一个非静态成员是必须通过实例来访问的，因为他是实例成员嘛，所以我们不能简单的使用OutClass.这样的形式来访问，而是必须先创建一个外部类实例，然后再创建内部类实例：

~~~java
//加入外部类叫做Out，内部类叫做In
Out a1 = new Out();
Out.In a2;
a2 = a1.new In();
~~~

我知道最后一行比较难懂，可以把`new In()`看作整体，先创建一个内部类实例，然后这个实例是依附于外部类实例的，只需要把它返回就好了

所以，上述步骤可以合并在一起`Out.In a2 = new Out.new In();`

对于上述代码还是可以分段理解，把`new out`看成一段，`new In()`看成一段

此外还可以让外部类的外部的类继承内部类，但是我感觉这就是吃饱撑了

###### 在外部类外使用静态内部类

因为静态的特点，我们使用的时候要比非静态简单一点，例如不需要创建实例就可以直接访问成员。

`Out.In a = new Out.In();`

继承和上面一样不写了。



##### 局部内部类

如上所述，定义在方法内的就是局部内部类

局部内部类只在方法内有效，因而访问控制符，static都是不存在的。所有操作都要在方法内进行。



##### 匿名内部类

像匿名函数一样，为便捷而生。

完了完了，我已经很难集中注意力了，先跳过

匿名内部类必须要继承一个父类，或者实现一个接口，当最多只能继承一个父类，或实现一个接口

没有类名，所以没有构造器，可以有初始块。

上述所谓实现一个接口指的是将一个已有的接口类做一个实现，而不是创建一个接口类。继承一个父类指的也不是extends，而是实现父类的构造器。

因为匿名内部类直接就被实例化了，所以他绝对不能是抽象类，因此，如果他继承了抽象类或者接口，就必须实现所有抽象方法。

###### 意义？

我感觉匿名内部类的意义很寥寥，如果它是继承了一个接口，那么还是可以理解的，因为可能在某一个方法里面，我们需要一个接口的实例，但是接口又无法创建实例，我们必须继承，可是我们只需要使用一次，很没用，这个时候就是匿名内部类可以起作用的时候。换句话说我们只能在匿名内部类里面实现所有抽象方法，然后把实例直接传递给某一个方法，而不能将这个实例赋给某个变量，因为类型名是没有办法写的。

可是，当匿名内部类继承父类的时候，我就感觉很鸡肋了，因为所谓继承大多是为了扩展，或者实现抽象方法，可是，有一个十分十分重要的点是，我们可以在匿名内部类里面实现父类，或者父接口没有的方法，但是写了也是白写，外面是绝对无法调用的，如果强制调用，就会编译错误

总而言之，匿名内部类必须继承父类，或者接口，但是也只有在继承抽象父类，或者接口的时候才有意义，不要实现父类没有的方法，没有意义。

一般情况下，我们是直接将匿名类的实例传入某个方法的，而不会真的创建一个变量，但继承父类的时候，我们其实也可以创建一个变量，这时变量的类型就是父类的类型。

至于代码，我就稍微贴一下吧：

~~~java
public class Learn
{  
	static void test(father t)
	{
		t.my();
	}
	public static void main(String[] args)
	{
		father w = new father("this is stan")
		{
			public void say()
			{
				System.out.println("I am anonymous class test");
			}
		};
		
		
		
		test(new father("this is stan")
				{
					public void say()
					{
						System.out.println("I am anonymous class test");
					}
				});	
	}
    
}

class father
{
	String name;
	public father(String s)
	{
		this.name = s;
	}
	public void my()
	{
		System.out.println(name);
	}
}
~~~

这里是一个继承父类的，主要看的是用法，写的格式，我还实现了父类没有的say方法，但是这是没效的，因为谁也用不了。



##### 闭包与回调

跳过跳过

呃，我看了书上给出的讲解代码，但是感觉很诡异，似乎有点白花力气的感觉，他只是通过一些手段，返回了一个非静态内部类的引用而已。

这里注意回去思考一下，我可以使用接口类型定义一个实例吗？我前面似乎认为不行，但是答案应该是可以的。



#### 枚举类

最后一种。实例有限且固定的类称为枚举类

其实我们是可以手动实现枚举类的

我们只需要使用private将类构造器隐藏，让外部无法使用，然后把直接在类内生成所有可能的实例，把这些实例定义为public static final，提供一个特定的方法，接收一个参数，根据参数返回固定的实例。

但是自定义十分之麻烦，并且会有一些缺陷。于是在JDK1.5里，提供了一个新的关键字，enum，用于定义枚举类。枚举类并不继承自Object，而是一个叫做Enum的基类。

他的构造器只能使用private修饰，如果省略，默认也是private

所有实例也必须显式列出，系统会自动定义实例为public static final，可以自己不写。

提供了一个values方法，可以遍历所有枚举值。

枚举类也可以是public，虽然他不使用class关键字而是enum，但是他也必须满足一个文件只能有一个public类

枚举类的定义可能比你想的还要简单：

~~~java
public enum Season
{
    spring,summer,fall,winter;
}
~~~

上面列出的就是所有的四个实例，Season.values()会是一个可迭代的方法，将依次返回四个实例

~~~java
public class Learn
{  
	
	public static void main(String[] args)
	{
		season first = season.valueOf("spring");
		System.out.println(first.name);
		
		
	}
    
}

enum season
{
	spring("stan"),summer("han");
	public final String name;
	season(String a)
	{
		this.name= a;
	}
}
~~~

这里我给出了一段代码，示范我们如何获取指定的实例，使用的就是类的valueOf方法，但是要求必须准确地传入字符串形式的实例的名字。

同时我也示范了如何使用构造器，这里必须要注意，我们必须把实例定义在最前面，如果你试图把name的声明写在实例之前，那么就会报错。注意怎么创建带有构造器的枚举类的实例。

##### 接口

枚举类也可以继承接口

~~~java
public class Learn
{  
	
	public static void main(String[] args)
	{
		season first = season.valueOf("spring");
		System.out.println(first.name);
		first.info();
		
		
	}
    
}

enum season implements hello
{
	spring("stan")
	{
		public void info()
		{
			System.out.println("this is spring");
		}
	},
	summer("han")
	{
		public void info()
		{
			System.out.println("this is summer");
		}		
	};
	public final String name;
	season(String a)
	{
		this.name= a;
	}
}


interface hello
{
	void info();
}



~~~

继承了接口之后，我们固然可以直接重写方法，但是这样的话，所有的实例都共享完全一致的方法，如果我们想实现定制化的，应该怎么办？

实现方法就是上面所展示的，虽然看起来有点诡异，但是这里实际上是匿名内部类。

呃，其实到这里之后，我已经基本上完全记不住上述所有不同的类对修饰符都有什么要求了，乱写，根本就是。

##### 包含抽象方法

可以为枚举类定义一个抽象方法，然后交由各个实例以匿名内部类的形式实现。

写法，我这里就不记录了，自己看书吧。



啊啊啊，终于补完了。



#### 垃圾回收与对象

系统会自动进行垃圾回收

系统对垃圾回收之前，总是会先调用它的finalize方法。

注意只是先调用，而不是使用这个方法完成垃圾回收，所以我们可以重写这个方法，搞一些通知之类的

我们可以使用System.gc()或者Runtime.getRuntime().gc()两个方法来强制系统进行垃圾回收，但是本质上这两个方法只是通知系统进行回收，系统会不会马上回收依旧不一定，大部分时间还是会起效的。

我们不要想在finalize()上面做太多的手脚，也不要尝试自行调用这个方法，更不要把它当成一定会被调用的方法。

##### 引用类型

java语言中，引用分四个等级，常见的创建实例，赋给引用变量是强引用，这时对象处于激活状态，绝对不会被回收

另外还有软引用，虚引用，弱引用三种，这三种需要借助java.lang.ref下面的SoftReference，PhantomReference，WeakReference三个类实现

软引用可能会被系统回收，当内存不足时

弱引用类似软引用，但级别更低，只要系统的垃圾回收工作，无论内存足不足，他都会被回收

虚引用类似于完全没有引用，对象都不会有感觉，主要用于跟踪对象被垃圾回收的状态，不能单独使用，必须与引用队列配合

三个类都有一个get方法，可以获得被他们引用的对象

引用队列来自于java.lang.ref.ReferenceQueue类

感觉这一部分用不上，先到这



#### 修饰符的应用范围

看表，有一些没有说，后面会提到。

![修饰符](images\修饰符.PNG)



#### 使用JAR文件

JAR文件意思为java档案文件，是一种压缩文件，兼容zip。开发中可能最终会产生一个很大的类文件群体，此时只需打包为jar文件，用户只要将这个文件加入classpath中，即可使用

jar文件是可以包装整个目录树的，我们只需要把它添加到类路径中就可以像引用普通文件的方式使用路径引用

创建一个jar文件：`jar cf test.jar test`将整个test目录压缩

查看jar包内容：`jar tf test.jar`

更详细查看：`jar tvf test.jar`

解压jar：`jar xf test.jar`

更新jar文件：`jar uf test.jar Hello.class`更新test里面的Hello文件，有的话替换，没有生成

##### 创建可执行jar包

这个意思是把可执行文件封装为jar，对于已经安装了JRE的用户，只需要双击JAR包即可执行

但是怎么创建一个可执行JAR包呢？关键在于让程序知道谁是主类，这个是写在jar包的清单文件中的，但是这个清单文件的内容要控制的话只能在生成的时候控制，可是生成的时候要想添加就必须先把内容写在文本文件中，读入。这里设计得很恶心。并且文件格式有严格要求，必须十分小心。这里暂时略过。





### Java集合

这是什么鬼？

数组是不是用起来很烦？想不想念python里面的列表？Java也提供了类似的东西。

Java的集合类是一个工具类，大概分为三种：Set，List，Map。第一个用于存储无序的，并且元素不可重复的集合，第二个是有序可重复的，与数组的区别就是长度可变。第三个类似于字典

呃，还有用Queue吗？

上述几个都没有你想的那么简单，每一个都是一个接口。

要注意这些集合里面只能存储对象，不支持基本类型。

集合类并不是一个两个类，而是相当多的接口的集合，这些接口通过继承构成了继承树

![第一个继承树](images\继承树1.PNG)

![第二个继承树](images\继承树2.PNG)

从上面可以看到，这是存在两个继承体系的，第一个继承树的父接口是Collection，下面产生了List，Set，Queue，但是这三个也有巨多的类型，我们最常用的是HashSet，ArrayList和HashMap

#### Collection与Iterator

Collection接口是list，set，queue的父接口。它里面定义了很多方法，这些方法可以操作这三种集合。

这里介绍一些常用的方法：

-   boolean add(Object o):添加
-   boolean addAll(Collection c)：将C整个加入
-   void clear():清空
-   boolean contains(Object O):检测O是否存在于集合中
-   boolean containsAll(Collection C)：检测是不是子集
-   boolean isEmpty()：检测是否为空
-   Iterator interator()：返回这个集合的可迭代对象
-   boolean remove(Object o) :移除
-   boolean removeAll(Collection c):
-   boolean retainAll(Collection c) :把集合删到剩下的元素c都有
-   int size()：大小
-   Object[] toArray():转换为数组

应用示例：

~~~java
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;


public class Learn
{  
	
	public static void main(String[] args)
	{
		Collection c = new ArrayList();
		c.add("stan");
		c.add(1);
		hello t = new hello();
		c.add(t);
		Collection cc = new HashSet();
		cc.add("stan");
		System.out.println("c完全包含了cc?:"+c.containsAll(cc));
		System.out.println(c);
		
	}
    
}


class hello
{
	public String toString()
	{
		return "this is class hello";
	}
}
~~~

应该从这个例子里看到什么？首先，所有的集合类都存在于另外的包里面，我们必须先导入。

然后，如何定义一个集合类，类型应该怎么写，我们可以在集合类里面添加任何元素，一个字符串，一个类。这里注意前面说了是不支持基本类型的，但是记得前面说的自动装箱吗？这里就是自动装箱，是不是很厉害。

然后我们如何使用前面给出的方法。接下来虽然HashSet和ArrayList不是一样的类，但是两个集合都被定义为了最基础的Collection类，所以，我们依旧可以检测包含关系，接下来注意输出，我们是可以直接输出集合的，这说明他重写了toString方法，我们也重写了自己的类的这个方法，实现了自我描述。

##### Iterator与遍历

Iterator接口的作用就是遍历Collection里面的元素。称之迭代器

它提供了三个方法：

-   boolean hasNext():是否还有未被遍历的元素
-   Object next():给出下一个
-   void remove():从集合里删除上一次next返回的元素

~~~java
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;


public class Learn
{  
	
	public static void main(String[] args)
	{
		Collection c = new HashSet();
		c.add("stan");
		c.add(1);
		c.add("han");
		c.add("han1");

		Iterator it = c.iterator();
		while(it.hasNext())
		{
			String h = ""+it.next();
			System.out.println(h);
			if(h.equals("han"))
			{
				it.remove();
			}
		}
		System.out.println(c);
		
	}
    
}
~~~

这里展示了如何创建Iterator接口，如何使用，以及注意一下我们想删除的时候是通过在迭代器里面删除来实现的，而不删除原集合

还有，当我尝试使用强制类型转换将迭代元素转换为String时，报错了，改成`""+`才成功

注意，不要在迭代进行中直接动手改变原集合



##### foreach

因为集合本身就是可迭代的，所以我们完全可以直接使用`for(Object o : c)`来进行迭代

但是这时候，不能进行删除操作



#### Set接口

下面介绍Set

我们将介绍Set接口里面的三个:HashSet,TreeSet,EnumSet

已经说过了，Set集合是不允许元素重复的，他判断元素重复的方法实际上就是调用的元素的equals方法，因此这个是我们可以控制的

##### HashSet

这是最常使用的Set类，从名字其实可以看出，他使用了hash来存储元素。

HashSet判断两个元素相等需要满足equals方法相等，同时hashCode方法也要返回值一致。每个Object类都有hashCode方法，我们也可以重写。

我们需要注意不要破坏一致性，不要随意的重写这些方法，如果重写了equals，让两个元素不等，但是没有重写hashCode，而两者的hashCode又一致，那么系统就要使用其他方法存储元素，会导致性能下降。

接下来讲了很多关于重写hashcode的时候应该遵循的原则，我就不说了，因为一般我不会重写的。

还有LinkedHashSet子类，他使用了链表维护元素次序。



##### TreeSet

从继承树可以看出TreeSet来自SortedSet，这个集合的特点是采用了排序。

既然是排序，那么就必然有排序算法，TreeSet提供了两种排序法，默认是自然排序，采用的是红黑树（？），然后进行升序排列。第二种就是我们可以自定义的定制排序

它提供了几个额外的方法：

-   Comparator comparator()，给出现在的排序器，如返回null，代表采用了自然排序
-   Object first()，返回第一个元素
-   Object last()
-   Object lower(Object e),返回比制定元素小的元素中最大的那个
-   Object higher(Object e)
-   SortedSet subSet(fromElement,toElement)，返回集合的子集，[fromelement，toelement)
-   SortedSet headSet(toElement)，小于制定元素的集合
-   SortedSet tailSet(fromElement)，大于等于指定元素的集合

要注意，当你把元素放进集合的时候系统就已经进行了排序，所以上述方法其实很简单



###### 自然排序

自然排序就是利用元素的compareTo(Object obj)来比较元素的大小关系的，然后升序

默认的compareTo方法会返回一个整数值，obj1.compareTo(obj2)，0代表相等，正数代表obj1比obj2大，负数代表小

常用类已经自行实现了这个方法，但是自定义类需要自己实现，如果没有的话就会抛出异常

因为这一点，我们常常存储的都是同一个类的实例

另外因为这个集合和元素自身密切相关，所以很忌讳当元素位于其中的时候改变元素属性，甚至无法从集合中删除



###### 定制排序

想要定制排序的话，我们应该在创建TreeSet集合的时候传入一个比较器实例，这个实例应该继承了Comparator接口，这个接口只包含了一个int compare(T o1,T o2)方法

这个时候最好的就是使用匿名内部类。

~~~java
import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;
import java.util.HashSet;
import java.util.Iterator;
import java.util.TreeSet;


public class Learn
{  
	
	public static void main(String[] args)
	{
		Collection c = new TreeSet(new Comparator()
				{
					public int compare(Object a1,Object a2)
					{
						hello m1 = (hello)a1;
						hello m2 = (hello)a2;
						if(m1.name>m2.name)
							return -1;
						else if(m1.name<m2.name)
							return 1;
						else
							return 0;
					}
				});
		c.add(new hello(5));
		c.add(new hello(10));
		c.add(new hello(3));
		c.add(new hello(-1));
		System.out.println(c);
		
	}
    
}


class hello
{
	int name;
	public String toString()
	{
		return ""+name;
	}
	public hello(int a)
	{
		this.name = a;
	}
}
~~~

这里要注意一个一直都存在的问题，如果你传入的参数指定了一个类，那么只要这个类没有某个属性，你就不能引用，即便你使用某种方法为之添加了这个属性，例如继承

所以，就是像上面一样，我们干脆就指定传入的参数就是hello类最好，不然还要强制转换



##### EnumSet

枚举类集合类

我不想多说了，用到的时候再学吧



#### List接口

list是有顺序的可以通过index来索引

List接口也提供了比Collection更多的方法：

-   void add(int index,Object element)，这是一个被重载的方法，可以提供index，也可以不提供
-   boolean addAll(int index,Collection c)，也可以不提供index，从index起把c里面的元素逐个插入
-   Object get(int index)
-   int indexOf(Object x)，获取元素第一次出现的的索引
-   int lastIndexOf(Object x)，获取x最后一次出现的位置
-   Object remove(int index)，移除指定位置
-   Object set(int index, Object element)，替换
-   List subList(int from,int to)，[from to)

这里我只提醒几点过去没注意的：

我前面几乎都把集合变量的类型写成了Collection，似乎从来没有问题，当然，因为类总是可以接受它的子类，但是代价是这个集合变量成了Collection类型的了，意味着我们无法使用新方法，所以建议以后还是把类型写准确

然后，查询的时候，其实对于集合几乎所有需要判断相等的操作都是调用实例equals方法是，所以，如果是你新建的类，你必须自己写一个equals方法。然后再写这个方法的时候必须要注意，一定要把参数的类型写成Object，然后再强制类型转换，否则查询的时候是不会调用你自己写的判断方法的。

##### listIterator

这里list提供了一个新的方法，返回一个更高级的迭代器，新的迭代器的类型是ListIterator，并在基本的迭代器的基础上提供了三个新的方法：

-   boolean hasPrevious()，是否有上一个
-   Object previous()
-   void add()，把给出的参数作为新元素，插入上一次迭代产生的元素的后面

##### ArrayList与Vector

Vector是在还没有集合框架的时候的一个古老遗存，现在虽然他也已经做过了一些改进，但是已经不太推荐使用了。

这里想要介绍的就是这两个类的capacity属性，因为事实上这两个集合封装着一个动态增长的数组，capacity属性是数组长度。

但是如果我们想写这个属性，就必须调用方法，不能直接写。

-   void ensureCapacity(int size)，把长度增加size
-   void trimToSize()，把长度调整到正好，控制内存

Vector提供了一个Satck子类，实现了栈

##### 固定长度List

呃，算了，先不记录他了，没啥意思



#### Queue接口

模拟了队列

新方法：

-   void add(Object e),加入对尾
-   Object element(),获取对头，但不删除
-   boolean offer(Object e)，其实和add功能一致，只是当队列长度有限时，性能更好
-   Object peek()，获取对头，不删除，空的话，返回null
-   Object poll()，获取对头，删除，空null
-   Object remove，获取对头，删除

呃，所以空的时候返不返回null，还要定义两个吗？

##### LinkedList

这个类很混血，有一个叫Deque的类，是Queue的子类，实现了双向队列，LinkedList继承了他，同时还继承了List，所以她拥有List的随机访问，还拥有双向队列，再加上一些其他的特性它还可以作为栈来使用，所以，很强。即使List，又是双向队列，还可以成为栈

内部使用链表实现

暂时不详细说明了，用了再说吧

##### PriorityQueue

这也是一个队列，但是比较奇葩，他对元素进行了排列，并且当使用peek或者poll时，他返回的是最小的元素

因为涉及了排序，所以呢，也支持自然排序，或者定制，和前面讲的一样



#### Map

就是字典，然后很明显要求key不能一样，方法还是equals

考虑一下python可以知道，key肯定是无序的，所以呢，key的集合就是一个极其类似于Set的存在

因为value是可以重复的，所以事实上value的集合是类似于List的，只是不能再用索引查了

提供的方法：

-   void clear()，清空
-   boolean containsKey(Object key)，是否有这个key
-   boolean containsValue(Object value)
-   Set entrySet()，将它变成一个set，每个元素是一个Map.Entry对象
-   Object get(Object key)，没有null
-   boolean isEmpty()，空不空
-   Set keySet()
-   Object put(Object key,Object value)，若以存在，会被覆盖
-   void putAll(Map a)
-   Object remove(Object key)
-   int size()，对数
-   Collection values()，给出所有的value组成的Collection


前面不是提到了Map.Entry吗？

这是一个只包含了一个键值对的集合，有三个方法

-   Object getKey()，返回key
-   Object getValue()
-   Obejct setValue(value)



##### HashMap与Hashtable实现

和前面的Vector类似，Hashtable也是历史遗存

从名字可以看出来，采用了hash，并且key是不能重复的，所以这个极其类似于HashSet，也是要注意equals方法和hashCode方法

然后检查是否有这个key的时候也是用的equals方法

我不希望在使用Hashtable，所以相关的介绍就不说了

同样不要修改

它们的子类我就不再介绍了

##### SortedMap和TreeMap

前面的set也是这样吧，这里也是Map接口的子接口是SortedMap，然后TreeMap是SortedMap的实现类

他也保证了键值对有序，自然排序和定制排序，这个顺序是按照key来排的

这里的要求更复杂，要求所有的key必须是同一个类，并且他们都要实现一个叫做Comparable的接口，这个接口的方法还是`int compareTo(Object obj)`

如果是定制排序的话就不需要这么复杂了，只要也传入继承了Comparator接口的对象就可以了

关于他提供的一系列根据有序的key来访问键值对的方法，我就不再细说了



##### WeakHashMap实现类

这个和HashMap的区别在于引用的类型，后者是强引用，这个是弱引用，这意味着对于后者，你要同时销毁HashMap对象，才能让key的被引用对象被回收，而这个不用



##### IdentityHashMap

这个只是把比较的方法从equals换成了`==`

不多说

##### EnumMap实现类

呃



#### HashMap与HashSet的性能选项

主要还是关于capacity的

这里只是几个属性：capacity，size，负载因子什么的



#### 集合操作的工具类：Collections

Collections完全是一个工具类，用来完成一些对于Set，List,Map的操作

##### 排序

排序的功能只针对List

-   static void reverse(List list)，反转
-   static void shuffle(List list)，随机排序
-   static void sort(List list)，自然排序，升序
-   static void sort(List list,Comparator c)，定制排序
-   static void swap(List list,int i,int j)，交换
-   static void rotate(List list,int s)，将最后s个元素整体平移到最前面



##### 查找，替换

-   static int binarySearch(List list,Object value)，要求输入一个有序的list，然后给定要查找的元素，会使用二分查找进行查找，返回索引
-   static Object max(Collection c),根据自然排序，返回最大的元素
-   static Object max(Collection c,Comparator cc)
-   static Object min(Collection c)
-   static Object min(Collection c,Comparator cc)
-   static void fill(List list,Object obj)，使用obj替换所有
-   static int frequency(Collection c,Object obj),c里面有几个obj
-   static int indexOfSubList(List source,List aim)
-   static int lastIndexOfSubList(List source,List aim)
-   static boolean raplaceAll(List list,Object old,Object newone)，使用newone替代所有的old



##### 同步控制

推荐的是HashSet,ArrayLsit,HashMap，但是他们都是线程不安全的，超过一个线程访问就会出错，为了解决，我们可以使用Collections.synchronizedXxx来包装，它会返回指定集合对象的同步对象

~~~java
Collection c = Collections.synchronizedCollection(new ArrayList());
List b = Collections.synchronizedList(new ArrayList());
Set s = Collections.synchronizedSet(new HashSet());
Map m = Collections.synchronizedMap(new HashMap());
~~~



##### 不可变集合

呃

Collections.emptyXxx

Collections.singletoXxx

Collections.unmodifiableXxx



#### Enumeration

这是古老版本的Iterator，建议弃用



好累，终于搞定了一章

### 泛型

首先必须要说的就是之前从来没有注意到的一点，集合是可以存储各种类型的，所以，事实上，他会忽略存储的元素的类型，也就是说，从集合里面get的返回值每一个都是Object类型的，我们可能会需要自行进行强制类型转换，也正因为如此i，如果一不小心存入了类型不一致的元素，就可能会导致转换错误。

我们可以手动包装一下一个集合，然后自定义一个add方法，只接受一种类型的参数，从而实现控制类型。

虽然有效，但是这种方法很是繁琐，意味着我们要创建大量的子类。

于是，现在引入了参数化类型，可以在创建的时候就制定集合的类型，参数化类型即所谓泛型

形式很简单：

~~~java
		List<String> c = new ArrayList<String>();
		c.add("hello");
		String a = c.get(0);
~~~

可以看出我们只需要在原来的代码中加入`<String>`即可

这样如果你尝试向里面add不是String的元素的时候，就会编译错误。我们从里边再获取的元素也完全不需要再经过类型转换



#### 深入研究

一般而言，可以看出泛型在集合类或者接口中应用最为广泛，但是这并不是唯一用途，我们也可以在其他类中使用泛型

呃，该怎么说？其实从名字也可以做一些推断，参数化类型，参数化。所以，本质上例如`List<String>`这里面的String实际是传入的一个参数，换句话说，在原型中定义泛型集合的时候，尖括号里面的是一个参数。也就是说现在多出来了一种新的参数，类型形参，之前只有方法中存在叫做数据形参的参数。

~~~java
public class Learn<T>
{  
	private T name;
	public Learn(T a)
	{
		this.name = a;
	}
	public void print_name()
	{
		System.out.println(this.name);
	}
	public static void main(String[] args)
	{
		Learn<String> first = new Learn<String>("stan");
		first.print_name();
		
		Learn<Integer> second = new Learn<Integer>(2);
		second.print_name();
		
	}
    
}
~~~

从这个例子里我们看出来，我们现在可以为自定义类型增加泛型声明，为之增加一个类型参数，然后当我们实例化的时候，只需要传入一个特定的类型就可以让这个类变成一个特定的包括了泛型声明的类。所以感觉上很像是一个工厂，也很类似于把类变成了定制化的。

这里我们需要注意几个点，当对类进行了泛型改造之后，任何用到这个类的地方，都必须使用包含了泛型的类代替。只有构造器要保持不变，构造器绝对不能改变名字。

然后实例化的时候，如果传入的类型参数必须是类名，所以如果是基本数据类型的时候，必须写作其包装类。

##### 泛型类的子类

可以考虑一下，我们接下来如果想在泛型类的基础上派生子类，我们应该怎么写，最关键的问题就是我们可不可以将父类的类型参数继续写称类型参数，还是传入一个实参。

答案是应该是`class Test extends Father<String>`

而不能是`class Test extends Father<T>`

接下来其实还有一个继承了泛型类型之后，将子类实例化应该怎么写，类型应该怎么写，这时我们应该仔细考虑规则，类实例化的时候，类型的名字就应该是类的名字，要严格遵守规则，所以：

~~~java
public class Learn extends Father<String>
{  
	public Learn(String a)
	{
		super(a);
	}
	public void print_name()
	{
		System.out.println(this.name);
	}

	public static void main(String[] args)
	{
		Learn test = new Learn("stan");
		test.print();
		
	}
    
}

class Father<T>
{
	public T name;

	public Father(T a)
	{
		this.name = a;
	}
	public void print()
	{
		System.out.println(this.name);
	}
}


~~~

这段代码要注意看泛型类的继承，子类的实例化，以及当父类只有有参数构造器的时候，子类必须显式调用父类构造器

##### 特别声明

一个泛型类实例化的时候是否必须给出类型参数？

不是必须的，但我们不给出的时候系统会自动传入Object作为类型参数，并不会报错，依然可以运行，但是我觉得这样很不好。

是否真的存在泛型类？

没有，从类型参数这一点就可以知道，这依旧只是一个普通的类，只不过多了一个参数，当你创建两个类型参数不一致的实例，然后getclass，然后使用==比较，你就可以发现答案是true

这会导致什么情况？可以考虑一下，如果不存在泛型类的话，也就是说不同类型参数的实例对应的是相同的类本体，这时如果我们在类本体中把static和类型形参放在一起就会导致问题，因为所有的实例共享静态成员，但是他们的类型形参又不一致，必然会报错。

总之，static与类型形参不能共存。

#### 类型通配符

之前有说，如果我们不为泛型类型传入类型参数的话，那么系统会为之传入Object，但是从表现上来看，这么说是不合理的。

在新版的JDK框架中，集合已经完全被改造成泛型类了，也就是说规范来说我们都要为之传入类型参数，但是我们的确可以不传，这也正符合了最开始所说的里面每一个元素都是Object

那么我们可以考虑一个问题，如果一个方法要求一个参数是A类的，那么我们传入的实参可以是A或者A得子类，可是如果参数是一个泛型类呢?，也就是说如果形参是List，那么实参可不可以是`List<String>`，但是如果形参是`List<Object>`，实参就不可以是`List<String>`

这实际表明了两个问题，首先就是我觉得不给类型参数和给出Object并不太一样，这个问题没有什么可解释的，接受就行。

其次,如果`G<A>`和`G<B>`，并且B是A的子类，那么`G<B>`并不是`G<A>`的子类，这一点很独特。

##### 使用类型通配符

所谓类型通配符就是`?`，我们只需要把泛型的类型参数替换为`?`，那么他就可以匹配所有类型

限制就是在于，如果在方法的参数里面，为泛型类型使用了类行通配符，那么我们将无从得知参数的真正类型，对于集合而言，我们将不知道get的是什么类型，但可以保证肯定是Object

##### 设置范围

类行通配符可以匹配所有的类型，如果我们不想让他匹配所有的类型，而是只匹配一个特定类型及其子类，那么我们可以使用`<? extends Father>`

这时我们就可以为之传入Father泛型类，或者Father的之类的泛型类

##### 类型形参的范围

对于普通的类型形参我们也可以使用上述语法限制泛型类的范围，例如`class Test<T extends Number>`，这里Number是所有数字类型的父类，那么我们为这个泛型类创建实例的时候就不能任意创建了，而是只能创建数字泛型类



#### 泛型方法

现在我们的确有了通配符加上范围限制这样的手段，来控制泛型类的类型参数的范围，但是现在还有一个问题，如果我们想对这样的泛型进行操作应该怎么办，以一个例子来说，在一个方法中，我们想实现对任意类型的形参操作，但同时又保留这种类型，而不是Object。怎么说呢？最初考虑泛型面对的是集合和类，我们希望类或者集合可以处理很多的类型，同时又不必把所有的元素都变成Object

那么现在转换为方法，我们希望方法可以对很多类进行操作，同时又可以记住类型，那么该怎么办？

~~~java
public void add_object(Object[] a,ArrayList<? extends Object> b)
{
  for(Object s:a)
    b.add(s);
}
~~~

考虑上面的应用，你会发现这样写并不行，问题出在参数b是一个泛型，这意味着它可以接受很多类型，但也意味着我们并不知道他的类型，如果不知道类型的话，竟不能对她操作。

于是，就有了新的语法，称之泛型方法，为方法也提供类似于泛型类的类型参数：

`修饰符 <T,S> 返回值类型 name(参数列表)`

例如：

~~~java
public <T> void add_object(T[] a,ArrayList<T> b)
{
  for(T s:a)
    b.add(s);
}
~~~

那么接下来可以考虑一下，我们为什么要使用泛型方法，为了适应所有类型，但同时又不会因为类型未知而无法操作。那么我们可以使用在泛型方法里面使用通配符范围限制呢？虽然通配符加范围限制依旧会导致不清楚准确类型，但是我们只要执行的操作是父类所支持的，那么就可以，所以，是可以的。



##### 泛型方法还是通配符



##### 通配符的下限

举个例子，在泛型方法中我们可以使用通配符设置参数的上限，也就是说参数类型只能是T或者T的子类，那么，如果我们想写返回值该怎么办？明显我们只能写T，也就是说返回值的类型只能是父类，这样就很不爽了。

这时我们要考虑使用通配符的下限，而不是上限。

`<? super T>`

这个时候泛型的类型参数就只能是T或者T的父类。

要注意，我们不能写一个重载的方法，区别只是一个用的是上限，一个用的是下限，这会导致程序无法区分而运行错误。



#### 擦除与转换

前面的说法是错误的，我前面说，如果不为泛型类传入类型参数的话，系统会传入Object，其实并不是。本质上自从JDK1.5之后，我们都应该携带类型参数，但是为了兼容以前的代码，才允许了不带的，如果不带的话，系统给予她的类型参数实际是raw type，即原始类型，而不是Object

如果我们把一个具有类型参数的泛型类实例赋值给了一个raw type的泛型类，那么原本具有的类型参数将会被强制擦除。信息将会丢失



#### 泛型与数组

允许声明`List<String>[] test;`，但是却不允许创建示例`new ArrayList<String>[10]`

这里我并搞不太懂，总之就是系统不允许数组元素的类型包含类型变量或者类型参数

书上的例子看不懂，所以不知道为什么。

呃，上网搜了一下，细节还是没看懂，我也无心细看，总之就是说，泛型的支持与编译器有很大关系，其中使用了强制类型转换，但是如果使用了泛型数组，那么强制类型转换很容易导致报错，所以最后决定不允许使用泛型数组。

完结

### 与运行环境交互

#### 与用户交互

##### 命令行运行的参数

我们在main里面已经写出了参数是一个字符串类型的数组，所以我们可以在运行的时候附上空格分隔的各种参数

##### 键盘输入

这里主要使用Scanner类来实现

首先需要实例化这个类，然后实例有两个最常用的方法：

-   boolean hasNextXxx()，这个方法可以检测是不是还有下一个输入项，Xxx是基本类型，首字母大写，我们可以省掉Xxx，这是默认的是字符串，也就是说所有的输入都会被当作字符串。当指定了类型的时候，如果输入和类型不符，就会强制退出程序
-   nextXxx()，给出下一个输入，类型由Xxx确定，不写的话就是String

你可以依次输入多个，然后项与项之间通过空白分割，回车就会被读入迭代对象内

可以使用useDelimiter方法，传入一个字符串，来确定分隔符，但是这个我在测试的时候表现很怪异。如果指定了分割符是空格，那么必须要在输入内容后面加空格然后回车，才会认为是正常的输入，否则根本不会读入

另外还提供了读入一行的方法，这时返回值肯定就是字符串了：

-   boolean hasNextLine()
-   String nextLine()

还可以用scanner读取文件

##### BufferedReader

在Scanner出现之前，使用的工具是这个。它读取的总是字符串



#### 系统相关

与运行平台的交互

##### System

这个类已经接触过了。

呃，好像没啥用呀

-   `Map<String,String> getenv()`，获取所有环境变量
-   `Properties getProperties()`，获取所有的系统属性
-   `long currentTimeMillis()`
-   `long nanoTime()`，和上面那个一起获取自1970.1.1到现在的时间差，前一个返回值是毫秒，后一个是微秒。但是毫秒都不会特别准，微秒更别提了
-   `indentityHashCode(Object a)`，获取根据地址得到的hashcode

##### Runtime

每个程序都有与之对应的Runtime类的一个实例，不能创建，但是可以通过`Runtime Runtime.getRuntime()`获取

获取的实例提供了下面的方法：

-   availableProcessor，获取处理器数量
-   freeMemory，获取空闲内存数
-   totalMemory，总内存数
-   maxMemory，可用最大内存



#### 常用类

##### Object类

常用方法：

-   boolean equals(Object obj)
-   protected void finalize()
-   int hashCode()
-   String toString()

##### String StringBuffer StringBuilder

关于字符串的操作

很多很多方法，就不详细说了



##### Math

-   toDegrees()
-   toRadians()
-   acos asin atan atan2
-   cos sin tan cot sinh tanh 
-   floor ceil round
-   sqrt exp pow log log10
-   abs max min random(0~1之间)

##### Random

首先创建一个Random的实例，然后就可以调用各种方法

-   nextDouble()，0-1之间的double
-   nextFloat()，0-1
-   nextGaussian()，平均值0，标准差是1
-   nextInt()，整个int范围
-   nextInt(int a)，0-a
-   nextLong()，整个long范围

可以在创建实例的时候传入一个随机数种子

Random a = new Random(2);



##### BigDecimal

前面我好像没有说，但是float和double两个实际上在使用的过程中很容易引起精度丢失，非常常见

这时可以考虑BigDecimal，但是要注意，给构造器传入的参数应该是字符串，而不应该是double，否则一样会造成精度丢失

缺陷是，没有运算符重载，所以使用的时候，无论什么操作，都要调用方法



#### 日期与时间处理

Date是一个很古老的类，已经不再推荐使用了

##### Calendar

呃，这些东西现查现用其实就好

还有一个处理时区的TimeZone类



#### 正则表达式

这个也不说了





### 异常处理

主要依靠5个关键字：try catch finally throw throws

java里面一场分两种checked和runtime，分别是编译异常和运行异常

~~~java
try
{
    
}
catch(Exception e)
{
    
}
~~~



### AWT编程

awt是早期的GUI库，之后又出现了更高级的Swing，某些情况下，两者会同时使用，后者并未完全替代前者。

#### 结构

相关类都存在于java.awt包及子包内。两个基类为Component和MenuComponent,继承关系如下图：

![继承图](D:\html_file\images\awt继承.PNG)

前者是一些可交互对象，后者主要是菜单组件

另外的两个重要概念是Container和LayoutManager，明显前者是容器，后者是层管理



