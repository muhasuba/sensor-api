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
    sensor = api.model('sensor', {
        'id': fields.Integer(required=True, description='sensor id'),
        'title': fields.String(required=True, description='sensor title'),
        'info': fields.String(description='sensor info'),
    })

class MeasurementDto:
    api = Namespace('measurement', description='measurement related operations')
    measurement = api.model('measurement', {
        'sensor_id': fields.Integer(required=True, description='sensor id'),
        'measurement_type_id': fields.Integer(required=True, description='measurement type id'),
        'value': fields.Float(required=True, description='numerical measurement value '),
        'recorded_on': fields.DateTime(required=True, description='timestamp measurement recorded'),
    })