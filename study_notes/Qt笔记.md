## Qt笔记

为了练习C++，我决定使用C++重新学习Qt，同时也是为了能够更加方便的发布。



### 发布

首先应该编译为release版本，然后应该下载一个叫做`Process Explorer`的软件，然后在Qt Creator里面运行release版本的应用，打开上述软件，找到这个应用，点击上面的view->lower pane view->DLLs，即可看到该应用运行所需的动态链接库，筛选其中来自Qt的，找到，拷出来，和应用的exe文件放在一个文件夹里面，这个文件夹就是一个发布版了，可以直接点击运行exe



### 源代码组织结构

mainwindow的头文件中类的声明最开始就写了`Q_OBJECT`，这是一个宏，这个宏必须放在类的最前面，它的功能是允许你为这个类定义信号和槽

在MainWindow类的private域里面，我们定义了一个指针，是Ui::MainWindow类型的指针，当你编译应用之后，Qt会自动生成一个`ui_MainWindow.h`文件，这个文件将ui文件转化为了c++文件，而上述指针和这个文件联系密切，总之它的功能就在于将ui文件和应用联系起来，这样你就可以操作和使用ui设计了。

会自动创建一个基类，可以自行命名，如Window，你会发现在头文件里面声明了一个`Ui::Window`，下面还声明了一个Window，Window里面的指针是一个`Ui::Window`类型的，这两个Window并不是同一个，这个真的很误导人，`Ui::Window`的定义在自动生成的`ui_window`头文件中，他继承了该头文件中定义的`Ui_Window`类，这个类实现了setupUi方法，差不多就是这样，或许听起来很迷糊，但就是这样。总而言之`Window`和`Ui::Window`不是同一个类，后者定义在`ui_window`中

然后在Window的定义源文件中，构造方法的定义看起来也很奇怪，其实那是一种叫做构造函数初始值列表的形式



### 预期

在早期，我觉得只要理解这些东西都是在干什么就可以，然后就可以写着玩了，中后期，我应该去试着理解pro文件，qmake，工程组织，代码分割等。



### 界面美化

我十分不喜欢丑陋的window默认窗口风格，窗口的边框极其丑陋，所以，在一切之前，我的第一个计划就是美化，但审美能力，设计能力太差，所以，这里的美化也只是最基本的。

#### 无边框

这是第一步。

这里稍微说明一下关于继承树，Qt中一切部件的基类是QWidget，我们一般继承他的一个子类QMainWindow，这个子类在他的基础上加了一些修饰，总而言之，对于无边框的方案，我们不应该继承他，而应该直接继承QWidget，这个需要在建立工程的时候就选择。

其他的，只需要在主程序内，对于窗口应用setWindowFlags方法，传入参数`Qt::FramelessWindowHint`即可。

#### 移动与关闭

边框被去掉之后，移动和关闭就要由我们自己来实现。

关闭只需要建立一个按钮，并用槽把它和退出连接

然后关于移动，这个涉及到了Qt的事件系统，简而言之，Qt中，窗口有`mouseMoveEvevt,mouseReleaseEvent,mouseMoveEvent`，等一系列方法，当对应的事件发生时，这些方法就会被自动调用，并传入一个`QMouseEvent*`的参数，我们只需要重写这些方法，完成自定义任务即可。

~~~c++
class Window : public QWidget
{
    Q_OBJECT

public:
    explicit Window(QWidget *parent = 0);
    ~Window();
    void set_area(QRect a);

protected :
    void mousePressEvent(QMouseEvent* e);
    void mouseReleaseEvent(QMouseEvent* e);
    void mouseMoveEvent(QMouseEvent* e);

private:
    Ui::Window *ui;
    bool press;
    QRect area;
    QPoint old_pos;
};

void Window::set_area(QRect a)
{
    this->area = a;
}

void Window::mousePressEvent(QMouseEvent *e)
{
    if(e->buttons() == Qt::LeftButton && this->area.contains(e->pos()))
    {
        this->press = true;
        this->old_pos = e->pos();
        this->window_pos = this->pos();
        qDebug() << "press left button";
    }
}

void Window::mouseReleaseEvent(QMouseEvent *e)
{
    this->press = false;
}

