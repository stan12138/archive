#ifndef WIDTHDIALOG_H
#define WIDTHDIALOG_H

#include <QPushButton>
#include <QWidget>
#include <QSpinBox>
#include "window.h"

class WidthDialog : public QWidget
{
    Q_OBJECT
public:
    WidthDialog(Window *parent);
    void paintEvent(QPaintEvent *event);

private:
    QPushButton *ok;
    int pen_width;
    Window *father;
    QSpinBox *selfdefine;

public slots:
    void change_width(int width);
    void close_send();
    void only_send(int i);
signals:
    void send_width(int width);
};

#endif // WIDTHDIALOG_H
