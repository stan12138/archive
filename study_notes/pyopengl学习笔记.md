## PyopenGL

> --by stan 
>
> -- 17.6.22

<font color="red"><b>最好的参考书是learnopengl_book,来自learnopengl.com</b></font>

发现了一个博客，基本上就是我现在看的书的英文译文：[参考博客](http://blog.csdn.net/ziyuanxiazai123/article/category/2107037/3)

还有人做了完整的翻译！[译文](https://learnopengl-cn.github.io/07%20PBR/01%20Theory/)

这个似乎也可以[教程](https://www.kancloud.cn/kancloud/opengl-tutorials/77864)

[好多呀](https://learnopengl-cn.readthedocs.io/zh/latest/06%20In%20Practice/02%20Text%20Rendering/)

### 环境构建

哇，之前竟然忘记记录一下我是怎么构建环境的，然后现在又费了九牛二虎之力去重新翻看youtube

地址就不粘了，去github上，我fork了一个opengl的教程，里面的readme里面给了作者的youtube链接

我并不清楚为什么要使用glfw，然后作者又开了一系列新的教程，使用glet

记得最初的时候网上推荐使用glut，现在说glut过时了，于是用了glfw，至于glet又是什么我也不知道

我只知道他们是一系列用于窗口创建和事件管理的库。

好了，废话不多说。

`pip install glfw`然后是`pip install pyopengl`

的确有一个pyglfw，但是我们要的不是它

然后运行你的程序，十之八九你会发现并不行。此时去glfw的官网，下载64位的glfw安装包，解压，把lib-vc2015里面的glfw3.dll文件拷贝至c盘的windows文件夹下，即可。



### GLSL

首先很有必要搞清GLSL的语法。 

##### 基本数据类型

	float   32位
	double  64位
	int     32位
	uint    32位
	bool
变量必须声明，除内置变量外

##### 聚合类型

聚合类型指的是含有多个分量的数据结构，一维的是向量vec，多维的是矩阵mat。  

其中向量和矩阵均有多种细分类型，如vec2,vec3等，不再细说。  

更多的向量和矩阵的初始化，截断，增长不再细说。  

向量的索引支持从0开始的下标索引，同时支持`rgba,xyzw,stpq`三组名称索引，同时可以使用诸如`color.xyz`这种方式同时拿到三个位置的数据。  

很多细节不再详尽描述

##### 存储限制符

	const    常量
	in       输入
	out      输出
	uniform  传递来的常量
	buffer   共享内存块
	shared   本地共享，只用于计算着色器

##### 计算不变性
为保证计算不变性可以使用关键字`invariant`或`precise`  



### glfw

使用glfw来创建窗口，不准备做太多的说明，下面会提供两个版本的基本程序，其中一个复杂版，一个简化版，两个均可工作，我并不太清楚复杂版好在哪  

复杂版 

~~~python
import glfw
from OpenGL.GL import *

(WIDTH, HEIGHT) = (800, 600)

def key_callback(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)

def main():
    if not glfw.init():
        return

    window = glfw.create_window(WIDTH, HEIGHT, "Hello World", None, None)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)
    if not window:
        glfw.terminate()
        return -1
    glfw.make_context_current(window)

    (width, height) = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)

    glfw.set_key_callback(window, key_callback)

    glClearColor(0.2, 0.3, 0.3, 1.0)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
~~~

​    



简化版  

~~~python
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy


def main():

    # initialize glfw
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "My OpenGL window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glClearColor(0.2, 0.3, 0.2, 1.0)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
~~~



关于glfw的上述代码，没有什么需要特别说明的  

### shader

对于每一个最基本的代码，我们必须编写至少两个着色器，其中一个是vertex shader,另一个是fragment shader。前者控制绘制像素时的位置，后者控制颜色。  

在顺序上，前者在前，后者在后，换句话说前者的输出可以做为后者的输入。截止到目前为止，我所接触的代码往往把所有需要输入的变量写在顶点着色器中。  

对于两个着色器，顶点着色器要求将顶点数据交给一个GLSL内置的变量gl_Position，这是一个四分量向量，片元着色器要求有一个输出，变量名不限，输出的这个变量是四分量颜色值。  

下面给出两个最基本的着色器：

~~~python
    v_shader = """
    #version 330
    in vec3 position;
    in vec3 color;
    out vec4 final_color;
    
    void main()
    {
       gl_Position = vec4(position,1.0f);
       final_color = vec4(color,1.0f);
    }
    """
    
    f_shader = '''
    #version 330
    in vec4 final_color;
    
    out vec4 f_color;
    
    void main()
    {
       f_color = final_color;
    }
    '''
~~~

有了着色器源码之后，下一步需要将着色器编译，连接，使用如下代码：  

~~~python
	vertex_shader = OpenGL.GL.shaders.compileShader(v_shader, GL_VERTEX_SHADER)
	fragment_shader = OpenGL.GL.shaders.compileShader(f_shader, GL_FRAGMENT_SHADER)
	shader = OpenGL.GL.shaders.compileProgram(vertex_shader, fragment_shader)
	。。。。。
	glUseProgram(shader)
~~~

### VBO与EBO
我会把顶点数据存储在数组中，同时OpenGL要求这些数据必须放入缓存。所以需要执行以下操作：  
~~~python
	vertex = [
	         0.5, 0.5, 0.0,  1.0,0.0,0.0,
	        -0.5, 0.5, 0.0,  0.0,1.0,0.0,
	        -0.5,-0.5, 0.0,  1.0,0.0,0.0,
	         0.5,-0.5, 0.0,  0.0,1.0,0.0
	        ]
	
	index = [0,1,2,  2,3,0]
	
	vertex = np.array(vertex,dtype=np.float32)
	index = np.array(index,dtype=np.uint32)    #此处绝对不能使用GLSL中没有的类型，如uint8
	
	VBO = glGenBuffers(1)
	EBO = glGenBuffers(1)
	
	glBindBuffer(GL_ARRAY_BUFFER,VBO)
	glBufferData(GL_ARRAY_BUFFER,4*len(vertex),vertex,GL_STATIC_DRAW)
	
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,EBO)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER,4*len(index),index,GL_STATIC_DRAW)
~~~

习惯的操作就是把所有的顶点，甚至顶点的颜色值聚合在一起，然后使用一个索引数组确定哪些顶点组成一个几何元素。顶点和其他数据聚合成的叫VBO，索引聚合成的叫EBO,有些东西看上述代码就能明白，我就不再过多叙述。  

关于上述代码的后半部分就是分配缓存，绑定，连接数据的过程，我觉得也能看懂，至于glBufferData函数里面个参数的意义，可以自己找资料看。

### 数据传入着色器
有了着色器，有了存入缓存的数据，下一步我们需要做的操作就是把数据传递给着色器。  

~~~python
    position = glGetAttribLocation(shader,'position')
    glVertexAttribPointer(position,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)
    
    color = glGetAttribLocation(shader,'color')
    glVertexAttribPointer(color,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)
