## python性能问题

首先应该考虑的是计时和分析。

对于计时，我们应该使用`timeit`模块。

在`ipython`中，是支持魔术命令`%timeit`的，此时最便捷的方法就是使用这个，例如：

`%timeit np.max(m, axis=0)`

如果没有ipython的话，可以在程序文件中使用timeit，例如：

~~~python
from numpy import sum,abs,max,min
import timeit

def test1() :
    a = np.random.random([1,1000])
    for i in range(1000) :
        b = sum(a)
        c = max(a)
        d = min(a)
        e = abs(a)
        
print(timeit.timeit("test1()",setup='from __main__ import test1',number=1000))
~~~

`timeit`的第一个参数是以字符串形式给出的要执行的语句，所以，当我们要执行一个片段的时候应该写成函数的形式，但是`timeit`是无法发现这个函数的，因此必须从本命名空间中手动导入



为了获得更加结构化的分析结果，我们可以使用`cProfile`，它可以追踪程序运行过程中的所有细节，并给出统计信息，这里只介绍最简单的使用：

~~~python
import cProfile
import pandas as pd
import numpy as np

from te import TE

import time

def work(o) :
	print(o,'begin')
	data = pd.read_csv("data/data2/"+str(o)+'.csv', names=['s1','s2'])
	data = data.values
	a = TE(data[:,0], data[:,1])

	return o,a.kde_te12(r=0.3),a.kde_te21(r=0.3)

prof = cProfile.Profile()
prof.enable()

work(10)

prof.create_stats()
prof.print_stats()
~~~

这里，就会详细追踪整个过程，最终输出如下：

~~~
         580744 function calls (580735 primitive calls) in 14.497 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:402(parent)
        9    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:989(_handle_fromlist)
        2    0.000    0.000    0.000    0.000 <string>:12(__new__)
        6    0.000    0.000    0.000    0.000 __init__.py:177(iteritems)
        1    0.000    0.000    0.000    0.000 __init__.py:183(itervalues)
    59994    0.019    0.000    7.146    0.000 _methods.py:25(_amax)
    79994    0.020    0.000    1.006    0.000 _methods.py:31(_sum)

~~~

这里只是一个片段，包含的信息包括调用了多少函数，其中多少是原生的，总的执行时间，下面的详细列表中：

`ncalls`代表调用次数，`tottime`代表从本调用中去除其他调用之后的运行时间，`cumtime`本函数的所有调用一共花费的时间

差不多这些就可以看出一点东西了



### 优化

矢量化的操作是一种合理的优化方案，但是也要适度，一般而言，优化都是拿内存换时间，所以必须要注意。我刚刚经历了一次极度失败的矢量化优化，费尽心思，把循环变成了矢量化操作，结果速度慢了至少40倍，同时内存飙升，以至于电脑会卡死。

其余，也有一些其他的操作可以达到优化的目的，例如经测试发现在大规模的循环操作中`from numpy import max, sum`也略快于`import numpy as np np.sum`这样的属性访问，性能的提升不多，可能只有几个百分点，例如`4%`

也有提到使用`numpy 的ndarray`的方法取代`ufunc`的，但是经我的测试，也只是微乎其微而已。

所以，本质上我掌握的优化技巧并不多。

我现在准备尝试一下python与C的混编。



### Python与Ctypes

这一部分只关注python通过ctypes调用c代码。

其实很细节的东西，我也没做太多研究，只是跑通了而已。

通用的步骤是，c代码编译为动态链接库，然后通过ctype包装，封装成python的函数形式，然后进行调用。如果从计算上来说，重点肯定是在于numpy的类型与c类型的接口了，另外一个重要问题就是编译。

