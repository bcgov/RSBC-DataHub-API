from python.prohibition_web_service.config import Config
from flask import request, make_response, Blueprint
from flask_cors import CORS

import logging.config
import python.common.helper as helper


logging.config.dictConfig(Config.LOGGING)
logging.info('*** cities blueprint loaded ***')

bp = Blueprint('cities', __name__, url_prefix='/api/v1')
CORS(bp, resources={"/api/v1/cities": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/cities', methods=['GET'])
def index():
    """
    List all cities
    """
    if request.method == 'GET':
        data = helper.load_json_into_dict('python/prohibition_web_service/data/cities.json')
        return make_response(data, 200)


@bp.route('/cities/<string:city_id>', methods=['GET'])
def get(city_id):
    """
    Get a specific city
    """
    if request.method == 'GET':
        return make_response({"error: method not implemented"}, 405)


@bp.route('/cities', methods=['POST'])
def create():
    """
    Save a new city
    """
    if request.method == 'POST':
        return make_response({"error: method not implemented"}, 405)


@bp.route('/cities/<string:city_id>', methods=['PATCH'])
def update(city_id):
    """
    Update a city
    """
    if request.method == 'PATCH':
        return make_response({"error: method not implemented"}, 405)



