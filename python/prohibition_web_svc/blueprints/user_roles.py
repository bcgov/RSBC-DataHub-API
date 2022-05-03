from python.prohibition_web_svc.config import Config
import python.common.helper as helper
from flask import request, Blueprint, make_response, jsonify
from flask_cors import CORS
import python.prohibition_web_svc.middleware.splunk_middleware as splunk_middleware
import python.common.splunk as splunk
import logging.config
import python.prohibition_web_svc.middleware.role_middleware as role_middleware
import python.prohibition_web_svc.business.keycloak_logic as keycloak_logic
import python.prohibition_web_svc.http_responses as http_responses


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
        kwargs = helper.middle_logic(
            keycloak_logic.get_authorized_keycloak_user() + [
                {"try": splunk_middleware.get_user_role, "fail": []},
                {"try": splunk.log_to_splunk, "fail": []},
                {"try": role_middleware.query_current_users_roles, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]}
            ],
            required_permission='user_roles-index',
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/user_roles', methods=['POST'])
def create():
    if request.method == 'POST':
        return make_response({"error": "method not implemented"}, 405)


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

