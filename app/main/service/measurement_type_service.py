import uuid
import datetime

from app.main import db
from app.main.model.measurement_type import MeasurementType
from typing import Dict, Tuple


def save_new_measurement_type(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    measurement_type = MeasurementType.query.filter_by(title=data['title']).first()
    if not measurement_type:
        new_measurement_type = MeasurementType(
            title=data['title'],
            info=data['info'],
            last_update=datetime.datetime.utcnow()
        )
        return save_changes(new_measurement_type)
    else:
        response_object = {
            'status': 'fail',
            'message': 'Measurement type already exists. Please Log in.',
        }
        return response_object, 409


def get_all_measurement_types():
    return MeasurementType.query.all()


def get_a_measurement_type(measurement_type_id):
    return MeasurementType.query.filter_by(id=measurement_type_id).first()


def save_changes(data: MeasurementType) -> None:
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
