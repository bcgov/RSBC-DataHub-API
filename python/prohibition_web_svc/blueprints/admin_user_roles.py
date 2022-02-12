from python.prohibition_web_svc.config import Config
import python.common.helper as helper
from flask import request, Blueprint, make_response, jsonify
from flask_cors import CORS
import logging.config
import python.prohibition_web_svc.middleware.role_middleware as role_middleware
import python.prohibition_web_svc.middleware.form_middleware as form_middleware
import python.prohibition_web_svc.middleware.keycloak_middleware as keycloak_middleware
import python.prohibition_web_svc.business.keycloak_logic as keycloak_logic
import python.prohibition_web_svc.http_responses as http_responses


logging.config.dictConfig(Config.LOGGING)
logging.info('*** admin/users_roles blueprint loaded ***')

bp = Blueprint('admin_users_roles', __name__, url_prefix=Config.URL_PREFIX + '/api/v1')
CORS(bp, resources={Config.URL_PREFIX + "/api/v1/admin/users/*": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/admin/users/<string:user_guid>/roles', methods=['GET'])
def index(user_guid):
    """
    List all user roles for a specific user
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
                {"try": role_middleware.query_all_users_roles, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]}
            ],
            required_permission='admin_user_roles-index',
            requested_user_guid=user_guid,
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/admin/users/<string:user_guid>/roles/<string:role_name>', methods=['PATCH'])
def update(user_guid, role_name):
    """
    Update an existing role
    """
    if request.method == 'PATCH':
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
                {"try": role_middleware.approve_officers_role, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
            ],
            required_permission='admin_user_roles-update',
            requested_user_guid=user_guid,
            role_name=role_name,
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/admin/users/<string:user_guid>/roles/<string:role_name>', methods=['DELETE'])
def delete(user_guid, role_name):
    """
    Delete a specific role
    """
    if request.method == 'DELETE':
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
                {"try": role_middleware.delete_a_role, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
            ],
            required_permission='admin_user_roles-delete',
            requested_user_guid=user_guid,
            role_name=role_name,
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/admin/users/<string:user_guid>/roles', methods=['POST'])
def create(user_guid):
    if request.method == 'POST':
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
                {"try": form_middleware.request_contains_a_payload, "fail": [
                    {"try": http_responses.payload_missing, "fail": []},
                ]},
                {"try": role_middleware.admin_create_role, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
            ],
            required_permission='admin_user_roles-create',
            requested_user_guid=user_guid,
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/admin/users/<string:user_guid>/roles/<string:role_name>', methods=['GET'])
def get(user_guid, role_name):
    if request.method == 'GET':
        return make_response({"error": "method not implemented"}, 405)

