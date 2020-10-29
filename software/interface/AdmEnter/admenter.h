#ifndef ADMENTER_H
#define ADMENTER_H

#include <QMainWindow>
#include <QStringList>
#include <QListWidget>

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

    void on_sala_computer_add_clicked();

private:
    QStringList cache;
    QString selected_table;
    QListWidgetItem *clicked_item;
    Ui::AdmEnter *ui;
};

#endif // ADMENTER_H
