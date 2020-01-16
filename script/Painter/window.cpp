#include "window.h"
#include "ui_window.h"
#include "stan_layout.h"
#include "pad.h"
#include "widthdialog.h"
//#include <QDebug>
#include <QPainter>
#include <algorithm>
#include <QDesktopWidget>
#include <QAction>


using std::max;

Window::Window(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Window)
{
    ui->setupUi(this);
    connect(ui->pb3, &QPushButton::clicked, QApplication::instance(), &QApplication::quit);
    connect(ui->pb1, &QPushButton::clicked, this, &Window::showMinimized);
    connect(ui->pb2, &QPushButton::clicked, this, &Window::max_or_recover);


    mypad = new Pad(340,230);
    mypad->setObjectName("mypad");

    this->setMouseTracking(true);
    this->press = false;
    this->move_press = false;
    this->change_size = false;
    this->max_flage = false;

    this->window_color = QColor(192,192,192,100);

    QDesktopWidget *desktop = QApplication::desktop();
    this->screen = desktop->screenGeometry();
    set_area(QRect(0,0,this->geometry().width(),30));

    set_style();
    set_layout();
    qDebug() << "layout done";
    set_menu();
    qDebug() << "menu done";

}

Window::~Window()
{
    delete mypad;
    delete layout;

    delete color_menu;
    delete windowColorAct;
    delete padColorAct;
    delete penColorAct;

    delete width_menu;
    delete savemenu;

    delete ui;
}

void Window::set_style()
{

    //QStyle *style = qApp->style();
    //QIcon closeIcon = style->standardIcon(QStyle::SP_TitleBarCloseButton);
    QFile file(":/style/style.css");
    file.open(QFile::ReadOnly);
    QString stylesheet = tr(file.readAll());
    qApp->setStyleSheet(stylesheet);
    file.close();

}

void Window::set_layout()
{
    layout =  new SLayout;

    layout->addWidget(ui->lpb1, 1, 60, 20);
    layout->addWidget(ui->lpb2, 1, 60, 20);
    layout->addWidget(ui->lpb3, 1, 60, 20);
    layout->addWidget(ui->pb1, 2, 20, 20);
    layout->addWidget(ui->pb2, 2, 20, 20);
    layout->addWidget(ui->pb3, 2, 20, 20);
    layout->addWidget(mypad, 3, 20, 20);
    this->setLayout(layout);
}


void Window::set_menu()
{
//    qDebug() << "begin generate action";
    color_menu = new QMenu(this);
//    qDebug() << "generate action 1";
    windowColorAct = new QAction(tr("set window color"), this);
//    qDebug() << "generate action 2";
    padColorAct = new QAction(tr("set pad color"), this);
//    qDebug() << "generate action 3";
    penColorAct = new QAction(tr("set pen color"), this);

//    qDebug() << "generate action";

    color_menu->addAction(windowColorAct);
    color_menu->addAction(padColorAct);
    color_menu->addAction(penColorAct);

//    qDebug() << "connect action";

    connect(windowColorAct, SIGNAL(triggered()), this, SLOT(set_window_color()));
    connect(padColorAct, SIGNAL(triggered()), this, SLOT(set_pad_color()));
    connect(penColorAct, SIGNAL(triggered()), this, SLOT(set_pen_color()));
    ui->lpb1->setMenu(color_menu);

//    qDebug() << "action done";

    width_menu = new QMenu(this);
    penWidthAct = new QAction(tr("set pen width"), this);
    width_menu->addAction(penWidthAct);
    connect(penWidthAct, SIGNAL(triggered()), this, SLOT(width_dialog()));
    ui->lpb2->setMenu(width_menu);

    savemenu = new QMenu(this);
    foreach (QByteArray format, QImageWriter::supportedImageFormats())
    {
            QString text = tr("%1...").arg(QString(format).toUpper());

            QAction *action = new QAction(text, this);
            action->setData(format);
            connect(action, SIGNAL(triggered()), this, SLOT(save_file()));
            savemenu->addAction(action);
    }
    ui->lpb3->setMenu(savemenu);
}

void Window::set_area(QRect a)
{
    this->area = a;
}


void Window::set_pad_color()
{
    QColorDialog *colordialog = new QColorDialog(mypad->padColor,this);
    connect(colordialog, &QColorDialog::currentColorChanged, this, &Window::pad_get_color);
    colordialog->setOption(QColorDialog::ShowAlphaChannel);
    colordialog->setWindowTitle("Pad Color");
    colordialog->show();
    //colordialog.setWindowModality(Qt::NonModal);
    //pad_color = colordialog.getColor(mypad->padColor, this, tr("choose color"), QColorDialog::ShowAlphaChannel);

}

void Window::set_window_color()
{
    QColorDialog *colordialog = new QColorDialog(window_color,this);
    connect(colordialog, &QColorDialog::currentColorChanged, this, &Window::window_get_color);
    colordialog->setOption(QColorDialog::ShowAlphaChannel);
    colordialog->setWindowTitle("Window Color");
    colordialog->show();
}

