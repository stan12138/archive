#ifndef PAD_H
#define PAD_H

#include<QWidget>

#include <QImage>

class Pad : public QWidget
{
    Q_OBJECT
public:
    explicit Pad(int width, int height, QWidget *parent = nullptr);

    void paintEvent(QPaintEvent *event);
    void resizeEvent(QResizeEvent *event);
    void mouseMoveEvent(QMouseEvent *event);
    void mousePressEvent(QMouseEvent *event);
    void mouseReleaseEvent(QMouseEvent *event);
    void resizeImage(QImage *image, const QSize &newSize);

    void set_pad_color(QColor padcolor);
    void set_pen_color(QColor pencolor);

    void drawline(QPoint pos);

    QImage image;
    QPoint lastpos;
    bool draw;
    QColor padColor;
    QColor penColor;
    int penWidth;
};

#endif // PAD_H
