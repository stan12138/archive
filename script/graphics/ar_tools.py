# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 15:58:14 2016

@author: stan han
"""

from numpy import array,dot,diag,sqrt,cos,sin,ones
from math import acos




def rotation(location,theta,direction='x') :
    '''所有的旋转均为逆时针，本函数现在大概已经不用了，只是作为一个示范性的，或者
    参考性质的函数继续存在。
    函数的原型如下：
    rotation(location,theta,direction='x')
    location原则上是一个1行3列的列表，不需要一定是数组，但是可以酌情改变
    theta是旋转的角度，第三个参数表明要绕哪个轴旋转
    '''
    x,y,z=location
    location = array(location)
    if direction == 'z' :
        matri = array([[cos(theta),sin(theta),0],[-sin(theta),cos(theta),0],[0,0,1]])
    elif direction == 'x' :
        matri = array([[1,0,0],[0,cos(theta),sin(theta)],[0,-sin(theta),cos(theta)]])
    elif direction == 'y' :
        matri = array([[cos(theta),0,-sin(theta)],[0,1,0],[sin(theta),0,cos(theta)]])
    out = dot(location,matri)

    return out

def move(location,distance) :
    '''
    本函数同样是一个原则上已经废弃的函数，示范性质，一次可以完成一个点同时沿x,y,x方向的平移
    函数原型：
    move(location,distance)
    location必须是三元的列表或者元组，代表一个点的坐标
    distance代表分别沿x,y,z方向的平移距离
    返回值是平移后的点的坐标
    '''
    x,y,z=location
    location = [x,y,z]
    location.append(1)
    matri = diag([1,1,1,1])
    matri[3,0:3]=distance
    matri = matri[:,0:3]
    out = dot(location,matri)

    return out




def count_angle(direction) :
    '''
    用于支持向量输入的旋转角度，此函数可以计算出你想要表达的角度，但是
    本函数默认角度只有俯仰角和偏航角，没有翻滚角
    函数原型：
    count_angle(direction)
    返回的结果可以直接输入到count_matrix中使用
    '''
    x,y,z = direction

    alpha = -x*acos(y/sqrt(x**2+y**2))/abs(x)

    beta = z*acos(sqrt(x**2+y**2)/sqrt(x**2+y**2+z**2))/abs(z)

    gama = 0

    return [alpha,beta,gama]

def to2d(f,loc,center=(400,300),way='t') :
    '''
    将计算完成的照相机坐标系中的三维坐标以平行投影或者透视投影的形式转换为
    荧幕坐标，关于技术细节，认为相机的标准指向为y轴正向
    函数原型为：
    to2d(f=30,loc,center=(400,300),way='t')
    f代表焦距，loc为三维点坐标，是一个矩阵，尺寸要求为3*n
    center代表屏幕的中心点坐标，way代表投影的方式，’t‘代表透视原理，’p‘代表平行投影
    返回值为2*n的尺寸
    '''
    sha = loc.shape
    if not sha[0] == 3 :
        print('屏幕坐标转换中....坐标矩阵格式错误！(行数为%d)'%sha[0])
        return

    out = ones([2,sha[1]])

    if way == 'p' :
        out = loc[(0,2),:]
    elif way == 't' :
        a = f/loc[1,:]
        out = loc[(0,2),:]
        out = out*a
    x,y=center
    out[0,:]=x+out[0,:]
    out[1,:]=y-out[1,:]

    return out

def translate(matri,loc,zoom_in=1) :
    '''
    本函数负责将三维世界坐标系中的坐标转换到照相机坐标系
    函数原型：
    translate(matri,loc,zoom_in=1)
    matrix代表转换矩阵，由count_matrix负责计算，loc为点坐标矩阵，尺寸n*3
    zoom_in代表放大倍数
    返回值为3*n
    '''
    length = loc.shape

    if not length[1]==3 :
        print('照相机坐标系转换中....坐标矩阵的输入格式错误！（列数为%d）'%length[1])
        return
    length = len(loc.flatten())
    length = length/3
    loc.shape = (length,3)
    loc = loc.transpose()

    loc = zoom_in*loc

    return dot(matri,loc)

def count_matrix(angle) :
    '''
    本函数根据相机姿态角计算出坐标转换矩阵，认为相机已经置于原点处，也即本函数只负责
    旋转，不负责平移
    函数原型：
    count_matrix(angle)
    angle依次为偏航角，俯仰角，翻滚角，均以逆时针方向为正
    相机的标准指向为y轴正向，水平面为xoy

    '''
    alpha,beta,gama = angle

    m1 = [[cos(alpha),sin(alpha),0],
          [-sin(alpha),cos(alpha),0],
          [0,0,1]]
    m1 = array(m1)

    x1 = array([1,0,0])
    x1 = dot(x1,m1)
    a,b,c = x1

    y1 = array([0,1,0])
    y1 = dot(y1,m1)

    m2 = [[a**2+(1-a**2)*cos(beta),a*b*(1-cos(beta))+c*sin(beta),a*c*(1-cos(beta))-b*sin(beta)],
          [a*b*(1-cos(beta))-c*sin(beta),b**2+(1-b**2)*cos(beta),b*c*(1-cos(beta))+a*sin(beta)],
          [a*c*(1-cos(beta))+b*sin(beta),b*c*(1-cos(beta))-a*sin(beta),c**2+(1-c**2)*cos(beta)]]

    y1 = dot(y1,m2)
    a,b,c = y1

    m3 = [[a**2+(1-a**2)*cos(gama),a*b*(1-cos(gama))+c*sin(gama),a*c*(1-cos(gama))-b*sin(gama)],
          [a*b*(1-cos(gama))-c*sin(gama),b**2+(1-b**2)*cos(gama),b*c*(1-cos(gama))+a*sin(gama)],
          [a*c*(1-cos(gama))+b*sin(gama),b*c*(1-cos(gama))-a*sin(gama),c**2+(1-c**2)*cos(gama)]]


    mat = dot(m1,m2)
    mat = dot(mat,m3)

    return mat

def easy_translate(loc,matri,f,center=(400,300),zoom_in=1,way='p',return_all=False) :
    '''
    本函数用于在pygame中的立方体示范程序，目的在于简化操作
    将世界坐标系中三位点的坐标输入，给定焦距，屏幕中心，放大倍数，坐标变换矩阵
    投影方式，本函数将直接给出屏幕上点的二维坐标。
    函数原型：
    easy_translate(loc,matri,f,center=(400,300),zoom_in=1,way='p',return_all=False)
    loc为世界坐标系坐标，尺寸n*3
    matri为变换矩阵，f焦距，其余的意义也比较明显
    最后的return_all为假的时候将只返回2*n的二维坐标，为真时将同时返回照相机坐标系
    的三维坐标和二维屏幕坐标，次序为三维，二维，三维坐标的尺寸为3*n
    '''
    m1 = translate(matri,loc,zoom_in)
#    print(m1.shape)
    m2 = to2d(f,m1,center,way)

    if return_all :
        return m1,m2
    else :
        return m2

def easy_move(loc,distance) :
    '''
    本函数是用来方便的完成平移的，只在立方体的示例程序中有用
    定制化函数
    函数原型：
    easy_move(loc,distance)
    loc为三维点矩阵尺寸3*n
    distance为现在的立方体中心坐标
    '''
    x,y,z = -distance
    x1,y1=loc.shape
    out = ones([y1,x1+1])
    out[:,:3]=loc.transpose()
    matri = diag([1,1,1,1])
    matri[3,0:3]=[x,0,z]
    matri = matri[:,0:3]
    out = dot(out,matri)
    return out.transpose()


if __name__ == '__main__' :
#    a = [[1,2,3],
#         [2,3,4],
#         [5,6,7]]
#    a = array(a)
#    ang = [-pi/6,pi/3,pi/4]
#    mat = count_matrix(ang)
#    tes = array([[10,10,10],[30,10,10],[30,30,10]])
#
#    bb = translate(mat,tes)
#
#    cc = to2d(50,bb,way='t')
    print(count_angle([1,1,1]))
