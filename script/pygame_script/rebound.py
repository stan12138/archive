import pygame , sys
from pygame.locals import *
from random import randint

pygame.init()

screentitle=pygame.display.set_caption('Creat by 韩仪')
screen=pygame.display.set_mode([800,600])


x=100
y=100
vx=2
vy=1

cr=0
cg=0
cb=0

sr=255
sg=255
sb=255

while True :
    for event in pygame.event.get() :
        if event.type in (QUIT,KEYDOWN) :
            pygame.quit()
            sys.exit()
    screen.fill([sr,sg,sb])
    x=x+vx
    y=y+vy

    if x > 700 or x < 100 :
        vx=-vx
        cr=randint(0,255)
        cg=randint(0,255)
        cb=randint(0,255)
        sr=randint(0,255)
        sg=randint(0,255)
        sb=randint(0,255)
    if y > 500 or y < 100 :
        vy=-vy
        cr=randint(0,255)
        cg=randint(0,255)
        cb=randint(0,255)
        sr=randint(0,255)
        sg=randint(0,255)
        sb=randint(0,255)


        
    pygame.draw.circle(screen,[cr,cg,cb],[x,y],100,0)


    pygame.display.update()
    

