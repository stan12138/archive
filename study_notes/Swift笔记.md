## Swift笔记

闲的无聊，虽然没有Mac，还是学学swift先。



### 环境

没办法，只能在windows上面写swift，其实Ubuntu会更好，但是每次切系统好麻烦，所以还是windows吧。

简而言之，我们只需要一个编辑器和一个编译器而已，编辑器很简单，还是sublime，默认是不支持swift格式的，必须要安装插件`ctrl+shift+p`，然后输入`install`，进入插件搜索框之后，输入`swift`，安装即可，然后应该就可以选择swift高亮显示了，似乎还是不能自动识别，需要手动选择。

至于编译器，[来这里](https://swiftforwindows.github.io/)，下载一个，安装即可，这是网友开发的，所以，界面做的很一般，但是好在清晰。首先选择代码文件，然后编译，然后点击run，运行即可。注意必须要通过run来运行，虽然你可以找到exe文件，但是它依赖一系列的动态链接库，所以并不能直接运行。



### 基础知识

swift代码文件的后缀是`.swift`，然后代码不要求使用`;`结尾，运行的入口和python一样，都是全局代码即入口

注释和c++一样

下面只做简单的的笔记

### 常量与变量

在swift里面似乎格外在意常量。

使用`let`声明常量，使用`var`声明变量。常量必须赋初值，不可变，变量随意。可以不标注类型，会自动推断，但是也可以指定。如果变量没有赋初值，就必须指定类型。

可以在同一语句中声明多个变量，逗号分隔，类型一致，只有最后一个需要指定类型。

变量和常量的名字很个性，范围要比其他语言广得多，几乎可以是任何Unicode字符，当然也肯定有一些限制，例如不能是数学符号，数字开头等等，但是说实话，我不喜欢，还是按照普遍规则来吧。

接下来是如何指定类型

~~~swift
let a: Double = 10
var b: String
~~~

说的是，似乎推荐在`:`和类型名字之间来个空格

### 数据类型

在swift中数据类型也就是`Int Double Float Bool String`这几种，很普通，特别之处在于名字首字母都是大写的

然后结构类型，或者集合类型有`Array Set Dictionary Tuple`

#### 整数

整数的格式也一样，包含了8，16，32，64位有无符号整数，例如`UInt8 Int32`这样的。普通的`Int`是因平台而异的

特别之处在于，整数类型有两个属性`max min`可以直接给出最大最小值

然后，也是支持二进制，八进制， 十六进制，指数这些我都没用过的东西

要注意，swift对类型的限制比较严格，以至于到了不同类型的变量不可运算的地步，例如Int和Double不能相加，所以，类型转换会比较常见

`Double(a)`即强制类型转换

#### 浮点数与布尔值

Float Double似乎没啥可说的

布尔值也没啥说的，值是true和false

要注意的是和java一样，判断语句只接收布尔

#### 类型别名

`typealias Stan = Int16`

没用过



#### 字符与字符串

在swift里面字符和字符串都使用双引号，字符串叫做`String`，字符叫做`Character`

然后定义一个空字符串可以使用空的双引号，也可以使用构造方法

字符串可以修改，除非是常量

支持`+ +=`这样的拼接操作，可以拼接字符串，或者字符

多行字符串，像python一样的策略，三重双引号

##### Unicode

字符和字符串完全兼容Unicode，这样是带来了一些比较讨厌的结果的

我们已经知道了字符串里面是可以使用转义字符的，这很正常，在swift里面，我们可以使用`\u{n}`这样的格式来使用Unicode，其中的n就是一个1至8位的十六进制Unicode码， 例如var a = "\u{24}"

但是，这里有一个需要注意的问题，就是扩展的概念，例如`var word = "e"`，那么`word += "\u{301}"`得到的实际上不是两个字符，因为e的Unicode码是65，如果他后面扩展一个301代表的急促重音得到的实际上是另外一个单独的Unicode字符，是一个e上面加一个撇的。

这意味着如果对字符串扩展了Unicode，并不一定会让字符串变长，可能只是修改了最后一个字符而已。

##### 统计 修改 索引

统计字符串的字符数目，可以使用`count属性`，如`word.count`

靠，swift版本变化太快了吧，感觉我应该去看swift4，而不是3

正是因为Unicode的原因，我们也无法直接使用整数索引字符串里面的元素，可以使用索引，但是这个索引是一个特殊的类型，必须使用字符串的index方法获得一个我们想要的索引

~~~swift
word[word.startIndex]
word[word.index(before:word.endIndex)]
word[word.index(after:word.startIndex)]
word[word.index(word.startIndex, offsetBy:2)]
for index in word.indices 
{
    print(word[index])
}
for item in word
{
    print(item)
}
~~~

基本上这就是常见的索引方法了，startIndex,endIndex两个属性可以给出第一个元素的索引，和最后一个的，index方法可以用来获取一个位置的索引，可以使用的参数是before和after，或者是offsetBy来指定一定偏移量的。最后一个indices属性可以获取所有索引的列表

###### 插入

在指定位置插入，需要使用insert方法，at参数指定位置，可以直接插入一个字符，或者使用contentsOf参数插入一个字符串

~~~swift
var word = "hello"
word.insert("!", at:word.endIndex)
word.insert(contentsOf:"stan", at:word.index(before:word.endIndex))
~~~

###### 移除

remove方法可以删除一个字符，使用at参数指定位置，移除子串的话需要使用removeSubrange方法，额外的，需要使用下面运算符部分的区间运算符获得一个区间，作为参数



如果要获取字符串的子串，需要传入一个range的索引，然后应该把结果转换为String以获取长久存储？



字符串的比较可以直接使用逻辑运算符`== !=`

##### 字符串格式化

~~~swift
var name = "stan"
print("this is name : \(name)")
~~~





字符串暂时到此为止吧，后面还有Unicode和前后缀，再说吧 





### 运算符

赋值，加减乘除，取余没有区别

支持`+=, /= `等一系列操作符

比较运算符也没有差异，`== != > < >= <=`

支持三目运算符，`问题 ？ 答案1:答案2`

逻辑运算也是和C一致的

#### 区间运算符

这个还是很重要的

闭区间`a...b`，包含a和b

半闭区间`a..<b`，包含a，不包含b

单边范围，对于一个数组，我们可以使用单边运算符

~~~swift
var a = [1,2,3,4]
for i in a[...2]
{
    print(i) //1,2,3
}
for i in a[..<2]
{
    print(i) //1,2
}
for i in a[2...]
{
    print(i) //3,4
}
~~~

注意数组的元素序号也是从0开始的，半边范围也是会包含首尾的

~~~swift
var range = ...5
var range = 5...
range.contains(1)
~~~

这个就比较迷了，可以用来生成单边的，但是指定了尾部的，开头相当于负无穷，大概就是这个意思，首部的也一样

### 结构类型

我这里把数组，集合，字典，元组都称之为结构类型

#### 数组

这里的数组用起来还是挺不错的，限制同一种类型，支持增删，支持索引，修改，相当好。

~~~swift
//初始化
var list = [Int]()
var list = Array(repeating:0.0, count:3)
var list = [1,2,3]
var list: [Double] = [1,2,3]

//扩增
list.append(10)
//两个同类型的数组可以相加
list.insert(3, at:0)

//移除
list[4...6] = [1,2]
list.remove(at:0)
list.removeLast()
list = [] 

list.count //这个属性获取长度
list.isEmpty //判断是否为空

print(list[0])

for item in list
{
    print(item)
}
~~~

就是上面这些了



#### 集合

集合同类型，但无序，因此元素不能重复

~~~swift
//创建集合
var letters = Set<Int>()
var letters: Set = [4, 4]
var letters: Set<Double> = [1,2,3]

//添加值
letters.insert(10)

//移除
letters = []
letters.removeAll()
letters.remove(1)

//长度 判断 遍历
letters.count
letters.isEmpty
letters.contains(3)
for item in letters
{
    print(item)
}
for item in letters.sorted()
{
    print(item)
}

//集合间操作
a.intersection(b) //交集
a.symmetricDifference(b) //共同的差集，不同时在两个集合内的元素的合集
a.union(b) //并集
a.subtracting(b) // a关于b的差集

a==b //两个集合全等
a.isSubset(of:b) //a是不是b的子集
a.isSuperset(of:b) //a是不是b的父集
a.isDisjoint(with:b) //a和b有无交集
a.isStricSubset(of:b)
a.isStrictSuperset(of:b) //是不是严格子集或父集
~~~



#### 字典

~~~swift
//创建
var dict: [String:int] = ["h":1, "b":2]
var dict = ["hahh":1.0, "hb":2.0]
var dict = [String:Int]()

//长度判断
dict.count
dict.isEmpty

//修改与索引
dict["h"]
dict["h"] = 10
dict["h"] = nil //移除这个键值对
dict.updateValue(20, forKey: "e")
dict.removeValue(forKey:"e")
dict = [:]

//遍历
for (key, word) in dict
{
    print(key, word)
}
for key in dict.keys
{
    
}
for word in dict.values
{
    
}
~~~

绝对需要注意的是，它的字典是有限制的，那就是所有的键必须类型一致，值也是

#### 元组

元组其实类似于一个结构体？大概是这样的吧，但是从索引上来看又类似于数组，元素的数据类型自然是不受限制的

~~~swift
var tup = ("stan", 100)
var tup = (name:"stan", year:100)

//索引
tup.0
tup.1
tup.name
tup.year

//解包？
var (first, second) = tup
var (first, _) = tup
tup = (1,2,3)
var (first, _, _) = tup
~~~

解包的时候，不想要的元素可以使用`_`，并且个数不受限制



### 语句

这里除了print之外，剩下的就是各种流控制语句了



#### print

输出语句，可以直接放进多个参数，从而输出，也可以通过`separator和terminator`两个参数指定分隔符和结束符



#### for语句

for语句的结构是

~~~swift
for item in stan
{
    print(item)
}
~~~

总之就是for-in了，支持的遍历结构还是非常广泛的，只要是序列类型就可以包括：

~~~
字符串
数组
集合
字典
区间
~~~

但是要注意的是，对于集合由于是无序的，所以如果不排序的话，输出也是无序的，另外对于字典的话，必须使用元组来作为循环变量

~~~swift
var dic = {"name":"stan", "year":"1000"}
for (key, value) in dic
{
    print(key value)
}
~~~

然后要注意的是元组不是序列类型的，所以，元组不能使用for-in

类似python里面的range还是很重要的，在swift里面使用区间运算符来生成



然后区间运算符的缺点是不能指定间隔什么的，不够灵活

于是有了stride函数，可以生成指定间隔的开闭区间，但左边肯定都是闭的

~~~swift
stride(from:0, to:10, by:2) //不包含10
stride(from:0, through:10, by:2) //包含10
~~~



!! 需要注意的是下面的while和if语句的条件都不需要括号



#### while系列

while有两种语法，感觉上就是类似于while和do...while的区别吧

~~~swift
while condition
{
    
}

repeat
{
    
} while condition
~~~



#### 判断语句

if语句没有差异，只是条件不要括号，然后也不提供快捷的elif，需要自行使用`else if`

switch语句

