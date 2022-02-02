from python.prohibition_web_svc.config import Config
import python.common.helper as helper
from flask import request, Blueprint, make_response, jsonify
from flask_cors import CORS
import logging.config
import python.prohibition_web_svc.business.roles_logic as rules


logging.config.dictConfig(Config.LOGGING)
logging.info('*** admin/users blueprint loaded ***')

bp = Blueprint('admin_users', __name__, url_prefix=Config.URL_PREFIX + '/api/v1')
CORS(bp, resources={Config.URL_PREFIX + "/api/v1/admin/users": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/admin/users', methods=['GET'])
def index():
    """
    List all authorized users
    """
    if request.method == 'GET':
        kwargs = helper.middle_logic(rules.list_all_users(),
                                     required_permission='admin_users-index',
                                     request=request,
                                     config=Config)
        return kwargs.get('response')


@bp.route('/admin/users/<string:username>', methods=['PATCH'])
def update(username):
    if request.method == 'PATCH':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/admin/users/<string:username>', methods=['DELETE'])
def delete(username):
    if request.method == 'DELETE':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/admin/users', methods=['POST'])
def create():
    if request.method == 'POST':
        return make_response({"error": "method not implemented"}, 405)


@bp.route('/admin/users/<string:username>', methods=['GET'])
def get(username):
    if request.method == 'GET':
        return make_response({"error": "method not implemented"}, 405)

