import python.common.helper as helper
import python.common.vips_api as vips
from python.ingestor.config import Config
from python.common.rabbitmq import RabbitMQ
from python.common.message import encode_message
import python.ingestor.business as business
from flask import request, jsonify, Response, g, Flask
import logging
import logging.config
from functools import wraps
import python.common.rsi_email as rsi_email


application = Flask(__name__)
application.secret = Config.FLASK_SECRET_KEY
logging.config.dictConfig(Config.LOGGING)
logging.warning('*** flask initialized  ***')


@application.before_request
def before_request_function():
    g.writer = RabbitMQ(Config())


available_parameters = {
      "expected_format": "application/xml",
      "encrypt_at_rest": False,
      "queue": "ingested"
    }


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


@basic_auth_required
@application.route('/v1/publish/event/etk', methods=["POST"])
def ingest_e_ticket_event():
    if request.method == 'POST' and request.content_type == 'application/json':
        payload = request.json
        encoded_message = encode_message(payload, Config.ENCRYPT_KEY)
        if payload is not None and g.writer.publish('ingested', encoded_message):
            return jsonify(payload), 200
        else:
            return Response({'error': 'Unavailable'}, 500, mimetype='application/json')


@application.route('/v1/publish/event/form', methods=["POST"])
def ingest_orbeon_form():
    if request.method == 'POST':
        logging.info("ingest_form_deprecated() invoked: {} | {}".format(request.remote_addr, request.get_data()))
        args = helper.middle_logic(business.ingest_form(),
                                   writer=g.writer,
                                   form_parameters=available_parameters,
                                   request=request,
                                   config=Config)
        return args.get('response')


@application.route('/schedule', methods=['POST'])
@basic_auth_required
def schedule():
    """
    Confirm prohibition number and last name matches VIPS.
    Return list of possible review dates for given prohibition.
    Note: using POST instead of GET to allow last names with
    special characters from Orbeon.
    """
    if request.method == 'POST':
        logging.info("schedule() invoked: {} | {}".format(request.remote_addr, request.get_data()))
        args = helper.middle_logic(business.get_available_time_slots(),
                                   prohibition_number=request.form['prohibition_number'],
                                   driver_last_name=request.form['last_name'],
                                   config=Config)
        if 'error_string' not in args:
            return jsonify(dict({
                "data": {
                    "is_valid": True,
                    "presentation_type": args.get('presentation_type'),
                    "time_slots": args.get('time_slots')
                }
            }))
        return jsonify(dict({
                    "data": {
                        "is_success": False,
                        "error": args.get('error_string'),
                        "timeSlots": []
                    }
                }))


@application.route('/evidence', methods=['POST'])
@basic_auth_required
def evidence():
    """
    Confirm prohibition number and last name matches VIPS and
    applicant business rules satisfied to submit evidence.
    """
    if request.method == 'POST':
        logging.info("evidence() invoked: {} | {}".format(request.remote_addr, request.get_data()))
        args = helper.middle_logic(business.is_okay_to_submit_evidence(),
                                   prohibition_number=request.form['prohibition_number'],
                                   driver_last_name=request.form['last_name'],
                                   config=Config)
        if 'error_string' not in args:
            return jsonify(dict({"data": {"is_valid": True}}))
        return jsonify(dict({
            "data": {
                "is_valid": False,
                "error": args.get('error_string'),
            }
        }))

@application.route('/check', methods=['GET'])
def check():
    """
    This endpoint displays the text of various email templates sent by the system. It
    is used for testing / debugging and only available in the DEV environment.
    """
    if request.method == 'GET' and Config.ENVIRONMENT in ['pr', 'dev']:
        t = request.args.get('template')
        prohibition_number = "99999999"
        content = rsi_email.get_email_content(t, prohibition_number)
        if content['subject'] is not None:
            template = rsi_email.get_jinja2_env().get_template(t)
            return template.render(
                full_name="[applicant name]",
                prohibition_number="[99-999999]",
                date_of_service="[December 29, 2020]",
                subject=content['subject'],
                phone="[2505551212]",
                friendly_review_time_slot="Friday, Nov 1 between 9:00am and 9:30am"
            )


@application.route('/check_templates', methods=['GET'])
def check_templates():
    """
    This endpoint returns a page with links to available templates. It
    is used for testing / debugging and only available in the DEV environment.
    """
    if request.method == 'GET' and Config.ENVIRONMENT in ['pr', 'dev']:
        template = rsi_email.get_jinja2_env().get_template('list_of_templates.html')
        return template.render(
            templates=rsi_email.content_data()
        )

@application.route('/duplicate', methods=['GET'])
@basic_auth_required
def check_duplicate():
    """
    This endpoint provides indication if a review has already been submitted for a given prohibition.
    """
    prohibition_number = request.args.get('prohibition_number')

    is_api_callout_successful, vips_duplicate_data = vips.duplicate_get(
        prohibition_id=prohibition_number, 
        config=Config)
    if is_api_callout_successful:
        return vips_duplicate_data
    error = 'the VIPS get_duplicate operation returned an invalid response'
    args['error_string'] = "The system is down, please try again later."
    logging.info(error)
    return False, args
         

if __name__ == "__main__":
    application.run(host='0.0.0.0')
