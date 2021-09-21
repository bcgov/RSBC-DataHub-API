from python.prohibition_web_service.config import Config
from flask import request, make_response, Blueprint
from python.prohibition_web_service.blueprints.common import basic_auth_required
import logging.config
import python.common.helper as helper
from flask import jsonify

logging.config.dictConfig(Config.LOGGING)
logging.info('*** colors blueprint loaded ***')

bp = Blueprint('colors', __name__, url_prefix='/api/v1')


@bp.route('/colors', methods=['GET'])
def index():
    """
    List all car colors
    """
    if request.method == 'GET':
        data = helper.load_json_into_dict('python/prohibition_web_service/data/car_colors.json')
        return make_response(jsonify(data), 200)


@bp.route('/colors/<string:color_id>', methods=['GET'])
@basic_auth_required
def get(color_id):
    """
    Get a specific color
    """
    if request.method == 'GET':
        return make_response({"error: method not implemented"}, 405)


@bp.route('/colors', methods=['POST'])
@basic_auth_required
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