~~~

这段代码的意思大概也很明了，首先获取着色器程序中in变量的位置引用，然后使用glVertexAttribPointer函数给变量赋值。关于这个函数，第二个参数指的是每一个点的position有几个数值组成，三分量自然是3，在接下来两个参数第一个指类型，第二个现在不需要知道。接下来一个指的是两个相邻的点的数据之间的间隔是多少字节，明显两者之间有三个顶点数据和三个颜色数据共24字节，最后一个量指的是第一个数据在缓存中的起始地址偏移量是多少。  

从这里其实可以看出有了这个函数程序会自动按照间隔和起始偏移量从缓存中取出所有的数据，传递到着色器中。  

至于ctypes.c_void_p(0)，ctypes.c_void_p(12)为什么要这样写，记住必须是c类型就好了（这里是经过测试的），为什么是12不需要解释吧。  

其实，还用另外一种写法，他会在着色器源码中为in变量再加一个layout(location=0),layout(location=1)诸如此类的描述符，这样可以让他省掉position = glGetAttribLocation(shader,'position')，直接在glVertexAttribPointer(position,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(0))中使用0代替position，详细的代码如下：

~~~python
vertex_shader_source = """
#version 330 core

layout (location = 0) in vec3 position;

void main()
{
    gl_Position = vec4(position, 1.0f);
}
"""
。。。。。
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(0)
~~~



但是，我不太喜欢，也不完全理解，所以我拒绝使用这种方法。

<u>再次声明，注意一点：数据类型是float32时，每个数据是4字节，而不是8字节，我在这个问题上已经吃过很多亏了</u>

### 使用EBO绘制矩形

这里不做很多的解释，只提供一个代码，代码里面省略了shader_loader的代码，和shader，两个shader都很简单，颜色都是一样的，没有传入颜色数据

~~~python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 18:05:10 2017

@author: stan han
"""

import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
import OpenGL.GL
from numpy import array,float32,uint32,pi
from shader_loader import My_shader

def main() :
    
    if not glfw.init() :
        return
    window = glfw.create_window(600,600,'my window',None,None)
    if not window :
        glfw.terminate()
        return
    glfw.make_context_current(window)
    
    point = array([-0.5,0.5,0,   0.5,0.5,0, 0.5,-0.5,0,  -0.5,-0.5,0],dtype=float32)
    index = array([0,1,2,2,3,0],dtype=uint32)
    shader = My_shader('v.vs','f.frags')
    shader.use()
    
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,vbo)
    glBufferData(GL_ARRAY_BUFFER,4*len(point),point,GL_STATIC_DRAW)
    
    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER,4*len(index),index,GL_STATIC_DRAW)
    
    glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,3*4,ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    glClearColor(0.2,0.3,0.2,1.0)
    #glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    
    while not glfw.window_should_close(window) :
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        
        glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_INT,None)
        
        glfw.swap_buffers(window)
        
    glfw.terminate()
    
    
if __name__ == "__main__" :
    main()
~~~

在这一段代码里，我们要注意，基本上除了我们添加了一个EBO的buffer，并且把绘制方式从glDrawArrays换成了glDrawElements之外，并没有太多的区别，这里绝对要注意的一个问题是，glDrawElements的最后一个参数，按照我看的资料上面说是偏置，应该设置为0，但是事实上，在python里，如果你设置为0，将会啥也不显示，必须设置为None

在接下来的一块里，我要详细说明一下重要函数的参数意义

### 参数

`glBufferData(GL_ARRAY_BUFFER,4*len(point),point,GL_STATIC_DRAW)`

这个函数是为了向buffer里面传入参数，第一个是类型，基本上都是GL_ARRAY_BUFFER，第二个是数据的总字节数，还是那句话，float32每个数据是4字节，而不是8，第三个参数是数据，第四个参数指定了你想把这些数据设置为什么类型，或者说想让显卡怎么管理这些数据，GL_STATIC_DRAW意味着很少改动，GL_DYNAMIC_DRAW常改变，GL_STREAM_DRAW每次绘制时都会改变，我们常用第一种

`glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,3*4,ctypes.c_void_p(0))`

这个参数是一个指示器，告诉显卡数据的结构。第一个参数是我们想设置哪一个数据，如果我们使用了layout的话，可能会是0，1这样的数字就可以，否则的话我们需要先用`glGetAttribLocation(shader,'position')`这个函数获得着色器内变量的引用，然后把返回值作为第一个参数。第二个参数说明每一个顶点有几个分量，我们通常给的数据都是3分量的，然后由着色器把它变成4分量的。第三个是类型。第四个是数据是否需要归一化，我们传入的数据一般已经转换到了0-1之间，就不需要了，设置为GL_FALSE即可。第五个数据是间隔，也就是第一个顶点的第一位数据与第二个顶点的第一位数据间隔是多少，三分量的情况下就是有三个数据间隔，每个4字节。第六个数据是数据在buffer里面的偏移，这里就是0，但必须是ctype

`glDrawArrays(GL_TRIANGLES,0,3)`

第一个参数是我们想绘制什么类型的对象。第二个指定我们从第几个顶点开始，一般是0，第三个是要绘制几个顶点。

`glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_INT,None)`

第二个参数是一共有几个顶点，第三个是类型，第四个是偏移，必须是None，但是在c++里面他们使用0

最后说一下注意在ebo的时候，我们的顶点也应该是4字节的，大概GL_UNSIGNED_INT就是4字节的。



### 绘制

当这些工作完成之后，接下来需要的就是在主事件循环中绘制即可。  

据我的观察，当没有索引数据时，换句话说只有一个三角形是，他们会使用glDrawArrays(GL_TRIANGLES, 0, 3)，当要使用索引绘制多个三角形时，他们会使用glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_INT,None)，至于这两个函数参数的意义我不多叙述。

### 一个完整的代码

~~~python
import glfw
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders

def main() :
    if not glfw.init() :
        return
    
    window = glfw.create_window(800,600,"stan's first example",None,None)
    
    if not window :
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    
    vertex = [
             0.5, 0.5, 0.0,  1.0,0.0,0.0,
            -0.5, 0.5, 0.0,  0.0,1.0,0.0,
            -0.5,-0.5, 0.0,  1.0,0.0,0.0,
             0.5,-0.5, 0.0,  0.0,1.0,0.0
            ]
    
    index = [0,1,2,  2,3,0]
    
    vertex = np.array(vertex,dtype=np.float32)
    index = np.array(index,dtype=np.uint32)    #此处绝对不能使用GLSL中没有的类型，如uint8
    
    
    v_shader = """
    #version 330
    in vec3 position;
    in vec3 color;
    out vec4 final_color;
    
    void main()
    {
       gl_Position = vec4(position,1.0f);
       final_color = vec4(color,1.0f);
    }
    """
    
    f_shader = '''
    #version 330
    in vec4 final_color;
    
    out vec4 f_color;
    
    void main()
    {
       f_color = final_color;
    }
    '''
    vertex_shader = OpenGL.GL.shaders.compileShader(v_shader, GL_VERTEX_SHADER)
    fragment_shader = OpenGL.GL.shaders.compileShader(f_shader, GL_FRAGMENT_SHADER)
    shader = OpenGL.GL.shaders.compileProgram(vertex_shader, fragment_shader)
    
    
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)
    
    glBindBuffer(GL_ARRAY_BUFFER,VBO)
    glBufferData(GL_ARRAY_BUFFER,4*len(vertex),vertex,GL_STATIC_DRAW)
    
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER,4*len(index),index,GL_STATIC_DRAW)
    
    
    position = glGetAttribLocation(shader,'position')
    glVertexAttribPointer(position,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)
    
    color = glGetAttribLocation(shader,'color')
    glVertexAttribPointer(color,3,GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)
    
    
    glUseProgram(shader)
    glClearColor(0.2,0.3,0.2,1.0)
    
    while not glfw.window_should_close(window) :
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        
        
        glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_INT,None)
        
        glfw.swap_buffers(window)
        
    glfw.terminate()
    
    
if __name__ == '__main__' :
    main()
~~~



这是我写的与上述笔记完全一致的示例代码。  

总而言之，我们需要完成的工作就是：创建窗口相关的事务，创建顶点数据，存入缓存，创建着色器并编译链接，传入数据进入着色器，绘制。  

### VAO

我剔除了关于VAO的内容，其实VAO的使用代码并不复杂，但是我始终搞不懂VAO是干什么的，又是怎么做的，并且从上述代码可以看出没有它也可以，所以，我就暂时不加VAO，留待后续。

现在说明一下什么是VAO，还有一些小的细节，我会在obj模型导入的部分做一些说明

首先声明VAO可以说并不是一种绝对必不可少的存在，至少现在是，使用它更多是出于结构化，便于操作的角度执行的，以及一些优化等角度。

当然，我说的这一切都是建立在我只载入一个物体的角度上实现的，我还没有做过导入多个模型或物体的尝试，但是我看了一些使用VAO完成多个物体导入的代码，结构很清晰，于是我决定开始使用VAO

当我们使用VAO的时候基本上就是把VBO和EBO包装了起来，在之前，我们初始化一个VBO的缓存，然后存入数据，到之后的某个位置，我们会再使用pointer指定数据在VBO中的位置。这样的问题就在于，直至程序要进行渲染的时候他才知道缓存中的数据都代表了什么含义，这并不是一种很结构化很规范的方式。于是我们将引入VAO

我们每设置一个VAO就相当于把VBO和EBO装进了一个箱子中，同时使用它的pointer指明数据的位置，然后当我们想进行绘制的时候，只需要再调用某一个VAO即可。

我们首先就要把VBO和EBO什么的统一绑进VAO，然后完成导入数据，指示数据位置之后，我们应该解除VAO的绑定

当你绘制的时候应该首先绑定VAO，然后绘制，绘制结束之后再解除绑定

例如：

~~~python
	vao = glGenVertexArrays(1)
	vbo = glGenBuffers(1)
	ebo = glGenBuffers(1)

	glBindVertexArray(vao)
	glBindBuffer(GL_ARRAY_BUFFER,vbo)
	glBufferData(GL_ARRAY_BUFFER,4*len(point),point,GL_STATIC_DRAW)
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8*4,ctypes.c_void_p(0))
	glEnableVertexAttribArray(0)
	glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,8*4,ctypes.c_void_p(12))
	glEnableVertexAttribArray(1)
	glVertexAttribPointer(2,3,GL_FLOAT,GL_FALSE,8*4,ctypes.c_void_p(20))
	glEnableVertexAttribArray(2)
	
	#glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ebo)
	#glBufferData(GL_ELEMENT_ARRAY_BUFFER,4*len(index),index,GL_STATIC_DRAW)
	glBindVertexArray(0)
~~~

绘制：

~~~python
		glBindVertexArray(vao)
		glDrawArrays(GL_TRIANGLES, 0, 36);
		glBindVertexArray(0)
~~~



### 结构化

接下来的任务是创建一段代码，可以从文件中导入着色器，并经过类的封装使其更加易用。  

vertex shader和fragment shader各自写一个文件，再定义一个shader类，它可以将shader源码文件读到字符串里面，然后编译连接成程序，并提供一个use方法。

~~~python
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 10:50:10 2017

@author: stan han
"""
__all__ = ['My_shader']

