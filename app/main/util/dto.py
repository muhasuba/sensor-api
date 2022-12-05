from xmlrpc.client import DateTime
from flask_restx import Namespace, fields


class SensorDto:
    api = Namespace('sensor', description='sensor related operations')
    sensor_payload = api.model('sensor_payload', {
        'title': fields.String(required=True, description='sensor title'),
        'info': fields.String(description='sensor info')
    })
    sensor_response = api.inherit('sensor_response', sensor_payload, {
        'id': fields.Integer(required=True, description='sensor id')
    })


class MeasurementTypeDto:
    api = Namespace(
        'measurement_type', description='measurement type related operations')
    measurement_type_payload = api.model('measurement_type_payload', {
        'title': fields.String(required=True, description='measurement type title'),
        'info': fields.String(description='measurement type info')
    })
    measurement_type_response = api.inherit('measurement_type_response', measurement_type_payload, {
        'id': fields.Integer(required=True, description='measurement type id')
    })


class MeasurementDto:
    api = Namespace(
        'measurement', description='measurement related operations')
    measurement_payload = api.model('measurement_payload', {
        'sensor_id': fields.Integer(required=True, description='sensor id'),
        'measurement_type_id': fields.Integer(required=True, description='measurement type id'),
        'value': fields.Float(required=True, description='numerical measurement value '),
        'timestamp_utc': fields.DateTime(required=True, description='timestamp data UTC, if empty default timestamp now')
    })
    measurement_response = api.inherit('measurement_response', measurement_payload, {
        'recorded_on': fields.DateTime(required=True, description='timestamp measurement recorded')
    })
    measurement_aggregate = api.model('measurement_aggregate', {
        'start_time': fields.DateTime(required=False, description='the start of time-frame for which the aggregates are to be returned'),
        'end_time': fields.DateTime(required=False, description='the end of time-frame for which the aggregates are to be returned'),
        'sensor_id': fields.Integer(required=True, description='sensor id'),
        'measurement_type_id': fields.Integer(required=True, description='measurement type id'),
        'time_split': fields.String(required=True, description='options time split mode of aggregate "1h" (default) or "5min", if not valid will back to default'),
        'list_time': fields.List(fields.DateTime(), required=True, description='list of time point in time range and split'),
        'list_min_value': fields.List(fields.Float(), required=True, description='list of min value associate index with with list time'),
        'list_max_value': fields.List(fields.Float(), required=True, description='list of max value associate index with with list time'),
        'list_mean_value': fields.List(fields.Float(), required=True, description='list of mean value associate index with with list time'),
    })