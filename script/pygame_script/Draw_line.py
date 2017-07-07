'''
负责处理scene中的直线
'''
from scene import *
from ui import *
from math import sin,cos
from math import radians as ra
#font = ('Apple SD Gothic Neo',25)
#texture = Texture('test:Lenna')
#这是一个利用scene画线的演示程序
def my_line(startx,starty,endx_or_r,endy_or_theta,two_point = True,tp = True) :
	a = Scene()
	pa = Path()
	if two_point and tp :
		pa.move_to(startx,a.size.h-starty)
		pa.line_to(endx_or_r,a.size.h-endy_or_theta)
		point = ((startx+endx_or_r)/2,(starty+endy_or_theta)/2)
		return pa,point
	else :
		point = startx + endx_or_r*cos(ra(endy_or_theta))
		endy_or_theta = starty + endx_or_r*sin(ra(endy_or_theta))
		endx_or_r = point
		pa.move_to(startx,a.size.h-starty)
		pa.line_to(endx_or_r,a.size.h-endy_or_theta)
		point = ((startx+endx_or_r)/2,(starty+endy_or_theta)/2)
		return pa,point
		#返回值里的pa是已经包含了一条指定直线的ui.Path,point是这条直线的中心点
'''
2016.7.13
作者:stan
从源文件中将line单独摘了出来，作为一个工具模块，已经完成修改。
使用说明:
	该函数用于pythonista的scene模块中绘制一条直线，注意，只用于此处。
	在scene中，绘制一条直线要新建一个shapenode节点，这个节点的第一个参数是一个来自ui的Path，该函数的目的就在于产生这样一个Path。
	关于实现方法的大概说明:Path中绘制一条直线大概相当于一支笔，首先将一个空的path移动到起点(move_to)，然后画一条直线到终点(line_to)，这样就产生了一个包含了一条直线的path。
	需要注意的问题大概有这些:第一，ui中的坐标系的原点在左上角，而scene中的坐标系和日常生活相同，原点都在左下，所以需要进行转换。哦，好像只有第一点吆。
	使用时，函数的变量名很明显，前两个参量是起点的x,y，中间两个要么是终点的x,y，要么是长度和角度，这个由最后两个参数决定，最后两个参数的功能相同，之所以设置两个是出于同时兼顾易懂和方便考虑的，想易懂设置two_point,想方便设置tp,它们的功能都是决定直线的设置方式，是两点法，还是一点加半径加角度的方法。默认使用两点法。另外，设置角度时，角度时角度制的，0度的位置及增加的方向都与数学保持一致。
	
	函数的返回值第一个参数是一个path，第二个是直线的中点，使用时将path传入scene的shapenode的第一个参数，然后设置这个node的锚点为(0.5,0.5)即(anchor_point),然后设置position为第二返回值。
	多说一句，千万要注意设置shapenode的stroke_color，因为默认值是'clear',这就意味着是透明，看不见的。还有不要忘记parent=self。
	就这样吧。
'''
	
	
	
