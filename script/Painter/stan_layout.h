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
    void addWidget(QWidget* widget, int p, int width1, int height1);


    QLayoutItem *itemAt(int index) const;
    QLayoutItem *takeAt(int index);
    QSize sizeHint() const;
    int count() const;
    void setGeometry(const QRect &rect);
private :
    struct SI
    {
        SI(QLayoutItem* i, int p, int width1, int height1)
        {
            item = i;
            order = p;
            width = width1;
            height = height1;
        }
        QLayoutItem * item;
        int order;
        int width;
        int height;
    };
    QList<SI *> list;
    int numl=0;
    int numr=0;
    int numm=0;
    int flage=1;
};
#endif // STAN_LAYOUT_H

