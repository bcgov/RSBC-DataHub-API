from python.prohibition_web_service.config import Config
import python.common.helper as helper
from flask import request, Blueprint, make_response, jsonify
from flask_cors import CORS
import logging.config
import python.prohibition_web_service.business.roles_logic as rules


logging.config.dictConfig(Config.LOGGING)
logging.info('*** admin/users_roles blueprint loaded ***')

bp = Blueprint('admin_users_roles', __name__, url_prefix='/api/v1/admin')
CORS(bp, resources={"/api/v1/admin/users/*": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/users/<string:username>/roles', methods=['GET'])
def index(username):
    """
    List all roles for the currently logged-in user
    """
    if request.method == 'GET':
        kwargs = helper.middle_logic(rules.list_any_users_roles(),
                                     required_permission='admin_user_roles-index',
                                     requested_username=username,
                                     request=request,
                                     config=Config)
        return kwargs.get('response')


@bp.route('/users/<string:username>/roles/<string:role_name>', methods=['PATCH'])
def update(username, role_name):
    """
    Update an existing role
    """
    if request.method == 'PATCH':
        kwargs = helper.middle_logic(rules.update_a_role(),
                                     required_permission='admin_user_roles-update',
                                     requested_username=username,
                                     role_name=role_name,
                                     request=request,
                                     config=Config)
        return kwargs.get('response')


@bp.route('/users/<string:username>/roles/<string:role_name>', methods=['DELETE'])
def delete(username, role_name):
    """
    Delete a specific role
    """
    if request.method == 'DELETE':
        kwargs = helper.middle_logic(rules.delete_a_role(),
                                     required_permission='admin_user_roles-delete',
                                     requested_username=username,
                                     role_name=role_name,
                                     request=request,
                                     config=Config)
        return kwargs.get('response')


@bp.route('/users/<string:username>/roles', methods=['POST'])
def create(username):
    if request.method == 'POST':
        kwargs = helper.middle_logic(rules.admin_create_a_role(),
                                     required_permission='admin_user_roles-create',
                                     requested_username=username,
                                     request=request,
                                     config=Config)
        return kwargs.get('response')


@bp.route('/users/<string:username>/roles/<string:role_name>', methods=['GET'])
def get(username, role_name):
    if request.method == 'GET':
        return make_response({"error": "method not implemented"}, 405)

