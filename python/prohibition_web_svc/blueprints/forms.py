from python.prohibition_web_svc.config import Config
import python.common.helper as helper
from flask import request, Blueprint, make_response, jsonify
from flask_cors import CORS
import logging.config
import python.common.splunk as splunk
import python.prohibition_web_svc.middleware.splunk_middleware as splunk_middleware
import python.prohibition_web_svc.middleware.form_middleware as form_middleware
import python.prohibition_web_svc.http_responses as http_responses
from python.prohibition_web_svc.business.keycloak_logic import get_authorized_keycloak_user


logging.config.dictConfig(Config.LOGGING)
logging.info('*** forms blueprint loaded ***')

bp = Blueprint('forms', __name__, url_prefix=Config.URL_PREFIX + '/api/v1')
CORS(bp, resources={Config.URL_PREFIX + "/api/v1/forms/*": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/forms/<string:form_type>', methods=['GET'])
def index(form_type):
    """
    List all forms for a user
    """
    if request.method == 'GET':
        kwargs = helper.middle_logic(
            get_authorized_keycloak_user() + [
                {"try": splunk_middleware.log_form_index, "fail": []},
                {"try": form_middleware.list_all_users_forms, "fail": [
                    {"try": http_responses.server_error_response, "fail": []},
                ]},
                {"try": splunk.log_to_splunk, "fail": []}
            ],
            required_permission='forms-index',
            request=request,
            form_type=form_type,
            config=Config)
        return kwargs.get('response')


@bp.route('/forms/<string:form_type>/<string:form_id>', methods=['GET'])
def get(form_type, form_id):
    """
    Get a specific form
    """
    if request.method == 'GET':
        return make_response({'error': 'method not implemented'}, 405)


@bp.route('/forms/<string:form_type>', methods=['POST'])
def create(form_type):
    """
    Save a new form.  The web_app uses this endpoint to lease a unique form_id
    for 30 days and save the user's name in the form table. This endpoint is not
    used to submit a new form.  All payloads to this endpoint are ignored.
    """
    if request.method == 'POST':
        logging.info("new {} form_id requested".format(form_type))
        kwargs = helper.middle_logic(
            get_authorized_keycloak_user() + [
                {"try": form_middleware.request_contains_a_payload, "fail": [
                    {"try": form_middleware.lease_a_form_id, "fail": [
                        {"try": splunk_middleware.insufficient_form_ids, "fail": []},
                        {"try": splunk.log_to_splunk, "fail": []},
                        {"try": http_responses.server_error_response, "fail": []},
                    ]},
                    {"try": splunk_middleware.log_form_create, "fail": []},
                    {"try": splunk.log_to_splunk, "fail": []},
                    {"try": http_responses.successful_create_response, "fail": []},
                ]},

                {"try": http_responses.bad_request_response, "fail": []}
            ],
            required_permission='forms-create',
            request=request,
            form_type=form_type,
            config=Config)
        return kwargs.get('response')


@bp.route('/forms/<string:form_type>/<string:form_id>', methods=['PATCH'])
def update(form_type, form_id):
    """
    Update an existing form is used when either a) submitting a form using an previously
    leased form_id; or, b) renewing the lease of a form_id.  If a patch request is
    received without a payload, this endpoint assumes the form lease should be renewed;
    otherwise, the payload is received as a form submission.
    """
    if request.method == 'PATCH':
        kwargs = helper.middle_logic(
            get_authorized_keycloak_user() + [
                {"try": form_middleware.request_contains_a_payload, "fail": [
                    # Request contains no payload - renew form lease
                    {"try": form_middleware.renew_form_id_lease, "fail": [
                        {"try": splunk_middleware.unable_to_renew_lease, "fail": []},
                        {"try": splunk.log_to_splunk, "fail": []},
                        {"try": http_responses.bad_request_response, "fail": []},
                    ]},
                    {"try": splunk_middleware.form_lease_renewed, "fail": []},
                    {"try": splunk.log_to_splunk, "fail": []},
                    {"try": http_responses.successful_update_response, "fail": []},
                ]},
                # Request contains a payload - process submitted form
                {"try": splunk_middleware.form_submitted, "fail": []},
                {"try": form_middleware.mark_form_as_printed, "fail": [
                    # TODO - Write to RabbitMQ fail queue
                    {"try": http_responses.record_not_found, "fail": []},
                ]},
                # TODO - Write to RabbitMQ ingested queue
                {"try": http_responses.successful_update_response, "fail": []}
            ],
            required_permission='forms-update',
            form_type=form_type,
            form_id=form_id,
            request=request,
            config=Config)
        return kwargs.get('response')


@bp.route('/forms/<string:form_type>/<string:form_id>', methods=['DELETE'])
def delete(form_type, form_id):
    """
    Delete a specific form
    """
    if request.method == 'DELETE':
        return make_response({'error': 'method not implemented'}, 405)

