# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 17:57:45 2016

@author: stan han
"""



'''
这是用来绘制示范性质的3维立方体的程序
'''
import pygame
import sys
from pygame.locals import *
from math import pi
from ar_tools import *

def easy_draw(poi) :

    le = poi.shape

    if le[0] == 2:
        pass
    else :
        poi = poi.transpose()

    le = poi.shape

    p1 = poi[:,(0,1,2,3,0)]
    p2 = poi[:,(4,5,6,7,4)]

    for i in range(4) :
        x0,y0 = p1[:,i]
        x1,y1 = p1[:,i+1]
        pygame.draw.line(screen,[255,0,0],[round(x0),round(y0)],[round(x1),round(y1)],2)

    for i in range(4) :
        x0,y0 = p2[:,i]
        x1,y1 = p2[:,i+1]
        pygame.draw.line(screen,[0,0,255],[round(x0),round(y0)],[round(x1),round(y1)],2)

    for i in range(4) :
        x0,y0 = p1[:,i]
        x1,y1 = p2[:,i]
        pygame.draw.line(screen,[0,0,0],[round(x0),round(y0)],[round(x1),round(y1)],2)
    x0,y0 = p1[:,0]
    x1,y1 = p2[:,2]
    pygame.draw.circle(screen,[255,0,0],[int(round(x0)),int(round(y0))],5,0)
    pygame.draw.circle(screen,[0,0,255],[int(round(x1)),int(round(y1))],5,0)
cube = [[10,10,10],[30,10,10],[30,30,10],[10,30,10],[10,10,30],[30,10,30],[30,30,30],[10,30,30]]
#p1,p2,p3,p4,p5,p6,p7,p8
cube = array(cube)

a1 = -pi/6
a2 = pi/3
a3 = pi/4

matri = count_matrix([a1,a2,a3])
poi = translate(matri,cube,zoom_in=7)
#print(poi.shape)
dis = (poi[:,0]+poi[:,6])/2

poi = easy_move(poi,dis)


pygame.init()

screen = pygame.display.set_mode([800,600])
pygame.display.set_caption('3D-2D')

screen.fill([255,255,255])

flage = False
x0,y0 = [200,100]
x1,y1 = [400,300]
while True :
    for e in pygame.event.get() :
        if e.type == QUIT :
            pygame.quit()
            sys.exit()
        elif e.type == MOUSEMOTION :
#            flage = True
            lx,ly = e.pos
#            x0,y0 = lx-100,ly-100
#            x1,y1 = lx+100,ly+100
            m_x ,m_y = e.rel
            a1 += m_x*pi/50
            a2 += m_y*pi/50
#            x0 += m_x
#            x1 += m_x
#            y0 += m_y
#            y1 += m_y

    screen.fill([255,255,255])

    matri = count_matrix([a1,a2,a3])
    poi = translate(matri,cube,zoom_in=7)
#    print(poi.shape)
    dis = (poi[:,0]+poi[:,6])/2

    poi = easy_move(poi,dis)
#    print(poi.shape)
    poi = to2d(50,poi,center=(lx,ly),way='p')

    easy_draw(poi)

    pygame.display.update()

