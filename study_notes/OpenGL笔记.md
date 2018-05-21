## OpenGL笔记



我曾经学习过使用pyopengl写过opengl代码，但是遇到过很多的问题，其中给我带来最大问题的就是assimp，虽然现在我认为使用我的C/C++编译的知识，加上已经安装过的Visual studio我已经可以解决这个问题，但是我并不准备在去解决这个问题并继续这个项目。我决定尝试使用C++来继续，如果我某天决定要继续的话。在一切之前，我首先将会做一些与环境设置相关的工作，为可能的继续铺平道路。



### IDE与编译

是否要选择使用IDE完成opengl的编译？我选择否。于是我选择使用GNU的编译器手动完成编译和连接工作。



### 库与库的编译

我们需要opengl的库，还有重要的窗口管理库glfw,glad，以及后期可能需要的模型加载库assimp。

opengl的静态库已经存在于windows系统中了，我们不需要做特别的处理

glfw提供的是源码，当然也有提供windows上面的预编译文件，因为接下来我们要使用的是mingw中的GNU编译器，所以需要的是其中的mingw文件夹里面的静态链接库

关于如何使用，也可以说是如何编译opengl代码，我在`C与C++代码组织与编译`笔记中已经作为最后一部分做过记录，这里不再赘述。

关键是，在那里我提到了截止到目前为止，我还没有解决如何才能不使用预编译的glfw库，自行手动编译的问题，这里，我已经解决了。

### Cmake与编译

之前已经了解过了，makefile是用于编译的一个很好的工具，但是问题在于他不是跨平台的，这意味着作者可能需要为不同的平台各写一份适合这个平台的makefile或者类似makefile的文件，这很不合理。于是便有了cmake，cmake的存在可以让作者只需要按照cmake的语法写一份`CMakeLists.txt`的文件，然后就可以在不同的平台进行编译，具体来说就是使用不同平台的编译器，通过cmake可以分别生成适合于该平台的makefile或者类似makefile的文件，然后再通过make或类似make的操作完成最终的编译。

关于cmake的下载安装，就不多说了，完后可以选择使用GUI或者命令行，二者没有区别，我建议使用GUI。

分别选择glfw的源码的文件夹和结果要存放的文件夹，然后configer选择编译工具，如果要生成visual studio的文件，一般选择visual studio 14 2015，然后重新点击configer确认config，然后点击生成即可，生成结果即可用于visual studio

但是，我想要的是mingw，我之前的问题就在于此，一直无法使用mingw完成cmake，我选择了mingw makefile，却报错说未发现。直到今天我才找出错误在哪。这个过程实际上调用了mingw32-make.exe，还记得这个命令吧，就是我在c++编译中建议修改为make.exe的那个程序，就是因为我的修改导致cmake无法发现编译工具的，只要再重新提供一个mingw32-make.exe即可。

照和之前一样的步骤，生成完成之后，我们就可以在结果的文件夹中发现makefile文件和一堆其他文件，这意味着成功了，只需要继续执行make完成编译即可，在src文件夹中就可以找到`libglfw3dll.a`文件，这就是我们需要的链接库，虽然他不是我们之前一直使用的`libglfw3.a`但是我测试了一下也是可以的。

#### Assimp的编译

接下来我就尝试了一下assimp的编译，也作为测试cmake之用

同样的步骤，我下载了最新版的源码，同样选择mingw进行生成，会报几个错，但是无所谓了。

接下来，执行make，针对我所使用的版本(assimp 4.1.0)来说，在make的过程中会多次出现错误，但是都不至于停止，直到69%的时候，报错：

~~~
C:\Users\Stan\Downloads\assimp\assimp-4.1.0\tools\assimp_cmd\assimp_cmd.rc:4:10: fatal error: ../../revision.h: No such
file or directory
 #include "../../revision.h"
          ^~~~~~~~~~~~~~~~~~
compilation terminated.
~~~

然后make终止，无法进行，明显这个错误是未发现`revision.h`这个头文件，经过网上查找，按照报错的指示，在`assimp_cmd.rc`文件所处的文件夹上两层文件夹，新建`revision.h`头文件，内容为：

~~~
#ifndef ASSIMP_REVISION_H_INC
#define ASSIMP_REVISION_H_INC

#define GitVersion 0x0
#define GitBranch "master"

#endif // ASSIMP_REVISION_H_INC
~~~

保存，继续make即可，虽然还会报错，但不至于终止，直至100%结束

但是我检查发现生成的结果，发现make前后似乎区别并不大？我也不知道需要的究竟是哪些库，反正code文件夹中的两个静态链接库在make之前就有了，make之后也似乎并没有生成其他的.a库

并且，看网上的assimp使用示例，还需要很多头文件，这里也没有显式的给出整合的头文件夹，似乎还是需要手动从源码中搜集，总之虽然勉强算是make成功了，但是感觉不太对。

至于测试，assimp的使用似乎很复杂，所以我没有做测试，所以也不知道到底对不对。

learnopengl这个网站是我常用的opengl的参考网站，它上面关于assimp提到了它使用的版本是`assimp3.1.1`，并提到这个版本会存在需要DirectX的问题，以及DirectX的安装报错问题，是的很不幸，在我测试的过程中，他提到的问题我全都遇到了，然后，我解决到安装问题的时候就不想再继续了。

至于最新版本中就似乎不再需要DirectX了，所以也就不再有解决这个问题的必要了。

总之，现在就是这样。