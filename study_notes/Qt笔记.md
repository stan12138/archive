## Qt笔记

为了练习C++，我决定使用C++重新学习Qt，同时也是为了能够更加方便的发布。

其实Qt里面的很多东西，我都是通过官网的例子学习的，而网上找到的例子大多质量很次，[官网例子点这里](http://doc.qt.io/qt-5/examples-widgets.html)

这是官网的[所有例子](http://doc.qt.io/qt-5/qtexamplesandtutorials.html)

### 参考资料

曾经参考过的，除了网上直接搜索得到的无法列举之外，我参考过的书是霍亚飞的Qt Creator快速入门第三版，尤其是信号和槽部分的一些区别，我最初看的就是这个

然后主要就是看的官网各种例子

然后，还有几个博客，可能有用，但是我基本上没怎么看过，[Qt学习之路](https://www.devbean.net/2012/08/qt-study-road-2-catelog/)，还有[Qt开源社区](http://www.qter.org/)

然后还有一个重要的无边框窗口实现参考的[无边框](http://www.cnblogs.com/xiongxuanwen/p/5384103.html)接下来

为了实现文件的拖拽，我可能会参考[文件拖放](http://www.cnblogs.com/findumars/p/5599427.html)这个还没开始做

然后，我所学到的绝大多数知识都被我应用到了我所写的画板中，有些代码和实现可以去[这里看](https://github.com/stan12138/archive/tree/master/script/Painter)

额外说一下，上面的文件拖放的那个博客似乎还是挺不错的





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

主界面半透明，同时圆角：

~~~cpp
void Window::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    painter.setBrush(QBrush(QColor(240,240,240,240)));
    painter.setPen(Qt::transparent);
    QRect rect1 = rect();
    rect1.setWidth(rect1.width()-1);
    rect1.setHeight(rect1.height()-1);
    painter.drawRoundedRect(rect1, 6, 6);
    //painter.fillRect(rect1, QColor(240,240,240,240));
}
~~~

主界面加背景图片，需要drawpixmap，然后要同时圆角的话，需要更复杂的做法。至于内部的部件的背景设置直接使用css即可

~~~css
QListWidget {
    background-color: rgba(255,255,255,0);
    background-image: url(./rain1.jpg);
    outline:0;
    border: none;
    border-radius: 5px;
}
~~~

注意这里是使用了特殊的文件系统，查看下面的笔记。



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



### 2D绘图

重点是学会如何将鼠标移动产生的内容绘制到窗口。

一般而言，非交互式的绘制可以在直接在重载的paintEvent函数里面完成。

对于Qt而言，paintEvent负责重绘，而一般情况下我们是无法直接调用这个函数的，所以，问题有点烦。

然后我们还必须决定绘制的方式，例如：利用一个结构保存所有的鼠标绘制位置点，然后在paintEvent里面每次都遍历整个列表，绘制一遍，这种方式导致的结果是鼠标移动过快的时候，结果严重不连续。

算了，不说那么细致了，总之最终的方法是这样的，我们一般会创造一个QImage，然后把这个QImage的尺寸设置到跟这个界面大小一致，在paintEvent函数里面绘制这张图片，对于鼠标移动，我们不再绘制点，而是连接上下两个点的直线，然后把这条线绘制在上述图片上，然后通过update函数强制重绘事件，但是为了优化速度，会只更新一个小矩形内的内容。大概就是这样。

需要注意的是，实际上你调用update并不会立即就让系统调用paintEvent，系统仍是在自行决定，但是从外在表现来说，你的确会感觉到paintEvent被调用了，总之不用担心这个问题。

然后就是一些小的细节问题，还有一些困难，例如当重设窗口大小的时候，必须同步调整QImage的尺寸，否则会导致无法绘图。包括如何为painter设置一个pen，以及如何可以调整笔的各种参数等等，总之，想要实现十分完美的画板需要做大量的工作，而绝佳的示范就是官网的[这个例子](http://doc.qt.io/qt-5/qtwidgets-widgets-scribble-example.html)



### 2D绘图续

当我试图规范化我的2D绘图时，出现了一系列的问题。或者说问题和某些未注意到的应知小细节。

首先，进行到这个阶段，我很依赖于外部样式表来设计样式，自定义布局来进行布局管理。但是问题在于，之前的外部样式表和自定义布局里面的组件都是来自于ui设计文件的，那么接下来需要考虑两个内容，第一如何将利用代码而不是ui设计加入的组件在样式表和布局中引用？第二，自定义的组件是否也能这样做？

首先对于第一个问题，对于内置的组件，例如QWidget或者QGraphicView等等组件，我们直接实例化，然后通过setObjectName方法可以为其设置一个ObjectName，这样一如ui中的组件一样，我们可以在样式表中直接通过这个名字选择它，对于自定义布局，我们只需要稍微回想一下，当初自定义布局类的addWidget方法要求传入的参数是指针，所以我们只要把这个组件的指针传进去，就可以完美应用了。真正麻烦的问题是第二个。

想来似乎合乎情理，如果我们的自定义部件继承了QWidget，然后他应该表现和QWidget类似，我们完全可以通过上述第一种方法搞定一切，但是，事实并非如此。布局还好，的确实现了。但是对于样式表，却会发现完全无法起作用。也就是说，现在出现了一个问题，继承了内置组件的自定义组件无法应用样式，这个问题很普遍，所有的自定义组件都会碰到，很多人也遇到了，在stackoverflow上面有多个[类似的问题](https://stackoverflow.com/questions/7276330/qt-stylesheet-for-custom-widget)，在官网上也出现了[类似的样例](http://doc.qt.io/qt-5/stylesheet-syntax.html#widgets-inside-c-namespaces)，有多种多样的解决方案，命名空间的，accessibleName什么的等等，但都无效，最终我还是找到了解决方案，其实就是前面stackoverflow上面被采用的那个答案，看起来很诡异，所以，我一直忽略，知道走投无路，尝试了一下，竟然真的可行。

总之解决方法就是，要重载paintEvent方法，然后在里面写：

~~~c++
QStyleOption opt;
opt.init (this);
QPainter p (this);
style()->drawPrimitive (QStyle::PE_Widget, &opt, &p, this);
~~~

引用必要的头文件之后，像普通内置组件一样，设置ObjectName就可以使用了。

好开心，同时，大师兄说本周组会不开了，这么，周五就可以回家了，哈哈哈哈，开心。



再次说明一下画板的结构，我仿照了官网例子来写的，整体可以说是分为三个部件，或者两个，一个QWidget，作为主窗口，经过了我前面所做的所有改造工作，包括去边框，透明化，外部样式表，自定义缩放，自定义按钮，自定义布局等等。然后在自定义布局的主部件的位置放了另一个QWidget，这个部件也是被自定义了，继承自QWidget，他就是画板，对他的改造只有监测鼠标的运动，以及重绘，另外在resizeEvent里面也添加了一点额外的操作，这个部件是画板，但是我们并不直接在画板上面绘制，而是在上面蒙了一张大小一致的QImage，一切绘制工作都在QImage上面完成，然后在画板的重绘事件中重绘这张图片，鼠标的运动会在图片上面绘制直线，然后强制update。比较麻烦的问题是怎么处理缩放，缩放的时候不能直接将图片尺寸更改，会导致什么后果我忘了，总之需要新建一张图片，与新的窗口尺寸一致，然后根据尺寸情况采用不同的方式将旧图片绘制在新图片上面。看起来一切都很顺利，实则不是这样的，问题在于如果我们想要一个透明的画板怎么办，明显，我们必须将图片设置为透明的，于是这就涉及到了如何重叠两个透明图片的问题，明显我们要保持透明度不变，内容直接覆盖，而Qt的painter提供了一个叫做复合模式的东西，可以完成各种类型的图片复合形式，看官网[这里](http://doc.qt.io/qt-5/qpainter.html#CompositionMode-enum)，我们使用setCompositionMode方法就可以设置painter的复合模式，经过测试，我想要的模式是`painter.setCompositionMode(QPainter::CompositionMode_SourceIn);`

这样就几乎完美了。很有图片的Format十分之关键，这里暂时就不提了。等做好了，我会放一份代码到github做存档，细节太多了，记录太费事，忘了就翻看源代码就好了。

其实我觉得画板是没必要存在的，直接把图片放在主窗口的合适位置就好了。

下面要做的工作是如何搞一些小菜单，用来设置画笔的各种属性。



### 下拉菜单的实现









### 自定义仿对话框







#### 信号与槽的说明

这一部分可以作为参考的资料是第三版的Qt Creator快速入门第三版的第七章。

普通情况下，直接connect即可，例如：

`connect(ui->option, &QPushButton::clicked, this, &Window::show_config_page);`

这里面的`show_config_page`只是一个普通的无参数方法而已

接下来，我们将可以自定义信号和槽。

自定义信号：

~~~h
signals:
    void set_ip_handler_info(QString ip, QString id, int port, int my_port);
    void make_ip_server_off_line();

    void set_server_info(int port);
    void make_server_off_line();
    void send_data(QString data, QString content_type);
    void set_send_delay(int delay);

    void set_client_info(QString ip, int port);
    void make_client_off_line();
~~~

自定义槽：

~~~h
public slots:
    void start();
    void set_info(int port);
    void set_delay(int delay);
    void off_line();

    void send_data(QString data, QString content_type);
~~~

然后连接`connect(this, &Window::set_server_info, server, &Server::set_info);`

只要它们的参数类型一致即可。

激发信号`emit set_server_info(63834);`

基本上这样就够用了









### 程序发布常见问题

#### 无法运行

提示`cound not find or load the Qt platform plugin windows`

这种情况下需要将`D:\Qt\Qt5.9.3\5.9.3\mingw53_32\plugins`下面的platforms文件夹整体拷贝到exe所在文件夹下，即可解决



#### 图标图片无法显示

需要在发布的时候新建文件夹`plugins\imageformats`，然后将原本放在外面的那些与图片格式相关的动态链接库剪切进入此文件夹，然后release的源代码在`main.cpp`文件中加入`a.addLibraryPath("./plugins");`，很明显，惯例a就是我们实例化的那个`QApplication`

有人说针对某些特殊版本的Qt可以不在源代码中加入这句话，但是据我测试，针对`Qt5.9.3`还是需要的

上述两个问题是一样的，都是发布时的问题，但是他们的解决方法并不准确。正确的解决思路是，打开聚集好的发布应用，运行，然后重新打开`Process Explorer`，观察需要的动态链接库，以及路径，再配合上述修改方法，大概就可以搞定了。



### 运行失败

特指开发过程中的debug阶段，程序crash，或者直接无法运行，或者关闭的时候弹出crash对话框，这种情况据上一次的经验主要是第一，我定义了一个QTcpSocket类型对象，却忘记初始化，然后接直接使用了，或者是忘记指出它的parent是this，又或者是程序退出的时候忘记同时close这个socket了，都有可能，所以大概以前遇到的也是类似原因



### Socket通信

我只是做了初步的尝试，因为某些原因而没有深入。

我们可以创建TCP类型的套接字，或者UDP类型的，但是一切之前必须在pro文件中给QT加上network，否则编辑的过程中甚至不会有代码提示，同时也会说找不到头文件，类似的。

然后结构是这样的对于TCP，server和client是不一样的，分别是不同的类型，定义也来自不同的头文件，对于UDP则是完全一样的。

然后，我们可以搭建一个简单的显示框，对于显示框，推荐的是QTextEdit，我似乎曾经在pyQt的笔记中列出过四种有潜力作为文本显示框的组件，最终推荐的似乎就是QTextEdit，我们可以使用setText方法，写入文字，可以使用toPlainText方法获取内容

对于TCP客户端来说，最简单的演示是，构建一个QTextEdit，然后创建一个socket，记得在mainWindow的初始化方法里面初始化socket，然后构建一个按钮，socket是提供了多个信号的，其中一个是`QTcpSocket::connected`，当连接成功的时候会触发这个信号，我们只需要做出相应处理即可，然后还有一个信号是`QTcpSocket::readyRead`当可读的时候就会触发这个信号，然后使用socket的readAll方法就可以拿到所有信息，所以我们只需要写出对应的方法，特别的当按下按钮的时候开始执行连接就可以`this->socket->connectToHost("10.210.68.195",5000);`

我暂时学到的就是这些。



### 多界面设计

这一块，我想解决的问题是，如果应用中存在着界面切换，那么应该怎么进行设计。

明显，合理的方式是每一个界面都应该使用一个单独的ui文件负责设计。所以，需要解决的问题是第一如何使用多个ui文件，第二如何在界面之间切换。

我当前所使用的结构是：存在一个主界面框架，他负责显示各种最小化最大化，关闭等各个界面通用的按钮，然后在这个界面的一个位置存在另外一个界面，各个界面的切换实际上切换的就是这个子界面。

在项目上右键添加新文件，选择Qt设计师界面类，一般选择继承自Widget，然后修改类名即可。最终将生成一个头文件，一个cpp文件，一个ui文件。

然后在主界面里面，声明一个QStackedWidget，这是一个栈，或者说是一个数组，生成上述界面类的实例，然后把这些实例放入堆栈，然后把这个堆栈放在主界面上，使用堆栈的设置当前索引来完成界面的切换，部分代码如下：

~~~h
    QStackedWidget *stack;   //界面的切换由这个堆提供服务

    Options *option_page = new Options(this);   //四个不同的界面，分别是设置，关于，设备选择，通信
    Info *info_page = new Info(this);
    Devices *devices_page = new Devices(this);
    Communicate *talk_page = new Communicate(this);
~~~

~~~cpp
    stack = new QStackedWidget(this);

    stack->addWidget(option_page);   //页面0, 设置页面
    stack->addWidget(info_page);     //页面1, 关于页面
    stack->addWidget(devices_page);  //页面2, 设备列表页面
    stack->addWidget(talk_page);     //页面3, 通讯页面
    stack->resize(430,440);

    Layout *lay = new Layout;
    lay->addWidget(ui->option, 1);
    lay->addWidget(ui->about, 1);
    lay->addWidget(ui->min, 2);
    lay->addWidget(ui->close, 2);
    lay->addWidget(stack, 3);

    this->setLayout(lay);

void Window::show_about_page()   //切换界面的例子
{
    stack->setCurrentIndex(1);
}
~~~



> 下面的一部分废弃，没有用

当项目当中具有多个ui文件的时候，我们应该如何引用这些ui文件？

解决这一切问题的关键在于我们需要直到ui文件是如何起作用的，每一个ui文件都有一个名字，例如`uiname.ui`，然后这个ui文件还有必然有一个根元素，例如是一个QWidget，它有一个objectName，例如是`Form`，那么我们其实可以尝试先编译一下，虽然会报错，但是会产生我们想要的一些文件，例如我们会发现每个ui文件都会生成一个`ui_uiname.h`的头文件，打开头文件，我们会发现里面包含了一个叫做`Ui_Form`的类，并且这个类被以`Form`的类名字放进了Ui的namespace中。至此，我们基本上已经得到了我们想要的所有信息。

如果我们想使用在主界面的类文件里面使用特定的ui文件，那么我们首先要包含这个ui文件对应的头文件，然后就可以通过头文件对应的类引用这个ui文件里面的主元素了，例如下面，虽然我将主窗口的类名设置为了View，也自动生成了名为`view.ui`的ui文件，和对应的`View`的根元素，但是我依旧可以通过修改上面的东西实现将主界面设置为任意我想要的ui文件：

~~~c++
#ifndef VIEW_H
#define VIEW_H

#include <QWidget>
#include "ui_config.h"   //引用这个头文件才能得到Ui::Form

namespace Ui {
class View;
}

class View : public QWidget
{
    Q_OBJECT

public:
    explicit View(QWidget *parent = 0);
    ~View();

private:
    Ui::Form *ui;  //更改主界面的类型
};

#endif // VIEW_H
~~~

~~~c++
#include "view.h"
#include "ui_config.h"  //应用config.ui文件对应的ui_config.h头文件

View::View(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Form)  //将默认的Ui:View更改为我们想要的config.ui的根元素的objectName：Ui::Form
{
    ui->setupUi(this);
}

View::~View()
{
    delete ui;
}
~~~



### 文件系统

当引用资源的时候，常用的方法是加入资源文件，然后使用`:/style/style.css`这样的路径进行引用，这种方式的特点是编译之后是看不到单独的css文件的，如果的确需要得到单独的文件，那么应该使用相对路径。

例如，应用使用了配置文件，对设置进行配置，然后发行的应用也需要可以看到这个单独的配置文件，并且可以通过直接修改这个配置文件对设置进行修改。那么配置文件的路径应该是这样的`./config.ini`，基本上编译完了之后，如果一切正常，应该是看不到配置生效的，因为在编译完的文件夹中没有这个文件，此时需要在编译完成的文件的exe所在文件夹的上一层文件夹加入这个文件，应该就能生效。然后发行的时候，应该放在exe文件的同一层。

差不多就是这个解决思路。

时间太久了，细节我已经记不太清楚了。



### 列表

当需要显示一些列表结构的时候，可以使用`QListWidget`

然后可以在上面添加列表项，例如：

~~~cpp
    ui->List->addItem(new QListWidgetItem("Stan"));
    ui->List->addItem(new QListWidgetItem("Stan"));
    ui->List->addItem(new QListWidgetItem("哈哈\n额呵呵"));
~~~

自然，也需要进行美化，方法还是使用css

~~~css
QListWidget {
    background-color: rgba(255,255,255,0);
    background-image: url(./rain1.jpg);
    outline:0;
    border: none;
    border-radius: 5px;
}
QListWidget::item{
    background-color:rgba(255,255,255,200);
    margin-bottom: 5px;
    padding:10px;
    border-radius:5px;
}

QListWidget::item:selected {
    border-left: 3px solid #f00;
    border-top:none;
    border-right:none;
    border-bottom:none;
    background: #0f0;
}

QListWidget::item:selected:active {
    background: #0f0;
    border-left: 3px solid #f00;
    border-top:none;
    border-right:none;
    border-bottom:none;
}
~~~

上面的css示例是很混乱的，很多东西都是没用的，重要的是，第一outline属性，如果不加这个属性的设置当点击某个项目的时候，会出现一个虚线边框，并且使用border属性也去除不掉，所以这个很重要。另外就是怎么引用表项，方法就是`::item`，另外还有各种伪选择器，也应该注意一下。



普通的item就是文字而已，如果想增加选择框之类的东西，实际上我们应该直接换一个部件，例如checkbox，他就可以自带选择框和字符串。使用方法如下：

~~~cpp
    QListWidgetItem *it;
    it = new QListWidgetItem(ui->List);
    QCheckBox *b;
    b = new QCheckBox("stan");
    b->setObjectName("Check");
    ui->List->setItemWidget(it, b);
~~~

我特意设置了objectname，这样就可以利用css对checkbox进行样式修正了。

这是checkbox的样式：

~~~css
QCheckBox {
	spacing: 5px;  # 在这里我们也可以设置复选的文本样式
    font-family: "Microsoft YaHei UI";
    font-size: 9;
}

QCheckBox::indicator {
	width: 15px;
	height: 15px;
}

QCheckBox::indicator:unchecked {
	image: url(:/buttonbg/checkbox_normal);
}

QCheckBox::indicator:unchecked:disabled {
	image: url(:/buttonbg/checkbox_disable);
}

QCheckBox::indicator:unchecked:hover {
	image: url(:/buttonbg/checkbox_hover);
}

QCheckBox::indicator:checked {
	image: url(:/buttonbg/checkbox_down);
}

QCheckBox::indicator:indeterminate {
	image: url(:/buttonbg/checkbox_indeterminate);
}
~~~

要注意的是，前面的选择框叫做indicator，如果想要修改它的长宽，直接使用width和height是无效的。必须自己定义图片，实在很麻烦，但是没办法。

[这是一个参考](https://cloud.tencent.com/developer/article/1022909)

[另一个参考](http://www.cnblogs.com/csuftzzk/p/qss_radiobutton_checkbox.html#)













## Quick

从现在起，我开始学习Qt Quick技术，据说这个开发起来会快一些？应该吧。

毕竟我的Qt学习都是为了满足自己的使用，所以，迅捷就很重要，我想要能够尽快的搞定。原本的每次都要搞无边框，动作定义，自定义布局等等，好费劲。但愿Quick会像它的名字一样。



现阶段的参考书是[QML Book中文版](https://github.com/cwc1987/QmlBook-In-Chinese)，感谢翻译者

### 初步认识

据说是这样的：Qt Quick技术下前后端分离，前端提供界面，使用QML这种新的标记语言制作界面，后端依旧是C++，所以这就是大概的结构框架了吧。



### QML快速入门

当初步学习QML的时候，也许不使用Qt Creator更好，因为他们会涉及一些其他的东西，也会有一些限制，尤其是在啥都不懂的情况下。此时，有一个工具可以使用。如果正常，那么安装了Qt Creator之后应该已经把路径加入环境变量了，在Qt的安装路径下的bin文件夹中有一个工具叫做`qmlscene.exe`，既然加入环境变量了，我们自然可以在任意位置的powershell下面调用`qmlscene`命令。

然后，我们可以构建一个`.qml`文件，然后使用`qmlscene name.qml`即可运行，很爽，很完美。

这里给出一个示例：

~~~QM
import QtQuick 2.0

Rectangle {

	id: root

	width: 120; height: 240

	color: "#D8D8D8"

	Image {
		id: wallpaper

		x: 10; y: 10

		source: "images/wall.png"
	}

	Text{

		y: 40

		width: root.width

		horizontalAlignment: Text.AlignHCenter

		text: "Stan"
	}
}
~~~

想简单一点可以直接把`Image`删掉，想使用图片的话，直接在这个文件的目录下按照`source`指定的路径放置图片即可加载。



#### 开始

这些东西其实是在是很简单，所以那些明显的什么`name:value`这样的结构，什么根元素子元素嵌套，语句结尾的分号什么的就不多说了，从上面的例子里面应该就能直接看出来。所以，下面只说一些有必要说明的。

每一个元素都可以使用id进行引用，所以如果不指定索引就会比较麻烦，但是特别的可以使用parent来访问父对象

然后定位上，还是使用左上原点的经典屏幕坐标系，子元素的坐标总是相对于父元素的，这一点很重要。

#### 属性

呃，我老是很没条理，所以，还是按照书上来，有条理一点吧。

- 属性绑定：这个似乎很厉害的样子，例如，如果设置了`height: 2*width`，那么二者就达成了属性绑定，会自动更新的。但是事实上我对宽高的绑定测试并不成功，大概是因为这一对属性比较特别吧，可能其他的就可以了
- 自定义属性：自定义属性要加上`property`修饰符
- 默认属性：`default`修饰符
- 属性转发： `alias`修饰符
- 自动类型转换：text属性需要字符串的值，但是字符串可以和整型相加，实现自动类型转换
- 结构化属性：有些属性是有结构化的复杂形式的，例如font自身还包含了family和pixelSize等，可以使用`font.family: "Ubuntu"`这样的形式来设置
- 信号处理也是属性的方式

输出， 这个很有用， `console.log("height: ", heigth)`这样子的，例如：

`onHeightChanged: console.log("height: ", height)`这个可以捕捉高度改变的信号，然后输出新的高度值

#### 脚本

可以使用脚本的哦，javascript脚本，很强，可以使用函数，还可以监控键盘等。



#### 基本元素

元素可以划分为可视化与非可视化，可视化元素中的几个比较基础的是：Item(基本元素对象),Rectangle(矩形框),Text,Image,MouseArea



### 题外话

我似乎并没有非常多的耐心继续下去，之前的c++配合ui设计的方法确实会比较麻烦，对于部件的掌控似乎没有十分自由，但是QML的确会感觉自由了很多，但是，要重新来一遍，真的好麻烦的样子。

我最在意的还是窗口外观，如果新建一个Qt Quick项目，默认的根元素就是Window，加载过程使用了`QQmlApplicationEngine`这个引擎，这个引擎要求根元素必须是`Window`或者`ApplicationWindow`，如果要使用Rectangle作为根元素，就必须更改加载引擎，详情见[这个回答](https://stackoverflow.com/questions/32392070/rectangle-as-a-root-element-in-qml)

我其实想说什么，窗口的美化依旧不能通过直接设置什么颜色来实现，这终究还是窗口的一些特殊设置，根元素一般还是要选择`Window`，然后：

~~~QML
import QtQuick 2.6
import QtQuick.Window 2.2

Window {
    visible: true
    width: 640
    height: 480
    //title: qsTr("Hello World")

    //flags:Qt.FramelessWindowHint
    //modality: Qt.WindowModal;

    flags: Qt.Window | Qt.FramelessWindowHint //| Qt.WindowSystemMenuHint

    color: Qt.rgba(1,1,1,0)

    MouseArea {
        anchors.fill: parent
        onClicked: {
            console.log(qsTr('Clicked on background. Text: "' + textEdit.text + '"'))
        }
    }

    TextEdit {
        id: textEdit
        text: qsTr("Enter some text...")
        verticalAlignment: Text.AlignVCenter
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 20
        Rectangle {
            anchors.fill: parent
            anchors.margins: -10
            color: "transparent"
            border.width: 1
        }
    }
}

~~~

注意上面大概有这么几个设置比较重要，模态：模态指的是当模态的对话框未被关闭之前，用户不能与同一应用程序的其他对话框交流，就像是ios上面的弹窗的感觉。

然后是flages，可以去看文档，flages应该是一个四个字节的二进制数值，一般用十六进制表示，不同的位用来设置窗口的不同表现，例如无边框，但是如果单独设置了无边框，那么实际意味着其它位就是0，其中就包含了任务栏小部件，这就意味着这个程序不会以小部件的形式出现在任务栏，当无边框，又没设置退出按钮的时候，这会很麻烦，所以上面设置了一下小部件。另外，颜色的透明是有用的，但是应该并不存在圆角设置，所以，它们一般使用覆盖圆角矩形的设置。

但是当要使用背景图片的时候，图片还是不能正确的显现圆角，必须加遮罩。[圆角解决方法](https://stackoverflow.com/questions/6090740/image-rounded-corners-in-qml)



#### 我在关心什么

无论使用原本的C++设计模式，还是现在的Qt Quick设计模式，我关注的第一件事就是窗口的美化，如果窗口无法美化到我想要的地步，那么我将止步不前，无法说服自己去做其他的事情。

我的要求其实很简单：

- 无边框
- 圆角
- 透明化

无边框是必须的，我无法忍受Windows默认的丑陋边框。圆角也是必须的，透明化也一样，但是这并不意味着我最后写的程序一定是极其透明的(往往只会稍微带一点透明)。

但是，这个一般都会带来一些额外的要求：

- 自定义窗口拖拽
- 自定义窗口缩放
- 自定义关闭等必要按钮

前面的笔记中以经记录了我在C++中为了达到以上效果的做法。

当我转向QML时，我也必须做到这些。其实，我并不打算让自己在Qt上面有多高的造诣，只是写着玩一玩而已，但是我也希望我的模式足够先进，不要用一些已经被遗弃的设计模式，我想努力做到这一点，当然现在还差得远。So，据说QML是未来，毕竟Qt的宣传片里面基本都是它，我会努力的使用QML，至于完整的Qt Quick这种方式，我还没有决定，因为我似乎不太想大量使用JS。所以我期待的方法是QML配合C++来完成，如果是这样的话，又涉及到另外一个选择：是用C++扩展QML还是反过来，我倾向于后者，也就是说使用QML设计界面以及一些简单的动作，后台与显示则由C++接手，换句话说，相当于把整个界面当作一个自定义的复杂部件，由C++负责控制及呈现这个界面。但是，现在的问题是，我并不太会。

总而言之，在现在这个阶段，我必须努力用QML完成所有设计，也许这也算是Qt Quick吧。

话说回来，如何使用QML完成上述基础任务：

无边框实际上上例已经实现现了，就不做赘述。

至于透明化，期待中是有一种极其简单的方式的，实际上确实有，很开心。只需要将Window根元素的颜色设置为transparent即可，如：`color: "transparent"`

另外要注意Window元素还有一个属性叫做`opacity`，这个属性的功能是透明化，效果是让Window及位于其上的所有元素都透明，所以这个属性没啥用。

接下来的策略是，主窗口完全透明，之后会在其上绘制一个`Rectangle`作为主窗口背景，至于它的颜色，透明度，以及圆角就随意设置了，非常自由化。

接下来，会设置一系列的`MouseArea`分别负责窗口的拖动和缩放，以及关闭窗口。

至于这些MouseArea的设置，自然也有不少技巧，出于友好的考虑，如果界面中不存在其它可能需要拖动的区域的话，那么负责拖动的MA应该覆盖除了缩放之外的全部区域，然后界面的缩放，传统上也要被分割为三个区域，右侧边缘负责横向缩放，下方边缘负责纵向缩放，右下角负责整体缩放。但是，明显，当界面中也有拖动元素操作的时候就要把拖动操作的区域设置为顶部边缘的某些区域了。

同时处于友好考虑，还要设置光标的形状，自然是鼠标处于特定区域，并且按下左键时会改变鼠标形状。要注意的是，鼠标形状的设置并不是在MA的onPressed事件的处理中设定的，而应该直接通过MA的属性设置，而事件只负责标志位，否则无效，总之，看代码吧：

~~~QML
import QtQuick 2.6
import QtQuick.Window 2.2

Window
{
    visible: true
    width: 640
    height: 480
    x: 200
    y: 200
    id: root

    property int resize_event_size: 15

    flags: Qt.Window | Qt.FramelessWindowHint //| Qt.WindowSystemMenuHint

    color: "transparent"

    //opacity: 1

    Rectangle
    {
        id: rect1
        width: root.width
        height: root.height
        color: "#00ff0000"
        radius: 10
    }



    MouseArea
    {
        id: move_window
        width: root.width-resize_event_size
        height: 2*resize_event_size
        anchors.top: rect1.top
        anchors.left: rect1.left
        propagateComposedEvents: true
        z: 1

        property bool press_already: false
        property int mx: 0
        property int my: 0
        onPressed: {
            //console.log(mouseX)
            mx=mouseX
            my=mouseY
            press_already=true
        }
        onPositionChanged: {
            //console.log(mouseX)
            root.x+=mouseX-mx
            root.y+=mouseY-my
        }
        onReleased: {
            press_already=false
        }

        cursorShape: press_already? Qt.SizeAllCursor:Qt.ArrowCursor

    }

    MouseArea
    {
        id: zoom_width
        width: resize_event_size
        height: root.height-resize_event_size
        anchors.right: rect1.right
        anchors.top: rect1.top
        property int mx: 0
        property int my: 0
        onPressed: {
            //console.log(mouseX)
            mx=mouseX
            console.log("ok1")
        }
        onPositionChanged: {
            //console.log(mouseX)
            root.width+=mouseX-mx
        }

        cursorShape: Qt.SizeHorCursor
    }
    MouseArea
    {
        id: zoom_height
        width: root.width-resize_event_size
        height: resize_event_size
        anchors.left: rect1.left
        anchors.bottom: rect1.bottom
        property int mx: 0
        property int my: 0
        onPressed: {
            //console.log(mouseX)
            my=mouseY
            console.log("ok2")
        }
        onPositionChanged: {
            root.height+=mouseY-my
        }
        cursorShape: Qt.SizeVerCursor
    }

    MouseArea
    {
        id: zoom_both
        width: resize_event_size
        height: resize_event_size
        anchors.right: rect1.right
        anchors.bottom: rect1.bottom
        property int mx: 0
        property int my: 0
        onPressed: {
            //console.log(mouseX)
            mx=mouseX
            my=mouseY
            console.log("ok3")
        }
        onPositionChanged: {
            //console.log(mouseX)
            root.width+=mouseX-mx
            root.height+=mouseY-my
        }
        cursorShape: Qt.SizeFDiagCursor
    }



    Rectangle
    {
        width: 30
        height: 30
        color: "#aa0000"
        radius: 3
        anchors.right: rect1.right
        anchors.rightMargin: 15
        anchors.top: rect1.top
        anchors.topMargin: 15

        MouseArea
        {
            hoverEnabled: true
            anchors.fill: parent
            onClicked: {
                Qt.quit();
            }
            onEntered: parent.color="#ff0000"
            onExited: parent.color="#aa0000"
            z: 10
            cursorShape: Qt.ArrowCursor

        }

        Text
        {
            text: "❌"
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.family: "Microsoft YaHei Ui"
            font.pixelSize: 20
        }
    }

}

~~~

上述代码里面的rect1就是作为主窗口背景的，同时也是基准元素，因为这里我使用了不少的anchors来进行元素的定位，而Window是不能作为它们的基准的，至少我在尝试中发现并不可行。

上面我使用

另外要注意的是，上面可能没有特别体现出来，一种可能碰到的情况就是MA的相互覆盖，这种情况的处理方式类似于上面的move_window的MA的`propagateComposedEvents: true`属性，大概原理就是声明事件可以继续向下传递，具体的等我再细致的试验一下，回头再来说。







#### QML文件路径

在qml文件中，设置资源的路径，例如Image的source，和Qt里面的c++的文件路径处理方式不一样。这里面有三种方式：

~~~qml
Image {
    source: "./images/wall.png"
}

Image {
    source: "file:.wall.png"
}

Image {
    source: "file:///D:wall.png"
}
~~~

这里面，第一种是默认的资源文件的路径，第二种是相对路径，第三种是绝对文件路径。如果不想资源被自动编译进入二进制包，应该使用后两者。



### 游戏与动画

近期的小目标是现简单的游戏。

实现游戏的第一要素是事件循环，以PyGame为例，它会提供给我们一个事件循环，在循环内部我们可以实现物体的持续动画，同时手动做事件的检测。

绝大多数游戏中都存在着可以脱离用户的操作而自行持续运动的物体，为了实现这个效果，必须要实现一个事件的循环。

现在看来，Qt里面的实现方式与PyGame并不相同，它并不会直接暴露给我们一个事件循环(但是也许可以使用多线程自己做一个呢？没试)，它的实现策略是Timer，可以设置一个定时器，定时器可以设定时间，然后时间耗尽就会触发事件，可以执行动作，定时器会自动的循环执行，于是最终实现的效果是每隔特定时间，物体就会执行一系列的任务，可以将这些任务设置为自动移动等等，即可。

呃，稍等，网上查到的资料在说，实际上如果用Timer来做实现的话，其实是这样的，同时设置多个Timer，然后如果某一个的timeout事件处理时间太长的话，错过的其它Timer的事件，会直接导致其他的被忽略。

所以，我其实在犹豫，我无法确定执行的事件以后会不会很复杂，这样的话是不是多线程也许会更好？

哦，等等，多线程我是不是已经使用过了？在文件传输的客户端里面？



### 着色器与OpenGL

另外一个可能比较有意思的话题就是通过着色器来设置图片的效果，以及初等的OpenGL了。等有空了，可以玩玩看。



### MouseArea

`mousearea`的重要性自不必说，在QML里面，所有的鼠标动作都需要它的参与。

这里要说的是几个需要注意的地方，这些东西其实完全可以去看官方的文档，说得非常仔细，这里我只是简单的说一下。

首先，很容易忽略的问题就是mousearea的anchors.fill或者是width和height。总而言之就是必须设置尺寸。如果想要可视化一下，可以在里面再嵌套一个Rectangle

然后就是重叠问题，如果Mousearea相互重叠的话，必须要考虑顺序问题，首先如果两个元素在源码里面有先后出现顺序，那么必然是后出现的叠在最上面，覆盖掉下面的区域。但是似乎可以通过z来进行设置，但是注意z只对并列的元素才有意义。例如源码中A出现在B之前，可以通过设置z让A覆盖在B上面(应该是，我并没有试验过)，但是并不能通过设置z让A的子元素覆盖在B之上。

总而言之，顺序很重要，要小心的根据想要的效果规划mousearea以及顺序，z其实真的不建议使用，感觉会导致混乱。

然后如果真的发生了覆盖，又想让信号传递到下层，例如A覆盖在B之上，那么默认click信号是不会传递到B的，那么首先需要设置A的属性:`propagateComposedEvents: true`，这个代表这可以传递信号向下，然后还要在他的onClicked里面处理完想要处理的事务之后设置`mouse.accepted=false`以伪装自己没有处理点击信号。这样下层就会收到信号。

另外需要提及的就是hover的问题，如果要处理`onEntered和onExited`信号的话，必须首先赋予这个区域接受悬浮信号的能力`hoverEnabled=true`

另一个重要问题，如果两个MouseArea有重叠，那么onEntered也会出问题，即上层元素的enter不会被传递到下层元素，并且还不存在前面像click那样的方法可以自行传递，这个问题就很烦。

我做了一些搜索和尝试，并没有找到十分满意的方法，现在使用的解决方法是，必须将上层元素设置为下层元素的子元素。也就是说子元素的onenter会被自动传递到父元素，当然并不要求必须是直接子元素，可以是多重的子元素也没问题。

这样虽然可以做，但是有时就不得不更改代码结构。现在只能这样了。

总而言之，就是这些了，规则很简单。但是事实上对于某些比较复杂的组件，情况会稍微复杂一点，后面会提及。



### 组件

当某些设计变得非常复杂的时候，我们需要将一部分组件拆分出来，单独写在一个`.qml`文件中，让它成为一个整体，然后引用。

其实用起来非常简单，随意的一些组件组合在一起就可以。然后保存成一个`.qml`文件，他们将成为一个以文件名为名字的新组件，所以最好文件名首字母大写比较好。

然后需要注意的就是接口。

新组件只有根目录的属性能被外界获取和设置。所以要注意，例如：

~~~QM
Rectangle {
    width:10
    height:11
    signal my_click
    property alias mo_width: mo.width
    MouseArea {
    	id: mo
        widht: 10'
        height: width
        onClicked: {
            console.log("hello");
            parent.my_click();
        }
    }
}
~~~

基本上，上面就是所有的重要内容了，对于普通的属性，可以使用`property alias mo_width: mo.width`，赋予子元素的属性一个别名，这样外部就可以通过这个别名修改子元素属性了。例外根元素的width等这些属性自然就可以直接获取。

另外就是信号问题，信号的处理逻辑是这样的，首先需要在根元素设置一个新的信号例如`signal my_click`，然后需要在子元素的某个事件中触发这个信号，如`parent.my_click()`，在外部可以设置如何处理这个信号，在本例上就是定义`onMy_click`信号的处理方法，这样就可以获取内部的信号了。明显一个信号对应的事件就是前面加一个`on`然后首字母变大写。

组件就是这些了。



### 打开新的窗口

假设现在想要实现一个新的功能，即窗口靠近屏幕边缘时隐藏，同时出现一个小的图标，点击之后窗口可以再次出现。

那么这个功能的设计涉及的要点如下：

- 窗口的隐藏
- 新图标

重中之重就是后者，他的实现方式是，在源文件钟添加一个新的元素：

~~~QML
    Window {
        id: hidden_area
        height: 80
        width: 80
        visible: false
        flags: Qt.Window | Qt.FramelessWindowHint
        color: "transparent"
        onActiveChanged: {
            if(!active)
            {
                hidden_area.visible = false
            }
        }

        Rectangle {
            color: "#220000ff"
            anchors.fill: parent
            radius: hidden_area.width/2

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    root.x = Math.max(0, root.x);
                    root.y = Math.max(0, root.y);
                    root.show();
                    hidden_area.hide();
                }
            }
        }


    }
~~~

这个元素也应该是一个Window元素，那么自然也可以通过设置实现他的无边框，然后透明，同时覆盖一个新的图形，并设置一个按钮来实现点击唤出窗口。

首先需要设置这个元素的`visible: false`，让它不可见。

在主窗口中首先要实现位置检测，这时可以通过`Screen.width`等获取屏幕的宽高信息，然后通过和窗口的`x,y`比对，决定是否隐藏窗口。考虑一下可知，自然是鼠标首先拖动窗口到边缘，然后释放，所以在释放鼠标的事件中检测，决定是否隐藏即可。

隐藏窗口只需调用窗口的hide方法即可，然后第二窗口的出现需要这样：

~~~QML
hidden_area.visible = true
hidden_area.requestActivate();
root.hide()
~~~

这里的hidden_area就是第二窗口的id，root是主窗口的id。

我并不确定上面代码里hidden_area的`onActiveChanged`事件是不是需要。应该不用吧，其实。

然后唤出主窗口只需要调用主窗口的`show`方法，同时隐藏自己即可。



### TextEdit

这里介绍一个新的组件，我非常喜欢。TextEdit是多行文本输入框，它的最大好处在于可以获取内容的尺寸，然后还可以通过设置实现自动换行。如下：

~~~QML
TextEdit {
anchors.top: parent.top
anchors.right: parent.right
id: plan_content
width: parent.width-35
height: paintedHeight+10
text: ""
wrapMode: TextEdit.Wrap
font.family: "Microsoft YaHei"
font.pixelSize: 15
}
~~~

自然首先需要锚定位置，然后如果要使用自动换行功能需要做两点，首先必须设置宽度，自然这个宽度可以和一个其他的值绑定例如窗口宽度等。然后需要设置`wrapMode: TextEdit.Wrap`，这个值有多种选择，对应不同的换行模式，具体看文档。

然后就是获取内容的尺寸，这一点可以通过`paintedHeight`来获取，自然还有一个对应的宽度。于是就可以实现文本框随内容的尺寸变化。

接下来还可以设置一些文本的属性这就不细说了。



最后要提及的就是mousearea的问题，有些时候，必须要在textedit上面覆盖一层mousearea，例如要设置鼠标进入该区域的动作。然后自然还需要实现点击之后进入编辑功能，那么就涉及到了信号在他们之间的传递。

~~~QML
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        propagateComposedEvents: true
        onEntered: {
            marker.visible = true
        }
        onExited: {
            marker.visible = false
        }
        onClicked: {
            marker.visible = false
            //mouse.accepted = false
            if (!plan_content.activeFocus) {
                plan_content.forceActiveFocus();
                plan_content.cursorPosition = plan_content.text.length;
            } else {
                plan_content.focus = false;
            }
        }

    }
~~~

这里的实现方法与之前说到的信号传递不同，我们需要做上面onClicked事件内的工作，这里的`plan_content`是TextEdit的id。所以大概这里的原理就是让TextEdit获取焦点。同时因为默认获取焦点之后光标在开头，于是需要设置光标的位置到尾部。



另外，默认情况下，TextEdit是不具备鼠标功能的，指的是鼠标点击更改光标位置，选中，复制，剪切等功能的，这些都需要自己实现，我还没做。





### ListView

这是另外一个我非常喜欢的部件，对于它的学习其实来自于qml book，就是上面提及的参考书的mvd部分。

ListView的优点在于，首先可以通过对于model的修改实现动态增删元素，然后另外它自动实现了滚动功能，只要设置了他自身的尺寸，它就会自动包含一个不可见的滚动条，然后当元素很多的时候可以通过鼠标实现滚动选择。

其实，我想说的差不多就是这些了，剩下的可以直接通过看书上的讲解就好，其实蛮详细的。

这里要说的最后一点就是ListView的mousearea功能，因为当使用listview的时候，自然会想要一个点击空白处添加新的项的功能，于是可以在ListView里面定义一个覆盖了parent的MouseArea，如下：

~~~QML
    Rectangle {
        width: root.width-40
        height: root.height-70
        anchors.centerIn: parent

        ListView {
            anchors.fill: parent
            anchors.margins: 10

            clip: true
            model: item_model
            delegate: number_delegate

            MouseArea {
                z: -1
                anchors.fill: parent
                onClicked: {
                    item_model.append({"number":1})
                }
            }
        }


        Component {
            id: number_delegate
            Plan_item {
                width: parent.width
                onClick_done: {
                    item_model.remove(index);
                }
                onClick_delete: {
                    item_model.remove(index);
                }
            }
        }
    }
~~~

这里的布局方式是，首先定义了一大块矩形，然后在矩形内部定义了一个ListView，ListView上面再覆盖一个MouseArea，下面再定义代理，代理里面使用了自定义组件，这个自定义组件对应ListView的一个条目，包含了几个图标和一个TextEdit，也挺复杂的。

于是要实现上面的功能首先要保证MouseArea应该在自定义组件的下面，这里用到了z属性，这个必须使用，然后应该注意自定义组件不要设置向下传递信号的功能。

这样有组件的地方点击就是执行组件的功能，没组件的地方点击添加组件。

自然，当满了之后，就不能继续点击添加了，解决方法就是在矩形下方再定义一个小的MouseArea，实现添加功能。



Ok，截止到现在，我想说的就是这些了，总而言之，最最重要的就是要厘清MouseArea的作用区域的问题。





### 新设计

明显. 我喜欢使用QML进行界面的设计, 可以比较轻松地做出想要的效果, 也很明显, 我也喜欢使用c++进行后台的设计, 而且现在我基本上都可以比较轻松的理清脉络, 让后台的界面之间完全使用信号和槽进行通信, 这样也算是比较规范的设计模式.

那么一个必须要搞定的点就是如何在QML里面使用c++类, 以及二者如何通过信号和槽进行交流.

关于这一部分的教程, [这是写得很好的我的主要参考博客]( https://www.cnblogs.com/lz20150121/p/5872293.html ), 感谢作者

#### 类的生成与注册

直接为工程添加新的c++ class, 即可添加类的头文件和源码, 假设我们的类叫做Backend, 那么要求这个类必须继承`QObject`, 一般情况下, 我们可能会需要调用这个类的普通方法, 发送信号到槽, 接受信号, 调用属性.

首先, 如果想要调用类的普通方法, 这个方法的声明必须加上`Q_INVOKABLE`宏, 例如:

~~~c++
Q_INVOKABLE void test(QString info);
~~~

对于类的信号和槽无需特别处理

对于想要提供给qml访问的属性, 需要使用如下定义:

~~~c++
Q_PROPERTY(int width READ get_width WRITE set_width NOTIFY change_width2)
~~~

上面的定义方式可以以名字`width`向qml开放一个属性的访问, 当qml试图获取width的值的时候, `get_width`方法将会被调用, 当qml试图使用`my_backend.width=30`这样的方式为width赋值的时候set_width方法将会被调用

至于最后一个是一个signal, 我觉得没啥用, 实际上可以删掉不写, 例如:

~~~c++
Q_PROPERTY(int width READ get_width WRITE set_width)
~~~

所以, 我们的一个类可以以这样的方式定义和声明:

~~~c++
// back.h

#ifndef BACK_H
#define BACK_H

#include <QObject>
#include <QString>
#include <QDebug>

class Backend : public QObject
{
    Q_OBJECT
public:
    explicit Backend(QObject *parent = nullptr);

    Q_INVOKABLE void test(QString info);

    Q_PROPERTY(int width READ get_width WRITE set_width)

    int get_width();
    void set_width(int w);


signals:
    void width_change(int width_a);

public slots:
    void get_info(QString info);

private:
    int _width;
};

#endif // BACK_H
~~~

~~~c++
//back.cpp
#include "back.h"

Backend::Backend(QObject *parent) : QObject(parent)
{
    qDebug("generate Back");
    _width = 20;
}


void Backend::test(QString info)
{
    qDebug("this is ordinary func call");
//    qDebug<< (info);
}


int Backend::get_width()
{
    qDebug("try to get width");
    return _width;
}

void Backend::set_width(int w)
{
    qDebug("try to set width");
    _width = w;
}


void Backend::get_info(QString info)
{
//    qDebug("I get info");
//    qDebug(info);
    qDebug() << info;
    emit width_change(20);
}

~~~

然后,这个类必须在main.cpp里面进行注册才能使用:

~~~c++
// main.cpp
#include <QGuiApplication>
#include <QQmlApplicationEngine>

#include "back.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    qmlRegisterType<Backend>("stan.qt.backend", 1, 0, "Backend");
    // 上为注册语句

    QQmlApplicationEngine engine;
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}
~~~

接下来就可以在qml里面使用这个类了:

~~~qml
import QtQuick 2.6
import QtQuick.Window 2.2

import stan.qt.backend 1.0

Window
{
    visible: true
    width: 640
    height: 480
    x: 200
    y: 200
    id: root

    property int resize_event_size: 15

    flags: Qt.Window | Qt.FramelessWindowHint //| Qt.WindowSystemMenuHint

    color: "transparent"
//    color: "red"

    //opacity: 1

    Rectangle
    {
        id: rect1
        width: root.width
        height: root.height
        color: "#55ff0000"
        radius: 10
    }

    Backend
    {
        id: my_backend
    }

    Rectangle
    {
        id: btn1
        width: 30
        height: 30
        color: "white"
        anchors.right: rect1.right
        anchors.rightMargin: 80
        anchors.top: rect1.top
        anchors.topMargin: 80


        MouseArea
        {
            hoverEnabled: true
            anchors.fill: parent
            onClicked: {
//                Qt.quit();
//                console.log("click");
                console.log(my_backend.width);
                my_backend.test("hello");
                my_backend.width = 30
            }
            onEntered: parent.color="#ff0000"
            onExited: parent.color="#aa0000"
            z: 10
            cursorShape: Qt.ArrowCursor

        }

    }



    Rectangle
    {
        id: btn2
        width: 30
        height: 30
        color: "white"
        anchors.right: rect1.right
        anchors.rightMargin: 80
        anchors.top: rect1.top
        anchors.topMargin: 130


        MouseArea
        {
            hoverEnabled: true
            anchors.fill: parent
            onClicked: {
//                Qt.quit();
//                console.log("click");
//                my_backend.test("hello");
                my_backend.get_info("this is slot test");
            }
            onEntered: parent.color="#ff0000"
            onExited: parent.color="#aa0000"
            z: 10
            cursorShape: Qt.ArrowCursor

        }

    }

    Connections
    {
        target: my_backend
        onWidth_change: {
            console.log(width_a);
        }
    }

}
~~~

从上述代码可以看出, 想使用这个类, 首先需要使用注册时的名字做一个导入, 然后像普通元素一样进行实例化, 代码里我们使用Rectangle生成了两个按钮, 在第一个按钮里, 我们展示了如何调用设置类的属性, 以及如何调用类的普通方法, 在第二个按钮里我们展示了如何使用类的槽, 最后的Connection展示了, 如何连接类的信号, 首先需要指定我们的目标, 然后qml连接到目标的信号上使用`on + signal name`, 然后signal的名字首字母需要大写, 例如这里我们的类有一个`width_change`方法, 那么在qml里面连接这个方法就放在`onWidth_change`里面, 这个里面就可以写被触发的时候想要执行的语句, 至于信号携带的参数, 使用和信号声明中一样的名字进行获取.



基本上, 我觉得到这里就基本够用了, 但是考虑到我的关于文件传输的新规范设计里面, 信号之间传递的是一个结构体, 所以接下来还需要了解一下结构体的使用.

呃, 资料搜索结果似乎是不可以. 但是回看ToDo的源码, 可以发现, 我曾经使用过类似的东西, 只是没做笔记:cry:

答案就是使用QVariantList和QVariantMap进行复杂类型的数据的传输, 具体细节甚至是sqlite的使用, 可以多看看ToDo的源码.

Sorry, 心情变得非常糟糕, 今天我没有任何心情再继续了.



### 主界面阴影

我实在是没有多少设计天赋，依旧没能设计出一个觉得满意的界面来，最近在网上看了一些别人的作品，其中有一些作品使用了阴影元素。

这里，记录一下如何在使用QML的情况下，为无边框主界面窗口添加阴影效果。代码如下：

~~~qml
import QtQuick 2.6
import QtQuick.Window 2.2
import QtGraphicalEffects 1.0

Window {
    visible: true
    width: 640
    height: 480
    flags: Qt.Window | Qt.FramelessWindowHint

    color: Qt.rgba(0,0,0,0)

    id: root

    Rectangle
    {
        id: rect
        width: root.width-20
        height: root.height-20
        anchors.centerIn: root
        radius: 10
    }

    DropShadow
    {
        anchors.fill: rect
        horizontalOffset: 6
        verticalOffset: 6
        radius: 15
        samples: 31
        color: "#f0101010"
        spread: 0.0
        source: rect
    }
}

~~~

以上。

原理就是利用QML自带的阴影效果元素DropShadow，但是它只能作用于元素，所以将主界面设置为透明，在上面蒙一个矩形，然后为矩形设置阴影效果，至于阴影元素的调整细节，去看一下官网文档吧，很简单的。



### 矩形圆角

在QML里面到目前为止，据我查到的资料四个圆角是必须一致的，如何分别为四个角设置不同的圆角呢？我的做法是自定义一个组件，包含一个矩形，然后在四个角分别覆盖一个小的矩形，然后为小矩形分别设置圆角。

代码如下：

```QML
import QtQuick 2.0

Rectangle {
    property double radius_left_upper: 0
    property double radius_left_lower: 0
    property double radius_right_upper: 0
    property double radius_right_lower: 0

    radius: Math.max(radius_left_lower, radius_left_upper, radius_right_lower, radius_right_upper)

    Rectangle {
        width: parent.width/2
        height: parent.height/2
        radius: radius_left_upper
        anchors.left: parent.left
        anchors.top: parent.top

        color: parent.color
    }

    Rectangle {
        width: parent.width/2
        height: parent.height/2
        radius: radius_left_lower
        anchors.left: parent.left
        anchors.bottom: parent.bottom

        color: parent.color
    }

    Rectangle {
        width: parent.width/2
        height: parent.height/2
        radius: radius_right_upper
        anchors.right: parent.right
        anchors.top: parent.top


        color: parent.color
    }

    Rectangle {
        width: parent.width/2
        height: parent.height/2
        radius: radius_right_lower
        anchors.right: parent.right
        anchors.bottom: parent.bottom


        color: parent.color
    }

}

```



### 无边框窗口的自定义关闭与最小化

自定义关闭很简单：

```QML
onClicked: {
	Qt.quit();
}
```

但是自定义最小化很麻烦，根据网上查到的资料，在Mac上无边框窗口的自定义最小化是有Bug的，无法工作，有人向Qt官方反馈，但是似乎并未修复。

然后有人给出了[解决方案](https://bugreports.qt.io/browse/QTBUG-64994)

解决方案的处理方法基本就是调用`root.showMinimized();`方法，但是之前必须重新设置`flags`，然后在root的`onVisibilityChanged`方法中重新恢复`flags`

具体细节看以上链接内的`ylilarry`的回答



### 多界面设计，信号与Loader

如何实现页面的切换，这个讲的很好的[wiki](https://wiki.qt.io/QML_Application_Structuring_Approaches)是我的主要参考

简而言之，最重要的技术就是使用Loader，然后借助信号可以串联不同的界面，然后同时QML还允许信号的由内向外和由外向内穿透，十分的自由。

同时，Loader也可以通过设置`source`来实现加载文件，设置`sourceComponent`来实现动态加载元素。细节可以看看官网。



[官方的wiki](https://wiki.qt.io/Special:AllPages)



我在测试中发现，Loader的加载方式存在一些问题，因此我抛弃了这种做法，换成了使用StackView来实现。

StackView的使用算不上复杂，需要注意的点包括如何知道当前元素是谁，以及如何在界面中生成一个定义在qml中的元素，但是却不显示，看一下如下代码：

```qml
    property Component device_page: DevicePage { objectName: "device"}
    property Component set_page: SetPage {objectName: "set"}

    StackView {
        id: stack
        width: 360
        height: 419
        anchors.bottom: rect.bottom
        anchors.left: rect.left
        initialItem: device_page
    }
    
    
    stack.currentItem.objectName!="set"
```

判断当前元素必须使用objectname，如何设置objectname呢？如上代码段

然后关于生成不显示元素也如上。

接下来需要注意的是，定义在qml中的元素和在文件里面定义一个component元素有什么不同呢？其实没什么太多不同，后者适用于简单结构，第一层只能有一个元素和一个id字段，前者可以比较复杂。



细节知识，我后面也许会补充，如果不，这些都是我在开发新的Filer界面时使用的知识，看看以后完成的源码就可以了。



现在我在专注于聊天界面的设计，重点在于ListView的使用，以及文本输入框的使用，对我非常具有参考意义的项目是官方的Qt Quick示例项目[Chat Tutorial](https://doc.qt.io/qt-5/qtquickcontrols-chattutorial-example.html)

不同之处在于，现在我是用的文本输入框是`TextEdit`

```qml
    TextEdit {
        id: input
        color: "black"
        width: 331
        height: 89
        wrapMode: TextEdit.Wrap
        anchors.bottom: main_rect.bottom
        anchors.left: main_rect.left
        textMargin: 10
        Rectangle {
            radius: 12
            anchors.fill: parent
            color: "#22ff0000"
        }
        Keys.onReturnPressed: {
            commu_info.append({value:input.text})
            input.clear();
        }
```

文本输入框是可以接受多行输入的，但是我给它想办法加了一个监听按回车键的方法，注意这里只能这样来监听回车。



除了一些小小的问题之外，我现在已经基本制作完毕了聊天界面的设计，主要遇到的问题在于：

1、如何让ListView自动滚动到底部，这个很简单，在向model添加内容的时候，设置一下positionViewAtEnd就可

2、我也不知道我写代码的时候出了什么问题，listview的item会出现重叠，设置了spacing，但是spacing竟然表现为了两个item顶部的间隔，十分诡异，花了居多的时间也没有找到问题在哪，以及如何解决，然后我删掉全部代码，从最基础的开始逐步重新写竟然又正常了，默认就没有重叠，spacing是上一个底部与下一个顶部的间隔，没能重现出问题所在，解决也就无从谈起。已经证实了，如果delegate没有设置width和height，那么就会出现重叠，这大概是ListView无法直接获取元素的尺寸导致

3、现在发现listview在滚动的时候，会出现超出Listview范围仍旧显示的情况，我不清楚该怎么解决，但是其实也可以，只要上下都用东西遮罩一下就可以，解决了！设置`clip:true`即可

4、自动滚动到底部的时候，底部会紧贴输入框的顶部，我希望保持一定的间隔，方法是给ListView设置一个footer，将footer设置为一个一定高度的透明矩形Component



需要注意的问题，如何设计一个气泡对话框：

一个气泡对话框包括一个圆角矩形主体，和一个三角形的装饰。

三角形部件可以使用Shape进行设计：

```qml
    Component {
        id: righttri
        Shape {
            anchors.top: parent.top
            anchors.topMargin: 10
            width: 21
            height: 24
            anchors.left: parent.right
            anchors.leftMargin: 73
            ShapePath {
                fillRule: ShapePath.WindingFill
                strokeWidth: 0
                strokeColor: "white"
                fillColor: "white"
                startX: 0; startY: 0
                PathLine { x: 21; y: 12 }
                PathLine { x: 0; y: 24 }
                PathLine { x: 0; y: 0 }
            }
        }
    }
```

但是，我写的这个三角形似乎在定位上遇到了一些问题，这就是anchors.leftmargin那个诡异的值的出现原因，细想起来，我似乎在swiftui的右侧气泡对话框上也遇到了类似的问题。

然后要注意的是fillrule的使用，默认的填充规则会导致特定的绘制顺序下没有填充

如何根据值的不同加载不同的部件呢？依旧可以使用Loader的sourceComponent功能，如下：

```qml
    Loader {
        sourceComponent: {
            switch(position) {
            case 1: return lefttri
            case 2: return righttri
            }
        }
    }
```



现在遇到的一个比较困难的问题，在ListView的delegate使用Loader实现根据值使用不同部件的情况下，例如会根据发送方，是文件还是消息等决定使用的部件，当使用的是文件消息框的时候，我在消息框内组合了一个文件图标，一个文件名字text，一个自定义进度条。那么此时就有一个问题，我们如何实时更新进度条呢？

我找了很多方法，都没作用，然后我想到了一个方法。在model里面集成一个字段，process，代表进度值，然后定位出来我们要更新进度的是model的哪一个item，方法就是保持一个index，然后使用ListModel.get(index).process += 0.1这样的方式更新model里面的进度信息，即可实现进度条的更新。其他方式没有发现有效的，甚至使用ListModel.setPorperty(index, “process”, 0.5)这样的方式都不行

另外一点，当使用text的时候，某些情况下，希望文本内容只有一行，并且有固定的宽高，超出范围使用省略号，设置如下：

```qml
                Text {
                    clip: true
                    padding: 3
                    elide: Text.ElideRight  //省略号
                    text: value
                    width: 110
                    height: 20
                }
```



