## PyopenGL

> --by stan 
>
> -- 17.6.22


<font color="red"><b>最好的参考书是learnopengl_book,来自learnopengl.com</b></font>

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

至于ctypes.c_void_p(0)，ctypes.c_void_p(12)为什么要这样写，记住必须是c类型就好了，为什么是12不需要解释吧。  

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

	from OpenGL.GL import *
	import OpenGL.GL.shaders
	
	class Shader:
	    def __init__(self, vertexShaderPath, fragmentShaderPath):
	        vertexFile = open(vertexShaderPath, 'r')
	        vertexShaderSource = []
	        for line in vertexFile.readlines():
	            vertexShaderSource.append(line)
	        vertexFile.close()
	        vertexShaderSource = ''.join(vertexShaderSource)
	
	        fragmentFile = open(fragmentShaderPath, 'r')
	        fragmentShaderSource = []
	        for line in fragmentFile.readlines():
	            fragmentShaderSource.append(line)
	        fragmentFile.close()
	        fragmentShaderSource = ''.join(fragmentShaderSource)
	
	        vertexShader = OpenGL.GL.shaders.compileShader(vertexShaderSource, GL_VERTEX_SHADER)
	        fragmentShader = OpenGL.GL.shaders.compileShader(fragmentShaderSource, GL_FRAGMENT_SHADER)
	        self.shader = OpenGL.GL.shaders.compileProgram(vertexShader, fragmentShader)
	
	    def Use(self):
	        glUseProgram(self.shader)

这个很简单明白，不再细说。  

### Texture

texture的坐标系为左下角为（0，0）的笛卡尔坐标系，范围为0~1。  

首先，我们必须改造顶点数据，在坐标，颜色之外再增加一个两分量的对应的texture的坐标。  

##### 其它相关设置  
首先要为texture分配一个ID：`texture = glGenTextures(1)`.  

然后是绑定：`glBindTexture(GL_TEXTURE_2D,texture)`  

再后是设置一些必要的参数：

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)	
其中的前两个设置如果图片太小，在两个轴的方向各自做什么操作，这里设置了重复，另外还有镜面重复，拉伸，填充等方法，自行查看，特别的填充的话是要指定填充颜色的，所以必须使用额外的函数  

后两者指定了坐标点的采样方法，还记得双线性内插法吗？差不多是同样的意思，为了解决坐标点不是整数的问题，可以指定两种方法，线性或者是近邻，同时可以为缩放各自指定不同的方法。具体不再细说。  

mipmaps, 这个是用来控制视角缩放时texture的过度问题的，这个参数完全是通过filter设定的，换句话说，只需要`glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)`的最后一个参数设置为GL_LINEAR_MIPMAP_LINEAR即可
##### 载入数据

	image = Image.open('../textures/wall.jpg')
	img_data = numpy.array(image, numpy.uint8)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
	glGenerateMipmap(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, 0)


算了，我不想再写纹理了，发现了一个博客，基本上就是我现在看的书的英文译文：[参考博客](http://blog.csdn.net/ziyuanxiazai123/article/category/2107037/3)



​	