#ifndef WINDOW_H
#define WINDOW_H

#include <QWidget>
#include<QMouseEvent>

namespace Ui {
class Window;
}

class Window : public QWidget
{
    Q_OBJECT

public:
    explicit Window(QWidget *parent = 0);
    ~Window();
    void set_area(QRect a);
    void drag_resize(QMouseEvent *e);
    void max_or_recover();

protected :
    void mousePressEvent(QMouseEvent* e);
    void mouseReleaseEvent(QMouseEvent* e);
    void mouseMoveEvent(QMouseEvent* e);
    void paintEvent(QPaintEvent*);

private:
    Ui::Window *ui;
    bool move_press;
    bool press;
    bool change_size;
    QRect area;
    QPoint old_pos;
    QPoint window_pos;
    QPoint change_old_pos;
    QRect screen;
    bool max_flage;
    //QIcon max_icon(":/ico/max.svg");
    //QIcon re_icon(":/ico/re.svg");
};

#endif // WINDOW_H
