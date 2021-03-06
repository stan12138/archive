## OS笔记

这个笔记主要侧重于记录我尝试根据各种资料学习写一个极简的OS的过程。

首先列出环境与主要参考书目

之后会拷贝原来写的很凌乱的一些早期的笔记，然后才会继续正题。

要注意的是，这一部分肯定会和汇编语言有很多的联系，所以有些内容可能需要结合汇编语言笔记。那里面写过的东西这里就不会再赘述。



### 环境与参考书目

主要的参考书目是[一个64位操作系统的设计与实现](https://book.douban.com/subject/30222325/)，我并未找到电子版，所以买了实体书。

然后书中建议的是，使用Linux平台，然后需要使用nasm进行汇编的编译，语法的话实际上是Intel语法和AT&T语法的结合，至于原因书中有详细解释，我觉得这样其实很好，从多学一些东西的角度来说。然后c语言的编译器来自于GNU的gcc。另外还有早期的模拟运行环境，明显在早期的时候，需要很多调试，所以直接使用U盘和物理平台结合的测试方法并不合适，于是需要一个虚拟机，这里使用的是Bochs，据说用它的原因是它是一个带了调试功能的虚拟机，这就是和普通虚拟机软件不一样的地方。

为什么会利用Linux作为开发平台呢？其实我并没有找到特别的理由，可能就是Linux上面工具链比较完善。但是实际上我现在使用的是windows平台，主要原因是我不习惯于日常使用Linux，虽然我装了双系统，我也不想通过虚拟机在windows上使用Linux，然后，现在我也得到了一个Linux系统的服务器，但是我在bochs的安装上遇到了问题，安装失败了。

总而言之，现在我的工作环境是：

windows，需要安装nasm，然后安装bochs，然后将nasm编译的bin文件写入img的时候，在Linux上面会使用dd命令，在windows上面为了方便就会安装cygwin这个软件，这个软件可以让我们使用linux的一些命令，其中就包含了dd。

bochs需要一个配置文件，这里我从网上搞到了一个极简版的配置文件：

~~~
megs:32

romimage:file=$BXSHARE/BIOS-bochs-latest
vgaromimage:file=$BXSHARE/VGABIOS-lgpl-latest

floppya:1_44=a.img,status=inserted

boot:floppy

log:bochsout.txt

mouse:enabled=0

keyboard: keymap=$BXSHARE/keymaps/x11-pc-de.map
~~~

保存为`stan.bxrc`文件即可。

然后要使用bochs生成一个img光盘文件。过程在书中有细致描述，不再赘述了。

然后通过cygwin.bat打开cygwin的命令行，进入到合适的文件夹下，通过`dd if=boot.bin of=a.img bs=512 count=1 conv=notrunc`来进行写入，当然为了方便起见的路径什么的就自己搞好了。总之这里和书上没什么区别。

#### 启动虚拟机

可以先试用书上提供的第一个boot.asm，得到bin，写入img，搞好bochs的配置文件，然后运行`bochs.exe`，选择load加载配置文件，然后start即可运行，一切顺利的话应该就能看到start boot这样的输出。





ok，如一开始所述，下面会拷贝一些早期的资料收集，仅作为记录，可以直接跳过。

### 早期记录

其实网上很多教程写的很好，只是我不懂的看而已。第一部分，我需要知道计算机是如何启动的。

我的参考文献和博客很杂，这里不再一一举出。

只是这一块主要来自于[这篇博客](https://blog.csdn.net/langeldep/article/details/8788119)，下面的内容基本完全来自这篇博客，只是精简了而已。

整个启动过程分为四部分，其中第一部分可以认为是由硬件制造商控制的，属于硬件自动执行的，我们无法接管。其余三部分或多或少都能控制。

这四部分分别是BIOS,MBR,硬盘启动，操作系统

#### BIOS

电脑中有一块ROM，其中刷写着开机程序，第一件事就是执行这里面的程序，这个程序叫BIOS，全称Basic I/O System

BIOS其实包含了很多功能模块，首先他会执行硬件自检(Power-On Self-Test)，检查硬件是否满足开机需要，没有问题的话，BIOS会从启动顺序里面找到开始执行下一阶段启动程序的设备，这就是我们会设置的启动顺序。

依次尝试各设备，直至成功启动

#### 主引导记录(MBR)

启动顺序中的存储设备都有特殊的存储结构，具体而言就是存储设备的第一个扇区512个字节必须是一段主引导记录(Master boot record)，这512个字节有特定的结构，计算机会首先取出这前512字节放入内存指定位置。

由于MBR只有512字节，因而内容有限，主要作用就是告诉计算机去何处寻找操作系统。

MBR的结构：

```
1-446字节：调用操作系统的机器码
447-510字节：分区表
511-512字节：主引导记录签名
```

对于第一顺位的存储设备，计算机先读取其MBR，之后会检查511和512两个字节，只有当这两个字节内容为`0x55 0xAA`的时候才会继续，否则换第二个存储设备

硬盘是可以分区的，每个区都可以安装不同的OS，主引导记录需要知道应该将控制权交给哪个分区。

分区表共64字节，分为四项，各16字节，每一项都代表一个主分区。因此一个硬盘最多只能有四个主分区。

每个项的16个字节都包含6个部分：

```
（1） 第1个字节：如果为0x80，就表示该主分区是激活分区，控制权要转交给这个分区。四个主分区里面只能有一个是	 激活的。
（2） 第2-4个字节：主分区第一个扇区的物理位置（柱面、磁头、扇区号等等）。
（3） 第5个字节：主分区类型。
（4） 第6-8个字节：主分区最后一个扇区的物理位置。
（5） 第9-12字节：该主分区第一个扇区的逻辑地址。
（6） 第13-16字节：主分区的扇区总数。
```

因为扇区的总数只有4字节，所以主分区的扇区不多于2的32次方。

#### 硬盘启动

这个也是分情况的，三种情况，分别是使用了主分区进行启动，逻辑分区或者扩展分区启动，启动管理器启动。这相当于给了一些多样化的启动选项，具体是哪种，就是由MBR的前446字节确定的了。而我提到过的GRUB就是第三种情况。

具体的，看博客原文吧。

#### 操作系统

转交控制权给操作系统之后，就开始载入操作系统了。从内核开始。





#### Boot

DIY的第一步是尝试接管启动过程的第二步，自己写一个MBR，这里也经常被叫做自己完成boot code

MBR的全部512个字节并不是全都重要，如果要写，就必须知道这512字节的详细构造：

![MBR](D:/Test_Project/Create_OS/archive/study_notes/images/MBR.png)

这张图片来自于[这个网站](http://www.independent-software.com/operating-system-development-boot-sector-structure.html)，这个网站也是重要的参考

这里面重要的是BPB和EBPB，以及最后的两个字节





总而言之，至此，最重要也是最棘手的初始环境的配置算是已经搞定了。然后就可以照着书上的继续了。



### 实模式下地址分配

启动之初，CPU是运行在实模式下的，这个阶段的内存地址是20位的，其中段地址16位，偏移地址16位，段地址左移4位，加上偏移地址构成真正的内存地址。

20位的地址一共是1MB，有必要知道这些地址的大概情况，因为在boot的后面阶段需要读软盘，然后把软盘的数个扇区的数据存入内存，这是需要决定存在哪，以及每次最多存几个扇区。

已知自0x7c00开始的512个字节存储的是主引导扇区的内容。按照参考书上面的习惯，同时也算是凑个整嘛，我倾向于把读取的软盘扇区数据存入0x10000开始的位置。

内存的分配情况是：

`0x00000---0x9ffff`是常规内存

`0xa0000---0xeffff`是320KB的外围设备寻址空间，其中包含显卡的空间，具体的`0xb8000---0xbffff`这一段是显卡的

`0xf0000---0xfffff`是ROM-BIOS的地址空间



### 一些说明

绝大多数的东西，不会再赘述，只会写一些让我疑惑的东西。

#### org问题

已知BIOS的最后，会读取一个扇区的数据进入内存的指定位置即`0x7c00`处，同时会设置`cs和IP`两个寄存器。这里看起来其实`boot.asm`里面设置`org 0x7c00`似乎没有什么意义，至少对于原本的第一个boot代码，去掉这一句似乎也没关系，检查编译得到的bin文件，似乎也的确没有区别。具体的更详细的研究可以看[这篇文章](https://blog.csdn.net/judyge/article/details/52333656)



### Boot

下面开始尝试第一次启动。

首先说明一下，环境问题已经说过了，我选择windows平台，之后我得到了帮助，成功在Linux上安装了bochs，但是最终无法运行，`cannot connect x display`这样的，我试过设置配置文件里面的display library为term或者nogui这样的选项，总之目标就是在命令行下使用bochs，结果呢，是不行，提示说这些选项不可用，我不确定原因是处在bochs的源码编译的时候还是bochs本身就要求必须使用图形界面。

所以现在我是在windows平台。

然后就是文件路径的问题，bochs自然是安装在一个单独的文件夹中，然后没被加入环境变量的话，bximage这样的命令就只能在它的文件夹下使用，条理起见，我倾向于将所有的代码文件，配置文件，光盘映像放在一个单独的文件夹内。配置文件是在启动bochs之后自由选择的，所以关键问题在于映像应该放在哪？bochs目录下还是配置文件目录下。我刚刚才发现，如果使用诸如上面贴出来的极简配置文件的话，a.img应该放在与配置文件同一目录下，这样非常让人满意，毕竟不用再每次拷来拷去了。

然后就是映像的问题。

问题在于，第一，为什么要特别使用bximage创建映像，为什么要特别选择fd或者hd？第二，dd有什么很特别的地方吗？第三，书中很快就开始使用了FAT12文件系统，已及mount挂载命令，这一切又有什么不同的？

这里，我想介绍一个windows平台下的工具--winHex，这个工具可以让我们查看任意文件的原始二进制内容。

首先就是第一个问题。选择fd或者hd发现最终得到的文件都是img文件，唯一的区别就是可选择的文件大小不同，用winhex检查，可以发现无论怎么搞，创建完之后得到的都是一个img后缀的，特定大小的文件，文件内容，所有的字节都是0，没有任何特殊信息。

所以这让我很怀疑bximage存在的意义，以及搞这些复杂选项的意义，事实上使用python我完全可以自己做到这些。

第二个问题，已经知道，boot.asm只是为了搞出一个512字节的完全指定信息的bin文件，也就是说boot.bin文件就是一个512字节的二进制文件，其实也的确知道dd命令只是原样将这512字节写入a.img的头部，即前512字节，作为主引导扇区。使用winhex检查也是的确如此，并没有任何特别指出。同样的这个过程使用python也完全可以实现。

第三个问题让我也非常的疑惑，我的步骤是首先，我知道这个挺复杂的，对于完全不懂的我来说，所以我会首先尝试直接使用书中提供的源码，先跑通了再说。然后我就被卡到了，cygwin无法使用mount挂载命令，经过一番搜索，网上的说法cygwin只是尽量在win上面模拟出一个linux环境，但是后面用的还是win提供的接口，总之就是mount就是不太能行。于是该怎么办？我完全不懂这个过程是在干嘛，自然我也不知道该使用什么工具在win上面完成这个过程。于是我采用了很无奈的迂回策略，我会在linux上面完成全部过程，然后把得到的img再弄回win，然后再跑。现在的结论是，我终于跑通了。

接下来要做的就是通过winhex进行对比，搞懂这个过程实际上到底干了什么，搞懂FAT12文件系统，然后努力使用python取代这一系列的费劲的命令。进行ing....



### FAT12

这一部分解释一下FAT12文件系统。

FAT12文件系统的头部是512字节的主引导扇区，主引导扇区的结构是非常固定的。

每个扇区一般都是512个字节，FAT12文件系统不以扇区为单位，而是簇，每个簇可以是多个扇区，简单情况下，一个簇就是1个扇区。

头部的512字节包含了一些FAT12的标识符，也包含了很多的相关信息，包括簇，扇区，磁头，柱面等等，其余就是引导代码，也即Boot部分。这些没什么难度，直接看书就行。

头部之后有两个完全一致的FAT表，这两个表每一个都占用9个扇区，每个表都是由表项组成，每个表项12位，这就是FAT12的名字来历，每个表项的值代表了一个数据簇的情况。但是特别的前两个表项并不代表数据簇，而是两个标识项，从第三个表项开始才代表了真正的数据簇，然后数据簇的标号实际也是从2开始的，从这个角度来看前两个表项其实代表了0，1两个数据簇。表项的值可以代表本数据簇是一个坏簇，保留簇，空白簇，文件最后一个簇，文件的下一个簇等这样的信息。

举例，第三个表项代表了2号数据簇的使用情况，如果它的值是3，那么这意味着该文件系统存储的某个文件的第一个簇是2号数据簇，然后是3号数据簇，第四个表项代表着下一个数据簇的簇号，如果是`FF8H~FFFH`那么代表着这是文件的最后一个簇。

总之FAT12文件系统中的FAT表以簇链的形式存储着文件的簇占用情况。

两个FAT表之后是目录表，目录表占用14个扇区，目录表里面的每一项代表着一个文件，每个目录项占用32个字节，其中最重要的内容是文件的名字和后缀，以及在数据区占用的首簇的簇号，文件的长度。其中文件长度是以字节为单位的。

接下来才是真正的数据区，数据区存储着文件内容，以簇为单位，序号如上所述，从2开始。

总之这就是简单的描述，具体的细节可以看[这里](http://blog.sina.com.cn/s/blog_3edcf6b80100crz1.html)

特别要注意的是，目录项里面的的首簇序号占两个字节，文件长度占四个字节，它们都是小端存储方式。

然后FAT表的每个表项占用1.5个字节，但是这1.5个字节并不是连续的1.5个字节，而是以一种特殊的方式重新排列了，具体的可以看上面的链接里面的图。也正是这个让我们自行实现FAT12文件系统的自行实现和读写变得很烦。

所以，到现在为止，我的目标可以有两个，第一彻底读懂书里面的boot代码和磁盘读写方式，第二摆脱bximage,dd,mount,cp这样的命令，利用python实现映像的创建，主引导扇区的写入，loader代码的存入。

只考虑最简单的情况，只写入一个主引导扇区和loader代码，同时创建相应的FAT表，目录表等相应的内容。这个相对比较简单，目录项我也可以简化到只写关键信息，时间，日期什么的都空着就好。最难的部分就在于FAT表的构建，但是其实想明白了之后这也很简单，只需要配合移位操作和位与操作提取出需要的字节，然后重新排列即可。

我已经实现了。当然功能还相当弱，只能拷贝一个文件进去。所以，暂时我总算是摆脱那些复杂的命令了。



我已经搞定了可以存入多个文件的fat12工具



### Bochs的使用

使用bochs最看重的是它的调试功能，下面记录一下调试功能怎么使用。注意，这里都是在windows平台下使用的。

如果要使用调试功能，就要运行`bochsdbg.exe`，而不是`bochs.exe`，前者也是一样的，选择配置文件，然后在命令窗口里面可以输入命令控制执行过程

详细的手册[看这里](http://bochs.sourceforge.net/doc/docbook/user/internal-debugger.html)

[这里还有一个中文版的](https://hoverwinter.gitbooks.io/hit-oslab-manual/content/bochs-manual.html)

还可以看看[这个](http://www.360doc.com/content/18/0418/23/9824753_746767808.shtml)，这一篇讲了debug的使用，同时也说了配置。

简单的记录一下：

- 继续执行：`c`
- 停止：`ctr-c`
- 指定执行的步数：`s n`，n是步数，不指定的话就是1步
- 查看内存： `xp /nuf addr`，这个方式很类似于GDB，n指要查看的单元数目，u是单元大小，例如b就是一个字节，f是显示格式，x就是十六进制，addr自然是起始的物理地址。
- 查看寄存器：`r`，这个列出的寄存器是rax这样的，这是64位的寄存器
- 查看段寄存器：`sreg`
- 退出： `q`，看一下提示信息，说明之后应该还要再回车一下
- 断点：`break addr`，看手册可以发现断点的种类还是挺多的，至于什么虚拟地址什么的我不太懂，这个break是物理地址，也就是说断点设置到了内存的addr位置，例如知道boot代码会被BIOS加载到内存的`0x7c00`位置，所以可以设置`break 0x7c00`，那么再执行`c`，程序会运行到断点处停止，然后我们可以逐步运行`s`，对照输出就可以发现boot代码正在被逐条执行

### 使用bochsdb再次探究org指令

前面说了一点点`org`的问题，但其实当时我并不懂，那里给的参考资料其实说得挺详细的。这里详细说一下。

首先，我们对比编译完的lst文件和bin文件其实可以发现org这条指令并不对应任何代码，也就说它并不会生成真实的代码。那么说的它指定了程序的起始地址是怎么回事？编译器并没有权利指定程序被加载到内存的哪个位置，或者说至少org指令没有这个能力。

我们说boot代码被加载到了`0x7c00`处，这是BIOS自身的功能，无论boot代码写不写org，它都会被加载到这个位置。所以其实`org`写不写都一样，boot都会被加载到`0x7c00`，然后cs与ip配合从这个位置逐条往下执行，直到发生了引用，就会出问题了。

例如：

~~~
    52 00000035 58                      	pop	ax
    53 00000036 BD[4300]                	mov	bp,	StartBootMessage
    54 00000039 CD10                    	int	10h
    55                                  
    56                                  ;=======	reset floppy
    57                                  
    58 0000003B 30E4                    	xor	ah,	ah
    59 0000003D 30D2                    	xor	dl,	dl
    60 0000003F CD13                    	int	13h
    61                                  
    62 00000041 EBFE                    	jmp	$
    63                                  
    64 00000043 537461727420426F6F-     StartBootMessage:	db	"Start Boot"
    64 0000004C 74                 
    65                                  
    66                                  ;=======	fill zero until whole sector
    67                                  
    68 0000004D 00<rept>                	times	510 - ($ - $$)	db	0
    69 000001FE 55AA                    	dw	0xaa55
~~~

上面是lst文件的部分内容，其中的53行明显我们把字符串的地址赋给了bp寄存器，明显这是一个偏移地址，无论加不加org，得到的lst文件都是一样的。但是bin是不同的，对比一下可以发现加了org之后这个位置变成了`437c`，没加则是`4300`，这意味着什么。其实这意味着org实际上改变的是偏移地址，如果没有org，就认为程序起始自`0x0000`，那么这个偏移地址自然就是`4300`，加了`org`，就认为程序起始自`0x7c00`，于是偏移地址就改了。

但是这个地址有点诡异，似乎，为什么是`437c`，而不是`7c43`，这大概和大小端存储有关。我们可以通过bochs的debug确认一下。

首先可以`break 0x7c35`，因为我们知道程序起始自`0x7c00`，那么上面的52行的地址一定是`0x7c35`，然后使用`s`逐步执行，再使用`r`和`sreg`分别查看寄存器和段寄存器的值，通过资料可以知道boot代码显示字符是通过调用int10的功能实现的，这个功能在显示字符串的时候字符串的地址通过`ES:BP`指定，查看寄存器可以发现`ES`的值总是`0`，那么BP就自然必须是`0x7c43`才能正确的指到字符串所在位置，对比可知当设置了org的时候BP的值如我们所想，不设置的时候是`0x43`，这样取到的自然是一个错误的位置，观察bochs的显示也可以发现显示是乱码。

至此，这个问题算是结束了



题外话，bochs可以逐步执行嘛，所以，其实我们也是可以观察int 10到底干了什么，可以先断点到int的上一条指令，然后逐步执行，就可以看到程序跳转到了`0xc0152`这样的地址去执行了，并且还可以继续`s`看每一步到底干了什么。



### 继续

我决定还是自己亲手写一写boot和loader的代码吧，否则老是看没什么用。

##### Boot

最简单的boot很简单，只用BIOS的int 10h实现字符显示即可。但是复杂一点的就要清屏，设置焦点。

书上关于清屏写错了，清屏的原理实际就是覆盖窗口的指定部分，所以指定BH,cx,dx肯定是有意义的。然后行号和列号也写反了。很简单，自己查下资料就好。

##### 软盘的结构

1.44M的软盘，一共有80个柱面，两个磁头，每个每个柱面18个扇区。共2880个扇区，编号从0到2879，这是LBA即逻辑寻址方式，在BIOS进行磁盘读取的时候，使用的是CHS格式的编号，即柱面，磁头，扇区。

两者转换的时候，自然必须知道扇区的编号方式。

柱面是最高级的目录，编号0到79，每个柱面包含两个磁头，编号0和1，每个磁头18个扇区，编号1到18

书上的转换公式写法也是错的，应该是：

~~~
LBA/18 = 商Q,余数R
R+1=扇区号
Q>>1得到柱面号
Q&1得到磁头号
~~~

读磁盘的操作书上写的没什么大问题，除了转换公式之外，另外要提醒的就是`ES:BX`指向数据缓冲区，也就是说从这个地址开始存储读取到的内容，书上使用了`ES=0x1000, BX=0x0000`，这就意味着数据存在`0x10000`开始的内存当中。



### Boot的FAT表解析

我在努力自行完成完成在FAT12系统内寻找loader，并且载入内存的汇编代码，但是真的很繁琐，首先要载入目录扇区，然后比对寻找目标文件的首簇序号，然后要载入FAT扇区，然后从扇区中解析出簇链，然后逐个载入。现在我进行到了汇编的FAT表解析。有些问题需要重新说明一下。

我真的很怀疑书上的说法，他说引入FAT12文件系统是一个明智的决定，但是如果没有FAT12文件系统，直接指定位置的话，我大概早就写完boot，早就已经开始是正式搞loader了，想哭。

说回正题，问题还是在这张图：

![IMG_2648](images/IMG_2648.JPG)

他告诉我们应该如何解析FAT表，上面是FAT的原始内存数据，下面是解析之后得到的表项。明显上面三个字节被解析为下面两个表项，每个表项都是一个半字节，需要由上面的原始内存数据经过半字节为单位的重排构成。

首先需要声明的就是上面的序列自左到右就是内存的从低地址到高地址。

但是呢，下面的表项内容的每一个半字节从高往低写的，与书写习惯符合，例如004h，而不是400h

要注意的问题第一在于，如果一次从内存中读取一个字到ax寄存器中，那么这一个字是怎么存的。intel处理器是小端存储，所以如果一次读入ff4fh的话，ax寄存器的ah实际上存的是4f，al寄存器是ff

但是如果我们每次都严格的只处理一个字节，上述问题其实不必过多考虑。

那么当读入一个字节的时候需要考虑的问题是：如果将ah置0，al读入ff，ch置0，cl读入4f。那么如何得到第一个表项fffh。

1、cl寄存器内4f这个字节是如何排列的，答案应该是就是4f，所以做and cl, 0fh操作就能得到f这半个字节

2、如何得到fffh这个表项，实际上应该是cx寄存器左移8位加上ax寄存器

。。。。差不多就是这些，不说了，实在不行可以配合debug自己再重新研究一下细节即可。



### 进度

我现在终于成功的跳转到了loader的代码区，有必要说一下我的地址安排，0x7c00开始的512个字节是boot代码，也就是主引导扇区。接下来会把目录扇区读入到0x10000开始的内存，当找到loader之后，会开始解析fat表，此时会一次性将全部9个扇区的fat表全部读入0x10000开始的内存空间。然后开始逐个扇区将loader的内容加载进入内存，存储位置从0x11400开始。

但是这样就有一个问题，因为无论是bp还是其他的寄存器都是16位的，那么loader代码里面一旦涉及到引用内存的操作，道理上来说也应该是设置org的，按照上面的内存规划，应该是`org 11400`，但是16位的寄存器不可能设置20位的初始地址的，所以。。。。咋办呢？要么就是不要org，每次引用内存的时候都自行设置段地址和偏移地址。

这样的话，其实我有点好奇，也的确是又回到了汇编里面让我一直有疑问的问题。假设我让代码放在了`org 8c00`，然后如果代码很长，超过了64kb怎么办？

换句话说还是不同的段之间怎么寻址。

