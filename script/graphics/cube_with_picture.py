# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 21:58:15 2016

@author: stan han
"""
import pygame
import sys
from pygame.locals import *
from math import pi
from ar_tools import *

from PIL.Image import *
from numpy import *
from numpy.linalg import *

ima = open('moumoon.JPG')

moon = array(ima)
moonr = moon[:,:,0]
moong = moon[:,:,1]
moonb = moon[:,:,2]

def pic_transform(poi,moon,moonr,moong,moonb) :



    xx = poi[0,:]
    yy = poi[1,:]
    ymin = min(yy)
    xmin = min(xx)
    h = int(max(yy)-ymin)
    l = int(max(xx)-xmin)

    poi = poi[:,0:3]
    xx = poi[0,:]
    yy = poi[1,:]

    xout=yy-ymin
    yout=xx-xmin
    xout.shape=(3,1)
    yout.shape=(3,1)
    inpoint = zeros([3,2])
    inpoint[:,0:1]=xout
    inpoint[:,1:2]=yout


    xout = poi[0,0]-inpoint[0,0]
    yout = poi[1,0]

    outpicr = 255*ones([h,l])
    outpicg = 255*ones([h,l])
    outpicb = 255*ones([h,l])
    outpica = ones([h,l])

    x,y,z = moon.shape


    picpoint = array([[0,0],[0,y-1],[x-1,y-1]])


    a = inpoint
    #a = array(a)
    b = picpoint
    a1 = ones([3,3])
    a1[:,0:2]=a
    b1 = b[:,0]
    b2 = b[:,1]
    ax = solve(a1,b1)
    ay = solve(a1,b2)
    for i in range(h) :
        for j in range(l) :
            x1 = dot(ax,array([i,j,1]))
            y1 = dot(ay,array([i,j,1]))
            if x1<x and y1<y and x1>=0 and y1>=0 :
                outpica[i,j]=255
                xi = int(x1)
                yi = int(y1)


                if xi==x1 :
                    xii = xi
                else :
                    xii = xi+1
                if yi==y1 :
                    yii = yi
                else :
                    yii = yi+1

                if xii>=x :
                    xii = xi
                if yii >=y :
                    yii = yi
                u = x1-xi
                v = y1-yi
                a = moonr[xi,yi]
                b = moonr[xii,yi]
                c = moonr[xi,yii]
                d = moonr[xii,yii]
                outpicr[i,j]=a*(1-u)*(1-v)+u*(1-v)*b+v*(1-u)*c+u*v*d
                a = moong[xi,yi]
                b = moong[xii,yi]
                c = moong[xi,yii]
                d = moong[xii,yii]
                outpicg[i,j]=a*(1-u)*(1-v)+u*(1-v)*b+v*(1-u)*c+u*v*d
                a = moonb[xi,yi]
                b = moonb[xii,yi]
                c = moonb[xi,yii]
                d = moonb[xii,yii]
                outpicb[i,j]=a*(1-u)*(1-v)+u*(1-v)*b+v*(1-u)*c+u*v*d

    outpic = ones([h,l,4])
    outpic[:,:,0] = outpicr
    outpic[:,:,1] = outpicg
    outpic[:,:,2] = outpicb
    outpic[:,:,3] = outpica
    out = fromarray(uint8(outpic))
    return out.tobytes(),[xmin,ymin],[l,h]







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
#cube = [[10,10,10],[30,10,10],[30,30,10],[10,30,10],[10,10,30],[30,10,30],[30,30,30],[10,30,30]]
#p1,p2,p3,p4,p5,p6,p7,p8
cube = [[10,-10,-10],[10,10,-10],[-10,10,-10],[-10,-10,-10],[10,-10,10],[10,10,10],[-10,10,10],[-10,-10,10]]
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

    data,location,sz = pic_transform(poi[:,0:4],moon,moonr,moong,moonb)
    ima = pygame.image.fromstring(data, sz,'RGBA')
    screen.blit(ima,location)


    easy_draw(poi)

    pygame.display.update()