from OpenGL.GL import *
import OpenGL.GL.shaders


class My_shader:
    
    def __init__(self,v_path,f_path) :
        
        with open(v_path,'r') as v_file :
            v_source = v_file.read()


        with open(f_path,'r') as f_file :
            f_source = f_file.read()


        v_shader = OpenGL.GL.shaders.compileShader(v_source,GL_VERTEX_SHADER)
        f_shader = OpenGL.GL.shaders.compileShader(f_source,GL_FRAGMENT_SHADER)
        self.shader = OpenGL.GL.shaders.compileProgram(v_shader, f_shader)

    def use(self) :
        glUseProgram(self.shader)

    def setvec3(self,name,a,b,c) :
        loc = glGetUniformLocation(self.shader,name)
        glUniform3f(loc,a,b,c)
~~~

这个很简单明白，不再细说。  

### Texture

texture的坐标系为左下角为（0，0）的笛卡尔坐标系，范围为0~1。  

首先，我们必须改造顶点数据，在坐标，颜色之外再增加一个两分量的对应的texture的坐标。  

#### 纹理包装

纹理包装指定了如果坐标超出了范围，我们应该如何扩展纹理图片。

-   `GL_REPEAT`，默认行为
-   `GL_MIRRORED_REPEAT`，以镜像的方式重复
-   `GL_CLAMP_TO_EDGE`，把边缘拉长
-   `GL_CLAMP_TO_BORDER`，超出范围的统一指定为用户给出的颜色

包括下面的一些，我们都是使用`glTexParameter*`函数设置，这里是i

`glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_MIRRORED_REPEAT)`

第一个参数说明texture是几维的，我们可以分别设置垂直方向和水平方向，通过第二个参数，最后一个字母分别是S或T。最后一个就不说了

#### 纹理滤波器

还记得双线性内插法吗？差不多是同样的意思，为了解决坐标点不是整数的问题，可以指定两种方法，线性或者是近邻，同时可以为缩放各自指定不同的方法。

`GL_LINEAR`和`GL_NEAREST`

`glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)`

我们可以通过第二个参数分别设置缩放两种行为，`MAG`是放大，`MIN`是缩小

##### 纹理映射

当一个图形距离我们很远的时候，我们是没有必要原样计算纹理的，因为已经看不清了，我们可以通过纹理映射产生一系列的不同尺寸纹理，然后在不同的距离应用不同的纹理。