前者可以看[这篇文章参考](https://segmentfault.com/a/1190000000479951)

这里也再给出一个额外的示例：

~~~c
#include <stdlib.h>
#include <math.h>

void te_box_kde(double (*record) [3], double (*p) [4], int times, double r, int out_length)
{
	double one_max;
	double sum_xn1xnyn;
	double sum_xn;
	double sum_xnyn;
	double sum_xn1xn;
	for(int i=0; i<times; i++)
	{
		sum_xn1xnyn = 0;
		sum_xnyn = 0;
		sum_xn = 0;
		sum_xn1xn = 0;
		for(int j=0; j<times; j++)
		{
			if(abs(j-i)>=out_length)
			{
				one_max = -1000;
				double x[3];
				for(int t=0; t<3; t++)
				{
					x[t] = fabs(record[j][t]-record[i][t]);
					if(x[t]>one_max) one_max=x[t];
				}
				if(r-one_max>0) sum_xn1xnyn++;

				if(r-x[1]>0) sum_xn++;
				if(r-(x[1]>x[2]?x[1]:x[2])>0) sum_xnyn++;
				if(r-(x[0]>x[1]?x[0]:x[1])>0) sum_xn1xn++;

			}
		}
		p[i][0] = sum_xn1xnyn;
		p[i][1] = sum_xn;
		p[i][2] = sum_xnyn;
		p[i][3] = sum_xn1xn;
	}
}

void mi_box_kde(double (*record) [2], double (*p) [3], int times, double r, int out_length)
{
	double one_max;
	double sum_pxy;
	double sum_px;
	double sum_py;
	for(int i=0; i<times; i++)
	{
		sum_pxy = 0;
		sum_px = 0;
		sum_py = 0;

		for(int j=0; j<times; j++)
		{
			if(abs(j-i)>out_length)
			{
				one_max = -1000;
				double x[2];
				for(int t=0; t<2; t++)
				{
					x[t] = fabs(record[j][t]-record[i][t]);
				}
				one_max = x[0]>x[1]?x[0]:x[1];
				if(r-one_max>0) sum_pxy++;
				if(r-x[0]>0) sum_px++;
				if(r-x[1]>0) sum_py++; 
			}
		}
		p[i][0] = sum_pxy;
		p[i][1] = sum_px;
		p[i][2] = sum_py;
	}
}
~~~

上述是`box_kde.c`源码

~~~python
import numpy as np
import numpy.ctypeslib as npct
from ctypes import c_int,c_double
import os

__all__ = ["te_box_kde", "mi_box_kde"]


array_in = npct.ndpointer(dtype=np.double, ndim=2, flags="CONTIGUOUS")
#array_out = npct.ndpointer(dtype=np.double, ndim=1, flags="CONTIGUOUS")

libcd = npct.load_library("box_kde.dll",os.path.dirname(__file__))

libcd.te_box_kde.restype = None
libcd.te_box_kde.argtypes = [array_in, array_in, c_int, c_double, c_int]

libcd.mi_box_kde.restype = None
libcd.mi_box_kde.argtypes = [array_in, array_in, c_int, c_double, c_int]

def te_box_kde(in_array, out_array, r, out_length) :
	return libcd.te_box_kde(in_array, out_array, len(in_array), r, out_length)

def mi_box_kde(in_array, out_array, r, out_length) :
	return libcd.mi_box_kde(in_array, out_array, len(in_array), r, out_length)
~~~

这里是`box_kde.py`源码

基本上源码就是这些。

另外的一个重要问题就是编译，原则上来说，我并不是很了解c到dll文件的过程(特指windows)，所以我并不清楚visual c++编译器和gcc编译器编译产生的dll是否相同，是否兼容。所以原则上来说，我们编译dll的编译器应该与生成python的编译器型号，版本一致。例如常见的python3.6，打开一个powershell运行python的交互命令行，就可以看到诸如`MSC ver 1900`类似的标识，查阅资料可以得到以下对应关系：

~~~
For this version of Visual C++  Use this compiler version
Visual C++ 4.x                  MSC_VER=1000
Visual C++ 5                    MSC_VER=1100
Visual C++ 6                    MSC_VER=1200
Visual C++ .NET                 MSC_VER=1300
Visual C++ .NET 2003            MSC_VER=1310
Visual C++ 2005  (8.0)          MSC_VER=1400
Visual C++ 2008  (9.0)          MSC_VER=1500
Visual C++ 2010 (10.0)          MSC_VER=1600
Visual C++ 2012 (11.0)          MSC_VER=1700
Visual C++ 2013 (12.0)          MSC_VER=1800
Visual C++ 2015 (14.0)          MSC_VER=1900
Visual C++ 2017 (15.0)          MSC_VER=1910
~~~

所以，原则上我们需要使用2015年的14版本，但是事实上，到现在为止我从未使用过visual c++编译器，手动编译任何源码，所以，我并不太会用。

我使用了gcc，这并不是一个合理的选择，但是它成功了，至少到目前为止运行良好。

`gcc -shared -o box_kde.dll box_kde.c`即可

如果在实际使用中报错，错误可能类似于`winerror 不是有效的win32应用程序什么的`差不多吧，这实际上的原因是gcc的版本错误，我们需要使用64位的，如果你的python是64位的话，而不是使用32位的gcc编译器。

至此，算是就结束了。

额外的说一句，cython是另外一种使用c代码的方式，他的编译自然是使用setup.py这样的方式，他的编译成功需要visual c++，应该是必须的，否则就会报错。

