#include "clienter.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    cliEnter w;
    w.show();
    return a.exec();
}
