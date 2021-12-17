from python.prohibition_web_svc.config import Config
from flask import request, Blueprint, make_response, jsonify
import python.common.helper as helper
from flask_cors import CORS
import logging.config
from functools import wraps
import python.prohibition_web_svc.middleware.form_middleware as form_middleware
import python.prohibition_web_svc.http_responses as http_responses

logging.config.dictConfig(Config.LOGGING)
logging.info('*** admin/forms blueprint loaded ***')

bp = Blueprint('admin_forms', __name__, url_prefix='/api/v1/admin')
CORS(bp, resources={"/api/v1/admin/forms*": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


def basic_auth_required(f):
    """
    Decorator that implements basic auth when added to a route
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not helper.check_credentials(
                Config.FLASK_BASIC_AUTH_USER, Config.FLASK_BASIC_AUTH_PASS, auth.username, auth.password):
            logging.warning("Request denied - unauthorized - IP Address: {}".format(request.remote_addr))
            message = {'error': 'Unauthorized'}
            resp = jsonify(message)
            resp.status_code = 401
            return resp
        return f(*args, **kwargs)
    return decorated


@bp.route('/forms', methods=['GET'])
@basic_auth_required
def index():
    """
    List all forms
    """
    if request.method == 'GET':
        kwargs = helper.middle_logic(
            [
                {"try": form_middleware.admin_list_all_forms_by_type, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]}
            ],
            form_type=request.args.get('type'),
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/forms/<string:form_id>', methods=['GET'])
def get(form_id):
    """
    Get a specific form
    """
    if request.method == 'GET':
        return make_response('method not implemented', 405)


@bp.route('/forms', methods=['POST'])
@basic_auth_required
def create():
    """
    Create a new form
    """
    if request.method == 'POST':
        kwargs = helper.middle_logic(
            [
                {"try": form_middleware.get_json_payload, "fail": [
                    {"try": http_responses.payload_missing, "fail": []},
                ]},
                {"try": form_middleware.validate_form_payload, "fail": [
                    {"try": http_responses.failed_validation, "fail": []},
                ]},
                {"try": form_middleware.admin_create_form, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]}
            ],
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/forms/<string:form_id>', methods=['PATCH'])
def update(form_id):
    """
    Update a specific form
    """
    if request.method == 'PATCH':
        return make_response('method not implemented', 405)


@bp.route('/forms/<string:form_id>', methods=['DELETE'])
def delete(form_id):
    """
    Delete a specific form
    """
    if request.method == 'DELETE':
        return make_response('method not implemented', 405)