void Window::mouseMoveEvent(QMouseEvent *e)
{
    if(this->press)
    {
        move(this->pos()+e->pos()-this->old_pos);
        qDebug() << "old pos" << this->old_pos ;
        qDebug() << e->pos()-this->old_pos;
        //this->window_pos = this->pos();
        //this->old_pos = e->pos();
    }
}
~~~

这里需要注意的几个点是首先，对于传入的鼠标事件的指针，鼠标事件这个类有很多的方法，例如`buttons()`给出了这是哪个按键，我们需要把它和Qt预定义的按键作比较即可，然后pos方法给出了鼠标的位置，是一个QPoint类，这个类重载了加减等运算符

然后，我们需要知道一些坐标系统的事情，Qt里面的坐标系也是左上原点。然后对于窗口，提供了一个move方法，这个方法可以让窗口的原点移动到屏幕上的指定坐标，接收QPoint作为参数。

到此为止，我们基本上已经可以完成移动了，但是这还不太够，有一种参考原始窗口的特性就是，并非鼠标在任何位置拖动都可以移动窗口，只能是在一个规定的矩形之内，所以我们应该设置一个矩形QRect，这个类接收四个参数x,y,width,height，相对于窗口，它提供了一个contains方法，只要将一个点传递进去，就可以给出一个布尔返回值，指明点是否在矩形内

除了窗口的坐标是相对于屏幕之外，上述提到的所有坐标都是相对于窗口的。

这样，我们要考虑的就是一些实现及数学上的问题，首先，鼠标按下的事件只会在按下的时候被触发一次，直至释放之后，再次按下，才会再次被触发，中途不放开不会连续触发，这是很常见，很合理的设计。然后考虑我们应该如何移动窗口，效果应该是鼠标相对窗口的位置一直不变，所以窗口要随鼠标而移动，所以`old_pos`只是在按下的时候被设置一次，之后都不应该再变。然后再移动事件里面检测现在的位置，计算差值，移动窗口即可，因而是`move(this->pos()+e->pos()-this->old_pos);`而不存在坐标更新操作，考虑一下，很容易理解。



所以差不多就是以上操作。



### 回顾

考虑一下到目前为止，学到了什么，基本的还需要些什么？

搞清了文件的结构，意义，整体的结构。鼠标事件，美化。

下面应该再学习一些部件，以及ui的设计，优化。样式表的使用。



### 资源文件

之后，我们也许想要添加一些资源文件，例如icon，外部样式表，也许是图片，但是，在qt里面，并不是把文件放进去，然后使用链接这么简单，我们必须使用资源文件。

在项目上右键，选择添加新文件，在模板里选择`Qt->Qt资源文件`，然后命名等等，最后你会发现多了一个资源目录，选择下面的qrc文件，右键在编辑器打开，添加前缀，这相当于在创建一个专门放置某种文件的目录，例如`/images`，然后选择添加文件，即可

在引用文件的时候，只需要使用`:/images/test.jpg`即可引用，是的，多了一个冒号，的确有些诡异。

我现在主要使用的就是样式表和图片

当你设置了资源文件之后就可以为自定义关闭按钮的图标了，此时只需要从网上搞到一个合适的图标，例如阿里图标字库，下载svg文件就好，也是支持的，直接设置按钮的icon即可

#### 关于样式表

使用样式表来更改样式是一个很好的选择，相比于逐个部件增加各自的样式表，我更喜欢搞一个统一的外部样式表，这样的话，就必须考虑文件的读取的问题，例如新建资源文件前缀`/style`，文件`/style.css`，那么我们需要使用如下代码引用：

~~~c++
QFile file(":/style/style.css");
file.open(QFile::ReadOnly);
QString stylesheet = tr(file.readAll());
qApp->setStyleSheet(stylesheet);
file.close();
~~~

这个一般写在Window的构造函数里面

然后要考虑的问题是css的选择器，以及支持的属性

对于选择器，我们一般应用的其实只有两种，某一类部件，或者某一个部件，前者类似于标签选择，直接使用`QPushButton{}`这样的进行选择，后者类似于id选择器，ui设计中每一个部件都有一个`Object Name`，这个名字就是id，使用`#pushButton{}`这种方式进行选择

