import uuid
import datetime

from app.main import db
from app.main.model.sensor import Sensor
from typing import Dict, Tuple


def save_new_sensor(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    sensor = Sensor.query.filter_by(title=data['title']).first()
    if not sensor:
        try:
            new_sensor = Sensor(
                title=data['title'],
                info=data['info'],
                last_update=datetime.datetime.utcnow()
            )
            db.session.add(new_sensor)
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


def delete_a_sensor(sensor_id):
    try:
        Sensor.query.filter_by(id=sensor_id).delete()
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.',
        }
        return response_object, 200
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 400


def update_a_sensor(data: Dict[str, str], sensor_to_update: Sensor) -> Tuple[Dict[str, str], int]:
    sensor = Sensor.query.filter_by(title=data['title']).first()
    if not sensor:
        try:
            sensor_to_update.title=data['title']
            sensor_to_update.info=data['info']
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully updated.',
            }
            return response_object, 200
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return response_object, 400
    else:
        response_object = {
            'status': 'fail',
            'message': 'Sensor already exists.',
        }
        return response_object, 409
