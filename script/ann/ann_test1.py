# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 22:21:16 2016

@author: stan han
"""

from numpy import *
from math import pi
from net_function import *
#from random import random
from numpy.linalg import *
from matplotlib.pyplot import *


y = array(range(1000))
y = y*5*pi/1000
t = sin(y)

w1 = random.random([8,1])
b1 = random.random([8,1])

w2 = random.random([1,8])
b2 = random.random([1,1])

n = 5000
alpha = 0.03
for times in range(n) :

    for n,i in enumerate(y) :

        a1 = dot(w1,i)+b1
        o1 = logsig(a1)

        a2 = dot(w2,o1)+b2
        o2 = purelin(a2)

        e = t[n]-o2
        s2 = -2*e

        w2t = w2.transpose()

        s1 = dot(diag(d_logsig(a1).flatten()),w2t)
        s1 = dot(s1,s2)

        o1t = o1.transpose()
        w2 = w2-alpha*dot(s2,o1t)
        b2 = b2-alpha*s2

        w1 = w1-alpha*dot(s1,i)
        b1 = b1-alpha*s1
out = ones(t.shape)
for n,i in enumerate(y) :
    a1 = dot(w1,i)+b1
    o1 = logsig(a1)

    a2 = dot(w2,o1)+b2
    o2 = purelin(a2)
    out[n] = o2

plot(y,t,y,out)
