import pygame
import sys
from pygame.locals import *
from random import randint
import math

pygame.init()

screen=pygame.display.set_mode([800,600])
pygame.display.set_caption('Creat by 韩仪')


sr=randint(0,255)
sg=randint(0,255)
sb=randint(0,255)

starta=math.radians(0)
starte=math.radians(250)

screen.fill([sr,sg,sb])

while True :
    for event in pygame.event.get() :
        if event.type in (QUIT,KEYDOWN) :
            pygame.quit()
            sys.exit()
    pygame.draw.line(screen,[0,0,0],[100,0],[800,600],10)
    pygame.draw.arc(screen,[0,0,0],[200,150,100,200],starta,starte,8)
    pygame.draw.rect(screen,[0,0,0],[200,150,100,200],8)
    pygame.display.update()

