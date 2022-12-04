from flask import request
from flask_restx import Resource

from ..util.dto import SensorDto
from ..service.sensor_service import save_new_sensor, get_all_sensors, get_a_sensor
from typing import Dict, Tuple

api = SensorDto.api
_sensor = SensorDto.sensor


@api.route('/')
class SensorList(Resource):
    @api.doc('list_of_sensors')
    @api.marshal_list_with(_sensor, envelope='data')
    def get(self):
        """List all registered sensors"""
        return get_all_sensors()

    @api.expect(_sensor, validate=True)
    @api.response(201, 'Sensor successfully created.')
    @api.doc('create a new sensor')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new Sensor """
        data = request.json
        return save_new_sensor(data=data)


@api.route('/<sensor_id>')
@api.param('sensor_id', 'The Sensor identifier')
@api.response(404, 'Sensor not found.')
class Sensor(Resource):
    @api.doc('get a sensor')
    @api.marshal_with(_sensor)
    def get(self, sensor_id):
        """get a sensor given its identifier"""
        sensor = get_a_sensor(sensor_id)
        if not sensor:
            api.abort(404)
        else:
            return sensor



