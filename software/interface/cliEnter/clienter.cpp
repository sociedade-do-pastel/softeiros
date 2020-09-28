#include "clienter.h"
#include "ui_clienter.h"
#include <QMessageBox>

cliEnter::cliEnter(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::cliEnter)
{
    ui->setupUi(this);
    this->setSoftwareListProperties();
}

void cliEnter::setSoftwareListProperties(){
    QStringList list;
    list << "teste" << "Clone Cartão";

    ui->softwareArea->addItems(list);

    QListWidgetItem* item = 0;
    for(int i = 0; i < ui->softwareArea->count(); ++i){
        item = ui->softwareArea->item(i);
        item->setFlags(item->flags() | Qt::ItemIsUserCheckable);
        item->setCheckState(Qt::Unchecked);
    }

    QObject::connect(ui->softwareArea, SIGNAL(itemChanged(QListWidgetItem*)),
                     this, SLOT(softwareAreaCheckActions(QListWidgetItem*)));
}

void cliEnter::softwareAreaCheckActions(QListWidgetItem* item){
    if(item->checkState() == Qt::Checked)
        QMessageBox::about(this, "Info", item->text() + " clicado");
    else
        QMessageBox::about(this, "Info", item->text() + " desclicado");
}

cliEnter::~cliEnter()
{
    delete ui;
}

void cliEnter::on_clearQt_clicked()
{
    ui->qtDispFilter->setValue(1);
}

void cliEnter::on_pushButton_clicked()
{
    QListWidgetItem* item = 0;
    for(int i = 0; i < ui->softwareArea->count(); ++i){
        item = ui->softwareArea->item(i);
        item->setCheckState(Qt::Unchecked);
    }
}
