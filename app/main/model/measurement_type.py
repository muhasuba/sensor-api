
from .. import db


class MeasurementType(db.Model):
    """ MeasurementType Model for storing measurement type related details """
    __tablename__ = "measurement_type"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    info = db.Column(db.String(250))
    last_update = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<MeasurementType id {self.id} title {self.title}>"
