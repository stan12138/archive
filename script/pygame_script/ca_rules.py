from numpy import array,zeros,bool
from numpy.random import randint
import pygame
import sys
from pygame.locals import *

def rule1(cut) :

    if cut[1,1] :
        a = sum(sum(cut))
        if a>4 or a<=2 :
            return False
    if not cut[1,1] :
        a = sum(sum(cut))
        if a==3 :
            return True
    return cut[1,1]




def evaluate(world,rule) :

    new_world = zeros([100,100],dtype=bool)
    x,y = world.shape
    for i in range(1,x-1) :
        for j in range(1,y-1) :
            cut = world[i-1:i+2,j-1:j+2]
            new_world[i,j] = rule(cut)

    return new_world

def draw(screen,world) :

    x,y = world.shape

    for i in range(x) :
        for j in range(y) :
            if world[i,j] :
                pygame.draw.rect(screen,[0,0,0],[i*7,j*7,7,7],0)


pygame.init()

screen = pygame.display.set_mode([700,700])
pygame.display.set_caption('3D-2D')

screen.fill([255,255,255])

world = randint(2,size=(100,100))



while True :
    for e in pygame.event.get() :
        if e.type == QUIT :
            pygame.quit()
            sys.exit()


    screen.fill([255,255,255])

    world = evaluate(world,rule1)
    draw(screen,world)

    pygame.display.update()



