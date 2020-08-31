from flask import Blueprint, request, jsonify, make_response
from python.paybc_api.website.oauth2 import authorization, require_oauth
import python.common.vips_api as vips
import python.common.prohibitions as pro
from python.paybc_api.website.config import Config
import logging
import datetime
import json

logging.basicConfig(level=Config.LOG_LEVEL)
logging.warning('*** Pay BC API initialized ***')
bp = Blueprint(__name__, 'home')


@bp.route('/oauth/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()


@bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')


@bp.route('/api_v2/search', methods=['GET'])
@require_oauth()
def search():
    """
    On the Pay_BC site, a user lookups an invoice to be paid. PayBC searches for
    the invoice in our system using a GET request with an invoice number and a
    check_value.  We return an array of items to be paid.
    :return:
    """
    if request.method == 'GET':
        last_name = request.args.get('check_value', None, type=str)
        prohibition_number = request.args.get('invoice_number', None, type=str)
        paybc_reference = request.args.get('pay_bc_reference', None, type=str)

        logging.info("GET request received - prohib: {}, ref: {}, last_name: {}".format(
            prohibition_number,
            paybc_reference,
            last_name
        ))

        if prohibition_number is None or last_name is None or paybc_reference is None:
            return make_response({
                "error": "insufficient parameters supplied"
            }, 400)

        is_successful, is_okay_2_pay = vips.is_application_ready_for_payment(prohibition_number, last_name, Config)
        logging.info("vips response: {}, okay to pay: {}".format(is_successful, is_okay_2_pay))
        if is_successful:
            if is_okay_2_pay:
                return jsonify({
                    "items": [{"selected_invoice": {
                           "$ref": request.host_url.replace('http', 'https') + 'api_v2/invoice/' + prohibition_number}
                        }
                    ]
                })
            else:
                error = 'A prohibition with that number is not found or not ready for payment'
                logging.info(error)
                return make_response({"error": error}, 404)
        else:
            error = 'No response from VIPS API'
            logging.critical(error)
            make_response({"error": error}, 500)


@bp.route('/api_v2/invoice/<prohibition_number>', methods=['GET'])
@require_oauth()
def show(prohibition_number):
    """
    PayBC requests details on the item to be paid from this endpoint.
    :param prohibition_number:
    :return:
    """
    # TODO - using regex, validate the number provided
    if request.method == 'GET':
        is_status_successful, invoice_data = vips.get_invoice_details(prohibition_number, Config)
        if is_status_successful:
            return jsonify(transform_invoice(prohibition_number, invoice_data))
        else:
            return make_response({"error": 'We are unable to find invoice ' + prohibition_number}, 404)


@bp.route('/api_v2/receipt', methods=['POST'])
@require_oauth()
def receipt():
    """
    After PayBC verifies that the payment has been approved, it submits
    a list of invoices that have been paid (a user can pay multiple
    payments simultaneously), we'll notify VIPS of the payment and
    return the following to show that the receipt has been received.
    :return:
    """
    if request.method == 'POST':
        payload = request.json

        # TODO
        #  - validated the data using Ceberus
        #  - save payment info to VIPS
        #  - if successful, return the following:

        return jsonify(dict({
            "status": "APP",
            "receipt_number": "TEST_RECEIPT",
            "receipt_date ": datetime.date.today().strftime('%d-%b-%Y'),
            "receipt_amount": 200.00
        }))


def transform_invoice(prohibition_number, invoice_data: dict):
    return dict({
        "invoice_number": prohibition_number,
        "pbc_ref_number": "10008",
        "party_number": 0,
        "party_name": "RSI",
        "account_number": "0",
        "site_number": "0",
        "cust_trx_type": "Review Notice of Driving Prohibition",
        "term_due_date": "2017-03-03T08:00:00Z",
        "total": invoice_data['amount'],
        "amount_due": invoice_data['amount'],
        "attribute1": "[Prohib. Period] and type: {}".format(invoice_data['notice_type_code']),
        "attribute2": invoice_data['service_date'],
        "attribute3": invoice_data['oral_or_written']
    })


@bp.route('/schedule/<notice_type>/<requested_date>', methods=['GET'])
def schedule(notice_type, requested_date):
    """
    GET timeslots for oral reviews for a specific date and prohibition_type
    """
    # TODO - validate inputs
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


@bp.route('/review_dates', methods=['POST'])
def review_dates():
    """
    Confirm prohibition number and last name matches VIPS.
    Return list of possible review dates for given prohibition.
    Note: using POST instead of GET to allow last names with
    special characters from Orbeon.
    """
    prohibition_number = request.form['prohibition_number']
    last_name = request.form['last_name']

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
