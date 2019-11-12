#include "widthdialog.h"
#include <QSlider>
#include <QSpinBox>
#include <QPainter>
#include <QPen>
#include <QLineEdit>
#include "window.h"

WidthDialog::WidthDialog(Window* parent)
{
    setFixedSize(200,200);
    pen_width = 1;
    father = parent;
    //this->resize(200,200);
    ok = new QPushButton(this);
    ok->setText(tr("OK"));
    ok->setGeometry(QRect(160,170,30,20));
    connect(ok, &QPushButton::clicked, this, &WidthDialog::close_send);

    QSlider *slider = new QSlider(Qt::Horizontal,this);
    slider->setGeometry(QRect(10,120,120,30));
    slider->setRange(1,50);

    QSpinBox *value = new QSpinBox(this);
    value->setGeometry(QRect(152,120,38,30));
    value->setRange(1,50);


    selfdefine = new QSpinBox(this);
    selfdefine->setGeometry(QRect(10,170,50,20));
    selfdefine->setButtonSymbols(QAbstractSpinBox::NoButtons);
    selfdefine->setRange(1,999);
    connect(selfdefine, SIGNAL(valueChanged(int)), this, SLOT(only_send(int)));

    connect(slider, SIGNAL(valueChanged(int)), value, SLOT(setValue(int)));
    connect(value, SIGNAL(valueChanged(int)), slider, SLOT(setValue(int)));
    connect(slider, SIGNAL(valueChanged(int)), this, SLOT(change_width(int)));

//    connect(this, &WidthDialog::send_width, parent, &Window::get_width);
}

void WidthDialog::change_width(int width)
{
    pen_width = width;
    selfdefine->setValue(pen_width);
    update();
}

void WidthDialog::paintEvent(QPaintEvent *event)
{
    QPainter painter(this);
    painter.setPen(QPen(Qt::black, pen_width, Qt::SolidLine, Qt::RoundCap,Qt::RoundJoin));
    painter.drawLine(QPoint(25,60),QPoint(175,60));

}



void WidthDialog::close_send()
{
    emit send_width(selfdefine->value());
    this->close();
}

void WidthDialog::only_send(int i)
{
    emit send_width(i);
}
