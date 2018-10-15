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



### 分布式计算

我现在使用了一点的分布式计算工具是`dispy`，但是似乎见到更多的是`Celery`或者其他的。

我设想中的分布式计算工具应该能够做到的是：工作节点只需要运行一个相同的监听任务的程序，主节点负责发放计算任务，然后计算任务一般使用函数的形式给出，工作节点和主节点之间会自动地完成相关文件的传输和函数代码的分发，而不需要手动将文件复制到个节点。

但是最初我尝试的`multiprocessing.BaseManger`和`Celery`似乎都做不到这一点，我感觉需要手动复制文件的方式真的很脑残。最终我找到了`dispy`，它完美的满足了我基本全部的设想，这两天我也做了一些学习和尝试，成功运行起来了，但是在最后的实践中却发现了一些问题，所以实际上我并未真正的应用，这个还需要继续学习。

首先自然是安装。

接下来，举一个栗子，来自官网的例子，它的应用场景是这样的：一个主节点负责运行任务文件，将任务发送出去，而计算节点负责监听，接受任务，执行，并将结果返回。

主节点的任务代码如下：

~~~python
def compute(n):
    import time, socket
    time.sleep(n)
    host = socket.gethostname()
    return (host, n)

if __name__ == '__main__':
    import dispy, random
    cluster = dispy.JobCluster(compute)
    jobs = []
    for i in range(10):
        # schedule execution of 'compute' on a node (running 'dispynode')
        # with a parameter (random number in this case)
        job = cluster.submit(random.randint(5,20))
        job.id = i # optionally associate an ID to job (if needed later)
        jobs.append(job)
    # cluster.wait() # waits for all scheduled jobs to finish
    for job in jobs:
        host, n = job() # waits for job to finish and returns results
        print('%s executed job %s at %s with %s' % (host, job.id, job.start_time, n))
        # other fields of 'job' that may be useful:
        # print(job.stdout, job.stderr, job.exception, job.ip_addr, job.start_time, job.end_time)
    cluster.print_status()
~~~

保存为`test.py`，保存到任意想要的位置即可。

第一步的尝试中，我们不会使用多个主机，而是在同一台电脑上执行，只是任务的发布和执行是两个不同的进程。

首先：找到dispy的安装目录，实在找不到，可以打开一个python的交互式，`import dispy`，然后`dispy.__file__`，就会输出。到这个目录下，可以发现其中有一个`dispynode.py`文件，这个文件就是工作节点要执行的代码，是的，计算节点我们完全不需要自己写一点代码，很厉害。在此处打开命令行，运行`python dispynode.py -d`，后面的参数表示的意思是debug，这样运行中会输出一些相关信息，便于观察。

然后回到`test.py`所在位置，在命令行运行`python test.py`，顺利的话，我们应该可以观察到代码被顺利执行了。

第一步搞定，真的没有成功运行的话也无所谓，可以继续往下。



下面要解决的问题有两个，第一是如果任务函数更加复杂怎么办，例如导入了其他自定义模块的内容怎么办，第二，如何利用多台机器。



对于第一个问题，当任务函数更加复杂的时候，需要做的是首先，需要在`JobCluster`中再加一个函数`depends`这个参数的值是一个列表，包含了额外的文件，依赖函数等，然后更加重要的是，我们必须要注意的是此种情况下，`import`语句必须写在函数内部，其实可以自己想一下，基本上dispy做的工作就是收集这些依赖，然后发送给计算节点，所以，你在工作函数外部写的所有内容计算节点都无法得知，所以import等内容如果不写在函数内部，计算节点自然无法使用。更复杂的，依赖函数如果使用了什么模块，也必须要将import写在自己内部。否则结果都是无法顺利执行。

举例：

~~~python
def distribute_work(order, omega_c, omega_e, lambda_1, num, delay_range, fun1, fun2, noise) :

    """
    依赖包： jpype, dispy
    依赖文件: infordynamics.jar  savedata.py
    依赖函数: generate_origin_sequence, func_center, func_edge, RK4

    """

    import numpy as np
    import jpype
    import savedata as sd

    jar = "infodynamics.jar"
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path="+jar)

    print("I am here")

    init_time = 100
    sample_time = 200
    time_step = 0.001
    
    delay_length = 100

    init_length = int(init_time/time_step)
    sample_length = int(sample_time/time_step)
    length = init_length + delay_length + sample_length

    res = np.zeros([2,6], dtype=np.float64)

    caculate_order = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]
    
    s = generate_origin_sequence(omega_c, omega_e, lambda_1, fun1, fun2, length, time_step, noisy=noise)
    s = s[init_length:, :]


    TE = jpype.JPackage("infodynamics.measures.continuous.kernel").TransferEntropyCalculatorKernel
    te = TE()

    r = 0.2


    for j in range(len(caculate_order)) :

        te.initialise(1, r)
        te.setObservations(s[:, caculate_order[j][0]], s[:, caculate_order[j][1]])
        res[0, j] = te.computeAverageLocalOfObservations()

        te.initialise(1, r)
        te.setObservations(s[:, caculate_order[j][1]], s[:, caculate_order[j][0]])
        res[1, j] = te.computeAverageLocalOfObservations()


    try :
        sd.save(collec_name, data_record)
    except :
        print("save error!!!!!!!!!!!!!!!!!!!!!")

    jpype.shutdownJVM()

    return order, res
