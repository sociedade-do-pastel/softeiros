#include "clienter.h"
#include "ui_clienter.h"

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

    software_items_list.push_back(new QListWidgetItem("teste"));
    software_items_list.push_back(new QListWidgetItem("teste2"));
    software_items_list.push_back(new QListWidgetItem("teste3"));
    software_items_list.push_back(new QListWidgetItem("teste4"));
    software_items_list.push_back(new QListWidgetItem("teste5"));

    setSoftwareListProperties();
    setRoomList();
    setRoomMap();
}

void CliEnter::setRoomList(){
    room_widgets_list.push_back(new RoomWidget("K301", "7h10", 15, 30));
    room_widgets_list.push_back(new RoomWidget("K305", "8h10", 13, 30));
    room_widgets_list.push_back(new RoomWidget("K307", "9h10", 30, 30));

    for(auto &x : room_widgets_list){
        room_list->addWidget(x);
        connect(x, &RoomWidget::mouseReleased, this, &CliEnter::roomClicked);
    }
}

void CliEnter::setSoftwareListProperties(){

    for(auto &x : software_items_list){
        ui->software_list->addItem(x);
        x->setFlags(x->flags() | Qt::ItemIsUserCheckable);
        x->setCheckState(Qt::Unchecked);
    }

    connect(ui->software_list, &QListWidget::itemChanged, this,
            &CliEnter::softwareAreaCheckActions);
}

void CliEnter::softwareAreaCheckActions(QListWidgetItem* item){
    if(item->checkState() == Qt::Checked)
        QMessageBox::about(this, "Info", item->text() + " clicado");
    else
        QMessageBox::about(this, "Info", item->text() + " desclicado");
}

CliEnter::~CliEnter()
{
    delete ui;
}

void CliEnter::on_software_list_clear_button_clicked()
{
    for(int i = 0; i < ui->software_list->count(); ++i)
        ui->software_list->item(i)->setCheckState(Qt::Unchecked);
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
    int altura{5}, largura{5};

    for(int i{0}; i < altura; i++){
        for(int j{0}; j < largura; j++){
            QLabel* icon = new QLabel();
            QPixmap map = QPixmap(":/icons/imgs/pcMapVerde.png");
            icon->setMargin(25);
            icon->setScaledContents(true);
            icon->setPixmap(map.scaled(icon->width()/5, icon->height()/5, Qt::KeepAspectRatioByExpanding));
            computer_grid->addWidget(icon, i, j);
        }
    }
}
