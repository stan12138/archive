# coding: utf-8
'''只是一个演示自由落体的程序'''
from scene import *
from ui import *

ball = Texture('emj:Blue_Circle')
font = ('Source Code Pro',20)
class Myscene (Scene):
	def setup(self) :
		self.flage = False
		self.posx=[]
		self.posy=[]
		self.v = []
		self.a = 0.12
		self.ballt = ball
		self.loss =[]
		self.background_color = '#8b51ff'
		self.ball=[]
		#ball1 = SpriteNode(self.ballt,parent = self)
		#ball1.position = (self.size.w/2,self.size.h/2)
		#self.ball.append(ball1)
		self.txt = LabelNode('I am here',font,parent = self)
		self.txt.anchor_point = (0.5,0.5)
		self.txt.position = (2*self.size.w/4,2*self.size.h/3)
		self.txt1=LabelNode('I am here',font,parent=self)
		self.txt1.position = (2*self.size.w/4,2*self.size.h/3-40)
		'''for i in self.ball :
		
		i.z_position = -2
		i.position = (self.size.w/2,self.size.h/2)
		i.anchor_point = (0.5,0.5)'''
		#self.rx,self.ry = ball.size
		#rec = Path.rect(self.size.w/2,self.size.h/2,57.7,57.7)
		
		#self.rect = ShapeNode(rec,parent = self)
		#self.rect.position =(self.size.w/2,self.size.h/2)
	def update(self) :
		x,y,z =gravity()
		self.a = -y
		self.txt1.text='x = : %.2f'%x+' y = : %.2f'%y
		if self.flage :
			for i in range(len(self.ball)) :
				self.posx[i]+=30*x
				self.posx[i]=max(57.7/2,min(self.size.w-57.7/2,self.posx[i]))
				self.txt.text = str(len(self.ball))
				self.posy[i] -= self.v[i]
	#self.txt.text = str(len(self.ball))
				self.v[i] += self.a
				if self.posy[i] <= 57.7/2 and abs(self.v[i]) < 1.6:
					self.loss[i] = 0.5 *self.loss[i]
					self.v[i] = -self.v[i]*self.loss[i]
					if self.v[i] <= 0.01 :
						self.ball[i].remove_from_parent()
						
					'''self.v = 0
					self.posy = 57.7/2
					self.flage = False'''
					
					
				elif self.posy[i] <= 57.7/2 and self.v[i]>0 :
					self.v[i] = -self.v[i]*self.loss[i]
					self.loss[i] = max(0,self.loss[i]-0.03)
					
				self.ball[i].position = (self.posx[i],self.posy[i])#min(self.posy[i],self.size.h-57.7/2))
				
				
				
	def touch_began(self,touch) :
		x,y = touch.location
		self.flage = True
		new = SpriteNode(self.ballt,parent=self)
		new.position=(x,y)
		self.ball.append(new)
		self.posx.append(x)
		self.posy.append(y)
		self.v.append(0.06)
		self.a = 0.12
		self.loss.append(0.9)
	def touch_moved(self,touch) :
		x,y = touch.location
		self.flage = True
		new = SpriteNode(self.ballt,parent=self)
		new.position=(x,y)
		self.ball.append(new)
		self.posx.append(x)
		self.posy.append(y)
		self.v.append(0.06)
		self.a = 0.12
		self.loss.append(0.9)
		
run(Myscene(),PORTRAIT,show_fps = True)