这种情况下产生的mipmap实际上是一系列的纹理，每一个的面积都是前者的开根，所以我们在滤波的时候要选择两种方式，首先，我们应该如何选择合适的纹理，是选择最接近的纹理还是在相邻两个纹理之间插值产生新的纹理，然后还要决定对于得到的纹理，我们如何滤波，所以：

`GL_NEAREST_MIPMAP_NEAREST`

`GL_LINEAR_MIPMAP_NEAREST`

这两个都是选择最接近的纹理，然后滤波

`GL_NEAREST_MIPMAP_LINEAR`

`GL_LINEAR_MIPMAP_LINEAR`

这两个是插值得到新纹理

注意纹理映射只能用在缩小的时候，而绝对不能是放大

`glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)`

#### 纹理使用步骤

首先要为texture分配一个ID：`texture = glGenTextures(1)`.  

然后是绑定：`glBindTexture(GL_TEXTURE_2D,texture)`  

再后是设置一些必要的参数：

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)	
##### 载入数据

	image = Image.open('../textures/wall.jpg')
	img_data = numpy.array(image, numpy.uint8)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
	glGenerateMipmap(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, 0)

`glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)`

第一个参数是纹理类型。第二个是如果你想手工设置纹理映射级别，那么你可以指定纹理的映射级别，这里设为0即可。第三个是格式。第四五个是宽高。第六个永远是0。第七八个也是格式。最后一个是数据



我们需要使用同样的方式获取纹理的坐标。然后在应用的时候，主要是位于片元着色器。我们可以声明一个`uniform sampler2D`的变量，名字随意，系统会自动把纹理传递给它，然后只需要把纹理赋值给片元着色器的输出即可`final_color = texture(te,texc);`，这里的texture是内置的专门处理纹理的函数，第一个参数是纹理，第二个是坐标。

这里给出一个参考代码：

~~~python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 18:05:10 2017

@author: stan han
"""

import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
import OpenGL.GL
from numpy import array,float32,uint8,uint32,pi
from shader_loader import My_shader
from PIL import Image

def main() :
    
    if not glfw.init() :
        return
    window = glfw.create_window(600,600,'my window',None,None)
    if not window :
        glfw.terminate()
        return
    glfw.make_context_current(window)
    
    point = array([-0.5,0.5,0,0,1,   0.5,0.5,0,1,1,  0.5,-0.5,0,1,0,  -0.5,-0.5,0,0,0],dtype=float32)
    index = array([0,1,2,2,3,0],dtype=uint32)
    shader = My_shader('v.vs','f.frags')
    shader.use()
    
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,vbo)
    glBufferData(GL_ARRAY_BUFFER,4*len(point),point,GL_STATIC_DRAW)
    
    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER,4*len(index),index,GL_STATIC_DRAW)
    
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,texture)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    image = Image.open('textures/wall.jpg')
    image = array(image,dtype=uint8)
    height,width,c = image.shape
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    glGenerateMipmap(GL_TEXTURE_2D)
    
    glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,5*4,ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,5*4,ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    
    glClearColor(0.2,0.3,0.2,1.0)
    #glEnable(GL_DEPTH_TEST)
    #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    
    while not glfw.window_should_close(window) :
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        
        glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_INT,None)
        
        glfw.swap_buffers(window)
        
    glfw.terminate()
    
    
if __name__ == "__main__" :
    main()
~~~

~~~
#version 330

layout (location=0) in vec3 position;
layout (location=1) in vec2 tex;

out vec2 texc;

void main()
{
	
	gl_Position = vec4(position.x,position.y,position.z,1.0f);
	texc = tex;

}
~~~

~~~
#version 330

out vec4 final_color;

in vec2 texc;

uniform sampler2D te;

void main()
{
	final_color = texture(te,texc);
}
~~~

当然我们还可以让颜色和纹理混合，只需要通过普通的方式拿到颜色，变成vec4，然后和texture函数相乘即可。

#### 纹理单元

名字怪怪的。

我们为什么将纹理设置为了uniform，但是却没有为它通过glUniform设置值，这就是纹理单元在起作用，绝大多数显卡会默认设置纹理单元为0，总之效果就是自动赋值。我们可以为其设置位置，从而实现多重纹理。

纹理单元类似于一个存储格子，我们每激活一个格子就可以绑定一个buffer，存储一张纹理，0号是默认被激活的。

步骤：

首先激活纹理单元：

~~~python
    texture1 = glGenTextures(1)
    texture2 = glGenTextures(1)
    
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D,texture1)
    
    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D,texture2)
~~~

然后载入图像，别无二致

接下来设置pointer：

~~~python
    glUniform1i(glGetUniformLocation(shader.shader,'te'),0)
    glUniform1i(glGetUniformLocation(shader.shader,'te1'),1)
~~~

然后改写片元着色器

~~~python
#version 330

out vec4 final_color;

in vec2 texc;
in vec4 co;

uniform sampler2D te;
uniform sampler2D te1;
void main()
{
	final_color = mix(texture(te,texc)*co,texture(te1,texc),0.2);
}
~~~

要注意的地方是，glUniform1i的后缀是数字1然后是i，而不是字母l

wahaha，真神奇，很早之前我在做立方体贴图的时候就出现了某些图片会严重变形的问题，变形的情况还比较复杂，而不是单纯的颠倒。现在我又一次碰到了，然后我解决了。我无法解释为什么，但是你只要记得就好，如果图片的长宽不是2的N次方，就会出现变形，差距越大，变形越严重。

#### 图片导入技术

图片的导入并没有之前的代码那么简单

我们要分情况来说，首先基本上所有的图片，我们都需要做一下上下倒置的工作

然后对于普通格式的图片，或者是没有alpha通道的PNG图片，我们需要的是获取尺寸信息，然后转换为二进制：

~~~python
    image = Image.open('textures/wall.jpg')
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    
    #image = array(image,dtype=uint8)
    height,width= image.height,image.width
    
    image = image.tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    glGenerateMipmap(GL_TEXTURE_2D)
~~~

并不需要numpy参与，就可以完成

然后对于	有alpha通道的PNG图片，我们需要额外增添一步转换为RGBA的操作，并且数据导入到buffer的时候格式也要更改

~~~python
    image = Image.open("res/smiley.png")
    #img_data = numpy.array(list(image.getdata()), numpy.uint8)
    flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = flipped_image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
~~~

#### 纹理混合技术

特别要注意的是，由于采用了多个纹理，我们必须在做两次Bind，第一次在初始化纹理单元的时候，第二次在导入数据之后

虽然很长，这里还是再给出一个例子：

~~~python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 18:05:10 2017

@author: stan han
"""

import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
import OpenGL.GL
from numpy import array,float32,uint8,uint32,pi
from shader_loader import My_shader
from PIL import Image

