#ifndef CLIENTER_H
#define CLIENTER_H

#include <QMainWindow>
#include <QListWidget>

QT_BEGIN_NAMESPACE
namespace Ui { class cliEnter; }
QT_END_NAMESPACE

class cliEnter : public QMainWindow
{
    Q_OBJECT

public:
    cliEnter(QWidget *parent = nullptr);
    ~cliEnter();

private slots:
    void setSoftwareListProperties();
    void softwareAreaCheckActions(QListWidgetItem *item);
    void on_clearQt_clicked();

    void on_pushButton_clicked();

private:
    Ui::cliEnter *ui;
};
#endif // CLIENTER_H
