#ifndef ROOMWIDGET_H
#define ROOMWIDGET_H

#include <QWidget>
#include <QPixmap>
#include <QString>
#include <string>
#include <vector>

namespace Ui {
class RoomWidget;
}

class RoomWidget : public QWidget
{
    Q_OBJECT

signals:
    void mouseReleased(RoomWidget *r);

public:
    explicit RoomWidget(QString name, QString close_Time, int qts, int qt_max, std::vector<std::string> s, QWidget *parent = nullptr);
    ~RoomWidget();
    QString getRoom_name();
    int getQt_pc();
    int getQt_max_pc();
    bool getMatchPCQt();
    bool getMatchSoftwares();
    void setMatchPCQt(bool n);
    void setMatchSoftwares(bool n);
    bool hasSoftware(std::string s);

protected:
    protected: virtual void mouseReleaseEvent ( QMouseEvent * event );

private:
    Ui::RoomWidget *ui;
    QPixmap icon_image;
    QString room_name;
    QString close_time;
    std::vector<std::string> software_list;
    int qt_pc;
    int qt_max_pc;
    bool matchPCQt;
    bool matchSoftwares;

    void updateLabels();
    void setIcon();
};

#endif // ROOMWIDGET_H
