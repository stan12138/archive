## PyopenGL

> --by stan 
>
> -- 17.6.22

<font color="red"><b>最好的参考书是learnopengl_book,来自learnopengl.com</b></font>

发现了一个博客，基本上就是我现在看的书的英文译文：[参考博客](http://blog.csdn.net/ziyuanxiazai123/article/category/2107037/3)

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

### 结构化

接下来的任务是创建一段代码，可以从文件中导入着色器，并经过类的封装使其更加易用。  

vertex shader和fragment shader各自写一个文件，再定义一个shader类，它可以将shader源码文件读到字符串里面，然后编译连接成程序，并提供一个use方法。

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







​	