#include "window.h"
#include "ui_window.h"
#include "stan_layout.h"
#include <QDebug>
#include <QPainter>
#include <algorithm>
#include <QDesktopWidget>

using std::max;

Window::Window(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Window)
{
    ui->setupUi(this);
    connect(ui->pb3, &QPushButton::clicked, QApplication::instance(), &QApplication::quit);
    connect(ui->pb1, &QPushButton::clicked, this, &Window::showMinimized);
    //connect(ui->pb1, &QPushButton::clicked, this, &Window::showMaximized);
    connect(ui->pb2, &QPushButton::clicked, this, &Window::max_or_recover);

    QStyle *style = qApp->style();
    QIcon closeIcon = style->standardIcon(QStyle::SP_TitleBarCloseButton);
    //ui->pushButton->setIcon(closeIcon);

    QFile file(":/style/style.css");
    file.open(QFile::ReadOnly);
    QString stylesheet = tr(file.readAll());
    qApp->setStyleSheet(stylesheet);
    file.close();

    this->setMouseTracking(true);
    this->press = false;
    this->move_press = false;
    this->change_size = false;
    this->max_flage = false;

    SLayout *layout = new SLayout;
    layout->addWidget(ui->pb1, 2);
    layout->addWidget(ui->pb2, 2);
    layout->addWidget(ui->pb3, 2);
    layout->addWidget(ui->g, 3);
    this->setLayout(layout);

    set_area(QRect(0,0,this->geometry().width(),30));

    QDesktopWidget *desktop = QApplication::desktop();
    this->screen = desktop->screenGeometry();

    QPainter painter(this);
    QPen pen(Qt::green, 5, Qt::DotLine, Qt::RoundCap, Qt::RoundJoin);
    painter.setPen(pen);
    painter.drawLine(QPoint(500,100), QPoint(500,500));

    //this->max_icon = new QIcon(":/ico/max.svg");
   // this->re_icon = new QIcon(":/ico/re.svg");

}

Window::~Window()
{
    delete ui;
}

void Window::set_area(QRect a)
{
    this->area = a;
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
    painter.fillRect(rect(), QColor(192,192,192,100));
    QPen pen(Qt::green, 5, Qt::DotLine, Qt::RoundCap, Qt::RoundJoin);
    painter.setPen(pen);
    painter.drawLine(QPoint(100,100), QPoint(500,500));
}

void Window::drag_resize(QMouseEvent *e)
{
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
