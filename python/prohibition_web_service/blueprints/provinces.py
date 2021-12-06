from python.prohibition_web_service.config import Config
from flask import request, make_response, Blueprint, jsonify
from flask_cors import CORS

import logging.config
import python.common.helper as helper


logging.config.dictConfig(Config.LOGGING)
logging.info('*** provinces blueprint loaded ***')

bp = Blueprint('provinces', __name__, url_prefix='/api/v1')
CORS(bp, resources={"/api/v1/provinces": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/provinces', methods=['GET'])
def index():
    """
    List all provinces
    """
    if request.method == 'GET':
        data = helper.load_json_into_dict('python/prohibition_web_service/data/provinces.json')
        return make_response(jsonify(data), 200)


@bp.route('/provinces/<string:province_id>', methods=['GET'])
def get(province_id):
    """
    Get a specific province
    """
    if request.method == 'GET':
        return make_response({"error: method not implemented"}, 405)


@bp.route('/provinces', methods=['POST'])
def create():
    """
    Save a new province
    """
    if request.method == 'POST':
        return make_response({"error: method not implemented"}, 405)


@bp.route('/provinces/<string:province_id>', methods=['PATCH'])
def update(province_id):
    """
    Update an province
    """
    if request.method == 'PATCH':
        return make_response({"error: method not implemented"}, 405)



