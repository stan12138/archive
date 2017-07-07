# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 23:58:19 2016

@author: stan han
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 20:49:50 2016

@author: stan han
"""


'''
这是一个多线程的示范样例，应用于bt的，可以工作，
但是接口问题并没有处理完，因而，还需要做一些微调。
时间:2016.7.31 23:59


bt最新版
2016.8.1 23:33

'''
import requests
import urllib.request

from bs4 import BeautifulSoup,Tag
import re
import PIL.Image

from xlwt import *
import threading



w = Workbook(encoding='utf-8')
ws = w.add_sheet('北邮人科幻电影列表')

w1 = Workbook(encoding='utf-8')
ws1 = w1.add_sheet('北邮人科幻电影列表')


filename = 'film.txt'


def get_captcha(bs) :
    goal = re.compile('imagehash=')
    lis = bs.findAll("input",{'name':"imagehash"})
    dd = lis[0]
    bb = dd.attrs['value']
    #print(bb)
    newurl = 'http://bt.byr.cn/image.php?action=regimage&imagehash='
    newurl +=bb
    #print(newurl)
    urllib.request.urlretrieve(newurl,'yanzhan.png')
    a = PIL.Image.open('yanzhan.png')
    a.show()
    return bb
#负责获取验证码及验证码图片的hash


def login(session,header) :
    url = 'http://bt.byr.cn/'
    r = session.get(url,headers=header)
    html = r.text
    #print(session.headers)
    bs = BeautifulSoup(html,'html.parser')

    bb = get_captcha(bs)
    return bb
#负责登陆

def cleanstr(url,str1) :
    l1 = len(str1)
    n = url.count(str1)
    for i in range(n) :
        l = len(url)
        loc = url.index(str1)
        url = url[0:loc]+url[loc+n+1:l]
    return url
#用于从字符串中删除指定字符串


def checknum(str1,zheng = False) :
    if zheng :
        a = '1234567890'
    else :
        a = '1234567890.'
    x = 0
    for i in str1 :
        if i in a :
            x += 1
    return x==len(str1)




def getnl(bs,imdb) : #获取中文名和对应的链接
    name = 0
    link = 0
    na = bs.get_text()
    if '[' in na :
        name = na
    for i in bs.next_siblings :
        if isinstance(i,Tag) :
            aa = i.findAll('a',{'href':imdb})
            for j in aa :
                link=j.attrs['href']
    return name,link

def getimdb(link,chinese,order1,c_name,e_name,year,score,people,order) :  #从link链接到imdb官网，获取所有的信息
    if not link==0 :
        e_name1 = 0
        year1 = 0
        score1 = 0
        people1 = 0
        uurl = urllib.request.urlopen(link)
        bs = BeautifulSoup(uurl)
        bsimdb = bs.findAll('meta',{'property':'og:title'})
        bimdb = bs.findAll('strong',{'title':goal2})
        for j in bsimdb :
            name = j.attrs["content"]
            e_name1 = name[0:-6]

            num = name[-5:-1]
            if checknum(num,zheng=True) :
                year1 = int(num)
            else :
                year1=num
        for j in bimdb :
            name = j.attrs["title"]
            #print(name)

            num = name[0:3]
            if checknum(num) :
                score1=float(num)
            else :
                score1=num
            num = name[13:-13]
            num = cleanstr(num,',')
            if checknum(num,zheng=True) :
                people1=int(num)
            else :
                people1=num

    else :
        e_name1 = '未发现'
        year1 = '未发现'
        score1 = '未发现'
        people1 = '未发现'
    print(e_name1)
    c_name.append(chinese)
    e_name.append(e_name1)
    year.append(year1)
    score.append(score1)
    people.append(people1)
    order.append(order1)
    #print(chinese)
    #print(e_name1,year1,score1,people1)
    #return c_name,e_name,year,score,people

def wr_excel(ws,x,*lis,txt=False) :
    if not txt :
        n = len(lis)
        length = len(lis[0])
        x = x-1
        #print(length)
        for i in range(n) :
            yuansu = lis[i]
            if not len(yuansu)==length :
                print(len(yuansu))
                print('输入列表长度不一致')
                return
        for i in range(n) :
            yuansu = lis[i]
            for j in range(length) :
                ws.write(x-j,i,yuansu[j])
                #print(x-j,i)
    else :
        pass

def wr_txt(filename,name,order) :
    file=open(filename,'a')
    for i in range(len(order)) :
        or1 = str(order[i])
        file.write(or1+'\n')
        file.write(name[i])
        file.write('\n')
        file.write('\n')
    file.close()



header = {'Pragma': 'no-cache',
          'Accept': 'text/html, application/xhtml+xml, */*',
          'Accept-Encoding': 'gzip, deflate',
          'Accept-Language': 'zh-CN',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
          'Referer': 'http://bt.byr.cn/login.php?returnto=torrents.php',
          'Connection': 'Keep-Alive',
          'Host': 'bt.byr.cn'
}


session = requests.Session()

im_hash = login(session,header)
captcha = input('输入验证码')

url = 'http://bt.byr.cn/'
url += '/takelogin.php'
id1 = '*****'
password = '*******'

postd = {'username':id1,
         'password':password,
         'imagestring':captcha,
         'imagehash':im_hash}
s = session.post(url,postd,headers=header)


x = 0
c_name = []
e_name = []
year = []
score = []
people = []
order=[]


alllink = []
name = []
delet_this = 'qwertyuiopasdfghjklzxcvbnm.-[]QWERTYUIPOASDFGHJKLZXCVBNM1234567890/()'

for page in range(2) :
    print('这是第%d页'%page)
    if page == 0 :
        url = 'http://bt.byr.cn/torrents.php?secocat=&cat=&incldead=0&spstate=0&inclbookmarked=0&search=%E7%A7%91%E5%B9%BB&search_area=0&search_mode=0'
    else :
        url = 'http://bt.byr.cn/torrents.php?inclbookmarked=0&incldead=0&spstate=0&search_area=0&search=%E7%A7%91%E5%B9%BB&search_mode=0&page='
        url = url+str(page)
    s = session.get(url)
    bs2 = BeautifulSoup(s.text,'html.parser')


    c_goal = re.compile("^details.*php\?id=.*hit=1$")
    bb = bs2.findAll('a',{'href':c_goal})
    imdb = re.compile("^http.*imdb.*$")

    goal2 = re.compile(".*")

    for n in bb :
        #print(x)
        name1,link = getnl(n,imdb)
        #print(name)
        x+=1
        alllink.append(link)
        name.append(name1)

n=len(alllink)
print(n)
flage = True
n1 = 0
while flage :
    print(n1)
    if n1<n-200 :
        thr = []
        for i in range(200) :
            t1 = threading.Thread(target=getimdb,args=(alllink[n1+i],name[n1+i],x-n1-i,c_name,e_name,year,score,people,order))
            thr.append(t1)

        for i in thr :
            i.setDaemon(True)
            i.start()

        for i in thr :
            i.join()
        n1 = n1+200
    else :
        thr = []
        for i in range(n-n1) :
            t1 = threading.Thread(target=getimdb,args=(alllink[n1+i],name[n1+i],x-n1-i,c_name,e_name,year,score,people,order))
            thr.append(t1)

        for i in thr :
            i.setDaemon(True)
            i.start()

        for i in thr :
            i.join()
        flage = False

for i in range(len(c_name)) :
    chat = c_name[i]
    orde = chat.find(']')
    c_name[i] = chat[1:orde]
for i in range(len(c_name)) :
    a = c_name[i]
    b = ' '
    for j in a :
        if not j in delet_this :
            b += j
    c_name[i] = b
    print(c_name[i])


wr_excel(ws1,x,e_name,year,score,people,order)
w1.save('bupt_movies_imdb34.xls')

wr_excel(ws,x,c_name,order)
w.save('bupt_movies_name34.xls')



