#include "clienter.h"
#include "ui_clienter.h"
#include <iostream>

CliEnter::CliEnter(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::cliEnter)
{
    ui->setupUi(this);

    room_list = new QVBoxLayout();
    ui->salasAreaContents->setLayout(room_list);

    computer_grid = new QGridLayout();
    ui->computer_area->setLayout(computer_grid);

    QPixmap green_pc = QPixmap(":/icons/imgs/pcMapVerde.png");
    QPixmap red_pc = QPixmap(":/icons/imgs/pcMapVermelho.png");

    ui->green_pc_legend->setPixmap(green_pc.scaled(20,15));
    ui->red_pc_legend->setPixmap(red_pc.scaled(20,15));

    selected_room = nullptr;

    dbInfo = controler.getInfo();

    setRoomList();
    setSoftwareListProperties();
}

void CliEnter::setRoomList(){
    for (const auto &x : dbInfo.items()){
        int qtLugares{0};

        QString qsala = x.key().data();
        string qhora = dbInfo[qsala.toStdString()]["hora_fechamento"];

        for (auto &y : dbInfo[qsala.toStdString()]["lista_computadores"])
            qtLugares++;

        for (auto &y : dbInfo[qsala.toStdString()]["lista_softwares"].get<std::vector<string>>())
            software_json[y] = 0;

        room_widgets_list.push_back(new RoomWidget(x.key().data(), QString::fromStdString(qhora), 0, qtLugares,
                                                   dbInfo[qsala.toStdString()]["lista_softwares"].get<std::vector<string>>()));
    }

    for(auto &x : room_widgets_list){
        room_list->addWidget(x);
        connect(x, &RoomWidget::mouseReleased, this, &CliEnter::roomClicked);
    }
}

void CliEnter::setSoftwareListProperties(){
    for (auto &y : software_json.items())
        software_items_list.push_back(new QListWidgetItem(QString::fromStdString(y.key().data())));

    for (auto &x : software_items_list){
        ui->software_list->addItem(x);
        x->setFlags(x->flags() | Qt::ItemIsUserCheckable);
        x->setCheckState(Qt::Unchecked);
    }

    connect(ui->software_list, &QListWidget::itemChanged, this,
            &CliEnter::softwareAreaCheckActions);
}

void CliEnter::softwareAreaCheckActions(QListWidgetItem* item){
    for (auto &x : room_widgets_list) {
        x->setMatchSoftwares(true);
        for (auto &y : software_items_list) {
            if (y->checkState() == Qt::Checked)
                if (!x->hasSoftware(y->text().toStdString()))
                    x->setMatchSoftwares(false);
      }
  }
  sortRooms();
}

CliEnter::~CliEnter()
{
    delete ui;
}

void CliEnter::on_software_list_clear_button_clicked()
{
    for(int i = 0; i < ui->software_list->count(); ++i)
        ui->software_list->item(i)->setCheckState(Qt::Unchecked);
    for (auto &x : room_widgets_list)
        x->setMatchSoftwares(true);
}

void CliEnter::on_computer_qt_clear_button_clicked()
{
    ui->computer_qt_disp_input->setValue(1);
}

void CliEnter::roomClicked(RoomWidget *r)
{
    if(selected_room)
        selected_room->setEnabled(true);
    selected_room = r;
    r->setEnabled(false);

    ui->room_map_group->setTitle("Mapa da Sala <" + r->getRoom_name() + ">");
    setRoomMap();
}

void CliEnter::setRoomMap()
{
    QLayoutItem* item;
    while ( ( item = computer_grid->layout()->takeAt( 0 ) ) != NULL )
    {
        delete item->widget();
        delete item;
    }

    for (auto &x : dbInfo[selected_room->getRoom_name().toStdString()]["lista_computadores"]) {
        QLabel* icon = new QLabel();
        QPixmap map;
        if (x["em_uso"])
            map = QPixmap(":/icons/imgs/pcMapVermelho.png");
        else
            map = QPixmap(":/icons/imgs/pcMapVerde.png");
        icon->setMargin(25);
        icon->setScaledContents(true);
        icon->setPixmap(map.scaled(icon->width()/5, icon->height()/5, Qt::KeepAspectRatioByExpanding));
        computer_grid->addWidget(icon, int(x["pos_x"])-1, int(x["pos_y"])-1);
    }

    for (int x{0}; x<computer_grid->columnCount(); ++x)
        computer_grid->setColumnStretch(x, 1);

    for (int y{0}; y<computer_grid->rowCount(); ++y)
        computer_grid->setRowStretch(y, 1);
}

void CliEnter::on_computer_qt_disp_input_valueChanged(int arg1)
{
    for (auto &x : room_widgets_list) {
        if (x->getQt_max_pc() - x->getQt_pc() < arg1)
            x->setMatchPCQt(false);
        else
            x->setMatchPCQt(true);
    }
    sortRooms();
}

void CliEnter::sortRooms()
{
    for (auto x : room_widgets_list) {
        if (x->getMatchPCQt() && x->getMatchSoftwares())
            x->setVisible(true);
        else
            x->setVisible(false);
    }
}

void CliEnter::on_actionRefresh_triggered()
{
    selected_room = nullptr;

    for (auto &item : software_items_list)
        delete item;

    software_items_list = {};
    ui->software_list->clear();

    room_widgets_list = {};
    QLayoutItem* item;
    while ( ( item = room_list->takeAt( 0 ) ) != NULL )
    {
        delete item->widget();
        delete item;
    }

    dbInfo = controler.getInfo();

    setRoomList();
    setSoftwareListProperties();
}