除此之外，其实还支持例如`hover`这样的伪选择器，暂时就不说明了。

至于样式，其实普通的常用样式都是支持的，我常用的`background-color,border,border-radius`什么的都还是支持的，所以暂时应该说可以放心大胆地用，真的不支持的话输出会提示的，到时候再改就可以

这里要特别声明的是，样式表中的颜色一般都是255，也见过百分数设置透明度的，一般透明度不在这里设置，即使设置了，一般也用255范围

### 窗口透明

其实这个属性似乎并不是很有必要存在，并不是非常实用，一般非透明即可

如果真的要透明，首先说明，绝对不能用css的rgba试图实现透明，因为实现不了

低级一点的窗口透明是直接在主程序设置`w.setWindowOpacity(0.5);`，范围就是`0~1`，这种方式很快捷，缺陷就在于它是全局的，即窗口和所有部件都是透明的，这个其实不太好，一般我们想要的效果是窗口透明，部件不透明，实现的方法，网上给了很多，我现在觉得比较好的是：

~~~c++
#include <QPainter>

w.setAttribute(Qt::WA_TranslucentBackground);

void Window::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.fillRect(rect(), QColor(255,255,255,10));
}
~~~

具体而言，我们需要在需要的地方增加一个上述头文件

然后在主程序加入第二行，把整个背景给去掉，去掉之后的后果在于，窗口消失了，所以事件系统也将消失，于是就不能用了，所以我们必须再重绘一个窗口出来，绘制的时候可以实现透明化，于是我们需要再重写Window的一个方法，就是上面的那个，这个方法也是一个内置方法，要做的就是实现。



这些就是今天的工作，明天继续。



### 计划

接下来要做的是：布局管理，最大最小化，缩放，2D绘图，目录接口

我很怕布局管理，我一直搞不好这个东西，因为我根本不知道自己想要什么，写前端的时候就是这样，但愿这一次会有所好转。



### 布局管理与缩放

当允许窗口执行缩放操作的时候就必须考虑布局管理功能了。

我把边框去掉了，去掉之后很棒的一个特性是只要我不自行提供实现，用户将无法缩放窗口。



布局问题确实恶心，我一直在这个上面遇到问题，简直不知道该怎么下手。我一直有一种感觉，就是既定的布局方式并不是完备的，也就是说，你并不能使用它们构造出所有你想要的布局，这就是我的感觉。或者说硬要用他们来实现十分之繁复。

那么该怎么办？有两种解决方法，首先，实际上很多情况下，我需要做布局处理的部件很简单，也很少，三四个而已，这时，其实我完全可以自行处理，一般窗口的缩放都是我在mouseMoveEvent里面实现的，所以，我可以在这里加入一些代码，当窗口改变的时候，重新计算部件的坐标，说起来有些复杂，其实实现很简单，基本上都是几个简单的数学公式就搞定。

第二种方法就比较高级了，那就是自定义布局管理器，继承QLayout布局类，然后只要实现必须实现的接口，内部布局的方式我们可以随心所欲，然后就可以像使用内置布局类一样使用自定义的布局了，这种方式相对而言，较为繁琐，但是接口更友好，更加整洁。

下面我会简单聊一下内置布局类，然后重点记录自定义布局类。

内置布局类主要包含三种，BoxLayout, GridLayout, FormLayout

其中的盒式布局又可以分为水平和垂直，指的就是将部件水平排列，或者垂直堆叠

网格布局就没什么可说了，最后一个Form布局实际上是针对那些有标签和文字框的成组的部件的

一般情况下，上述布局形成的每个单元格都是大小相等的，但是通过设置拉伸因子，可以让他们成比例，但是依旧是变化的，也就是说，我没有办法设计一个某些格子是固定的这样的布局。

除此之外，每个部件其实都是有一些sizepolicy属性的，指定了该部件的尺寸策略，固定，最大值，最小值还是随意拉伸。

然后，还提供了一些spacer部件用来占据空间，我也没用过，就不说了。

虽然设计界面是支持拖拉式的布局管理的，但是我并不提倡，他还不如代码式的清晰明了和方便。

那么如何在代码中使用布局？很简单

~~~c++
#include<QHBoxLayout>

