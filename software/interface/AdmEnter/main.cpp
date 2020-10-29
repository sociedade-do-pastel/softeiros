#include "admenter.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    AdmEnter w;
    w.show();
    return a.exec();
}
