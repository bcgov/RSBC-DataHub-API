from python.prohibition_web_svc.config import Config
import python.common.helper as helper
from flask import request, Blueprint, make_response, jsonify
from flask_cors import CORS
import logging.config
import python.prohibition_web_svc.business.roles_logic as rules


logging.config.dictConfig(Config.LOGGING)
logging.info('*** user_roles blueprint loaded ***')

bp = Blueprint('user_roles', __name__, url_prefix=Config.URL_PREFIX + '/api/v1')
CORS(bp, resources={Config.URL_PREFIX + "/api/v1/user_roles/*": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/user_roles', methods=['GET'])
def index():
    """
    List all roles for the currently logged-in user
    """
    if request.method == 'GET':
        kwargs = helper.middle_logic(rules.list_my_roles(),
                                     required_permission='user_roles-index',
                                     request=request,
                                     config=Config)
        return kwargs.get('response')


@bp.route('/user_roles', methods=['POST'])
def create():
    """
    Save a new user-role.
    """
    if request.method == 'POST':
        kwargs = helper.middle_logic(rules.create_a_role(),
                                     request=request,
                                     config=Config)
        return kwargs.get('response')


@bp.route('/user_roles/<string:role_name>', methods=['GET'])
def get(role_name):
    if request.method == 'GET':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/user_roles/<string:role_name>', methods=['PATCH'])
def update(role_name):
    if request.method == 'PATCH':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/user_roles/<string:role_name>', methods=['DELETE'])
def delete(role_name):
    if request.method == 'DELETE':
        return make_response({"error": "method not implemented"}, 405)

