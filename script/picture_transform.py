# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 20:58:59 2016

@author: stan han
"""

from PIL.Image import open,fromarray
from numpy import array,ones,zeros,dot
from numpy.linalg import solve
from matplotlib.pyplot import *
#import StringIO

ima = open('moumoon.JPG')

moon = array(ima)
moonr = moon[:,:,0]
moong = moon[:,:,1]
moonb = moon[:,:,2]
x,y,z = moon.shape

outpicr = 255*ones([100,100])
outpicg = 255*ones([100,100])
outpicb = 255*ones([100,100])
outpica = ones([100,100])


def picture_transform(pic,poi,out,flage='f') :

    '''

    因为要实现完美的效果，所以不支持灰度图片，只支持rgb
    传入的四个参考点，必须自左上角开始，逆时针

    '''

    if type(pic)==str :
        pic = array(open(pic))

    if not poi.shape==(2,4) :
        print('参考点的数量必须是四个，二维坐标点，数组，并且排列为2*4')
        return

    x,y,z = pic.shape
    picr = pic[:,:,0]
    picg = pic[:,:,1]
    picb = pic[:,:,2]


    xx = poi[0,:]#参考点的尺寸2*4
    yy = poi[1,:]
    xmin = min(xx)
    ymin = min(yy)
    l = max(xx)-xmin
    h = max(yy)-ymin

    outr = ones([h,l])
    outg = ones([h,l])
    outb = ones([h,l])
    outa = ones([h,l])



    if flage == 'f' :

        poi = poi[:,0:3]
        poi = poi.transpose()

        picpoint = array([[0,0],[x-1,0],[x-1,y-1]])

        bx = picpoint[:,0]
        by = picpoint[:,1]

        a = ones([3,3])
        a[:,0:2]=poi

        ax = solve(a,bx)
        ay = solve(a,by)

        for i in range(h) :
            for j in range(l) :
                x1 = dot(ax,array([i,j,1]))
                y1 = dot(ay,array([i,j,1]))

                if x1<x and y1<y and x1>=0 and y1>=0 :

                    outa[i,j]=255
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

                    a = picr[xi,yi]
                    b = picr[xii,yi]
                    c = picr[xi,yii]
                    d = picr[xii,yii]
                    outr[i,j]=a*(1-u)*(1-v)+u*(1-v)*b+v*(1-u)*c+u*v*d
                    a = picg[xi,yi]
                    b = picg[xii,yi]
                    c = picg[xi,yii]
                    d = picg[xii,yii]
                    outg[i,j]=a*(1-u)*(1-v)+u*(1-v)*b+v*(1-u)*c+u*v*d
                    a = picb[xi,yi]
                    b = picb[xii,yi]
                    c = picb[xi,yii]
                    d = picb[xii,yii]
                    outb[i,j]=a*(1-u)*(1-v)+u*(1-v)*b+v*(1-u)*c+u*v*d

        outpic = ones([h,l,4])
        outpic[:,:,0] = outr
        outpic[:,:,1] = outg
        outpic[:,:,2] = outb
        outpic[:,:,3] = outa
        outpic = fromarray(uint8(outpic))

    if flage == 's' :
        poi = poi.transpose()
        pass



















def second_important_function() :

    aimpoint = array([[0,0],[0,99],[99,29],[89,89]])
    picpoint = array([[0,0],[0,y-1],[x-1,0],[x-1,y-1]])
    a1 = zeros([4,8])
    a11 = -aimpoint[:,0]*picpoint[:,0]
    a12 = -aimpoint[:,1]*picpoint[:,0]
    a11.shape=(4,1)
    a12.shape=(4,1)
    a1[:,0:2]=aimpoint
    a1[:,2:3]=ones([4,1])
    a1[:,6:7]=a11
    a1[:,7:8]=a12

    b1 = zeros([4,8])
    b11 = -aimpoint[:,0]*picpoint[:,1]
    b12 = -aimpoint[:,1]*picpoint[:,1]
    b11.shape=(4,1)
    b12.shape=(4,1)
    b1[:,3:6]=a1[:,0:3]
    b1[:,6:7]=b11
    b1[:,7:8]=b12

    a = zeros([8,8])
    a[0:4,:]=a1
    a[4:8,:]=b1

    b = zeros([8,1])
    b[0:4]=picpoint[:,0:1]
    b[4:8]=picpoint[:,1:2]
    a1 = solve(a,b)
    a1 = a1.flatten()
    print('begin')
    for i in range(100) :
        for j in range(100) :
            k1,k2,k3,k4,k5,k6,k7,k8=a1
            a11 = k7*i+k8*j+1
            x1 = (k1*i+k2*j+k3)/a11
            y1 = (k4*i+k5*j+k6)/a11
    #        plot(x,y,'r*')
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
    print('ok')

    outpic = ones([100,100,4])
    outpic[:,:,0] = outpicr
    outpic[:,:,1] = outpicg
    outpic[:,:,2] = outpicb
    outpic[:,:,3] = outpica
    out = fromarray(uint8(outpic))
    out.show()
    out.save('wtf.png')











def one_import_function() :
    x,y,z = moon.shape
    inpoint = array([[0,199],[0,99],[99,99]])
    picpoint = array([[0,0],[0,y-1],[x-1,0]])
    outpicr = 255*ones([100,200])
    outpicg = 255*ones([100,200])
    outpicb = 255*ones([100,200])
    outpica = ones([100,200])
    a = inpoint
    #a = array(a)
    b = picpoint
    a1 = ones([3,3])
    a1[:,0:2]=a
    b1 = b[:,0]
    b2 = b[:,1]
    ax = solve(a1,b1)
    ay = solve(a1,b2)
    for i in range(100) :
        for j in range(200) :
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

    outpic = ones([100,200,4])
    outpic[:,:,0] = outpicr
    outpic[:,:,1] = outpicg
    outpic[:,:,2] = outpicb
    outpic[:,:,3] = outpica
    out = fromarray(uint8(outpic))



#a1 = ones((510,375,4))
#a1[:,:,0:3]=a
#a1[:,:,3]=uint8(100*ones((510,375)))
#
##c = a[:,:,3]
##
##d = ones(c.shape)
##d = 100*d
##
##a[:,:,3] = d
##
#im = fromarray(uint8(a1))
#im.save('wtf.png')