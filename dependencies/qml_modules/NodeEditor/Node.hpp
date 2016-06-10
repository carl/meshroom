#pragma once

#include <QObject>
#include "AttributeModel.hpp"

namespace nodeeditor
{

class Node : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString name READ name CONSTANT)
    Q_PROPERTY(QString type READ type CONSTANT)
    Q_PROPERTY(AttributeModel* inputs READ inputs CONSTANT)
    Q_PROPERTY(AttributeModel* outputs READ outputs CONSTANT)
    Q_PROPERTY(Status status READ status WRITE setStatus NOTIFY statusChanged)
    Q_PROPERTY(int x READ x WRITE setX NOTIFY xChanged)
    Q_PROPERTY(int y READ y WRITE setY NOTIFY yChanged)

public:
    enum Status
    {
        READY = 0,
        WAITING,
        RUNNING,
        ERROR,
        DONE
    };
    Q_ENUMS(Status)

public:
    Node() = default;
    Node(const Node& obj) = delete;
    Node& operator=(Node const&) = delete;

public:
    const QString& name() const { return _name; }
    const QString& type() const { return _type; }
    AttributeModel* inputs() const { return _inputs; }
    AttributeModel* outputs() const { return _outputs; }
    Status status() const { return _status; }
    int x() const { return _x; }
    int y() const { return _y; }
    void setStatus(Status);
    void setX(int);
    void setY(int);

public:
    QJsonObject serializeToJSON() const;
    void deserializeFromJSON(const QJsonObject& obj);

public:
    Q_SIGNAL void statusChanged();
    Q_SIGNAL void xChanged();
    Q_SIGNAL void yChanged();

private:
    QString _name = "unknown";
    QString _type = "Unknown";
    AttributeModel* _inputs = new AttributeModel(this);
    AttributeModel* _outputs = new AttributeModel(this);
    Status _status = READY;
    int _x = 10;
    int _y = 10;
};

} // namespace