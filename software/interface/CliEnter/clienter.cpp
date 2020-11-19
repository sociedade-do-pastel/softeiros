#include "clienter.h"
#include "ui_clienter.h"
#include <iostream>

CliEnter::CliEnter(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::cliEnter)
{
    ui->setupUi(this);

	// layout for room widgets
    room_list = new QVBoxLayout(); 
    ui->salasAreaContents->setLayout(room_list);

	// layout for room map
    computer_grid = new QGridLayout();
    ui->computer_area->setLayout(computer_grid);

	// icons that will be used in the room map
    QPixmap green_pc = QPixmap(":/icons/imgs/pcMapVerde.png");
    QPixmap red_pc = QPixmap(":/icons/imgs/pcMapVermelho.png");

    ui->green_pc_legend->setPixmap(green_pc.scaled(20,15));
    ui->red_pc_legend->setPixmap(red_pc.scaled(20,15));

	// this variable will carry the current clicked room
    selected_room = nullptr;

	// sync and get the info from the server
    dbInfo = controler.getInfo();

    setRoomList();
    setSoftwareListProperties();
}

void CliEnter::setRoomList(){
	// access the server data with a key : value format
    for (const auto &x : dbInfo.items()){
        int qtLugares{0};		// counter for the amount of PCs

        QString qsala = x.key().data(); // get the key name
        string qhora = dbInfo[qsala.toStdString()]["hora_fechamento"]; // get the close time

		// count the amount of PCs
        for (auto &y : dbInfo[qsala.toStdString()]["lista_computadores"])
            qtLugares++;

		// get the software name iterating as vector, uses a JSON to store by key and make unique
        for (auto &y : dbInfo[qsala.toStdString()]["lista_softwares"].get<std::vector<string>>())
            software_json[y] = 0;

		// make the room widgets
        room_widgets_list.push_back(new RoomWidget(x.key().data(), QString::fromStdString(qhora), 0, qtLugares,
                                                   dbInfo[qsala.toStdString()]["lista_softwares"].get<std::vector<string>>()));
    }

	// add the items to the layout and bind the functions
    for(auto &x : room_widgets_list){
        room_list->addWidget(x);
        connect(x, &RoomWidget::mouseReleased, this, &CliEnter::roomClicked);
    }
}

void CliEnter::setSoftwareListProperties(){
	// iterate the software_json to get the software names and place in the software list
    for (auto &y : software_json.items())
        software_items_list.push_back(new QListWidgetItem(QString::fromStdString(y.key().data())));

	// add the list to the UI and make the proper config
    for (auto &x : software_items_list){
        ui->software_list->addItem(x);
        x->setFlags(x->flags() | Qt::ItemIsUserCheckable); // make checkable
        x->setCheckState(Qt::Unchecked);				   // default unchecked
    }

	// bind the items to their actions
    connect(ui->software_list, &QListWidget::itemChanged, this,
            &CliEnter::softwareAreaCheckActions);
}

void CliEnter::softwareAreaCheckActions(QListWidgetItem* item){
    for (auto &x : room_widgets_list) {	                       // iterate all room widgets
        x->setMatchSoftwares(true);                            // make defaullt matching
        for (auto &y : software_items_list) {                  // iterate software list 
            if (y->checkState() == Qt::Checked)				   // get the checked softwares
                if (!x->hasSoftware(y->text().toStdString()))  // if widget don't have a checked software
                    x->setMatchSoftwares(false);			   // make matching false
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
	/*  
	 * iterate the software list, uncheck
	 * and make all match softwares to true
	 */ 
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
    if(selected_room)			         // if has previous selected software
        selected_room->setEnabled(true); // make it enabled
    selected_room = r;					 // attribute the current to the selected
    r->setEnabled(false);				 // disable it to highlight

    ui->room_map_group->setTitle("Mapa da Sala <" + r->getRoom_name() + ">");
    setRoomMap();
}

void CliEnter::setRoomMap()
{
	// clear all widgets in room map
    QLayoutItem* item;
    while ( ( item = computer_grid->layout()->takeAt( 0 ) ) != NULL )
    {
        delete item->widget();
        delete item;
    }

	// iterate all PCs in selected room
    for (auto &x : dbInfo[selected_room->getRoom_name().toStdString()]["lista_computadores"]) {
        QLabel* icon = new QLabel(); // make the label
        QPixmap map;				 // attribute an icon to the label
        if (x["em_uso"])
            map = QPixmap(":/icons/imgs/pcMapVermelho.png");
        else
            map = QPixmap(":/icons/imgs/pcMapVerde.png");

		// attributes settings
        icon->setMargin(25);
        icon->setScaledContents(true);
        icon->setPixmap(map.scaled(icon->width()/5, icon->height()/5, Qt::KeepAspectRatioByExpanding));
        computer_grid->addWidget(icon, int(x["pos_x"])-1, int(x["pos_y"])-1); // att to respective position
    }

	// adjust column stretch
    for (int x{0}; x<computer_grid->columnCount(); ++x)
        computer_grid->setColumnStretch(x, 1);

	// adjust row stretch
    for (int y{0}; y<computer_grid->rowCount(); ++y)
        computer_grid->setRowStretch(y, 1);
}

void CliEnter::on_computer_qt_disp_input_valueChanged(int arg1)
{
	// check if the avaliable amount of free PCs match the
	// inputed amount and then mark it as matching true
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
	// if match both softwares and avaliable places, make visible
	// else make invisible
    for (auto x : room_widgets_list) {
        if (x->getMatchPCQt() && x->getMatchSoftwares())
            x->setVisible(true);
        else
            x->setVisible(false);
    }
}

void CliEnter::on_actionRefresh_triggered()
{
	// reset the variables
	// delete dynamic elements
    selected_room = nullptr;

    for (auto &item : software_items_list)
        delete item;

    software_items_list = {};
    ui->software_list->clear();
	software_json.clear();

    room_widgets_list = {};
    QLayoutItem* item;
    while ( ( item = room_list->takeAt( 0 ) ) != NULL )
    {
        delete item->widget();
        delete item;
    }

	// get new info from the server
    dbInfo = controler.getInfo();

	// redo the initial config
    setRoomList();
    setSoftwareListProperties();
}
