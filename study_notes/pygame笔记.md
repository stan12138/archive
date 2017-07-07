

    import os
	import StringIO
	import Image, ImageFont, ImageDraw
	import pygame
 
	pygame.init()
 
	text = u"这是一段测试文本，test 123。"
 
	im = Image.new("RGB", (300, 50), (255, 255, 255))

	font = pygame.font.Font(os.path.join("fonts", "simsun.ttc"), 14)
 

	rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
 

	sio = StringIO.StringIO()
	pygame.image.save(rtext, sio)
	sio.seek(0)
 
	line = Image.open(sio)
	im.paste(line, (10, 5))
 
	im.show()
	im.save("t.png")



以屏幕左上角为原点，面对屏幕 以向右为x轴正向，向下为y轴正向建立直角坐标系，称x方向为长，y方向为宽
建立screen对象，[a,b],a代表x轴,b代表y轴

绘制矩形时，[left,top,lenth,width],含义为第一个参数为边框距离左边的距离，或者说与y轴的距离，第二个参数为上边距离x轴的距离，第三个参数为长度，第四个参数为宽度。

绘制圆形时，[left,top]，含义为圆心距离左边和顶部的距离

绘制直线时，[xstart,ystart],[xend,yend],此即为起点与终点的坐标

绘制弧线时，会要求定出一个矩形，也就是说参数与矩形是相同的形式，[left,top,lenth,width],弧线的中心即为矩形的圆心，矩形为正方形则为圆弧，矩形是长方形，弧线就是椭圆弧，同时另外一对参数会给出起始弧度和终止弧度，弧度的方向和数学中相同


暂时的一个 ：
似乎有这样一个类型，叫Rect，导入一幅图片，使用rectangle=Rect.get_rect()可以获得一个Rect，然后可以设置这个类型的属性，例如bottomright,center等，然后在使用screen.blit()绘制这幅图片时，将第二个参数设置为rectangle这样可以依据前面属性的设置直接定位center等的位置