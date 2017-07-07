###PIL,pygame,scene

这是关于如何将PIL和pygame或者pythonista上面的scene结合的几句重要语法：

pygame :

	out = fromarray(uint8(outpic))
	data = out.tobytes()
	ima = pygame.image.fromstring(data, (200,100),'RGBA')
	screen.blit(ima,[50,50])

大概不需要太多的说明吧，out是从数组中转换得到的图片，然后使用tobytes方法进行转换，然后在pygame中使用image.fromstring转换从而得到pygame的surface，于是done完成了

scene：

	from PIL import Image,ImageOps,ImageFilter
	import ui
	import io

	def pil2ui(ui_image) :

		buffer = io.BytesIO()
		pil_image.save(buffer,format='PNG')
		return ui.Image.from_data(buffer.getvalue())

这样调用这个函数就可以得到一个ui image然后使用Texture转换，然后传入spritenode即可


###crop
PIL的crop函数，要注意采用的坐标系是左上角为原点，crop的参数box的四个值分别是左上右下，代表一个矩形区域，可以这样看，这四个值的前两个代表矩形区域左上角的坐标，后两个代表右下角的坐标，因而，后两个值应该大于前两个值

###rotate
PIL旋转函数rotate的特性在于旋转后得到的新图片大小保持与原图一致，所以，当选转角度不是180度是就会造成图片损失，并被添加黑色区域。参数是角度制