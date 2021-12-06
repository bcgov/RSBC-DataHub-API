from flask import Blueprint, request, jsonify, make_response
from python.paybc_api.website.oauth2 import authorization, require_oauth
import python.common.helper as helper
import python.paybc_api.business as rules
from python.paybc_api.website.config import Config
from python.common.rabbitmq import RabbitMQ
import logging
import logging.config

logging.config.dictConfig(Config.LOGGING)
logging.warning('*** Pay BC API initialized ***')
bp = Blueprint('paybc', __name__)


@bp.route('/oauth/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()


@bp.route('/api_v2/search', methods=['GET'])
@require_oauth()
def search():
    """
    On the Pay_BC site, a user lookups an prohibition_number (invoice) to be paid.
    PayBC searches for the invoice in our system using a GET request with an
    invoice number and a check_value.  We return an array of items to be paid.
    """
    if request.method == 'GET':
        logging.info("search() invoked: {} | {}".format(request.remote_addr, request.get_data()))
        prohibition_number = request.args.get('invoice_number')
        driver_last_name = request.args.get('check_value')
        args = helper.middle_logic(
            rules.search_for_invoice(),
            request=request,
            config=Config,
            prohibition_number=prohibition_number,
            driver_last_name=driver_last_name)
        return args.get('response', jsonify({"error": args.get('error_string')}))


@bp.route('/api_v2/invoice/<prohibition_number>', methods=['GET'])
@require_oauth()
def show(prohibition_number):
    """
    PayBC requests details on the item to be paid from this endpoint.
    """
    if request.method == 'GET':
        logging.info("show() invoked: {} | {}".format(request.remote_addr, request.get_data()))
        args = helper.middle_logic(rules.generate_invoice(),
                                   prohibition_number=prohibition_number,
                                   config=Config)
        return args.get('response', jsonify({"error": args.get('error_string')}))


@bp.route('/api_v2/receipt', methods=['POST'])
@require_oauth()
def receipt():
    """
    After PayBC verifies that the payment has been approved, it submits
    the payment details of the invoice that was paid.  We'll save the
    payment info to VIPS and acknowledge receipt of payment.
    """
    if request.method == 'POST':
        logging.info("receipt() invoked: {} | {}".format(request.remote_addr, request.get_data()))
        payload = request.json
        # invoke middleware business logic
        args = helper.middle_logic(rules.save_payment(),
                                   payload=payload,
                                   config=Config,
                                   writer=RabbitMQ(Config))
        return args.get('response', make_response({'status': 'INCMP'}, 400))
