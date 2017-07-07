# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 21:33:58 2016

@author: stan han
"""

from numpy import *
from math import pi
from net_function import *
#from random import random
from numpy.linalg import *
from tree import *



def ann(n,f) :
    if len(n)<2 :
        print('网络的层数不得少于两层')
        return
    if not len(f)+1==len(n) :
        print('层数与传输函数的个数不符')
        return



#初始化程序段
    layer = len(n)
    w = list(range(layer-1))
    b = list(range(layer-1))
    a = list(range(layer-1))
    o = list(range(layer-1))
    df = list(range(layer-1))
    s = list(range(layer-1))
    e = list(range(n[-1]))

    layer = n
    n = len(n)


    for i in range(n-1) :
        w[i] = random.random([layer[i+1],layer[i]])
        #print('w%s'%i,w[i])
        b[i] = random.random([layer[i+1],1])
        #print('b%s'%i,b[i])
        a[i] = random.random([layer[i+1],1])
        #print('a%s'%i,a[i])
        o[i] = random.random([layer[i+1],1])
        #print('o%s'%i,o[i])
        df[i] = function_d[can_d_function.index(f[i])]
        #print('df%s'%i,can_d_function.index(f[i]))
        s[i] = ones([layer[i+1],1])
        #print('s%s'%i,s[i])



#生成图形结构
    ax=init(size=(30,10))
    dx = 1/(n+1)
    node_list = list(range(n))
    for i in range(n) :

        li = []
        dy = 1/(layer[i]+1)
        for j in range(layer[i]) :
            nod = node(ax,((i+1)*dx,dy*(j+1)),str(i)+','+str(j))
            li.append(nod)
        node_list[i] = li
    for i in range(n-1) :
        nod = node_list[i]
        nod1 = node_list[i+1]
        for j1 in nod :
            for j2 in nod1 :
                j1.connect(j2)
    node_list[0][0].show()
    node_list[0][0].save('anntest')



if __name__ == '__main__' :
    ann([15,3,10,2,10],[logsig,logsig,purelin,purelin])

