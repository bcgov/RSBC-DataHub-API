import python.common.helper as helper
from python.ingestor.config import Config
from python.common.rabbitmq import RabbitMQ
from python.common.message import encode_message
import python.common.vips_api as vips
import python.common.prohibitions as pro
from flask import request, jsonify, Response, make_response
from flask_api import FlaskAPI

import xmltodict
import logging
import json
import re


application = FlaskAPI(__name__)
application.secret = Config.FLASK_SECRET_KEY
logging.basicConfig(level=Config.LOG_LEVEL)
logging.warning('*** ingestor initialized ***')

rabbit_mq = RabbitMQ(
        Config.RABBITMQ_USER,
        Config.RABBITMQ_PASS,
        Config.RABBITMQ_URL,
        Config.LOG_LEVEL,
        Config.MAX_CONNECTION_RETRIES,
        Config.RETRY_DELAY)

available_parameters = helper.load_json_into_dict('python/ingestor/' + Config.PARAMETERS_FILE)


@application.route('/v1/publish/event/<data_type>', methods=["POST"])
@application.route('/v1/publish/event', methods=["POST"])
def create(data_type='ETK'):

    if data_type not in available_parameters:
        warning_string = data_type + ' is a not a valid parameter'
        logging.warning(warning_string)
        return jsonify({"error": warning_string}), 500

    logging.debug('content-type: ' + request.content_type)

    if data_type == "ETK":
        payload = request.json
    elif data_type == "form":
        payload = {
            "event_version": "1.4",
            "encrypt_at_rest": available_parameters[data_type]['encrypt_at_rest'],
            "event_date_time": "",
            "event_type": "form_submission",
            "form_submission": xmltodict.parse(request.get_data())
        }
    else:
        payload = None

    encoded_message = encode_message(payload, Config.ENCRYPT_KEY)
    if payload is not None and rabbit_mq.publish(available_parameters[data_type]['queue'], encoded_message):
        return jsonify(payload), 200
    else:
        return Response('Unavailable', 500, mimetype='application/json')


@application.route('/schedule/<notice_type>/<requested_date>', methods=['GET'])
def schedule(notice_type, requested_date):
    """
    GET timeslots for oral reviews for a specific date and prohibition_type
    """

    if re.match("^UL|ADP|IRP$", notice_type) is None or \
            re.match("^\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])$", requested_date) is None:
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
def review_dates():
    """
    Confirm prohibition number and last name matches VIPS.
    Return list of possible review dates for given prohibition.
    Note: using POST instead of GET to allow last names with
    special characters from Orbeon.
    """
    prohibition_number = request.form['prohibition_number']
    last_name = request.form['last_name']

    if re.match("^\d{6,20}$", prohibition_number) is None:
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


if __name__ == "__main__":
    application.run(host='0.0.0.0')
