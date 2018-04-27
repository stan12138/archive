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