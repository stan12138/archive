'''
这是一段用于制造树，在其中添加图片的代码，原理并不清楚，作用很重要，千万不要乱动

'''
from matplotlib.pyplot import *
from PIL.Image import *
from numpy import *
from matplotlib.offsetbox import OffsetImage,AnnotationBbox

figure(figsize=(10,10))

ax = axes()
im = array(open('mou1.JPG'))

ima = OffsetImage(im,zoom=0.2)

ab = AnnotationBbox(ima,xy=(0.5,0.5),xycoords='data',pad=0.1)

ax.add_artist(ab)

show()
