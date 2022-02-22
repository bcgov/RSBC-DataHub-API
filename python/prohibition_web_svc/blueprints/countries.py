from python.prohibition_web_svc.config import Config
from flask import request, make_response, Blueprint, jsonify
from flask_cors import CORS

import logging.config
import python.common.helper as helper


logging.config.dictConfig(Config.LOGGING)
logging.info('*** countries blueprint loaded ***')

bp = Blueprint('countries', __name__, url_prefix=Config.URL_PREFIX + '/api/v1')
CORS(bp, resources={Config.URL_PREFIX + "/api/v1/countries": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/countries', methods=['GET'])
def index():
    """
    List all driver's license countries
    """
    if request.method == 'GET':
        data = helper.load_json_into_dict('python/prohibition_web_svc/data/countries.json')
        return make_response(jsonify(data), 200)


@bp.route('/countries/<string:country_id>', methods=['GET'])
def get(country_id):
    """
    Get a specific country
    """
    if request.method == 'GET':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/countries', methods=['POST'])
def create():
    """
    Save a new country
    """
    if request.method == 'POST':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/countries/<string:country_id>', methods=['PATCH'])
def update(country_id):
    """
    Update an country
    """
    if request.method == 'PATCH':
        return make_response({"error": "method not implemented"}, 405)



