
from .. import db


class Measurement(db.Model):
    """ Measurement Model for storing measurement related details """
    __tablename__ = "measurement"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sensor_id = db.Column(db.Integer, nullable=False)
    measurement_type_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=True)
    recorded_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<Measurement '{}'>".format(self.title)
