#include "logindialog.h"
#include "ui_logindialog.h"

LoginDialog::LoginDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::LoginDialog)
{
    ui->setupUi(this);
}

LoginDialog::~LoginDialog()
{
    delete ui;
}

void LoginDialog::on_login_button_clicked()
{
    QDialog::accept();
}

void LoginDialog::on_cancel_button_clicked()
{
    QDialog::reject();

}
