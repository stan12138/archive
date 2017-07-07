import pygame , sys
from pygame.locals import *
pygame.init()

screentitle=pygame.display.set_caption('Creat By 韩仪')
screen=pygame.display.set_mode([800,600])
screen.fill([255,255,255])
textfont=pygame.font.SysFont('simsunnsimsun',15)
text=textfont.render('这是韩仪的第一个成功输出中文的例子abc',True,[0,0,0])

while True :
    for event in pygame.event.get() :
        if event.type in (QUIT,KEYDOWN) :
            pygame.quit()
            sys.exit()
    screen.blit(text,[250,300])
    pygame.display.update()
