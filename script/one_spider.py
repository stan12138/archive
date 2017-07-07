# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 00:22:41 2016

@author: stan han
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import codecs
import threading
from numpy import *

head = '*******'

ji = 45856


#tt = codecs.open('tt.txt','a','utf-8')

def way(tag) :
    return tag.get_text()

def take(name,url,end1,order,tag1,tag2,tag3) :
    text = codecs.open(name,'a','utf-8')
    for i in order :
        print(url+str(i)+end1)
        html = urlopen(url+str(i)+end1)
        #print(html)
        bs = BeautifulSoup(html)
        #print(bs)
        bs = bs.findAll(tag1,{tag2:tag3})

        for j in bs :
            #print(j)
            text.write(way(j))
        print(i)
    text.close()




def auto(for_name,url,end,tag1,tag2,tag3,begin,eend,length):
    al = eend-begin
    n = int(al/length)
    la = al-n*length

    th = []

    for i in range(n) :
        a = range(begin+i*length,begin+(i+1)*length)
        name = for_name+'_'+str(i)+'.txt'
        t1 = threading.Thread(target=take,args=(name,url,end,a,tag1,tag2,tag3))
        th.append(t1)
        #take(name,url,end1 = end,a,tag1,tag2,tag3)
    a = range(begin+n*length,begin+n*length+la)
    name = for_name+'_'+str(i+1)+'.txt'
    t1 = threading.Thread(target=take,args=(name,url,end,a,tag1,tag2,tag3))
    th.append(t1)
    for i in th :
        i.setDaemon(True)
        i.start()

    for i in th :
        i.join()


url = head
auto('rxx',url,'/','div','id','nr1',ji,46066,50)





'''
def text(begin,name) :
    tt = codecs.open(name,'a','utf-8')
    for n in range(begin,begin+50) :
        html = urlopen(head+str(ji+n)+end)
        bs = BeautifulSoup(html)
        bb = bs.findAll('div',{'class':"nr_nr"})
        for j in bb :
            tt.write(j.get_text())
        print(n)
    tt.close()
def last() :
    tt = codecs.open('new111.txt','a','utf-8')
    for n in range(150,181) :
        html = urlopen(head+str(n+ji)+end)
        bs = BeautifulSoup(html)
        bb = bs.findAll('div',{'class':"nr_nr"})
        for j in bb :
            tt.write(j.get_text())
        print(n)
    tt.close()

'''
#for n in range(214) :
#        html = urlopen(head+str(ji+n)+end)
#        bs = BeautifulSoup(html)
#        bb = bs.findAll('dd',{'id':"contents"})
#        for j in bb :
#            tt.write(j.get_text())
#        print(n)
#
#tt.close()

'''
th = []
t1 = threading.Thread(target=text,args=(0,'t111.txt'))
th.append(t1)
t1 = threading.Thread(target=text,args=(50,'t211.txt'))
th.append(t1)
t1 = threading.Thread(target=text,args=(100,'t311.txt'))
th.append(t1)
#t1 = threading.Thread(target=text,args=(150,'t41.txt'))
#th.append(t1)
t1 = threading.Thread(target=last)
th.append(t1)

for i in th :
    i.setDaemon(True)
    i.start()

for i in th :
    i.join()
'''





