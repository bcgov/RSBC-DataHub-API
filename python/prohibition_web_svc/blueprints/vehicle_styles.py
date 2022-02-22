from python.prohibition_web_svc.config import Config
from flask import request, make_response, Blueprint
from flask_cors import CORS

import logging.config
import python.common.helper as helper


logging.config.dictConfig(Config.LOGGING)
logging.info('*** vehicle styles blueprint loaded ***')

bp = Blueprint('vehicle_styles', __name__, url_prefix=Config.URL_PREFIX + '/api/v1')
CORS(bp, resources={Config.URL_PREFIX + "/api/v1/vehicle_styles": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/vehicle_styles', methods=['GET'])
def index():
    """
    List all styles
    """
    if request.method == 'GET':
        data = helper.load_json_into_dict('python/prohibition_web_svc/data/vehicle_styles.json')
        return make_response(data, 200)


@bp.route('/vehicle_styles/<string:style_id>', methods=['GET'])
def get(style_id):
    """
    Get a specific style
    """
    if request.method == 'GET':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/vehicle_styles', methods=['POST'])
def create():
    """
    Save a new style
    """
    if request.method == 'POST':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/vehicle_styles/<string:style_id>', methods=['PATCH'])
def update(style_id):
    """
    Update a style
    """
    if request.method == 'PATCH':
        return make_response({"error": "method not implemented"}, 405)



