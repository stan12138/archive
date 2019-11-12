#include "pad.h"
#include <QPainter>
#include <QPen>
#include <QMouseEvent>
#include<QStyleOption>
#include<QWidget>
//#include <QDebug>
Pad::Pad(int width, int height, QWidget *parent) : QWidget(parent)
{
    padColor = QColor(255,255,255,180);
    penColor = QColor(0,0,0,255);
    image = QImage(width, height, QImage::Format_ARGB32_Premultiplied);
    image.fill(padColor);
    draw = false;
    penWidth = 2;
}

void Pad::paintEvent(QPaintEvent *event)
{

    QStyleOption opt;
    opt.init (this);
    QPainter p (this);
    style()->drawPrimitive (QStyle::PE_Widget, &opt, &p, this);
    //QPainter painter(this);
    QRect dirty = event->rect();
    p.drawImage(dirty, image, dirty);
}


void Pad::mousePressEvent(QMouseEvent *event)
{
    if(event->button()==Qt::LeftButton)
    {
        lastpos = event->pos();
        draw = true;
    }
}


void Pad::mouseMoveEvent(QMouseEvent *event)
{
    setCursor(Qt::ArrowCursor);
    if(draw)
    {
        drawline(event->pos());
    }
}

void Pad::mouseReleaseEvent(QMouseEvent *event)
{
    draw = false;
}

void Pad::drawline(QPoint pos)
{
    QPainter painter(&image);
    painter.setPen(QPen(penColor, penWidth, Qt::SolidLine, Qt::RoundCap,Qt::RoundJoin));
    painter.drawLine(lastpos, pos);

    int rad = penWidth/2 + 2;

    update(QRect(lastpos, pos).normalized().adjusted(-rad,-rad,rad,rad));

    lastpos = pos;
}

void Pad::resizeEvent(QResizeEvent *event)
{
    if (width() > image.width() || height() > image.height())
    {
        int newWidth = qMax(width() + 128, image.width());
        int newHeight = qMax(height() + 128, image.height());
        resizeImage(&image, QSize(newWidth, newHeight));
        update();
    }
    //qDebug() << width() << height();
}

void Pad::resizeImage(QImage *image, const QSize &newSize)
{
    if (image->size() == newSize)
        return;

    QImage newImage(newSize, QImage::Format_ARGB32_Premultiplied);
    newImage.fill(padColor);
    QPainter painter(&newImage);
    painter.setCompositionMode(QPainter::CompositionMode_SourceIn);
    painter.drawImage(QPoint(0, 0), image->convertToFormat(QImage::Format_RGB32));
    *image = newImage;
}

void Pad::set_pad_color(QColor padcolor)
{
    padColor = padcolor;
    QImage newImage(QSize(width(), height()), QImage::Format_ARGB32_Premultiplied);
    newImage.fill(padColor);
    image = newImage;
    update();
}

void Pad::set_pen_color(QColor pencolor)
{
    penColor = pencolor;
}
