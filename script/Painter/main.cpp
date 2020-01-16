#include "window.h"
#include <QApplication>


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    a.addLibraryPath("./plugins");
    Window w;
    w.setWindowFlags(Qt::FramelessWindowHint);
    w.setAttribute(Qt::WA_TranslucentBackground);

    //w.setWindowOpacity(0.5);
    w.show();

    return a.exec();
}
