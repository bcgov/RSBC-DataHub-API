from python.prohibition_web_service.config import Config
from flask import request, make_response, Blueprint
from flask_cors import CORS

import logging.config
import python.common.helper as helper


logging.config.dictConfig(Config.LOGGING)
logging.info('*** vehicles blueprint loaded ***')

bp = Blueprint('vehicles', __name__, url_prefix='/api/v1')
CORS(bp, resources={"/api/v1/vehicles": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})



@bp.route('/vehicles', methods=['GET'])
def index():
    """
    This returns a list of vehicle make, model and years.
    TODO - replace this list with an authoritative list from PrimeCorp
    """
    if request.method == 'GET':
        data = helper.load_json_into_dict('python/prohibition_web_service/data/vehicle_make_model.json')
        return make_response(data, 200)


@bp.route('/vehicles/<string:vehicle_id>', methods=['GET'])
def get(vehicle_id):
    """
    Get a specific vehicle
    """
    if request.method == 'GET':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/vehicles', methods=['POST'])
def create():
    """
    Save a new vehicle
    """
    if request.method == 'POST':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/vehicles/<string:vehicle_id>', methods=['PATCH'])
def update(vehicle_id):
    """
    Update a vehicle
    """
    if request.method == 'PATCH':
        return make_response({"error": "method not implemented"}, 405)



