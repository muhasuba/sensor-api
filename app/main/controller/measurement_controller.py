from flask import request
from flask_restx import Resource, reqparse

from ..util.dto import MeasurementDto
from ..service.measurement_service import save_new_measurement, get_all_measurements, get_measurement_aggregate
from typing import Dict, Tuple

api = MeasurementDto.api
_measurement_payload = MeasurementDto.measurement_payload
_measurement_response = MeasurementDto.measurement_response
_measurement_aggregate = MeasurementDto.measurement_aggregate


@api.route('/')
class MeasurementList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sensor_id', type=int, help="filter sensor id")
    parser.add_argument('measurement_type_id', type=int, help="filter measurement type id")
    parser.add_argument('limit', type=int, help="limit size measurement list", default=5)
    parser.add_argument('order_type', type=str, help="order by timestamp_utc, type order 'asc' or 'desc', default ascending", default='asc')

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
        

@api.route('/aggregate')
class MeasurementAggregate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sensor_id', type=int, help="filter sensor id")
    parser.add_argument('measurement_type_id', type=int, help="filter measurement type id")
    parser.add_argument('start_time', type=str, help="the start of time-frame for which the aggregates are to be returned")
    parser.add_argument('end_time', type=str, help="the end of time-frame for which the aggregates are to be returned")
    parser.add_argument('time_split', type=str, help="options time split mode of aggregate '1h' (default) or '15min', if not valid will back to default")

    @api.doc('get a measurement aggregate', parser=parser)
    @api.marshal_with(_measurement_aggregate)
    def get(self):
        """Get a measurement aggregate"""
        args = self.parser.parse_args()
        return get_measurement_aggregate(args)