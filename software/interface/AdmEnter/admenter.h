#ifndef ADMENTER_H
#define ADMENTER_H

#include <QMainWindow>
#include <QStringList>
#include <QListWidget>
#include "logindialog.h"

namespace Ui {
class AdmEnter;
}

class AdmEnter : public QMainWindow
{
    Q_OBJECT

public:
    explicit AdmEnter(QWidget *parent = nullptr);
    ~AdmEnter();

private slots:
    void on_table_combo_currentTextChanged(const QString &arg1);

    void on_selected_table_list_itemClicked(QListWidgetItem *item);

    void on_edit_button_clicked();

    void on_add_button_clicked();

    void on_room_computer_edit_button_clicked();

    void on_delete_button_clicked();

    void on_software_confirm_button_clicked();

    void on_room_computer_add_button_clicked();

    void on_room_computer_delete_button_clicked();

    void on_room_computer_confirm_button_clicked();

    void on_computer_current_software_delete_button_clicked();

    void on_computer_confirm_button_clicked();

    void on_actionSair_triggered();

    void autentication_handler(int result);

private:
    void autenticate();

    LoginDialog login;
    QStringList cache;
    QString selected_table;
    QListWidgetItem *clicked_item;
    Ui::AdmEnter *ui;
};

#endif // ADMENTER_H
