from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.sensor_controller import api as sensor_ns
from .main.controller.measurement_controller import api as measurement_ns

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='SENSOR API',
    version='1.0',
    description='REST API which is capable of storing raw measurements from sensors as well as retrieve data aggregates from these sensors upon request',
    security='apikey'
)

api.add_namespace(user_ns, path='/user')
api.add_namespace(sensor_ns, path='/sensor')
api.add_namespace(measurement_ns, path='/measurement')
