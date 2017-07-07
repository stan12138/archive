# coding: utf-8
from math import sqrt,atan2,pi,cos,sin,degrees
'''此为一个向量类，初始化要输入向量的坐标或者长度和角度，支持print,+,-,X操作'''
class vec :

	def __init__(self,x,y,location=True) :
		#同时支持坐标输入，弧度输入，默认为坐标输入，将location设置为false切换至半径角度输入，注意，角度为弧度制，范围0～2*pi
		if location :
			self.name = [x,y]
			self.lenth = sqrt(x**2+y**2)
			self.angel = (atan2(y,x))
			if self.angel <0 :
				self.angel+=2*pi
		else :
			self.lenth = x
			self.angel = y
			self.name = [x*cos(self.angel),x*sin(self.angel)]
		#self.angel = degrees(self.angel)
	def __len__(self) :
		#原来想把这个也设置为向量的长度，但len只能返回整数，所以。。。。
		return len(self.name)
	def __str__(self) :
		return 'location : '+str(self.name[0])+','+str(self.name[1])+' '+'lenth : '+str(self.lenth)+' angel : '+str(degrees(self.angel))
	def __add__(self,other) :
		return vec(self.name[0]+other.name[0],self.name[1]+other.name[1])
	def __sub__(self,other) :
		return vec(self.name[0]-other.name[0],self.name[1]-other.name[1])
	def __mul__(self,other) :
		if isinstance(other,vec) :
			return self.name[0]*other.name[0]+self.name[1]*other.name[1]
		else :
			return vec(other*self.name[0],other*self.name[1])
	def __truediv__(self,other) :
		return  vec(self.name[0]/other,self.name[1]/other)
if __name__ == '__main__' :

	a = vec(-1,-2)
	b = vec(-1,2)
	print(a)
	print('len a:',len(a))
	print(a*b)
	print(a*2)
	c = vec(2,pi/6,location = False)
	print('c')
	print(c)
	a = vec(2,2)
	a = a/2
	print(a)

