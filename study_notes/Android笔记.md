# Android笔记

我学习Java的唯一目的就是为了Android服务，我希望可以开发一个应用，我希望可以控制硬件，windows应用也好，android应用也好，ios应用也好，但是windows的开发环境大到恐怖，ios的开发又需要MAC，所以我只能选择android

### 准备开发环境

首先我们必须在电脑上安装JDK，这个在java里面已经处理过了，我选择的开发环境是Android Studio，直接去官网下载，然后安装就好，安装的过程中并没有太多的讲究和困难，安装完成之后，打开还会给你继续安装SDK之类的。然后我们就可以创建一个项目了，可能要做一些选择，例如我们要选择一个什么形式的应用，暂时只需要选择空白的就可以。

然后当我们打开第一个应用的时候会遇到第一个问题所在，界面可能会卡在`Building xxx Application project info`类似的页面打不开，这是因为创建这个信息的过程中会使用一个叫做gradle的东西，默认会从谷歌下载，所以，你懂的，这是我们需要关掉软件，找到刚才创建的项目所在的文件夹，在它的`gradle\wrapper`里面找到`gradle-wrapper.properties`的配置文件，用sublime打开，他的最后一行是`distributionUrl=https\://services.gradle.org/distributions/gradle-3.3-all.zip`，这个指定了我们需要的gradle的版本，自己找个合适的地方去下载与要求完全一致的版本就好。

然后，不论你在安装的过程中选择的是什么文件夹，也不管你在哪里创建的工程，你总是可以在`C:\Users\stan han`找到一个名为`.gradle`的文件夹，在`.gradle\wrapper\dists\gradle-3.3-all\55gk2rcmfc6p2dg9u9ohc3hw9`里面放进刚才下载好的zip的gradle文件，不需要解压

此时重新打开软件，载入创建的项目，稍等就可以加载成功。

根据我的经验，有一定的可能性你打开之后发现整个页面啥也没有，这基本上说明创建的工程有问题，不需要在意，废掉，重新按照步骤来一遍就好，实在不行就继续重新创建，直到看到下面的页面：

![正常的页面](D:\html_file\images\安卓.PNG)

你应该注意到左侧目录项的上方是一个名字的project的选项，这说明下方显示的是项目的目录树，我们可以点击，选择Android，下方便会更新为android的目录树，这个才是我们常用的目录

这个目录下的结构应该是这样的：

![目录树](D:\html_file\images\dir_three.PNG)

一般情况下我们是要设置字体的，打开file选项卡，下面有设置，找到编辑器的字体，系统提供的样式是不能更改的，我们必须先save as保存我们自己的样式，然后就可以更改字体，字号等想要的设置了

开发环境的准备介绍到这里先。



### Android Studio介绍

我使用csnd上面名为Android开发之路里面关于目录的介绍来学习，网址为[参考学习网站](http://blog.csdn.net/eastmoon502136/article/details/50596806)

Android工程下面的app是主目录，里面的

>   manifests：
>
>   ​         AndroidManifest.xml：APP的配置信息
>
>   java：主要为源代码和测试代码
>
>   res：主要是资源目录，存储所有的项目资源
>
>   ​        drawable：存储一些xml文件，-*dpi表示存储分辨率的图片，用于适配不同的屏幕。
>
>   ​                           -mdpi:320x480
>
>   ​                           -hdpi:480x800、480x854
>
>   ​                           -xhdpi:至少960x720
>
>   ​                           -xxhdpi:1280x720
>
>   ​        layout：存储布局文件
>
>   ​        mipmap：存储原声图片资源
>
>   ​        values：存储app引用的一些值
>
>   ​                     - colors.xml：  存储了一些color的样式
>
>   ​                     - dimens.xml：存储了一些公用的dp值                       
>
>   ​                     - strings.xml： 存储了引用的string值
>
>   ​                     - styles.xml：   存储了app需要用到的一些样式
>
>   ​         Gradle Scripts:build.gradle为项目的gradle配置文件

Project工程下面的：

>   build：系统生成的文件目录，最后生成的apk文件就在这个目录，这里是app-debug.apk
>
>   libs：为项目需要添加的*.jar包或*.so包等外接库
>
>   src：项目的源代码，其中android test为测试包，main里为主要的项目目录和代码，test为单元测试代码

还有一些其他的东西，参考上述博客就好，不再记录



另外再推荐一个主要参考学习网站[参考网站](http://www.runoob.com/w3cnote/android-tutorial-contents.html)

