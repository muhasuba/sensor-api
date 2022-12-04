from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


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
        'value': fields.Float(required=True, description='numerical measurement value ')
    })
    measurement_response = api.inherit('measurement_response', measurement_payload, {
        'recorded_on': fields.DateTime(required=True, description='timestamp measurement recorded')
    })