def main() :
    
    if not glfw.init() :
        return
    window = glfw.create_window(600,600,'my window',None,None)
    if not window :
        glfw.terminate()
        return
    glfw.make_context_current(window)
    
    point = array([-0.5,0.5,0,1,0,0,0,1,   0.5,0.5,0,0,1,0,1,1,  0.5,-0.5,0,0,0,1,1,0,  -0.5,-0.5,0,1,1,0,0,0],dtype=float32)
    index = array([0,1,3,1,2,3],dtype=uint32)
    shader = My_shader('v.vs','f.frags')
    shader.use()
    
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,vbo)
    glBufferData(GL_ARRAY_BUFFER,4*len(point),point,GL_STATIC_DRAW)
    
    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER,4*len(index),index,GL_STATIC_DRAW)
    
    texture1 = glGenTextures(1)
    
    
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D,texture1)
    
    image = Image.open('textures/wall.jpg')
    height,width = image.height,image.width
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image = image.convert("RGB").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    glGenerateMipmap(GL_TEXTURE_2D)
    
    glBindTexture(GL_TEXTURE_2D,texture1)
    
    
    
    texture2 = glGenTextures(1)
    
    
    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D,texture2)
    image1 = Image.open('textures/smile.png')
    image2 = image1.transpose(Image.FLIP_TOP_BOTTOM)
    image2 = image2.convert("RGBA").tobytes()
    height,width = image1.height,image1.width
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image2)
    glGenerateMipmap(GL_TEXTURE_2D)    
    
    glBindTexture(GL_TEXTURE_2D,texture2)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    

    

    
    glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,8*4,ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,8*4,ctypes.c_void_p(24))
    glEnableVertexAttribArray(1)
    
    glVertexAttribPointer(2,3,GL_FLOAT,GL_FALSE,8*4,ctypes.c_void_p(12))
    glEnableVertexAttribArray(2)
    
    glUniform1i(glGetUniformLocation(shader.shader,'te'),0)
    glUniform1i(glGetUniformLocation(shader.shader,'te1'),1)
    
    glClearColor(0.2,0.3,0.2,1.0)
    #glEnable(GL_DEPTH_TEST)
    #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    
    while not glfw.window_should_close(window) :
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        
        glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_INT,None)
        
        glfw.swap_buffers(window)
        
    glfw.terminate()
    
    
if __name__ == "__main__" :
    main()
~~~

所以，纹理的处理变得越来越长，大概很快就要在写一个帮助的模块了。

注意这里，为了对同一个shader使用多个纹理，我们使用了`glActiveTexture(GL_TEXTURE0)`

最多大概可以激活16个，我记得。但是，再次声明，这是对于同一个着色器，如果是不同的着色器，就不必这样。

纹理部分暂时到此结束



### 坐标系统

在这里，最重要的变换矩阵有三个，model,view,projection

第一个负责从模型坐标空间转换至世界坐标空间

第二个负责从世界坐标空间转换至相机坐标空间

第三个负责投影

总之在他的世界里，我们应该对物体的坐标进行这样的转换`gl_Position = projection*view*model*vec4(position.x,position.y,position.z,1.0f);`

暂时我并不打算继续深入这一部分，乃至完成相机，而是将直接学习光照，所以这里将给出一个例子,作为结束：

~~~python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 18:05:10 2017

