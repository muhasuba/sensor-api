import uuid
import datetime
import pandas as pd

from app.main import db
from app.main.model.measurement import Measurement
from typing import Dict, List, Tuple
from dateutil import parser


def save_new_measurement(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    try:
        timestamp_now = datetime.datetime.utcnow()
        timestamp_utc = parser.parse(data['timestamp_utc'])
        new_measurement = Measurement(
            sensor_id=data['sensor_id'],
            measurement_type_id=data['measurement_type_id'],
            value=data['value'],
            timestamp_utc=timestamp_utc,
            recorded_on=timestamp_now
        )
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
        query = query.order_by(Measurement.timestamp_utc.desc())
    else:
        query = query.order_by(Measurement.timestamp_utc.asc())

    result = query.limit(limit).all()
    return result


def get_measurement_aggregate(args: Dict) -> Dict:
    sensor_id, measurement_type_id, start_time, end_time, time_split = args['sensor_id'], args[
        'measurement_type_id'], args['start_time'], args['end_time'], args['time_split']

    start_time = parser.parse(start_time)
    end_time = parser.parse(end_time)

    query = Measurement.query.with_entities(
        Measurement.timestamp_utc, Measurement.value)
    query = query.filter(Measurement.sensor_id == sensor_id, Measurement.measurement_type_id ==
                         measurement_type_id, Measurement.timestamp_utc >= start_time, Measurement.timestamp_utc <= end_time)

    list_time = []
    list_min_value = []
    list_max_value = []
    list_mean_value = []
    query_result = query.all()
    if query_result:
        time_split = time_split if time_split == '15min' else '1h'
        df = pd.DataFrame(query_result)
        df = df.groupby(pd.Grouper(key='timestamp_utc', freq=time_split)).agg(
            ['min', 'max', 'mean'])
        list_min_value = df[('value',  'min')]
        list_max_value = df[('value',  'max')]
        list_mean_value = df[('value',  'mean')]
        list_time = df.index

    result = dict(
        start_time=start_time,
        end_time=end_time,
        sensor_id=sensor_id,
        measurement_type_id=measurement_type_id,
        time_split=time_split,
        list_time=list_time,
        list_min_value=list_min_value,
        list_max_value=list_max_value,
        list_mean_value=list_mean_value
    )

    return result
