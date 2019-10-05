### 图形编程与GUI和3D

我确实对图形化很感兴趣，我也在积极的尝试各种关于图形绘制，图形界面甚至3D图形学的工具。到目前为止，我尝试过python版的，例如pygame,turtle或者pyqt等，尝试过QT, Qt Quick，也尝试过前端，OpenGL，今天还稍微测试了一下基于简单的Windows API和GDI的图形接口，再稍微低级一点，当我尝试着写OS的时候，直接通过写入显存实现了简单的(也相当低效的)字符输出和图形绘制。

但是，我依旧觉得这不是我想要的，我想要一些更加简单，更加底层的知识，更加不依赖特定平台的，但是我也清楚知道这本身就是相互矛盾的，根本就是不可能的，显卡越来越复杂，甚至都是闭源的，根本没有办法知道底层知识，各个平台也都有自己的一套工具，DirectX，OpenGL，据说似乎苹果连OpenGL都不打算支持了？

像QT连手动编译我都没试过，只能依赖IDE；OpenGL总算是实现了手工编译，可是一大堆的动态静态链接库，头文件搞得我心力交瘁。

唉，好复杂呀。



我懂，其实我并没有说什么有用的东西。

所以，这一份笔记到底是干什么的？这一份笔记的目的是，帮助我记录一下我目前为止搜集到的，我觉得很有意思，但是也许暂时又不想学习的关于图形和游戏相关的工具和教程。

我最深切的体会就是，学习一些东西的时候，最重要也最困难的收找到自己应该学什么，(例如想学习C语言游戏编程，就需要知道应该尝试SDL)，开发环境的部署，以及一个好用的学习教程。

### Python

如果，你对python感兴趣，也不介意速度略慢，那么python绝对是做图形的一个非常好的选择，简单易懂，选择多样，用起来巨爽。

如果想做一些游戏，Pygame是个不错的选择，如果想做GUI，pyqt很不错，QT官方现在也似乎开始非常非常重视python的接口了，所以pyqt和pyside应该会变得越来越好用。

如果只想要一些更加特异化和简单的，其实也可以尝试一下matplotlib，其实都蛮好玩的。

PyOpenGL也是可以玩玩看的，但是，为什么要选择PyOpenGL呢？我宁愿选择OpenGL。



### C++和C

我现在非常想可以锻炼自己多用一些C和C++，因为它们很强，超厉害的。

如果使用这二者，你可以尝试一下Qt，Qt挺好的，现在官方应该更多在推广Qt Quick，以类似于前端的语法来做GUI也是很爽的，做一些高级的自定义部件，例如模仿iOS的滚轮时间选择器比Qt要便捷太多了。

Qt也可以直接用来做游戏，搞一些定时器什么的，至少做个自由落体的弹球还是很简单的。



如果你想尝试炒机激动人心的(同时也是蛮折磨人的)3D图形学，那么你应该尝试OpenGL。



想要更简单的，我就是随便画画，那么试试Windows API和GDI吧，在windows上，你不再需要去下载什么超级复杂的IDE，也不需要一堆的库(当然基本的mingw还是必须的)。关于教程的链接，去看一下我的windows API笔记。



