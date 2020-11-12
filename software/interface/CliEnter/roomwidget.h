#ifndef ROOMWIDGET_H
#define ROOMWIDGET_H

#include <QWidget>
#include <QPixmap>
#include <QString>

namespace Ui {
class RoomWidget;
}

class RoomWidget : public QWidget
{
    Q_OBJECT

signals:
    void mouseReleased(RoomWidget *r);

public:
    explicit RoomWidget(QString name, QString close_Time, int qts, int qt_max, QWidget *parent = nullptr);
    ~RoomWidget();
    QString getRoom_name();

protected:
    protected: virtual void mouseReleaseEvent ( QMouseEvent * event );

private:
    Ui::RoomWidget *ui;
    QPixmap icon_image;
    QString room_name;
    QString close_time;
    int qt_pc;
    int qt_max_pc;

    void updateLabels();
    void setIcon();
};

#endif // ROOMWIDGET_H
