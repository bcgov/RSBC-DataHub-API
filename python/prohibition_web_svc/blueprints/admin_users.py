from python.prohibition_web_svc.config import Config
import python.common.helper as helper
from flask import request, Blueprint, make_response, jsonify
from flask_cors import CORS
import logging.config
import python.prohibition_web_svc.business.keycloak_logic as keycloak_logic
import python.prohibition_web_svc.http_responses as http_responses
import python.prohibition_web_svc.middleware.keycloak_middleware as keycloak_middleware
import python.prohibition_web_svc.middleware.role_middleware as role_middleware


logging.config.dictConfig(Config.LOGGING)
logging.info('*** admin/users blueprint loaded ***')

bp = Blueprint('admin_users', __name__, url_prefix=Config.URL_PREFIX + '/api/v1')
CORS(bp, resources={Config.URL_PREFIX + "/api/v1/admin/users": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/admin/users', methods=['GET'])
def index():
    """
    List all authorized users and their associated user-roles
    """
    if request.method == 'GET':
        kwargs = helper.middle_logic(
            keycloak_logic.get_keycloak_user() + [
                {"try": keycloak_middleware.load_roles_and_permissions_from_static_file, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
                {"try": keycloak_middleware.query_database_for_users_permissions, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
                {"try": keycloak_middleware.check_user_is_authorized, "fail": [
                    {"try": http_responses.unauthorized, "fail": []},
                ]},
                {"try": role_middleware.query_all_users, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
            ],
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

