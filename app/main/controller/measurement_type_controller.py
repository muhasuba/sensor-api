from flask import request
from flask_restx import Resource

from ..util.dto import MeasurementTypeDto
from ..service.measurement_type_service import save_new_measurement_type, get_all_measurement_types, get_a_measurement_type
from typing import Dict, Tuple

api = MeasurementTypeDto.api
_measurement_type_payload = MeasurementTypeDto.measurement_type_payload
_measurement_type_response = MeasurementTypeDto.measurement_type_response


@api.route('/')
class MeasurementTypeList(Resource):
    @api.doc('list_of_measurement_types')
    @api.marshal_list_with(_measurement_type_response, envelope='data')
    def get(self):
        """List all registered measurement types"""
        return get_all_measurement_types()

    @api.expect(_measurement_type_payload, validate=True)
    @api.response(201, 'Measurement type successfully created.')
    @api.doc('create a new measurement type')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new measurement type """
        data = request.json
        return save_new_measurement_type(data=data)


@api.route('/<measurement_type_id>')
@api.param('measurement_type_id', 'The measurement type identifier')
@api.response(404, 'Measurement type not found.')
class MeasurementType(Resource):
    @api.doc('get a measurement type')
    @api.marshal_with(_measurement_type_response)
    def get(self, measurement_type_id):
        """get a measurement type given its identifier"""
        measurement_type = get_a_measurement_type(measurement_type_id)
        if not measurement_type:
            api.abort(404)
        else:
            return measurement_type