~~~

假设上面是某个任务函数的部分片段，从一开始的注释可以看到他的一些依赖，注意看import的位置。

然后下面的几个依赖函数实际上和这个工作函数位于同一个代码文件，它们也使用了numpy，所以在这些函数的内部也都需要重新导入numpy才行，然后主任务的depends参数是这样写的：

`depends=["infodynamics.jar", "savedata.py", generate_origin_sequence, fun_center, fun_edge, RK4]`

另外特别人性化的一点是，即便我们使用的代码文件是有路径结构的，例如savedata.py放在stan文件夹下，那么，import肯定是要改的，然后依赖里面写`stan/savedata.py`，dispy就会自动的在任务节点建立相同的文件结构，非常贴心。

然后就是debug问题了，据我目前观察计算节点目前是不接受print的，也就是说任务函数的print都不会被输出，于是当任务函数出了问题的时候就很恶心，纠错的方式是检查诸如test.py里面的job的exception属性，如果不为空，代表计算节点发生了错误，并被返回了，输出这个属性就可以看到问题，对应纠正即可。



我的表达能力实在捉急，所以说的很啰嗦。

下面解决第二个问题，怎么使用多台机器计算。其实很简单，只需要和开始一样在每台机器上都执行`dispynode.py`即可，要注意的是，此时，我们一般会利用`-i`参数指定本机ip地址，尤其是我们这种在局域网内的，它很可能会自动检测到公网ip地址，然后绑定成公网ip，结果造成局域网内的设备无法发现，总而言之，例如`10.112.145.120`这台机器是一个计算节点，那么就执行`python dispynode.py -d -i 10.112.145.120`即可，当然还有很多其它参数，看文档即可。另外要说一句并行计算问题，计算节点默认会自动检测本机CPU是几核的，例如四核，那么它会自动每次请求四个任务，并行计算，很不错。当然也可以指定几个核心参与运算，看文档。

另外，任务发布节点呢，也必须指定出计算节点的地址，这样他才能发现这些节点，建立连接，方法就是继续在`JobCluster`里面加入nodes参数，以列表形式指定计算节点的ip，例如：

`nodes=["10.112.145.120","10.210.68.195", "10.112.141.23", "10.112.179.65"]`

那么原则上来讲，先将各个节点运行起来，然后执行任务发布代码即可。计算节点完全不需要管，只要不关闭，他们会永远保持监听状态，任务执行完毕后会自动恢复监听。

但是，有时并不顺利，表现是代码已经可以保证没有问题了，但是只有个别节点，甚至一个节点都接听不到任务。这个的原因在于任务发布节点的ip地址出问题了。像之前提到的一样，任务节点可能也是错误地把自己绑定到了公网ip，此时我们必须自行再添加一个参数明确指出ip地址，所以最后可能是这样的：

`cluster = dispy.JobCluster(distribute_work, nodes=["10.112.145.120","10.210.68.195", "10.112.141.23", "10.112.179.65"],  depends=["infodynamics.jar", "savedata.py", generate_origin_sequence, fun_center, fun_edge, RK4], ip_addr="10.112.145.120")`

于是test.py的部分主要代码基本上是这样的：

~~~python
import dispy
import numpy as np
cluster = dispy.JobCluster(distribute_work, nodes=["10.112.145.120","10.210.68.195", "10.112.141.23", "10.112.179.65"],  depends=["infodynamics.jar", "savedata.py", generate_origin_sequence, fun_center, fun_edge, RK4], ip_addr="10.112.145.120")
jobs = []
n = lambda_1.shape[0]

res1 = np.zeros([n, 6], dtype=np.float64)
res2 = np.zeros([n, 6], dtype=np.float64)


for i in range(n) :
    job = cluster.submit(i, omega_c, omega_e, lambda_1[i], num, delay_range, fun_center, fun_edge, noise)
    job.id = i
    jobs.append(job)

for job in jobs :
    if job.exception :
        print(job.exception)
    else :
        order, res = job()
        res1[order, :] = res[0, :]
        res2[order, :] = res[1, :]

        np.save("res1_other_system", res1)
        np.save("res2_other_system", res2)
        cluster.print_status()
~~~

更仔细的细节我还没能搞得特别清楚，例如查文档就可以看到JobCluster不仅有一个ip addr参数，还有另外一个ip参数等等。。。



然后原则上，基本上到此为止，一切都很完美了。我们可以执行比较复杂的分布式任务了，但是就这样吗？naive，实际测试中，依旧出了问题，部分节点依旧未能顺利接受任务，部分节点莫名其妙执行失败，可能是代码文件传输中导致的某些问题，不知道。总而言之，我依旧失败了，原因未知。

不管怎么说，上面就是基础和一些简单示范了。

