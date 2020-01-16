#ifndef WINDOW_H
#define WINDOW_H

#include <QWidget>
#include<QMouseEvent>
#include <QMenu>


#include "pad.h"

#include "stan_layout.h"

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
    void set_style();
    void set_layout();
    void set_menu();

public slots:
    void get_width(int width) const;
    void pen_get_color(const QColor& color);
    void pad_get_color(const QColor& color);
    void window_get_color(const QColor& color);

private slots:
    void set_window_color();
    void set_pad_color();
    void set_pen_color();
    void set_pen_width(int width);

    void width_dialog();

    void save_file();

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

    QAction *windowColorAct;
    QAction *penColorAct;
    QAction *padColorAct;
    QAction *penWidthAct;

    QMenu *color_menu;
    QMenu *width_menu;
    QMenu *savemenu;

    Pad *mypad;

    SLayout *layout;

    QColor window_color;
    QColor pad_color;
    QColor pen_color;
};

#endif // WINDOW_H