QHBoxLayout *layout = new QHBoxLayout;
layout->addWidget(ui->pb1);
layout->addWidget(ui->pb2);
layout->addWidget(ui->pb3);
this->setLayout(layout);
~~~

一般情况下，我们都是在Window的构造方法里面设置布局，然后要记得带着头文件。

上述是单种布局的使用方法，但是实际使用中往往是多种布局混合，首先设定一个主布局，然后主布局再包含子布局，使用主布局的addLayout方法可以增加子布局

关于内置布局的介绍大致如此，不同布局管理的addWidget方法的参数要求各有不同，还有就是一般可以设置单元之间的间隔。



#### 自定义布局管理器

意义就不说了，很好用，随心所欲就是了。

明显我们是要添加一个头文件和一个类的源文件，添加方式是分别在header和source里面新增文件，分别是头文件和源文件，它会自动加入到pro文件里面。

以一种布局为例，我们想要实现一种SLayout，这种布局的特点是窗口分为两个部分，一上一下，上面是类似于菜单栏，下面是一个大界面，菜单栏距上边缘10，距大界面10，菜单栏的元素是一个个小按钮，尺寸均为20*20，菜单栏距左右边缘都是10，菜单栏本身也可以分为左右，左侧的部件总是靠左，右侧的部件也总是靠右，同一侧部件间距10，大界面距离下左右边缘都是10

那么，我们首先增加两个文件，`stan_layout.h`和`stan_layout.cpp`

文件内容分别为：

~~~c++
#ifndef STAN_LAYOUT_H
#define STAN_LAYOUT_H

#include <QtWidgets>
#include <QList>
#include <QLayout>
#include <QRect>

class SLayout : public QLayout
{
public :
    explicit SLayout(QWidget *parent, int spacing = 0);
    SLayout(int spaceing=0);
    ~SLayout();

    void addItem(QLayoutItem *item);
    void addWidget(QWidget* widget, int p);


    QLayoutItem *itemAt(int index) const;
    QLayoutItem *takeAt(int index);
    QSize sizeHint() const;
    int count() const;
    void setGeometry(const QRect &rect);
private :
    struct SI
    {
        SI(QLayoutItem* i, int p)
        {
            item = i;
            order = p;
        }
        QLayoutItem * item;
        int order;
    };
    QList<SI *> list;
    int numl=0;
    int numr=0;
    int numm=0;
    int flage=1;
};
#endif // STAN_LAYOUT_H


~~~

~~~c++
#include "stan_layout.h"

SLayout::SLayout(QWidget *parent, int spacing)
    : QLayout(parent)
{
    flage = spacing;
}

SLayout::SLayout(int spacing)
{
    flage = spacing;
}

SLayout::~SLayout()
{
    QLayoutItem *l;
    while ((l = takeAt(0)))
        delete l;
}

void SLayout::addItem(QLayoutItem* item)
{
    list.append(new SI(item, 1));
    numl = numl+1;
}

int SLayout::count() const
{
    return list.size();
}


void SLayout::addWidget(QWidget* widget, int p)
{
    if(p==1)
    {
        list.append(new SI(new QWidgetItem(widget), p));
        numl = numl + 1;
    }
    else if(p==2)
    {
        list.append(new SI(new QWidgetItem(widget), p));
        numr = numr + 1;
    }
    else if(p==3)
    {
        list.append(new SI(new QWidgetItem(widget), p));
        numm = numm + 1;
    }

}

QLayoutItem *SLayout::itemAt(int index) const
{
    if(index >= 0 && index < list.size())
    {	SI *wrapper = list.value(index);
        return wrapper->item;
    }
    else
        return 0;
}

void SLayout::setGeometry(const QRect &rect)
{
    QLayout::setGeometry(rect);
    int i;
    int lorder=0;
    int rorder=0;
    for(i=0; i<list.size(); ++i)
    {
        SI *wrapper = list.at(i);
        QLayoutItem *item = wrapper->item;
        int order = wrapper->order;

        if(order==1)
        {
            item->setGeometry(QRect(10+lorder*30, 10, 20, 20));
            lorder = lorder + 1;
        }
        else if(order==2)
        {
            item->setGeometry(QRect(rect.width()-(numr-rorder)*30, 10, 20 ,20));
            rorder = rorder + 1;
        }
        else if(order==3)
        {
            item->setGeometry(QRect(10, 40, rect.width()-20, rect.height()-50));
        }

    }

}



