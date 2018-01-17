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