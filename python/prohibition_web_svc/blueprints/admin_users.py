from python.prohibition_web_svc.config import Config
import python.prohibition_web_svc.middleware.splunk_middleware as splunk_middleware
import python.common.splunk as splunk
import python.common.helper as helper
from flask import request, Blueprint, make_response
from flask_cors import CORS
import logging.config
import python.prohibition_web_svc.business.keycloak_logic as keycloak_logic
import python.prohibition_web_svc.http_responses as http_responses
import python.prohibition_web_svc.middleware.user_middleware as user_middleware
import python.prohibition_web_svc.data.validation_schemas as validation_schemas
import python.prohibition_web_svc.middleware.form_middleware as form_middleware


logging.config.dictConfig(Config.LOGGING)
logging.info('*** admin users blueprint loaded ***')

bp = Blueprint('agency_admin_users', __name__, url_prefix=Config.URL_PREFIX + '/api/v1')
CORS(bp, resources={Config.URL_PREFIX + "/api/v1/admin/users*": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/admin/users', methods=['GET'])
def index():
    """
    RSBC admins can list all users.
    """
    if request.method == 'GET':
        kwargs = helper.middle_logic(
            keycloak_logic.get_authorized_keycloak_user() + [
                {"try": splunk_middleware.get_users, "fail": []},
                {"try": splunk.log_to_splunk, "fail": []},
                {"try": user_middleware.query_all_users, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
            ],
            required_permission='admin-users-index',
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/admin/users', methods=['POST'])
def create():
    """
    Create a new user
    """
    if request.method == 'POST':
        kwargs = helper.middle_logic(
            keycloak_logic.get_authorized_keycloak_user() + [
                {"try": form_middleware.request_contains_a_payload, "fail": [
                    {"try": http_responses.payload_missing, "fail": []},
                ]},
                {"try": form_middleware.validate_payload, "fail": [
                    {"try": http_responses.failed_validation, "fail": []},
                ]},
                {"try": splunk_middleware.create_user, "fail": []},
                {"try": splunk.log_to_splunk, "fail": []},
                {"try": user_middleware.create_a_user, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
                {"try": http_responses.successful_create_response, "fail": []},
            ],
            validation_schema=validation_schemas.admin_user_schema(),
            required_permission='admin-users-create',
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/admin/users/<string:user_guid>', methods=['PATCH'])
def update(user_guid):
    if request.method == 'PATCH':
        kwargs = helper.middle_logic(
            keycloak_logic.get_authorized_keycloak_user() + [
                {"try": form_middleware.request_contains_a_payload, "fail": [
                    {"try": http_responses.payload_missing, "fail": []},
                ]},
                {"try": form_middleware.validate_payload, "fail": [
                    {"try": http_responses.failed_validation, "fail": []},
                ]},
                {"try": user_middleware.payload_user_matches_url_user_guid, "fail": [
                    {"try": http_responses.cannot_change_user_guid, "fail": []},
                ]},
                {"try": splunk_middleware.update_user, "fail": []},
                {"try": splunk.log_to_splunk, "fail": []},
                {"try": user_middleware.update_the_user, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
                {"try": http_responses.successful_update_response, "fail": []},
            ],
            validation_schema=validation_schemas.admin_user_schema(),
            url_user_guid=user_guid,
            required_permission='admin-users-update',
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/admin/users/<string:user_guid>', methods=['DELETE'])
def delete(user_guid):
    if request.method == 'DELETE':
        kwargs = helper.middle_logic(
            keycloak_logic.get_authorized_keycloak_user() + [
                {"try": user_middleware.delete_a_user, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
                {"try": http_responses.successful_update_response, "fail": []},
                {"try": splunk_middleware.delete_user, "fail": []},
                {"try": splunk.log_to_splunk, "fail": []},
            ],
            url_user_guid=user_guid,
            required_permission='admin-users-delete',
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/admin/users/<string:user_guid>', methods=['GET'])
def get(user_guid):
    if request.method == 'GET':
        return make_response({"error": "method not implemented"}, 405)