QSize SLayout::sizeHint() const
{
    QSize a(1,1);
    return a;
}

QLayoutItem *SLayout::takeAt(int index)
{
    if (index >= 0 && index < list.size()) {
        SI *wrapper = list.takeAt(index);
        return wrapper->item;
    }
    return 0;
}

~~~

对于类的定义呢，需要注意的点包括：

-   包含需要的头文件
-   继承QLayout
-   一般会实现两个构造方法和一个析构方法，但是其实构造方法没啥用，像上面一样随便写写就好了。析构方法必须要按上面标准实现，它是用来删除部件的。
-   我们必须要有一个容器，例如QList，用来记录我们添加到布局里面的部件
-   必须像上面一样重写`addItem,itemAt,takeAt,sizeHint,count,setGeometry`方法，其中的addItem,itemAt,takeAt,sizeHint,count其实没用，只需要随便瞎写，返回一个他需要的类型的返回值就可以，但是呢，事实上addItem是向列表内增加一个部件，itemAt和takeAt都是返回列表指定位置的部件，按这样的标准来实现一下其实也很简单，所以最好还是不要瞎写，就按标准实现一下最好，这里要注意的是itemAt里面的list.value，takeAt里面的list.takeAt，这两个方法一定要这样写，不要用其他方法替代，其实前者还好，关键是后者，我曾经写的是list.at，结果程序就出现crash错误了，可能是因为涉及到删除的问题吧。至于sizeHint这个方法，我暂时根本用不上，只要随便返回一个QSize值给他就好。按照官网上的说法，我们并不需要实现count方法，但是以为count方法来自QLayout，如果不实现，那么这个新类就将成为一个抽象类，进而无法在window.cpp里面用`SLayout *layout = new SLayout;`这样的方式实例化，如果不这样实例化，据测试是会出问题的，乃至无法运行，总之，必须实现count，这个方法返回的是部件的个数。
-   真正最最有用，几乎是对我们唯一有价值的方法就是setGeometry，当窗口尺寸发生变化的时候，程序会自动调用这个方法，并把整个布局应该位于的矩形传递给这个方法，我们可以在矩形里面任意随心所欲排列我们的部件。
-   因为大多时候，对于我们想要自定义的布局，并不是所有的部件都是平等的，例如这个例子里面，明显菜单栏左侧部件，右侧部件，主界面是三种不同类型的部件，我们必须把他们统一放进list里面，同时又保留类型信息，常用的解决方法就是自定义一个结构体，例如上面的SI这个结构体，然后，我们在向布局内增加部件的时候明显不会使用addItem方法，因为这个方法必须只能传入一个参数，所以，一般对于自定义的布局，我们虽然都必须实现这个方法，但是我们都会额外自定义一个addWidget方法（名字自己随便起），用于真正的增加部件。



