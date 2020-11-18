#ifndef CLIENTER_H
#define CLIENTER_H

#include <QMainWindow>
#include <QListWidget>
#include <QMessageBox>
#include <QVBoxLayout>
#include <QString>
#include <QGroupBox>
#include <vector>
#include <nlohmann/json.hpp>
#include "roomwidget.h"
#include "../../logicas/LogicaCliEnter.hpp"

QT_BEGIN_NAMESPACE
namespace Ui { class cliEnter; }
QT_END_NAMESPACE

class CliEnter : public QMainWindow
{
    Q_OBJECT

public:
    CliEnter(QWidget *parent = nullptr);
    ~CliEnter();

private slots:
    void softwareAreaCheckActions(QListWidgetItem *item);

    void roomClicked(RoomWidget *r);

    void on_software_list_clear_button_clicked();

    void on_computer_qt_clear_button_clicked();

    void on_computer_qt_disp_input_valueChanged(int arg1);

    void on_actionRefresh_triggered();

private:
    Ui::cliEnter *ui;
    std::vector<QListWidgetItem*> software_items_list;
    std::vector<RoomWidget*> room_widgets_list;
    QVBoxLayout *room_list;
    RoomWidget *selected_room;
    QGridLayout *computer_grid;
    LogicaCliEnter controler;
    json dbInfo;
    json software_json;

    void sortRooms();
    void setSoftwareListProperties();
    void setRoomList();
    void setRoomMap();
};
#endif // CLIENTER_H
