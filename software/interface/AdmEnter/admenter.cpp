#include "admenter.h"
#include "ui_admenter.h"

AdmEnter::AdmEnter(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::AdmEnter)
{
    ui->setupUi(this);

    ui->software_manipulate->hide();
    ui->room_manipulate->hide();
    ui->computer_manipulate->hide();

    this->cache << "teste" << "de" << "lista" << "jaaj";
    ui->selected_table_list->addItems(cache);

    selected_table = ui->table_combo->currentText();

    connect(&login, &QDialog::finished, this, &AdmEnter::autentication_handler);
    autenticate();
}

AdmEnter::~AdmEnter()
{
    delete ui;
}

void AdmEnter::on_table_combo_currentTextChanged(const QString &arg1)
{
    selected_table = arg1;

    ui->delete_button->setEnabled(false);
    ui->edit_button->setEnabled(false);

    ui->software_manipulate->hide();
    ui->room_manipulate->hide();
    ui->computer_manipulate->hide();
}

void AdmEnter::on_selected_table_list_itemClicked(QListWidgetItem *item)
{
    if(ui->table_combo->currentText() == "Salas")
        ui->edit_button->setEnabled(true);
    else
        ui->edit_button->setEnabled(false);

    ui->delete_button->setEnabled(true);
    clicked_item = item;
}

void AdmEnter::on_edit_button_clicked()
{
    ui->software_manipulate->hide();
    ui->room_manipulate->show();
    ui->computer_manipulate->hide();

    ui->room_name_input->setText(clicked_item->text());
}

void AdmEnter::on_add_button_clicked()
{
    if(selected_table == "Softwares")
    {
        ui->software_manipulate->show();
        ui->room_manipulate->hide();
        ui->computer_manipulate->hide();
    }
    else
    {
        ui->software_manipulate->hide();
        ui->room_manipulate->show();
        ui->computer_manipulate->hide();
    }
}

void AdmEnter::on_room_computer_edit_button_clicked()
{
    ui->computer_manipulate->show();
}

void AdmEnter::on_delete_button_clicked()
{

}

void AdmEnter::on_software_confirm_button_clicked()
{

}

void AdmEnter::on_room_computer_add_button_clicked()
{

}

void AdmEnter::on_room_computer_delete_button_clicked()
{

}

void AdmEnter::on_room_computer_confirm_button_clicked()
{

}

void AdmEnter::on_computer_current_software_delete_button_clicked()
{

}

void AdmEnter::on_computer_confirm_button_clicked()
{

}

void AdmEnter::autenticate(){
   login.open();

}

void AdmEnter::autentication_handler(int result){
    if(result)
        setEnabled(true);
    else
        close();

}

void AdmEnter::on_actionSair_triggered()
{
    autenticate();
}
