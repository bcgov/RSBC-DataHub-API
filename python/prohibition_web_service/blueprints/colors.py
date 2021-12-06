from python.prohibition_web_service.config import Config
from flask import request, make_response, Blueprint
from flask_cors import CORS

import logging.config
import python.common.helper as helper
from flask import jsonify

logging.config.dictConfig(Config.LOGGING)
logging.info('*** colors blueprint loaded ***')

bp = Blueprint('colors', __name__, url_prefix='/api/v1')
CORS(bp, resources={"/api/v1/colors": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/colors', methods=['GET'])
def index():
    """
    List all car colors
    """
    if request.method == 'GET':
        data = helper.load_json_into_dict('python/prohibition_web_service/data/car_colors.json')
        return make_response(jsonify(data), 200)


@bp.route('/colors/<string:color_id>', methods=['GET'])
def get(color_id):
    """
    Get a specific color
    """
    if request.method == 'GET':
        return make_response({"error: method not implemented"}, 405)


@bp.route('/colors', methods=['POST'])
def create():
    """
    Save a new color
    """
    if request.method == 'POST':
        return make_response({"error: method not implemented"}, 405)


@bp.route('/colors/<string:color_id>', methods=['PATCH'])
def update(color_id):
    """
    Update an color
    """
    if request.method == 'PATCH':
        return make_response({"error: method not implemented"}, 405)



