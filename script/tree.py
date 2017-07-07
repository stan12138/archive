'''
16.7.16
作者:Stan
这是一个创造可视化的树状结构的工具模块
代码依旧不完善，显示过程中箭头会被遮挡，大概通过坐标系设置可以解决
本工具使用说明:
	1,调用初始化函数(可以设置尺寸)，会返回一个根节点
	2，创建一个node类，需要传入名字，位置，根结点
	3，增加子节点只需要调用已有节点的add方法
	4，如果要创建与已有节点均无链接关系的新节点必须使用node创建一个新的
	5,如果要链接两个节点，可以使用connect方法
	6,默认情况下是不会进行显示和储存的，想要显示和储存，要调用任意节点的show和save方法
	7,特殊说明关于位置，左下角坐标为(0，0)，右上角为(1，1)，每个节点的坐标范围都在此之内
'''
from matplotlib.pyplot import *
from matplotlib.offsetbox import  OffsetImage,AnnotationBbox
from PIL.Image import *
import numpy as np


def init(size=(10,10)) :
	figure(figsize=size)
	ax=axes([0,0,1,1])
	axis('off')
	return ax
#每次使用之前，先要调用初始化函数，用于创建一个空的画板:Figure，和根结点:ax，可以设置尺寸
#默认情况下，隐藏了坐标轴

class node() :
	#这是主干部分，一个树节点的类
	def __init__(self,ax,position,str,ima = False,zoom1=0.1) :
		if not ima :
			bo=dict(boxstyle='round',fc=(1.0, .95, .95))
			a=ax.annotate(str,xy=position,size=20,va='top',ha='center',bbox=bo,zorder=2)
			self.position = (position[0],position[1])
			self.name=a
			self.parent = ax
		else :
			a = np.array(open(str))
			im = OffsetImage(a,zoom=zoom1)
			ab = AnnotationBbox(im, xy=position,xycoords='data',pad=0)
			ax.add_artist(ab)
			self.position = (position[0],position[1]+0.05)
			self.name=a
			self.parent = ax
	#创建节点的初始化代码，首先要求表明这个节点是一个文本节点还是图片节点，两者处理方式不同
	#对于文本节点，将使用matplotlib的注释函数，创建文本，文本框的样式和颜色没有额外提供更改
	#的接口，其它的细节也没有什么了
	#对于图片，使用几行特别的代码将其添加到ax中去，具体原理现在不甚清楚，提供缩放比例控制
	def connect(self,node1) :
		bo=dict(arrowstyle='fancy',connectionstyle='arc3,rad=0')
		self.parent.annotate('',xy=node1.position,xytext=self.position,arrowprops=bo,zorder=1)
		#connect方法是用于使用箭头连接当前节点和一个其他节点，同样适用注释的方法实现
		#同样的箭头的样式也没有提供更改接口
	def show(self) :
		show()
		#调用任意一个节点的该方法就可以显示整张图片
	def add(self,position,str,ima=False,zoom1=0.1) :
		b = node(self.parent,position,str,ima,zoom1)
		self.connect(b)
		return b
		#提供了另外一种方式产生一个子节点，其实就是上面的方法整合了一下
	def save(self,name) :
		savefig(name+'.png')
		#调用任意节点的该方法即可以给定名字以默认格式保存图片


if __name__=='__main__' :
	#以下为测试代码
	ax=init(size=(30,10))
	b = node(ax,(0.5,0.9),'stan')
	d = b.add((0.5,0.5),'yi')
	c = d.add((0.1,0.2),'han')
	#e = c.add((0.7,0.3),'mou1.JPG',ima=True,zoom1=0.25)
	#w = e.add((0.1,0.6),'demo.png',ima=True,zoom1=0.1)
	#b.connect(e)
	c.show()
	#c.save('demo')