差不多到这里就可以了，应该已经可以使用了，这些东西都是我参考官网的例子，然后花费大量时间逐个尝试修改删除，找出来的最小可用集合，想看的话，可以到[这里](http://doc.qt.io/qt-5/layout.html#how-to-write-a-custom-layout-manager)看官网的例子，但是这个例子并不特别好，我真正参考的是官网的[这个例子](http://doc.qt.io/qt-5/qtwidgets-layouts-borderlayout-example.html)，这个例子包含了完整的项目的所有文件，并且我逐个拷贝下来，测试了，的确可以顺利运行。



自定义已经完成，怎么使用呢？和内置布局一样：

~~~
#include "stan_layout.h"

SLayout *layout = new SLayout;
layout->addWidget(ui->pb1, 2);
layout->addWidget(ui->pb2, 2);
layout->addWidget(ui->pb3, 2);
this->setLayout(layout);

~~~

包含上述头文件，然后把代码片段放进构造函数就好。

哦，c++没学好的问题，其实上述的布局类实例化方式我并不太理解。

到此，自定义布局算是完美结束了。



#### 界面缩放

这里要实现的是，如何实现界面的拖拉缩放操作，只需要在mouseMoveEvent方法里面监测鼠标的位置，如果鼠标进入右边缘一定范围内，将光标设置为水平更改尺寸的形状，然后如果恰好检测到鼠标是按下左键的，就根据鼠标的移动使用resize()方法重设窗口尺寸，重设宽度。同样的下边缘基本是一样的操作，重设高度，然后再设置一个右下角，允许同时重设宽高，这里给出部分主要代码片段（不完整，有些布尔量的定义什么的可能没详细给出）：

~~~c++
if(e->x()>(this->geometry().width()-30) && e->y()>(this->geometry().height()-30))
    {
        this->setCursor(Qt::SizeFDiagCursor);
        this->change_size = true;
        if(this->press)
        {
            QPoint e1(e->pos()-change_old_pos);
            int w = max(400,this->geometry().width()+e1.x());
            int h = max(this->geometry().height()+e1.y(),300);
            resize(w, h);
            change_old_pos = e->pos();
        }
    }
    else if(e->x()>(this->geometry().width()-20) && e->y()>30)
    {
        this->setCursor(Qt::SizeHorCursor);
        if(this->press)
        {
            QPoint e1(e->pos()-change_old_pos);
            int w = max(400,this->geometry().width()+e1.x());
            //int h = max(this->geometry().height()+e1.y(),300);
            resize(w, this->geometry().height());
            change_old_pos = e->pos();
        }

    }
    else if(e->y()>(this->geometry().height()-30))
    {
        this->setCursor(Qt::SizeVerCursor);
        if(this->press)
        {
            QPoint e1(e->pos()-change_old_pos);
            //int w = max(400,this->geometry().width()+e1.x());
            int h = max(this->geometry().height()+e1.y(),300);
            resize(this->geometry().width(), h);
            change_old_pos = e->pos();
        }
    }
    else
    {
        this->setCursor(Qt::ArrowCursor);
        this->change_size = false;
    }

    set_area(QRect(0,0,this->geometry().width(),30));
~~~

要注意的事情是，第一，在Qt的默认设置里面，为了提高性能，并不是只要鼠标移动就会触发mouseMoveEvent，而是，必须在按下鼠标键的同时移动才会触发，为了提升用户体验，我需要开启随时追踪的设置，在构造函数加入`this->setMouseTracking(true);`即可。



下面的计划是将上面很凌乱的重设尺寸的操作写成一个类，规范化一点，然后现在还没有实现最大最小化按键，下一步也准备做。



#### 最大最小化

前面的尺寸重设，考虑了一下，只是把它归结为一个方法了，没必要重设一个类。

最大最小化，说来很简单，但是也挺弯弯绕的。

首先，事实上，Qt提供了很友好的最大最小化默认方法，`&Window::showMinimized`和`&Window::showMaximized`,按说，只需要`connect(ui->pb1, &QPushButton::clicked, this, &Window::showMinimized);`这样链接就完美了。但是，最小化的确很完美，对于最大化，我们实际上想拦截，因为我们要完成将图标重设为还原，以及再次点击还原的操作，所以，对于最大化，我们必须自行实现。

其实很简单：

~~~c++
#include <QDesktopWidget>


QRect screen;

QDesktopWidget *desktop = QApplication::desktop();
this->screen = desktop->screenGeometry();
~~~

先这样，得到屏幕的矩形，然后只需要最大化的时候setGeometry即可。

关于图标的问题，应该这样写`ui->pb2->setIcon(QIcon(":/ico/max1.svg"));`

然后是按钮行为的设置，两种思路，最大化和还原通过将按键的信号重新链接到两个不同函数实现，另一种就是设一个flage记录当前是否最大化，只将按键链接到一个函数上，通过判断flage实现不同行为，要选后者，因为前者会导致窗口几乎崩溃，卡在最大化和还原之间，闪烁。教训是，不要重连同一个按键的信号。

至于还原，人性化一点，是把窗口放在屏幕中间。

然后还要考虑的是，必须在已经最大化的时候，禁用拖动窗口操作，否则用户可能会尝试拖拽实现重设大小，这往往会导致窗口重设错误，乃至卡死，策略是一旦在最大化时拖动窗口就将窗口还原。

差不多就这样了。

窗口的处理大概已经算是结束了。

下一步是尝试功能化操作，例如2D绘图。