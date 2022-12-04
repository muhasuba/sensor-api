from flask import request
from flask_restx import Resource, reqparse

from ..util.dto import MeasurementDto
from ..service.measurement_service import save_new_measurement, get_all_measurements
from typing import Dict, Tuple

api = MeasurementDto.api
_measurement_payload = MeasurementDto.measurement_payload
_measurement_response = MeasurementDto.measurement_response


@api.route('/')
class MeasurementList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sensor_id', type=int, help="filter sensor id")
    parser.add_argument('measurement_type_id', type=int, help="filter measurement type id")
    parser.add_argument('limit', type=int, help="limit size measurement list", default=2)
    parser.add_argument('order_type', type=str, help="order by recoded time, type order 'asc' or 'desc', default ascending", default='asc')

    @api.doc('list_of_measurements', parser=parser)
    @api.marshal_list_with(_measurement_response, envelope='data')
    def get(self):
        """List all registered measurements"""
        args = self.parser.parse_args()
        return get_all_measurements(args)

    @api.expect(_measurement_payload, validate=True)
    @api.response(201, 'Measurement successfully created.')
    @api.doc('create a new measurement')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new measurement"""
        data = request.json
        return save_new_measurement(data=data)
