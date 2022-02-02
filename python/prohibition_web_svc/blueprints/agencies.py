from python.prohibition_web_svc.config import Config
from flask import request, make_response, Blueprint
from flask_cors import CORS

import logging.config
import python.common.helper as helper
from flask import jsonify

logging.config.dictConfig(Config.LOGGING)
logging.info('*** agency blueprint loaded ***')

bp = Blueprint('agencies', __name__, url_prefix=Config.URL_PREFIX + '/api/v1')
CORS(bp, resources={Config.URL_PREFIX + "/api/v1/agencies": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/agencies', methods=['GET'])
def index():
    """
    List all agency ids
    """
    if request.method == 'GET':
        agencies = helper.load_json_into_dict('python/prohibition_web_svc/data/agencies.json')
        ids = [o['id'] for o in agencies]
        return make_response(jsonify(ids), 200)


@bp.route('/agencies/<string:agency_id>', methods=['GET'])
def get(agency_id):
    """
    Get a specific color
    """
    if request.method == 'GET':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/agencies', methods=['POST'])
def create():
    """
    Save a new color
    """
    if request.method == 'POST':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/agencies/<string:agency_id>', methods=['PATCH'])
def update(agency_id):
    """
    Update an color
    """
    if request.method == 'PATCH':
        return make_response({"error": "method not implemented"}, 405)



