## Kotlin笔记

要不再看看Kotlin吧



### 环境

kotlin依赖于java，但是也需要一个编译工具，似乎是先把`.kt`源文件编译成jar，然后使用java运行jar包

去[github](https://github.com/JetBrains/kotlin/releases/tag/v1.2.50)下载编译工具，很小的，解压，然后把bin目录加入path

#### hello world!

~~~kotlin
//hello.kt
fun main(args: Array<String>) {
    println("Hello, World!")
}
~~~

然后用`kotlinc hello.kt -include-runtime -d hello.jar`编译得到`hello.jar`包

接下来用`java -jar hello.jar`运行jar包，即可

