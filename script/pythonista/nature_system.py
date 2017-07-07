from scene import *
from Ve import vec
from Draw_line import my_line

ball = Texture('emj:Blue_Circle')


def handle(me) :
	pass


class myscene(Scene) :
	
	def setup(self) :
		self.background_color = '#fbaeff'
		self.ball = SpriteNode(ball,parent=self)
		self.v = vec(0,1)
		self.ball.position=(self.size.w/5,self.size.h/2)
		self.f = vec(0,0)
		self.m = 3
		self.a = self.f/self.m
		self.wmax,self.hmax = self.size
		li,po = my_line(self.ball.position[0],self.ball.position[1],self.size.w/2,self.size.h/2)
		self.line = ShapeNode(li,stroke_color='#2336ff',parent=self)
		self.line.position=po
		#print(self.wmax,self.hmax)
		
	def update(self) :
		
		self.ball.position += self.v.name
		x,y = self.ball.position
		vx,vy = self.v.name
		if (x<=57.7/2 and vx<=0) or (x >= self.wmax-57.7/2 and vx>0) :
			vx = -vx
		if (y<=57.7/2 and vy<=0) or (y >= self.hmax-57.7/2 and vy>0):
			vy = -vy
		self.v = vec(vx,vy)
		self.line.remove_from_parent()
		#f = (self.size.w/2,self.size.h/2)-self.ball.position
		#f = vec(f[0],f[1])
		#self.f = f/f.lenth
		self.a = self.f/self.m
		self.v += self.a
		self.v = self.v/self.v.lenth
		li,po = my_line(self.ball.position[0],self.ball.position[1],self.size.w/2,self.size.h/2)
		self.line = ShapeNode(li,stroke_color='#2336ff',parent=self)
		self.line.position=po
		
			
		
	def touch_began(self,touch) :
		f = touch.location-self.ball.position
		f = vec(f[0],f[1])
		self.f = f/f.lenth
	def touch_ended(self,touch) :
		self.f = vec(0,0)
		

run(myscene(),PORTRAIT,show_fps=True)
