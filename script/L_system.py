# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 11:51:19 2016

@author: stan han
"""

from matplotlib.pyplot import *
from math import radians,sin,cos
from copy import deepcopy

def update(s,rule) :
    for key in rule :
        s = s.replace(key,rule[key])
    
    return s


def translate(state,s,d,theta) :
    store = []
    for i in s :

        if i == '[' :
            store.append(deepcopy(state)) #切记deepcopy

        elif i == '+' :
            state[2]-=theta
        elif i == '-' :
            state[2]+=theta
        elif i == ']' :
            state = deepcopy(store[-1])
            store.pop(-1)
        elif i == 'F' :

            plot([state[0],state[0]+d*cos(radians(state[2]))],[state[1],state[1]+d*sin(radians(state[2]))],'k-')
            state[0] = state[0]+d*cos(radians(state[2])) 
            state[1] = state[1]+d*sin(radians(state[2]))

    return state


if __name__ == '__main__' :
    
    
    #rule = {'F':'F[-F]F[+F]'}
    s = 'F'
    state = [0.5,0,90] #x,y,theta

    rule = {'F':'FF-[-F+F+F]+[+F-F-F]'}
    #rule = {'G':'GFX[+++++GFG][-----GFG]','X':'F-XF'}
    #rule = {'S':'[+++H][---G]TS','G':'+H[-G]L','H':'-G[+H]L','T':'TL','L':'[-FFF][+FFF]F'}
    for i in range(6) :
        state = translate(state,s,0.1,30)
        s = update(s,rule)


    #axis([0,30,0,30])
    #plot(0,0,1,1,'r-')
    
    
    