void Window::set_pen_color()
{
    QColorDialog *colordialog = new QColorDialog(mypad->penColor,this);
    connect(colordialog, &QColorDialog::currentColorChanged, this, &Window::pen_get_color);
    colordialog->setOption(QColorDialog::ShowAlphaChannel);
    colordialog->setWindowTitle("Pen Color");
    colordialog->show();
}

void Window::set_pen_width(int width)
{
    mypad->penWidth = width;
}


void Window::mousePressEvent(QMouseEvent *e)
{
    if(e->buttons() == Qt::LeftButton && this->area.contains(e->pos()))
    {
        this->move_press = true;
        this->old_pos = e->pos();
        this->window_pos = this->pos();

        //qDebug() << "press left button";
    }
    if(e->buttons() == Qt::LeftButton)
    {
        this->press = true;
        this->change_old_pos = e->pos();
    }
}

void Window::mouseReleaseEvent(QMouseEvent *e)
{
    this->press = false;
    this->move_press = false;
}

void Window::mouseMoveEvent(QMouseEvent *e)
{
    //qDebug() << e->x() << e->y() ;

    drag_resize(e);

    if(this->move_press)
    {
        if(this->max_flage)
        {
            this->setGeometry(screen.width()/2-200,screen.height()/2-150,400,300);
            //QCursor::setPos(QPoint(200,10));
            max_flage = false;
            move_press = false;
        }
        else move(this->pos()+e->pos()-this->old_pos);
        ui->pb2->setIcon(QIcon(":/ico/max1.svg"));
        //qDebug() << e->pos().x() << e->pos().y() ;
        //qDebug() << e->pos()-this->old_pos;
        //this->window_pos = this->pos();
        //this->old_pos = e->pos();
    }

}

void Window::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.fillRect(rect(), window_color);
}

void Window::drag_resize(QMouseEvent *e)
{
    if(e->x()>(this->width()-30) && e->y()>(this->height()-30))
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
    else if(e->x()>(this->width()-20) && e->y()>30)
    {
        this->setCursor(Qt::SizeHorCursor);
        if(this->press)
        {
            QPoint e1(e->pos()-change_old_pos);
            int w = max(400,this->width()+e1.x());
            //int h = max(this->geometry().height()+e1.y(),300);
            resize(w, this->height());
            change_old_pos = e->pos();
        }

    }
    else if(e->y()>(this->height()-30))
    {
        this->setCursor(Qt::SizeVerCursor);
        if(this->press)
        {
            QPoint e1(e->pos()-change_old_pos);
            //int w = max(400,this->geometry().width()+e1.x());
            int h = max(this->height()+e1.y(),300);
            resize(this->width(), h);
            change_old_pos = e->pos();
        }
    }
    else
    {
        this->setCursor(Qt::ArrowCursor);
        this->change_size = false;
    }

    set_area(QRect(0,0,this->width(),30));
}

void Window::max_or_recover()
{
    if(!this->max_flage)
    {
        this->setGeometry(screen);
        this->max_flage = true;
        ui->pb2->setIcon(QIcon(":/ico/re.svg"));
    }
    else
    {
        this->setGeometry(screen.width()/2-200,screen.height()/2-150,400,300);
        this->max_flage = false;
        ui->pb2->setIcon(QIcon(":/ico/max1.svg"));
    }
}


void Window::width_dialog()
{
    WidthDialog *dialog = new WidthDialog(this);
    connect(dialog, &WidthDialog::send_width, this, &Window::get_width);
    dialog->show();
}

void Window::get_width(int width) const
{
    mypad->penWidth = width;
}

void Window::save_file()
{
    QAction *action = qobject_cast<QAction *>(sender());
    QByteArray fileFormat = action->data().toByteArray();
    QString initialPath = QDir::currentPath() + "/untitled." + fileFormat;

    QString fileName = QFileDialog::getSaveFileName(this, tr("Save As"),
                                   initialPath,
                                   tr("%1 Files (*.%2);;All Files (*)")
                                   .arg(QString::fromLatin1(fileFormat.toUpper()))
                                   .arg(QString::fromLatin1(fileFormat)));
    if (! fileName.isEmpty())
    {
        mypad->image.save(fileName, fileFormat.constData());
    }

}

void Window::pad_get_color(const QColor &color)
{
    //qDebug() << color;
    pad_color = color;
    mypad->set_pad_color(pad_color);
}

void Window::pen_get_color(const QColor &color)
{
    //qDebug() << color;
    pen_color = color;
    mypad->set_pen_color(pen_color);
    //mypad->set_pad_color(pad_color);
}

void Window::window_get_color(const QColor &color)
{
    //qDebug() << color;
    this->window_color = color;
    update();
}