前两天，我看了一篇文章，作者讲解了他为什么会选择使用C语言开发游戏，看了作者的网站，他的确做了好多游戏呀，但是，但是，最可惜的是，他完全没有写过自己是怎么做的，用的什么工具。我也想试试C语言，这些其实吧，你可以去谷歌搜索一下，应该能找到一些建议，这里我找到了一个，叫做[SDL](https://www.libsdl.org/)，这也是一个超级强的工具，但是强的代价就是也包含了一大堆头文件和库，根据说明，他是可以支持mingw的，这说明，也可以不用IDE，手动搞定一切，我喜欢。我还没试，这里是一些教程，我随便挑了几个。

- [这是CSDN上的中文教程](https://blog.csdn.net/lf426/article/category/364048/2)
- [这个是官方网站教程部分给出的一个推荐网站](http://www.sdltutorials.com/sdl-tutorial-basics)，不过是英格力士的。
- [这个网站更好](http://lazyfoo.net/tutorials/SDL/index.php)，这个也是官网推荐的英格力士的网站，上一个可以不用看了，这个网站可以选择系统，使用环境，编译器等，特别令我在意的是提供了mingw的使用和makefile，以及源码。



### 其它的

如果你使用HTML/CSS/JS，那么也可以试试canvas，粒子系统什么的，做个模仿烟花什么的还是很好玩的。



### 关于SDL

欧科，其实之所以会写这一份笔记，主要就是总结一下我知道什么图形化工具，另外就是说一下我新发现的SDL。

据我的了解，SDL是一个相当成熟的工具，有不少的挺好的游戏都是使用SDL完成的，现在的版本是`[2.0.10]`，看起来SDL2是一个大的版本。

我这里使用Windows系统，和Mingw64，不用IDE。(64位)

#### 下载

下载SDL，到[这里](https://www.libsdl.org/download-2.0.php)，只需要下载其中的Development Libraries中的`mingw 32/64bit`的`tar.gz`包，解压之后的文件夹中应该是已经make之后的库，其中最重要的就是`i686-w64-ming32`和`x86_64-w64-mingw32`两个文件夹，明显后者才是我们需要的64位的库。

#### 环境布置

在后者的文件夹中，应该包含`bin, include, lib, share`四个文件夹，按照习惯的规范，明显bin应该是运行时的动态链接库，include是头文件，lib是一些连接过程中要使用的静态链接库等，最后一个没啥用。

在bin文件夹里，需要取出其中的`SDL2.dll`动态链接库，放到和我们的代码同一目录下。然后把`include和lib`两个文件夹拷贝到代码同级目录下。

PS.你应该能发现其中`lib`文件夹下主要是一些库，`include`文件夹下应该有一个SDL2文件夹，其中是头文件。

#### 第一个测试代码

我们的第一个测试代码应该是这样的：

~~~c
// window.c
#include <stdio.h>

#include "SDL2/SDL.h"

const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;


int main(int argc, char *args[])
{
	SDL_Window* window = NULL;

	SDL_Surface* screen_surface = NULL;

	if(SDL_Init(SDL_INIT_VIDEO) < 0)
	{
		printf("SDL init fail ! SDL_Error: %s\n", SDL_GetError());
	}
	else
	{
		//Create window
        window = SDL_CreateWindow( "SDL Tutorial", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN );
        if( window == NULL )
        {
            printf( "Window could not be created! SDL_Error: %s\n", SDL_GetError() );
        }
        else
        {
			screen_surface = SDL_GetWindowSurface(window);

			SDL_FillRect(screen_surface, NULL, SDL_MapRGB(screen_surface->format, 0xFF, 0x00, 0XFF));

			SDL_UpdateWindowSurface(window);

			SDL_Delay(2000);        	
        }

	}

	SDL_DestroyWindow(window);

	SDL_Quit();

	return 0;
}
~~~

`Makefile`应该是这样的：

~~~makefile
headers = ./include
libs = ./lib

OBJS = window.c
OBJ_NAME = window

all : $(OBJS)
	gcc $(OBJS) -I$(headers) -L$(libs) -w -lmingw32 -lSDL2main -lSDL2 -o $(OBJ_NAME)
~~~

反正按照我的测试，这样是可以编译成功的。



需要特别注意的是，这个代码的`main`函数必须是带参的，如果不带参就会编译失败，至于原因，我在C语言笔记里面稍微做了一点解释。

另外，如果参考我给出的主要推荐的那个英文网站的教程，可以看到编译中有这样的参数`-Wl,-subsystem,windows`， 如果看一下解释，就会知道这个参数的意思是不让同时生成命令行窗口，特别主要这个参数必须这样写，逗号之间不能有空格之类的。当然如果无所谓有没有命令窗口，可以使用我上述的makefile。

如此。

如果想继续深入学习SDL，那么可以多看看这个网站，也可以看看官网上推荐的书，例如`SDL Game Development`。

如果，后面我决定多学一点SDL玩玩，也许会继续写更多关于SDL的学习笔记。