@author: stan han
"""

import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
import OpenGL.GL
from numpy import array,float32,uint8,uint32,pi
from shader_loader import My_shader
from PIL import Image
import pyrr
from math import radians
from time import time


def main() :
	
	
	if not glfw.init() :
		return
	window = glfw.create_window(600,600,'my window',None,None)
	if not window :
		glfw.terminate()
		return
	glfw.make_context_current(window)
	point = [-0.5, -0.5, 0.5, 0.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            -0.5, 0.5, -0.5, 0.0, 1.0,

            0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, -0.5, 0.5, 0.0, 1.0,

            -0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, -0.5, -0.5, 1.0, 0.0,
            -0.5, -0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 1.0,

            0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, 0.5, -0.5, 1.0, 0.0,
            -0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, 0.5, 0.5, 0.0, 1.0]
	point = array(point,dtype=float32)
	#point = array([-0.5,0.5,0,1,0,0,0,1,   0.5,0.5,0,0,1,0,1,1,  0.5,-0.5,0,0,0,1,1,0,  -0.5,-0.5,0,1,1,0,0,0],dtype=float32)
	
	index = [0, 1, 2, 2, 3, 0,
               4, 5, 6, 6, 7, 4,
               8, 9, 10, 10, 11, 8,
               12, 13, 14, 14, 15, 12,
               16, 17, 18, 18, 19, 16,
               20, 21, 22, 22, 23, 20]
	index = array(index,dtype=uint32)
	
	#index = array([0,1,3,1,2,3],dtype=uint32)
	shader = My_shader('v.vs','f.frags')
	shader.use()
	
	vb = pyrr.matrix44.create_from_y_rotation(radians(70))
	
	model = pyrr.matrix44.create_from_x_rotation(radians(-55))
	view = pyrr.matrix44.create_from_translation(array([0,0,-6]))
	projection = pyrr.matrix44.create_perspective_projection_matrix(45,1,0.1,100)
	
	
	
	
	vbo = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER,vbo)
	glBufferData(GL_ARRAY_BUFFER,4*len(point),point,GL_STATIC_DRAW)
	
	ebo = glGenBuffers(1)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,ebo)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER,4*len(index),index,GL_STATIC_DRAW)
	
	texture1 = glGenTextures(1)
	
	
	glActiveTexture(GL_TEXTURE0)
	glBindTexture(GL_TEXTURE_2D,texture1)
	
	image = Image.open('textures/container.jpg')
	height,width = image.height,image.width
	image = image.transpose(Image.FLIP_TOP_BOTTOM)
	image = image.convert("RGB").tobytes()
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
	glGenerateMipmap(GL_TEXTURE_2D)
	
	glBindTexture(GL_TEXTURE_2D,texture1)
	
	
	
	texture2 = glGenTextures(1)
	
	
	glActiveTexture(GL_TEXTURE1)
	glBindTexture(GL_TEXTURE_2D,texture2)
	image1 = Image.open('textures/smile.png')
	image2 = image1.transpose(Image.FLIP_TOP_BOTTOM)
	image2 = image2.convert("RGBA").tobytes()
	height,width = image1.height,image1.width
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image2)
	glGenerateMipmap(GL_TEXTURE_2D)	
	
	glBindTexture(GL_TEXTURE_2D,texture2)
	
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	

	

	
	glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,5*4,ctypes.c_void_p(0))
	glEnableVertexAttribArray(0)
	
	glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,5*4,ctypes.c_void_p(12))
	glEnableVertexAttribArray(1)
	
	#glVertexAttribPointer(2,3,GL_FLOAT,GL_FALSE,8*4,ctypes.c_void_p(12))
	#glEnableVertexAttribArray(2)
	
	
	m_loc = glGetUniformLocation(shader.shader,'model')
	glUniformMatrix4fv(m_loc,1,GL_FALSE,model)
	
	my_loc = glGetUniformLocation(shader.shader,'modely')
	glUniformMatrix4fv(my_loc,1,GL_FALSE,vb)
	
	v_loc = glGetUniformLocation(shader.shader,'view')
	glUniformMatrix4fv(v_loc,1,GL_FALSE,view)
	
	p_loc = glGetUniformLocation(shader.shader,'projection')
	glUniformMatrix4fv(p_loc,1,GL_FALSE,projection)
	
	
	
	glUniform1i(glGetUniformLocation(shader.shader,'te'),0)
	glUniform1i(glGetUniformLocation(shader.shader,'te1'),1)
	
	glClearColor(0.2,0.3,0.2,1.0)
	glEnable(GL_DEPTH_TEST)
	#glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
	start = time()
	while not glfw.window_should_close(window) :
		glfw.poll_events()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		model = pyrr.matrix44.create_from_x_rotation(radians((time()-start)*10))
		m_loc = glGetUniformLocation(shader.shader,'model')
		glUniformMatrix4fv(m_loc,1,GL_FALSE,model)
		glDrawElementsInstanced(GL_TRIANGLES, len(index), GL_UNSIGNED_INT, None, 125000)
		
		glfw.swap_buffers(window)
		
	glfw.terminate()
	
	
if __name__ == "__main__" :
	main()
  
~~~

shader：

~~~c
#version 330

layout (location=0) in vec3 position;
layout (location=1) in vec2 tex;

out vec2 texc;



uniform mat4 model;
uniform mat4 modely;
uniform mat4 view;
uniform mat4 projection;


void main()
{
	
	gl_Position = projection*view*modely*model*vec4(position.x,position.y,position.z,1.0f);
	texc = tex;

}


#version 330

out vec4 final_color;

in vec2 texc;


uniform sampler2D te;
uniform sampler2D te1;
void main()
{
	final_color = mix(texture(te,texc),texture(te1,texc),0.2);
}


~~~



注意，这里面涵盖了立方体的产生，双重纹理，旋转等



okay，继续来进行这一部分，这一次将会连续进行，直至完成一个相机。

再次说回坐标空间与矩阵变换。

从模型空间到世界空间，完成的是如何将模型安置在世界坐标系中，我们可以进行模型的平移旋转，换句话说我们可以通过调整model矩阵实现模型的任意位置与姿态调整。

当模型进入世界坐标空间，我们就可以在模型之外安置相机了。当然我们可以做任意的简化，例如直接将相机安置在原点处，保持标准姿态，那么将意味着我们几乎不需要什么变换，当然我们也可以平移相机。但是如果我们想实现一个相机，我们就必须考虑最复杂的状态，相机即不在原点，姿态也并非标准。这种情况下，所谓视变换，或者说从世界坐标系到相机坐标系的变换就是实现一个新的坐标系，以相机的指向为z轴负方向，相机的上为y轴正向，相机的正右方向为x轴正向。

首先，我们要确定相机的指向，即forward向量，这个向量可以由两个坐标确定，即相机的位置pos，和目标的位置target，那么forward向量就是target-pos(注意这个方向实际上是z轴负向)

然后我们要谋求右向量side，这里需要使用一点小的技巧，我们并不能明确up向量究竟是哪个，但是我们可以明确的知道，side垂直于up与forward确定的平面，那么我们实际上只需要知道这个平面上任意一个和forward不在同一条直线的一个向量就可以了，称之up1，只是单纯的调整up1和forward的夹角是毫无意义的，不会对相机姿态产生任何影响，但是当up1以forward为轴旋转的时候实际上是在调整相机的翻滚角

当我们确定了大概的up1的时候，我们就可以使用二者确定最终的side

当我们知道了side的时候，我们又可以确定真正的up

大概的流程就是这样。

总之在求view的过程中，变量一共有三个，pos,target,up1。如果我们考虑使用欧拉角来确定相机的姿态，那么相机的姿态会有三个决定量，分别是俯仰角pitch，偏航角yaw，翻滚角roll.

考虑一下你就会发现up1决定roll，pos和target决定了一个平面，两者任意一个在平面内的非延长线方向的平移决定了pitch，垂直平面的移动决定了yaw。总之pos和target具有同样的地位，可以决定yaw和pitch

现在说一下计算，forward和up1的叉积是符合右手坐标系的，自己考虑一下，x和y叉乘得到的是z，而forward是z轴的反向，up1代表y，所以-z与y的叉积是x，也即cross(forward,up1)=side，注意单位化

然后cross(-forward,side)=up

至此新的x,y,z分别是side,up,-forward

假设我们有一个变换矩阵p，世界坐标系中的a向量转换至相机坐标系中的新向量为a1，变换为pa = a1

那么事实上我们可以考虑相机坐标系中的一组基，它们在世界坐标系中的表示其实就是我们算出的size,up和-forward，那么他们都可以通过与p相乘，得到自己在相机坐标系中的表示，毫无疑问，他们在自己空间中的表示就是标准单位向量，从而组成了单位矩阵E，稍作变换，我们可以知道p=invers(B)，B就是由side,up,-forward竖列组成的，仔细考虑一下，如果单纯这样组成`3*3`的矩阵，那么应该有点不太对，这意味着相机的原点和原空间的原点一致，所以我们需要一个`4*4`的矩阵，第四列是原点坐标，这是一个齐次坐标组成的矩阵
$$
\begin{vmatrix} 
s[0] & up[0] & -forward[0] & pos[0] \\
s[1] & up[1] & -forward[1] & pos[1] \\
s[2] & up[2] & -forward[2] & pos[2] \\
0 & 0 & 0 & 1 \\
\end{vmatrix}
$$
对这个矩阵求逆即可

投影矩阵，我们并没有什么实际操作上的需要，因此暂时推迟，利用view矩阵即可完成相机。

上面的view矩阵是我们通过变换得到的，但是因为第一人称相机涉及到了欧拉角，所以我们还必须学会使用旋转的方式得到view矩阵。



#### 第一人称相机

我们应该将所有的相机控制分解，姿态角方面，我们应该控制俯仰角，偏航角，至于翻滚角是一种类似飞行器的操作，可以暂时忽略。

我们还应该可以控制相机的位置坐标，于是可以分解为上下，左右和前后。

在鼠标手势方面，我认为默认情况下鼠标不起作用，滚轮负责前后移动，等价于放大缩小操作；左键+鼠标的移动控制上下左右；ctrl+鼠标移动控制偏航和俯仰角。

要解决的问题有两个：第一，鼠标与键盘事件接口；第二位置与角度映射方式

##### glfw事件监听

我不以标准的c++格式下的glfw来说，而是python下的glfw

完成键盘的监听，我们需要注册一个handler，这个函数会接受5个参数，window,key,scancode,action,mode

其中的key是一个数字，代表着不同的按键，action有两个值:glfw.PRESS和glfw.RELEASE，换句话说，当一个键被按下的时候，会接收到一个press，当被释放的时候也会接受到一个release

我们需要注册`glfw.set_key_callback(window,handler)`

我们需要的是：滚轮事件，key，鼠标移动，鼠标点击，所以一个示例是这样的：

~~~python
def key_handler(window,key,scancode,action,mode) :
	#print(key,action)
	if key == 341 and action == glfw.PRESS :
		print('press ctrl..')
	if key == 341 and action == glfw.RELEASE :
		print('release ctrl...')
def scroll_handler(window,xoffset,yoffset) :
	print(xoffset,yoffset)
	
def mouse_button_handler(window,button,action,mods) :
	if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS :
		print('press left')
	elif  button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE :
		print('release left')
		
def mouse_move_handler(window,xpos,ypos) :
	print(xpos,ypos)
    
 	glfw.set_key_callback(window,key_handler)
	glfw.set_scroll_callback(window,scroll_handler)
	glfw.set_mouse_button_callback(window,mouse_button_handler)
	glfw.set_cursor_pos_callback(window,mouse_move_handler)   
~~~

最后一部分应该写在window创建之后，这就很明显了。

如果不够，接下来可能还会加。















### 光照

反射可以使用颜色相乘来表示

我们为了测试需要创建一个新的片元着色器：

~~~c
#version 330

out vec4 final_color;

in vec2 texc;

uniform vec3 ocolor;
uniform vec3 light;

uniform sampler2D te;
uniform sampler2D te1;
void main()
{
	final_color = vec4(ocolor*light,1.0f);
}
~~~

为了稍作简化，我们也重新修正了shader_loader

~~~python
__all__ = ['My_shader']

from OpenGL.GL import *
import OpenGL.GL.shaders


class My_shader:
    
    def __init__(self,v_path,f_path) :
        
        with open(v_path,'r') as v_file :
            v_source = v_file.read()


        with open(f_path,'r') as f_file :
            f_source = f_file.read()


        v_shader = OpenGL.GL.shaders.compileShader(v_source,GL_VERTEX_SHADER)
        f_shader = OpenGL.GL.shaders.compileShader(f_source,GL_FRAGMENT_SHADER)
        self.shader = OpenGL.GL.shaders.compileProgram(v_shader, f_shader)

    def use(self) :
        glUseProgram(self.shader)

    def setvec3(self,name,a,b,c) :
        loc = glGetUniformLocation(self.shader,name)
        glUniform3f(loc,a,b,c)
~~~

可以使用setvec3方法方便的设置光照颜色和物体的颜色

#### 基础光照

我们要学习的第一个光照模型是Phong光照模型，这个模型将光照分为三个部分：环境光(ambient)，漫反射(diffuse)，镜面反射(specular)

##### 环境光

环境光可以很复杂，也可以很简单。高级的要用到全局光照算法之类的进行模拟，很复杂，我们就不用这个了。我们选择最简单的，只是将光源乘上一个很小的因子就好:

`ambient = 0.1*light`

##### 漫反射

简单的环境光并不是十分有意思，加入漫反射就会大有不同。

计算漫反射，我们需要知道法向量，但是我们事实上并不方便直接计算法向量，因此我们会直接传入法向量，明显顶点会经过model的变换，那么法向量应该也做相应的变换，但是并没有这么简单，试想，在平移的情况下，如果法向量是(1,0,0)，那么难道沿y轴平移之后就应该是(1,y,0)吗？明显不是。那正确的表达应该是：`mat3 normalMatrix = mat3(transpose(inverse(view * model)));`

至于推导，见[推导过程](http://blog.csdn.net/chenhittler/article/details/51348209)

原理就是计算从表面上的点到灯的向量L，然后计算法向量，两者同时单位化，然后计算cos$\theta$

如果角度大于90°就说明光无法照到上面，就应该设置为0

所以漫反射因子应该是`max(dot(normal,lightdir),0.0);`

漫反射因子和光源的乘积就是漫反射分量，与环境光叠加再乘上物体颜色就是得到的反射颜色

例子暂时不写，等到写完镜面反射一起给出







### Obj模型加载

#### 文件格式

以`#`开始的行是注释行

`v`代表的是几何顶点

`vt`是纹理坐标

`vn`是法线

`f`代表面

基本上最初只需要关注这些就可以

然后我要总结一下代码的特性，我参考其他作者的代码完成的ObjLoader将所有的数据存入到了model属性中，存储的顺序是:顶点，纹理坐标，法线坐标

然后因为在设置pointer的时候需要用到起始点的偏移量，所以有提供了vert_start，tex_start，normal_start这三个属性，然后整个model的字节数使用size属性提供，绘制的时候还需要三角形的数目，所以还提供了triangle_num这个属性，然后，并不是所有的obj文件都提供了法向，使用之前应该检查has_normal属性，代码如下所示：

~~~python
import numpy as np

class ObjLoader :
	def __init__(self,path) :
		self.vertex = []
		self.tex_coords = []
		self.normals = []

		self.vertex_index = []
		self.tex_index = []
		self.normal_index = []

		self.model = []
		self.load(path)

	def load(self,path,dtype=np.float32) :

		with open(path,'r') as fi :
			content = fi.readlines()

		for line in content :
			if line.startswith('#') :
				continue
			values = line.split()
			if not values :
				continue
			if values[0] == 'v' :
				self.vertex.append(values[1:4])
			elif values[0] == 'vt' :
				self.tex_coords.append(values[1:3])
			elif values[0] == 'vn' :
				self.normals.append(values[1:4])
			elif values[0] == 'f' :
				face = []
				tex = []
				normal = []

				for va in values[1:4] :
					val = va.split('/')
					self.vertex_index.append(int(val[0])-1)
					self.tex_index.append(int(val[1])-1)
					if len(val)==3 :
						self.normal_index.append(int(val[2])-1)
						self.has_normal = True

		self.model.extend([valu for i in self.vertex_index for valu in self.vertex[i]])
		self.model.extend([valu for i in self.tex_index for valu in self.tex_coords[i]])
		if self.has_normal :
			self.model.extend([valu for i in self.normal_index for valu in self.normals[i]])

		self.model = np.array(self.model,dtype=dtype)

		self.vert_start = 0
		self.tex_start = len(self.vertex_index)*3*4
		self.normal_start = (len(self.vertex_index)*3+len(self.tex_index)*2)*4
		self.size = self.model.itemsize*len(self.model)
		self.triangle_num = len(self.vertex_index)
if __name__ == '__main__' :
	test = ObjLoader('cube.obj')
	print(test.model)
	print(test.vert_start)
	print(test.tex_start)
	print(test.normal_start)
	print(test.size)
~~~

使用的时候，只需要把model存入VBO即可，然后使用pointer指示位置即可。

这里说明两个问题：第一，数据的存储，第二，stride参数

这里在model中，所有的顶点数据存在最前面，然后是纹理坐标，最后是法向

但是你应该注意到pointer里面的参数只给出了，是几元组，相邻数据的偏移，开始的偏移。并没有关于有几组数据这样的参数，那么我们使用这样的数据格式会出问题吗？大可放心，没事

第二个问题，当我们使用交错存储的时候，我们需要制定相邻数据的偏移，但是像这种存储格式，我们还要指定吗？逻辑上的思考是需要的，但是事实是这种紧密存储可以指定，也可以设为0



我们下一步的工作是，应该完成一个纹理导入类了。







### Give up

这是自服务器之后，第二个我被逼到走投无路，无可奈何而放弃的项目，我的确获得了很多的知识，因为时间关系我也没有详细记录。

这里只是大概说一下，然后记录一下我遇到的问题和进展，然后，opengl的学习就告一段落了。

从何说起呢？

纹理，相机控制，模型加载。

我最近所关注的就是这几个部分，然后我无一例外地失败了。

先说一下相机控制的问题吧，你知道我一直对于只有pitch,yaw,前后，左右，上下的相机控制不满意，然后我终于找到了我想要的，他的名字叫轨迹球，英文trackball或者arcball，我收集了很多的资料，其中一个是包含了全部源码的小应用，我存在文件夹里面了，叫earth。

再说一下什么叫轨迹球，本质是，轨迹球就是通过平面上鼠标的二维移动，控制相机在一个球面上运动，相机永远指向球体的中心，最简单的情况下，这个中心是原点，要获得最好的观测效果，应该把物体也放在原点。

听起来似乎不算很复杂，我们只需要对相机做一些改造，想想一下，在屏幕的平面上突起了一个半球，我们通过很简单的映射可以把半球下面的一个二维的点映射到球面上，当我们获得两个这样的点之后，就得到了两个向量op1和op2，很容易求得二者之间的夹角，以及垂直二者构成的平面的轴，最简单的想法，我们只要让球绕这个轴旋转这个角度即可，需要考虑和小心的问题是，我们必须让之前的手势控制可以和这个很好的融合在一起。

方法就是考虑记忆性和统一的接口，外部看来从相机拿到的就是view矩阵，从内部来看每次获取这个矩阵都是通过position,forward，up来拿到的，进一步的，我们也很有必要直到right

然后对于着色器而言，是没有什么记忆的，每次都是最原始的顶点与转换矩阵相乘，所以为了保持连贯性，我们必须让相机自己记住自己之前的参数，换句话说，每次的改变都是增量操作，而不是覆盖。

再从yaw和pitch的角度考虑，我们没什么必要让这两个量有什么记忆性，但是如何让这两个量转换为上述的position,forward,up和right？

之前我一直采用数学计算法进行转换，但是这一次不一样了，我们必须使用旋转的方法，一次拿到绕当前的right和up旋转的矩阵，然后对三个向量进行操作，就得到了最新的三个向量。

这和之前的大不相同，我们的相机俯仰，偏航不再有角度范围限制，将是无限连续的操作，对于移动也很有必要做相同的操作

可能还略有一些小细节，但大体上就是如此。

这种操作还有一个很严重的问题，就是当你在操作的时候你会发现球并没有完全按照鼠标移动的方向滚动，方向总是不一致，虽然勉强可用。

理想的状态是这样的样子，鼠标点下去，你会按到一个点，当你移动的时候，这个点会始终在鼠标下面，只是释放，这样你才会观察到绝对完美的轨迹球。正如我前面说的小软件。

那么问题出在哪里？据我分析，问题在于坐标系变换的过程，导致点的位置发生了变化，也就是说你鼠标下方的你想要的那个点经过变换变到了其他位置，这样虽然你鼠标在这里操作，但是对于轨迹球来说你实际上在制定其他位置的两个点，自然旋转轴就不是你所想要的那个，如何解决？我们需要反变换。

我想知道屏幕坐标系里面的二维点还原到原来的世界坐标系里面是什么坐标。

我知道怎么从剪切空间转换到世界坐标系，只需要对projection，view，model组成的矩阵做逆变换就好，很简单，也十分准确，问题的关键在于，我们少了一个维度z，但是经过我的测试z并不重要，重要的是w

举个栗子，世界坐标系里面的(x,y,z,1.0)以此做`projection*view*model*p`的操作可以得到(x1,y1,z1,w1)

w1并不是1，我们只要知道(x1,y1,z1)里面的任一一个量，和w1，就可以通过反变换得到他们对应的x,y,z，换句话说x,y,z是独立的，互相没关系，但是他们都和w1有关系，可是我们对鼠标的点击位置做一些变换之后得到的只是x1,y1。w1怎么拿到？网上大多说使用`glReadPixels`可以拿到深度值，我推理了一下，只要有x,y就能拿到一个深度，这说明深度与z无关，所以深度值一定不是z1，我又试了一下的确只要提供一样的x,y就能得到一样的w1，那么深度值一定是w1了

但是我做了很多复原测试，发现并非如此，并不行。

我还尝试了网上提供的其他方案，例如设置z1为1，w1为1，也不行

我觉得问题应该很简单才对，不然岂不是连个画板都做不出来了？

我也试了`gluUnProject`，也不怎么行

总之，衡量标准是，你画一个点，只要你能让这个点随鼠标移动就算成功了

但我还做不到，我完全不知道着色器拿到了gl_position之后怎么把这个四元数画到二维的屏幕上的。

很乱，但是基本上相机控制就是这样了。

在做轨迹球的测试的时候，你应该使用一个球作为参考模型。

下面是纹理加载

纹理的加载，也是一个比较麻烦的问题，因为格式实在太多了，我对使用PIL转换到二进制颇为不信任，是否每个都需要上下翻转吗？格式是RGBA吗？我觉得应该有一个专门的库

然后就是我见到了好几个模型的纹理坐标出现了负数，或者是超出了1，那么我该如何应对？完全没有主意，我尝试过不做处理，但是加载出来的啥也不是，一团糟糕。

然后是模型加载

我已经为网上找到的基本obj加载类做了优化处理，提供了更友好的接口，但是即便对于obj文件，你观察结构也会发现它会包含很多个mesh，你必须改进代码以实现多个mesh的存储和解析，但是这个工作很繁琐，我并没有做。

进一步的，网上找到的模型格式多了去了，怎么加载？说使用assimp，对于python，有pyassimp，但是我根本没有安装成功，dll文件该怎么处理？我也不知道。

还有什么经验？

绘制的时候，注意我们是可以使用除了三角形之外的其他绘制方式的，例如`GL_LINES`等

别的没什么，我要暂时放弃了。



然后现在攒的文件已经太多了，我也没有太多的能力整理出来一套合理的了。

现在就这样吧。也许有些经验忘记记录了，想起来再说吧。

也许换成`c++`才是王道

