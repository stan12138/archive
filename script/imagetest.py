import pygame,sys
from math import radians as ra
from pygame.locals import *
from math import cos , sin

pygame.init()

screen = pygame.display.set_mode([800,600])
pygame.display.set_caption('Creat by 韩仪')

earth = pygame.image.load('a.png').convert_alpha()
ship = pygame.image.load('spaceship.png')

x,y = earth.get_size()
i=100
r=220

screen.fill([0,255,255])
while True :
    for event in pygame.event.get() :
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
    screen.blit(earth,[400-x/2,300-y/2])
    
    i = i-0.2
    i=i%360
    rx=int(400+cos(ra(i))*r)
    ry=int(300-sin(ra(i))*r)
    newship = pygame.transform.rotate(ship,i-90)
    x2,y2 = newship.get_size()
    x1 = rx-x2/2
    y1 = ry-y2/2
    screen.fill([0,255,255])
    screen.blit(earth,[400-x/2,300-y/2])
    screen.blit(newship,[x1,y1])
    pygame.draw.circle(screen,[255,0,0],[rx,ry],6,0)

    
    
    pygame.display.update()
