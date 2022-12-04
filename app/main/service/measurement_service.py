import uuid
import datetime

from app.main import db
from app.main.model.measurement import Measurement
from typing import Dict, List, Tuple


def save_new_measurement(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    try:
        new_measurement = Measurement(
            sensor_id=data['sensor_id'],
            measurement_type_id=data['measurement_type_id'],
            value=data['value'],
            recorded_on=datetime.datetime.utcnow()
        )
        # return save_changes(new_measurement)
        db.session.add(new_measurement)
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


def get_all_measurements(args: Dict) -> List:
    sensor_id, measurement_type_id, order_type, limit = args['sensor_id'], args[
        'measurement_type_id'], args['order_type'], args['limit']

    if sensor_id and measurement_type_id:
        query = Measurement.query.filter(
            Measurement.sensor_id == sensor_id, Measurement.measurement_type_id == measurement_type_id)
    elif sensor_id:
        query = Measurement.query.filter(Measurement.sensor_id == sensor_id)
    elif measurement_type_id:
        query = Measurement.query.filter(
            Measurement.measurement_type_id == measurement_type_id)
    else:
        query = Measurement.query

    if order_type == 'desc':
        query = query.order_by(Measurement.recorded_on.desc())
    else:
        query = query.order_by(Measurement.recorded_on.asc())

    result = query.limit(args['limit']).all()
    return result
