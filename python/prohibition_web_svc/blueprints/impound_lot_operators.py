from python.prohibition_web_svc.config import Config
from flask import request, make_response, Blueprint
from flask_cors import CORS

import logging.config
import python.common.helper as helper


logging.config.dictConfig(Config.LOGGING)
logging.info('*** impound lot operators blueprint loaded ***')

bp = Blueprint('impound_lot_operators', __name__, url_prefix='/api/v1')
CORS(bp, resources={"/api/v1/impound_lot_operators": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/impound_lot_operators', methods=['GET'])
def index():
    """
    List all impound lot operators
    """
    if request.method == 'GET':
        data = helper.load_json_into_dict('python/prohibition_web_svc/data/impound_lot_operators.json')
        return make_response(data, 200)


@bp.route('/impound_lot_operators/<string:ilo_id>', methods=['GET'])
def get(form_type, ilo_id):
    """
    Get a specific impound lot operator
    """
    if request.method == 'GET':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/impound_lot_operators', methods=['POST'])
def create():
    """
    Save a new impound lot operators
    """
    if request.method == 'POST':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/impound_lot_operators/<string:ilo_id>', methods=['PATCH'])
def update(ilo_id):
    """
    Update an existing impound lot operator
    """
    if request.method == 'PATCH':
        return make_response({"error": "method not implemented"}, 405)



