import python.common.helper as helper
from python.ingestor.config import Config
from python.common.rabbitmq import RabbitMQ
from python.common.message import encode_message
import python.common.vips_api as vips
import python.common.prohibitions as pro
from flask import request, jsonify, Response, make_response
from flask_api import FlaskAPI
from datetime import datetime
import base64
import xmltodict
import logging
import json
import re
from functools import wraps


application = FlaskAPI(__name__)
application.secret = Config.FLASK_SECRET_KEY
logging.basicConfig(level=Config.LOG_LEVEL)
logging.warning('*** flask initialized ***')

rabbit_mq = RabbitMQ(
        Config.RABBITMQ_USER,
        Config.RABBITMQ_PASS,
        Config.RABBITMQ_URL,
        Config.LOG_LEVEL,
        Config.MAX_CONNECTION_RETRIES,
        Config.RETRY_DELAY)

available_parameters = helper.load_json_into_dict('python/ingestor/' + Config.PARAMETERS_FILE)


def basic_auth_required(f):
    """
    Decorator that implements basic auth when added to a route
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_credentials(Config, auth.username, auth.password):
            message = {'error': 'Unauthorized'}
            resp = jsonify(message)
            resp.status_code = 401
            return resp
        return f(*args, **kwargs)
    return decorated


@application.route('/v1/publish/event/ETK', methods=["POST"])
@application.route('/v1/publish/event', methods=["POST"])
def ingest_etk():
    payload = request.json
    encoded_message = encode_message(payload, Config.ENCRYPT_KEY)
    if payload is not None and rabbit_mq.publish(available_parameters['form']['queue'], encoded_message):
        return jsonify(payload), 200
    else:
        return Response('Unavailable', 500, mimetype='application/json')


@application.route('/v1/publish/event/form', methods=["POST"])
def ingest_form():
    logging.debug('content-type: ' + request.content_type)
    form_name = request.args.get('form')
    payload = {
        "event_version": "1.4",
        "encrypt_at_rest": available_parameters['form']['encrypt_at_rest'],
        "event_date_time": datetime.now().isoformat(),
        "url_parameters": request.args.to_dict(),
        "event_type": form_name,
        form_name: xmltodict.parse(request.get_data())
    }
    payload[form_name]['xml'] = base64.b64encode(request.get_data()).decode()
    encoded_message = encode_message(payload, Config.ENCRYPT_KEY)
    if payload is not None and rabbit_mq.publish(available_parameters['form']['queue'], encoded_message):
        return jsonify(payload), 200
    else:
        return Response('Unavailable', 500, mimetype='application/json')


@application.route('/schedule/<notice_type>/<requested_date>', methods=['GET'])
@basic_auth_required
def schedule(notice_type, requested_date):
    """
    GET timeslots for oral reviews for a specific date and prohibition_type
    """
    if re.match("^UL|ADP|IRP$", notice_type) is None or \
            re.match(r"^\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])$", requested_date) is None:
        logging.warning('schedule method failed validation: {}, {}'.format(notice_type, requested_date))
        return make_response({"error": "failed validation"}, 400)

    if request.method == 'GET':
        logging.warning('form parameters: {}, {}'.format(notice_type, requested_date))
        is_successful, data = vips.schedule_get(notice_type, requested_date, Config)

        if is_successful:
            return jsonify(dict({
                "is_success": True,
                "data": {
                  "timeSlots": vips.schedule_to_friendly_times(data['data']['timeSlots'])
                }}
            ))
        return jsonify(dict({
            "data": {
                "is_success": False,
                "timeSlots": []
            }
        }))


@application.route('/review_dates', methods=['POST'])
@basic_auth_required
def review_dates():
    """
    Confirm prohibition number and last name matches VIPS.
    Return list of possible review dates for given prohibition.
    Note: using POST instead of GET to allow last names with
    special characters from Orbeon.
    """
    prohibition_number = request.form['prohibition_number']
    last_name = request.form['last_name']

    if re.match(r"^\d{6,20}$", prohibition_number) is None:
        logging.warning('review_dates method failed validation: {}'.format(prohibition_number))
        return make_response({"error": "failed validation"}, 400)

    # TODO - add last_name validation

    if request.method == 'POST':
        logging.warning('form parameters: {}, {}'.format(prohibition_number, last_name))
        correlation_id = vips.generate_correlation_id()
        is_response, vips_status = vips.status_get(prohibition_number, Config, correlation_id)
        logging.info("current prohibition status: {}".format(json.dumps(vips_status)))
        if is_response and vips.is_last_name_match(vips_status, last_name):
            prohibition = pro.prohibition_factory(vips_status['noticeTypeCd'])
            service_date = vips.vips_str_to_datetime(vips_status['effectiveDt'])
            presentation_type = ''
            if 'applicationId' in vips_status:
                application_id = vips_status['applicationId']
                is_application_success, application = vips.application_get(application_id, Config, correlation_id)
                logging.info("current application status: {}".format(json.dumps(application)))
                if is_application_success and 'presentationTypeCd' in application:
                    presentation_type = application['presentationTypeCd']
            return jsonify(dict({
                "data": {
                    "is_valid": True,
                    "is_paid": "receiptNumberTxt" in vips_status,
                    "presentation_type": presentation_type,
                    "notice_type": vips_status['noticeTypeCd'],
                    "max_review_date": prohibition.get_max_review_date(service_date).strftime("%Y-%m-%d")
                }
            }))
        return jsonify(dict({
            "data": {
                "is_valid": False,
            }
        }))


def check_credentials(config, username_submitted, password_submitted) -> bool:
    username = config.FLASK_BASIC_AUTH_USER
    password = config.FLASK_BASIC_AUTH_PASS
    logging.info('credentials: {}:{}'.format(username, password))
    if username_submitted == username and password_submitted == password:
        return True
    return False


if __name__ == "__main__":
    application.run(host='0.0.0.0')
