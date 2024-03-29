
from .. import db


class Sensor(db.Model):
    """ Sensor Model for storing sensor related details """
    __tablename__ = "sensor"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    info = db.Column(db.String(250))
    last_update = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Sensor id {self.id} title {self.title}>"
