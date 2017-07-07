# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 22:15:20 2016

@author: stan han
"""

from numpy import *
from PIL.Image import *
from matplotlib.pyplot import *
from numpy.linalg import *
from math import pi
#import time
'''
问题好多呀，注意要做的事：调整格式一致，输入图像名字，输出调整之后的一个同样大小的
数组；使用interp优化速度;因为array不够智能化，如果数据是浮点型，而array是整型，数据
会出错，审查一下这个问题；最后要注意在转换为uint8
2016.6.25已经修改审查完成，作者：stan

16.8.14 stan
确认已经将itools2中的内容整合到一起

'''



def hist_equal(imagename,show_image = True,save_image = False,is_array=False,name='xxx',check = True) :
    '''这是一个使用直方图均衡的图像处理函数
    支持以数组形式输入'''
    #start = time.clock()
    if not is_array :
        im_origin = array(open(imagename).convert('L'))
    else :
        im_origin = imagename
    im_flatten = im_origin.flatten()
    length = len(im_flatten)
#打开图像，转换为256灰度，压平为一维数组，并计算像素个数
    count = [0]*256
    count = bincount(im_flatten)

    count = append(count,[0]*(256-len(count)))
    count = float32(count)
#使用内置函数统计各灰度级的像素数，并补充扩展为256个灰度级
#转换格式为浮点数，此步十分必要
    #first = time.clock()
    #print('first',first-start)

    count[0] = count[0]/length
    for i in range(1,256) :
        count[i] = count[i]/length + count[i-1]
#计算灰度级的密度，并做累计，下一步是直方图均衡的处理
    count = 255*array(count)

    im_flatten = interp(im_flatten,range(256),count)

    if check :
        for i in range(len(im_flatten)) :
            if im_flatten[i]<=0 :
                im_flatten[i] = 0
            if im_flatten[i]>=255 :
                im_flatten[i] = 255
#使用内置的一维插值函数，高速完成图片灰度级的映射
    new = im_flatten.reshape(im_origin.shape)

    new = uint8(new)
#将一维数组重整形状为图片的尺寸，转换为256灰度级，uint8类型
    if show_image :
        gray()
        imshow(new)
#显示图片，注意先设置为gray,否则会显示出假彩色
    #print('second',time.clock()-start)
    if save_image :
        save_image1 = fromarray(new)
        save_image1.save(name+'increase'+'.jpg')
#保存图片，先将array转换为图片类型，然后保存设置保存格式和名字
    return new

def fast_hist_equal(imagename,show_image = True,save_image = False) :
	#start = time.clock()
    '''这是一个来自参考书的示例直方图均衡的程序，不做过多说明'''
    nbr_bins = 256
    im_origin = array(open(imagename).convert('L'))

    imhist,bins = histogram(im_origin.flatten(),nbr_bins,normed=True)

    cdf = imhist.cumsum() # cumulative distribution function

    cdf = 255 * cdf / cdf[-1]
	#print(cdf.shape,bins.shape)
	#print(bins[10:20])
    im2 = interp(im_origin.flatten(),bins[:-1],cdf)
    im2 = im2.reshape(im_origin.shape)
    im2 = uint8(im2)

    if show_image :
        gray()
        imshow(im2)
#显示图片，注意先设置为gray,否则会显示出假彩色
    #print('second',time.clock()-start)
    if save_image :
        save_image1 = fromarray(im2)
        save_image1.save(imagename[:-4]+'increase'+'.jpg')
	#print(im2.mode)

	#print(time.clock()-start)
def im_map(imagename,in_range=[200,50],out_range=[80,100],gama = 0.2,show_image = True,save_image = False,is_array=False,name='xxx') :
    '''总算是搞定了。函数使用方法说明:1、infan输入原始图像的要映射的灰度范围
    outfan输入对应的输出映射范围，2、规范情形下，要求输入范围是256灰度级
    3、第三个参数决定映射曲线的形状，必须大于零，等于1时线性映射，小于1时
    映射曲线上凸，大于1映射曲线下凹，数的大小决定凹凸程度
    支持以数组形式输入'''
    if is_array :
        im_origin = imagename
    else :
        im_origin = array(open(imagename).convert('L'))

    im_flatten = im_origin.flatten()

    in_min = min(in_range)
    out_min = min(out_range)
    in_max = max(in_range)
    out_max = max(out_range)

    n_or_p = (in_max==in_range[0] and out_max==out_range[0]) or (in_min==in_range[0] and out_min==out_range[0])


    f = lambda x,y,a,b,k : ((x-a)**y)*k+b
    bili = abs(out_range[1]-out_range[0])/(abs(in_range[1]-in_range[0])**gama)
    #上面这两个应用于正常的正的映射，下面这两个应用于反的映射
    f2 = lambda x,y,a,b,k : -((x-a)**y)*k+b
    bili2 = abs(out_range[1]-out_range[0])/(abs(in_range[1]-in_range[0])**(1/gama))
    #在这个处理的函数中，映射曲线是指数函数
    x = range(256)
    y = list(range(256))
    for i in range(256) :
        if i<in_min :
            if n_or_p :
                y[i] = out_min
            else:
                y[i] = out_max
        elif i>in_max :
            if n_or_p :
                y[i] = out_max
            else:
                y[i] = out_min
        else :
            if n_or_p :
                y[i] = f(i,gama,in_min,out_min,bili)
            else:
                y[i] = f2(i,1/gama,in_min,out_max,bili2)
#    plot(x,y)
#    show()
    im = uint8(interp(im_flatten,x,y))
    im = im.reshape(im_origin.shape)
    if show_image :
        gray()
        imshow(im)
#显示图片，注意先设置为gray,否则会显示出假彩色
    #print('second',time.clock()-start)
    if save_image :
        save_image1 = fromarray(im)
        save_image1.save(name+'increase'+'.jpg')

    return im

def im_map_log(imagename,show_image = True,save_image = False,is_array = False,name = 'xxx') :
    '''按照对数的规则进行映射，没有可调整性
    支持以数组形式输入'''
    if is_array :
        im_origin = imagename
    else :
        im_origin = array(open(imagename).convert('L'))
    im_flatten = im_origin.flatten()
    y = list(range(256))
    y = array(y)
    #c = arr[:]
    y = 46*log(1+y)#核心函数
    x = range(256)
    im = uint8(interp(im_flatten,x,y))
    im = im.reshape(im_origin.shape)
    if show_image :
        gray()
        imshow(im)
#显示图片，注意先设置为gray,否则会显示出假彩色
    #print('second',time.clock()-start)
    if save_image :
        save_image1 = fromarray(im)
        save_image1.save(name+'increase'+'.jpg')
    return im
def im_stretch(imagename,midpoint=128,slop=9,show_image = True,save_image = False,is_array=False,name = 'xxx') :
    '''对比度拉伸的函数，输入的两个参数负责设置映射曲线的中点和倾斜程度
    支持以数组形式输入'''
    if is_array :
        im_origin = imagename
    else :
        im_origin = array(open(imagename).convert('L'))
    im_flatten = im_origin.flatten()
    a = list(range(256))
    a[0] = 1
    a = array(a)
    b = 255/(1+(midpoint/a)**slop)#核心函数
    a = range(256)
    im = uint8(interp(im_flatten,a,b))
    im = im.reshape(im_origin.shape)
    if show_image :
        gray()
        imshow(im)
#显示图片，注意先设置为gray,否则会显示出假彩色
    #print('second',time.clock()-start)
    if save_image :
        save_image1 = fromarray(im)
        save_image1.save(name+'increase'+'.jpg')
    return im
def open2(imagename,midpoint = 100,is_array = False) :
    '''支持以数组形式输入
       打开一个二值图像，保存倒数组内，返回这个数组'''
    if is_array :
        origin = imagename
    else :
        origin = open(imagename).convert('L')
    a = array(origin)
    b = a > midpoint
    return b

def show2(array2) :
    '''
    显示一个存储了二值图像的数组'''
    a = uint8(array2*255)
    gray()
    imshow(a)
    #show()

def save2(array2,name) :
    '''以给定的名字保存存储了二值图像的数组'''
    a = uint8(array2*255)
    b = fromarray(a)
    b.save(name+'.jpg')
    #b.show()


def imfilter(imarray,masking,check = False) :
    '''这是一个掩模计算函数，因为没有找到快速算法，因此只用了慢速的双重循环法
    扩充矩阵填充值为零
    脑子很晕，名字很乱，凑合一下吧
    支持uint8检查
    16.8.27 千万要小心，应用的目的是什么，因为有些时候，负值和超过255的值是有特殊用途的
    因而这些时候要把check废掉'''
    m_size = masking.shape
#    print(masking)
#    print(m_size)
    i_size = imarray.shape
    msize = array(m_size)-1
    out_im = zeros(imarray.shape)
#    print(msize)
    x = msize[0]/2
    y = msize[1]/2
    new_im = zeros(array(i_size)+msize)
    new_im[x:x+i_size[0],y:y+i_size[1]] = imarray
    #print(new_im)
    for i in range(i_size[0]) :
        for j in range(i_size[1]) :
            cut = new_im[i:i+m_size[0],j:j+m_size[1]]
            out_im[i,j] = sum(cut*masking)
    #print(out_im)
    if check :
        for i in range(i_size[0]) :
            for j in range(i_size[1]) :
                if out_im[i,j]<=0 :
                    out_im[i,j]=0
                if out_im[i,j]>=255 :
                    out_im[i,j]=255


    return out_im

def imdilate(array2,masking) :
    '''本算法只处理二值图像数组和二值膨胀masking'''
    if  array2.dtype == bool and masking.dtype == bool :
        pass
    else :
        return
    m_size = masking.shape
    i_size = array2.shape
    msize = array(m_size)-1
    #out_im = zeros(array2.shape)
    x = msize[0]/2
    y = msize[1]/2
    new_im = zeros(array(i_size)+msize,dtype = bool)

    new_im[x:x+i_size[0],y:y+i_size[1]] = array2
    out_im = zeros(new_im.shape,dtype = bool)
    #print(new_im)
    for i in range(i_size[0]) :
        for j in range(i_size[1]) :
            cut = new_im[i:i+m_size[0],j:j+m_size[1]]

            cu1 = out_im[i:i+m_size[0],j:j+m_size[1]]
            if cut[x,y] == masking[x,y] :
                cu2 = cut|masking
                #print(cu1.dtype)
                out_im[i:i+m_size[0],j:j+m_size[1]] = cu2|cu1
    #print(out_im)
    return out_im[x:-x,y:-y]

def imerode(array2,masking) :
    '''本算法只处理二值图像数组和二值腐蚀masking'''
    if  array2.dtype == bool and masking.dtype == bool :
        pass
    else :
        return
    m_size = masking.shape
    i_size = array2.shape
    msize = array(m_size)-1
    #out_im = zeros(array2.shape)
    x = msize[0]/2
    y = msize[1]/2
    new_im = zeros(array(i_size)+msize,dtype = bool)
    #print(new_im.shape,x,x+i_size[0],y,y+i_size[1])
    new_im[x:x+i_size[0],y:y+i_size[1]] = array2
    out_im = zeros(array2.shape,dtype = bool)
    #print(new_im)
    for i in range(i_size[0]) :
        for j in range(i_size[1]) :
            cut = new_im[i:i+m_size[0],j:j+m_size[1]]

            #cu1 = out_im[i:i+m_size[0],j:j+m_size[1]]
            if (cut&masking == masking).all() :
                #cu2 = cut|masking
                #print(cu1.dtype)
                out_im[i,j] = True
    #print(out_im)
    return out_im

def imopen(array2,masking) :
    im1 = imerode(array2,masking)
    return imdilate(im1,masking)

def imclose(array2,masking) :
    im1 = imdilate(array2,masking)
    return imerode(im1,masking)

def bwhitmiss(array2,masking1,masking2) :
    im1 = imerode(array2,masking1)
    im2 = imerode(~array2,masking2)
    return im1&im2

def scaling(ima,aim,check=True) :
    '''支持uint8的处理
    双线性内插法图像缩放函数'''
    x0,y0 = ima.shape
    x1,y1 = aim
    aim = ones(aim)
    for i in range(x1) :
        for j in range(y1) :
            x = i*(x0-1)/(x1-1)
            y = j*(y0-1)/(y1-1)
            xi = int(x)
            yi = int(y)
            if xi==x :
                xii = xi
            else :
                xii = xi+1
            if yi==y :
                yii = yi
            else :
                yii = yi+1
            u = x-xi
            v = y-yi
            a = ima[xi,yi]
            b = ima[xii,yi]
            c = ima[xi,yii]
            d = ima[xii,yii]
            aim[i,j]=a*(1-u)*(1-v)+u*(1-v)*b+v*(1-u)*c+u*v*d
    if check :
        for i in range(x1) :
            for j in range(y1) :
                if aim[i,j]<=0 :
                    aim[i,j]=0
                if aim[i,j]>=255 :
                    aim[i,j]=255
        aim = uint8(aim)
    return aim

def mapping(loc,ax,ay) :
    '''此函数是一个在图像配准中的辅助函数，
    用来帮助利用计算出来的系数计算映射坐标'''
    x,y=loc
    a = array([x,y,x*y,1])
    x = dot(a,ax)
    y = dot(a,ay)
    return x,y

def im_regis(ima,ax,ay,out_size) :
    '''此函数也是一个辅助函数，用来负责遍历所有像素点，完成坐标映射和灰度值计算
    灰度值的映射采用了双线性内插法'''
    out = ones(out_size)
    nx,ny = out.shape
    for i in range(nx) :
        for j in range(ny) :
            x,y=mapping([i,j],ax,ay)
            xi = int(x)
            yi = int(y)


            if xi==x :
                xii = xi
            else :
                xii = xi+1
            if yi==y :
                yii = yi
            else :
                yii = yi+1


            u = x-xi
            v = y-yi
            a = ima[xi,yi]
            b = ima[xii,yi]
            c = ima[xi,yii]
            d = ima[xii,yii]
            out[i,j]=a*(1-u)*(1-v)+u*(1-v)*b+v*(1-u)*c+u*v*d
    return out

def im_registration(ima,out_size,in_point) :
    '''用于完成图像配准的函数，要求输入要配准图像的数组
    使用双线性内插法计算坐标映射，因而在图像畸变上大概是有一定的限制的，
    要求有四个参考点，out_size指输出的图像得尺寸，in_point指输入的图像中参考点的位置
    技术要点：反向映射，从输出图像计算在输入图像中的位置。双线性内插法计算灰度值'''
    p1,p2 = out_size
    out_point = array([[0,0],[0,p2-1],[p1-1,0],[p1-1,p2-1]])
    a = ones([4,4])
    a[:,0:2]=out_point
    a[:,2]=out_point[:,0]*out_point[:,1]

    b = in_point[:,0]
    b1 = in_point[:,1]

    ax = solve(a,b)
    ay = solve(a,b1)
#上述语句构造出了系数矩阵，值矩阵，然后使用numpy的求解线性方程组的内置函数求解，答案为ax,ay
#ax,ay分别对应x,y坐标的映射参数
    out = im_regis(ima,ax,ay,out_size)
#为了简化结构此处应用另一个自定义函数完成最后的映射
    return out

def fspecial(size,sigma) :
    '''产生指定尺寸的高斯滤波器模板，均值为0，标准差由sigma指明，不支持偶数尺寸'''
    x,y=size
    if x%2 and y%2 :
        pass
    else :
        print('现在不支持偶数形状的模板')
        return False
    rx = (x-1)/2
    ry = (y-1)/2
    out = zeros(size)
    for i in range(x) :
        for j in range(y) :
            out[i,j] = exp(-((i-rx)**2+(j-ry)**2)/(2*sigma**2))/(2*pi*sigma**2)
    x = sum(sum(out))
    out = out/x
    return out


def harris(name,bound=False,le=5,size=[3,3],sigma=2,r=6,is_array=False) :
    '''这是一个基础基础版本的harris角点检测函数，精度只是像素级的，运算速度也比较慢

    关于参数及使用的说明：

    首先支持以数组或者图片名字的形式输入
    支持设置检测的范围，范围的形式为：bound=[a,b,c,d],a,b代表从第a到b行，c,d表示从
    第c到d列，当然，也可以不设置
    le为梯度检测模板的长度，这是一个重要的参数，要求必须是奇数
    size是高斯滤波器的尺寸，sigma为标准差，这两个参数也十分重要
    r为局部最大值检测的窗口尺寸，同样十分重要
    需要注意的是，返回的结果，目前只有检测出来的角点在原图片中的行标和列标分别
    储存在x,y中
    '''
    if is_array :
        a = name
    else :
        a = array(open(name).convert('L'))
#支持以数组或者文件的形式打开
    nx,ny = a.shape

    if bound :
        if not len(bound)==4 :
            print('范围必须长度为4')
            return False,False
        if bound[0]>=0 and bound[1]<nx and bound[2]>=0 and bound[3]<ny :
            pass
        else :
            print('范围错误')
            return False,False
        a = a[bound[0]:bound[1],bound[2]:bound[3]]
    mas = fspecial(size,sigma)
#高斯滤波器支持尺寸和标准差的调整
    if  not le%2 :
        print('梯度滤波器只支持奇数长度')
        return False,False
#    print(le)
    mas2 = linspace(-(le-1)/2,(le-1)/2,le)
    mas2 = mas2.reshape([1,le])
    mas3 = mas2.reshape([le,1])
    #此处必须要注意，因为在filter的函数中要求模板的shape必须是二维的，因而
    #需要这一步，因为numpy的另一个bug是例如5行1列只会显示（5，）
#梯度滤波器只支持长度的调整，并且梯度滤波器只支持奇数长度
#    print(mas2.shape)
#    print(mas3.shape)
    c2 = imfilter(a,mas2)
    c3 = imfilter(a,mas3)
#大概的工作过程是，首先使用x,y方向的梯度滤波器，计算出Ix,Iy，然后再
#计算出M矩阵元,结果使用高斯滤波器进行平滑

    c4 = c2**2
    c5 = c3**2
    c6 = c2*c3

    c4 = imfilter(c4,mas)
    c5 = imfilter(c5,mas)
    c6 = imfilter(c6,mas)

    big = 0
#c3、big分别负责记录每个像素点的R值，和所有R之中的最大值，是叫R值吗？记不太清了
#差不多吧，大概是这样，如果想确认的话，自己去查阅资料
    c3 = ones(a.shape)
    xx = ones([2,2])#这只是一个辅助变量

    nx,ny = a.shape
    for i in range(nx) :
        for j in range(ny) :
            xx[0,0] = c4[i,j]
            xx[1,1] = c5[i,j]
            xx[0,1] = c6[i,j]
            xx[1,0] = c6[i,j]

            c3[i,j] = det(xx)-0.04*(trace(xx))**2
            if c3[i,j] >big :
                big = c3[i,j]
#此循环负责计算每个像素点的R值
    con = 0
    x = []
    y = []
#接下来需要在计算完的R矩阵中，使用一个窗口，计算局部最大值，超过阈值的局部最大值
#局部最大值的窗口的大小由r负责调控,这也是一个重要参数
#使用x,y记录检测出来的角点的坐标，分别是行和列，con是角点的数目，并未返回
    result = zeros(a.shape)
    for i in range(r,nx-r) :
        for j in range(r,ny-r) :
            xx = c3[i-r:i+r,j-r:j+r]
            ma1 = amax(xx)
            if c3[i,j]>0.004*big and c3[i,j]==ma1 :
                result[i,j] = 1
                x.append(i)
                y.append(j)
                con+=1
    #print(con)
    result = 255*result
#result会是一个二值图像数组，使用白点标记出检测出的角点的位置，尚未返回，可以考虑
#
    x = array(x)
    y = array(y)
    if bound :
        x = x+bound[0]
        y = y+bound[2]
    return x,y


def hough_lines(name,is_array = False,gate = 30,distance = 30,show_image=True) :
    ''''
    本函数是基础基础版的霍夫直线检测函数
    要求：如果以数组形式输入，必须是二值的
    如果以图片形式输入，将自动以最简单的方法处理成二值，总之，建议自行将
    图片做好妥善处理之后以二值数组输入函数
    返回的结果是两个列表，分别为r,theta这两个量是以r = y*sin(theta)+x*cos(theta)
    形式表示的直线方程
    输入参数中重点可调整项是：gate,distance
    其中的gate是阈值，即认为一条直线得到的票数超过了多少票即认为是一条直线
    distance是是筛掉接近的直线的，它的计算方式就是直接算了两条直线的r的差值与倾角的
    差值之和，典型的distance是100,20差不多的量级，看着调
    '''
    if is_array :
        a = name
    else :
        a = open2(name)
#首先获取二值矩阵
    nx,ny = a.shape
    n1 = int(sqrt(nx**2+ny**2))

    xy = zeros([n1,180])
#xy是一个霍夫空间，至于这个空间的设置，在写的时候我依旧有些不是十分明白
    for i in range(nx) :
        for j in range(ny) :
            if a[i,j] :
                for m in range(1,181) :
                    r = int(j*cos(m*pi/180)+i*sin(m*pi/180))
                    if r<(n1) and r>0 :
                        xy[r,m]+=1
#上面就是核心代码
    big = []
    axi = []
    ayi = []
    le = 0

#    gray()
#    imshow(a)
#    xlim(0,300)
#    ylim(0,300)
    for i in range(n1) :
        for j in range(180) :
            if xy[i,j]>gate :
                flage = True
                for ii in range(le) :
                    if abs(i-axi[ii])+abs(j-ayi[ii]) <distance :
                        flage = False
                        break
                if flage :
                    big.append(xy[i,j])
                    axi.append(i)
                    ayi.append(j)
                    le +=1
#上面是统计投票数超过了阈值的直线，但是我在中间加了一段用来滤掉接近直线的代码
    if show_image :
        gray()
        imshow(a)
        xlim(0,ny)
        ylim(0,nx)
        x = array(range(300))
        for i in range(len(ayi)) :
            y = (axi[i]-x*cos(ayi[i]*pi/180))/sin(ayi[i]*pi/180)
            plot(x,y)
        show()
    return axi,ayi


def bin_image(name,is_array=False,start=70,gate=3,way='whole') :
    '''
    这是一个将灰度图像转换为二值图像的函数
    目前支持两种算法：全局最佳阈值和大津算法
    控制两种算法的切换使用way，等于‘whole’时为全局最佳，等于‘otsu’时为大津算法
    程序中都已经做了计算速度上的优化
    至于具体的原理和详细的注释，我暂时不想写了，想知道自己看资料
    只说明对于全局时，初始值start的选择有时很重要
    程序最后会返回一个二值图像数组

    '''
    if is_array :
        a = name
    else :
        a = array(open(name).convert('L'))

    nx,ny = a.shape
    t = start
    start = 10000

    if way == 'whole' :
        while start>gate :
            b = a>t
            num1 = sum(sum(b))
            all1 = sum(sum(b*a))
            b = a<=t
            num0 = sum(sum(b))
            all0 = sum(sum(b*a))

            if num0 == 0:
                all0 = 0
            else :
                all0 = all0/num0
            if num1 == 0 :
                all1 = 0
            else :
                all1 = all1/num1
            t1 = (all0+all1)/2
            start = abs(t1-t)
            t = t1
        a = a>t
    elif way == 'otsu' :
        b = a.flatten()
        length = len(b)
        #打开图像，转换为256灰度，压平为一维数组，并计算像素个数

        count = bincount(b)

        count = append(count,[0]*(256-len(count)))
        count = float32(count)
        p = count/sum(count)
        c = array(range(256))
        mg = sum(count*c)/sum(count)
        big = [0,0]
        for i in range(256) :
            p11 = p[0:i+1]
            mk1 = array(range(i+1))
            mk = sum(p11*mk1)
            p1 = sum(p11)
            if p1 == 1:
                sig =0
            else :
                sig = (mg*p1-mk)**2/(p1*(1-p1))

            if sig > big[0] :
                big = [sig,i]

        a = a>big[1]

    return a


if __name__ == '__main__' :

    #hist_equal('histimage.tif',show_image = True,save_image = False)
    #fast_hist_equal('histogram.JPG')
    im_map('histimage.tif')
    #im_map_log('histimage.tif')
    #im_stretch('histimage.tif',slop = 0.5)
