#include "roomwidget.h"
#include "ui_roomwidget.h"

RoomWidget::RoomWidget(QString room_name, QString close_time, int qt_pc, int qt_max_pc, std::vector<std::string> s, QWidget *parent) :
    QWidget(parent),
    ui(new Ui::RoomWidget)
{
    ui->setupUi(this);
    this->room_name = room_name;
    this->close_time = close_time;
    this->qt_pc = qt_pc;
    this->qt_max_pc = qt_max_pc;
    software_list = s;

    matchPCQt = true;
    matchSoftwares = true;

    updateLabels();
}

RoomWidget::~RoomWidget()
{
    delete ui;
}

void RoomWidget::updateLabels()
{
    ui->room_name->setText(room_name);
    ui->room_fullness->setText("Lugares: "+QString::number(qt_pc)+"/"+QString::number(qt_max_pc));
    ui->room_closure_time->setText("Fechamento: " + close_time);
    setIcon();
}

void RoomWidget::setIcon()
{
    float fracFull = float(qt_pc)/float(qt_max_pc);

    if(fracFull == 1)
        icon_image = QPixmap(":/icons/imgs/pcVermelho.png");
    else if(fracFull < 0.5)
        icon_image = QPixmap(":/icons/imgs/pcVerde.png");
    else
        icon_image = QPixmap(":/icons/imgs/pcAmarelo.png");

    ui->room_fullness_icon->setPixmap(icon_image.scaled(80, 80, Qt::KeepAspectRatio));
}

QString RoomWidget::getRoom_name()
{
    return room_name;
}

int RoomWidget::getQt_pc()
{
    return qt_pc;
}

int RoomWidget::getQt_max_pc()
{
    return qt_max_pc;
}

bool RoomWidget::getMatchPCQt()
{
    return matchPCQt;
}

bool RoomWidget::getMatchSoftwares()
{
    return matchSoftwares;
}

void RoomWidget::setMatchPCQt(bool n)
{
    matchPCQt = n;
}

void RoomWidget::setMatchSoftwares(bool n)
{
    matchSoftwares = n;
}

void RoomWidget::mouseReleaseEvent (QMouseEvent * event)
{
    QWidget::mouseReleaseEvent(event);
    emit mouseReleased(this);
}

bool RoomWidget::hasSoftware(std::string s)
{
    for (auto &x : software_list){
        if (x == s)
            return true;
    }
    return false;
}
