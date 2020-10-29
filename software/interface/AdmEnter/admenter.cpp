#include "admenter.h"
#include "ui_admenter.h"
#include <iostream>

AdmEnter::AdmEnter(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::AdmEnter)
{
    ui->setupUi(this);

    ui->software_add->hide();
    ui->sala_manipulate->hide();
    ui->computer_manipulate->hide();

    this->cache << "teste" << "de" << "lista" << "jaaj";
    ui->selected_table_list->addItems(cache);

    selected_table = ui->table_combo->currentText();
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

    ui->software_add->hide();
    ui->sala_manipulate->hide();
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
    ui->software_add->hide();
    ui->sala_manipulate->show();
    ui->computer_manipulate->hide();

    ui->sala_name->setText(clicked_item->text());
}

void AdmEnter::on_add_button_clicked()
{
    if(selected_table == "Softwares")
    {
        ui->software_add->show();
        ui->sala_manipulate->hide();
        ui->computer_manipulate->hide();
    }
    else
    {
        ui->software_add->hide();
        ui->sala_manipulate->show();
        ui->computer_manipulate->hide();
    }

}

void AdmEnter::on_sala_computer_add_clicked()
{
    ui->computer_manipulate->show();

}
