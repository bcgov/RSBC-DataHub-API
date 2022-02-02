from python.prohibition_web_svc.config import Config
from flask import request, make_response, Blueprint
from flask_cors import CORS

import logging.config
import python.common.helper as helper


logging.config.dictConfig(Config.LOGGING)
logging.info('*** jurisdictions blueprint loaded ***')

bp = Blueprint('jurisdictions', __name__, url_prefix=Config.URL_PREFIX + '/api/v1')
CORS(bp, resources={Config.URL_PREFIX + "/api/v1/jurisdictions": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/jurisdictions', methods=['GET'])
def index():
    """
    List all driver's license jurisdictions
    """
    if request.method == 'GET':
        data = helper.load_json_into_dict('python/prohibition_web_svc/data/jurisdictions.json')
        return make_response(data, 200)


@bp.route('/jurisdictions/<string:jurisdiction_id>', methods=['GET'])
def get(jurisdiction_id):
    """
    Get a specific jurisdiction
    """
    if request.method == 'GET':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/jurisdictions', methods=['POST'])
def create():
    """
    Save a new jurisdiction
    """
    if request.method == 'POST':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/jurisdictions/<string:jurisdiction_id>', methods=['PATCH'])
def update(jurisdiction_id):
    """
    Update an jurisdiction
    """
    if request.method == 'PATCH':
        return make_response({"error": "method not implemented"}, 405)



