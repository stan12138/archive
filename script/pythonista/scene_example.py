from scene import *
from Draw_line import my_line
from sound import play_effect


pic = Texture('mou1.JPG')
font = ('Apple Color Emoji',25)
class myscene(Scene) :
	def setup(self) :
		self.background_color = '#f868ff'
		
		self.pic_node = SpriteNode(pic,parent=self)
		self.pic_node.anchor_point=(0.5,0.5)
		self.pic_node.position=(self.size.w/2,self.size.h/2)
		self.pic_node.scale=0.5
		
		line,pos=my_line(100,100,300,300)
		self.lin_node = ShapeNode(line,stroke_color='#6875ff',parent=self)
		self.lin_node.position=pos
		
		self.txt_node = LabelNode('Hello,this is stan',font,parent=self)
		self.txt_node.position = (self.size.w/2,4*self.size.h/5)
		self.txt_node.color='#ff4646'
		
	def touch_moved(self,touch) :
		x,y=touch.location
		self.pic_node.position=touch.location
		play_effect('8ve:8ve-slide-network',2)
		
		
	def touch_began(self,touch) :
		self.txt_node.position=touch.location
		play_effect('digital:HighDown',0.1)
	def touch_ended(self,touch) :
		self.lin_node.position=touch.location
		play_effect('digital:HighUp',0.5)
		
		
		
		
		
		
		
run(myscene(),PORTRAIT,show_fps=True)
