import uuid
import datetime

from app.main import db
from app.main.model.sensor import Sensor
from typing import Dict, Tuple


def save_new_sensor(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    sensor = Sensor.query.filter_by(title=data['title']).first()
    if not sensor:
        new_sensor = Sensor(
            title=data['title'],
            info=data['info'],
            last_update=datetime.datetime.utcnow()
        )
        return save_changes(new_sensor)
    else:
        response_object = {
            'status': 'fail',
            'message': 'Sensor already exists.',
        }
        return response_object, 409


def get_all_sensors():
    return Sensor.query.all()


def get_a_sensor(sensor_id):
    return Sensor.query.filter_by(id=sensor_id).first()


def save_changes(data: Sensor) -> None:
    try:
        db.session.add(data)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully created.',
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 400
