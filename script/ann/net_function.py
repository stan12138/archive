# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 23:04:05 2016

@author: stan han
"""
from numpy import *
#from matplotlib.pyplot import *

def hardlim(x) :
    return x>=0

def hardlims(x) :

    x1 = x<0
    x1 = -1*x1
    x2 = x>=0
    return x1+x2

def purelin(x) :
    return x

def satlin(x) :

    x1 = x>1
    x2 = logical_and(x<=1,x>=0)
    x2 = x2*x
    return x1+x2

def satlins(x) :
    x1 = x>1
    x2 = logical_and(x<=1,x>=-1)
    x2 = x2*x
    x3 = x<-1
    x3 = -1*x3
    return x1+x2+x3

def logsig(x) :
    return 1/(1+exp(-x))

def tansig(x) :
    return (exp(x)-exp(-x))/(exp(x)+exp(-x))

def poslin(x) :
    x1 = x>=0
    return x1*x

def d_purelin(x):

    return ones(x.shape)

def d_logsig(x) :
    return exp(-x)/((1+exp(-x))**2)

def d_tansig(x) :
    return 4/((exp(-x)+exp(x))**2)

can_d_function = [purelin,logsig,tansig]
function_d = [d_purelin,d_logsig,d_tansig]

if __name__ == '__main__' :
    x = range(-100,100)
    x = array(x)
    x= 0.1*x
    y = d_tansig(x)

    plot(x,y)










