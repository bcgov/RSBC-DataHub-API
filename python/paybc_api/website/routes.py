from flask import Blueprint, request, jsonify, make_response
from python.paybc_api.website.oauth2 import authorization, require_oauth
import python.common.vips_api as vips
import python.common.prohibitions as pro
import python.common.helper as helper
import python.common.business as rules
from python.paybc_api.website.config import Config
from python.common.helper import load_json_into_dict
from cerberus import Validator as Cerberus
import logging
from datetime import datetime, timezone
import pytz
import json
import re

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
    """
    if request.method == 'GET':
        # invoke middleware functions
        prohibition_number = request.args.get('invoice_number')
        driver_last_name = request.args.get('check_value')
        logging.info('inputs: {}, {}'.format(prohibition_number, driver_last_name))
        args = helper.middle_logic(
            rules.ready_for_payment(),
            config=Config,
            prohibition_number=prohibition_number,
            driver_last_name=driver_last_name)
        if 'error_string' not in args:
            # TODO - http replaced with https for local development - REMOVE BEFORE FLIGHT!
            host_url = request.host_url.replace('http', 'https')
            return jsonify({
                "items": [{"selected_invoice": {
                       "$ref": host_url + 'api_v2/invoice/' + args.get('prohibition_number')}
                    }
                ]
            })
        return jsonify({"error": args.get('error_string')})


@bp.route('/api_v2/invoice/<prohibition_number>', methods=['GET'])
@require_oauth()
def show(prohibition_number):
    """
    PayBC requests details on the item to be paid from this endpoint.
    """
    if request.method == 'GET':
        # invoke middleware functions
        args = helper.middle_logic(rules.ready_for_invoicing(),
                                   prohibition_number=prohibition_number,
                                   config=Config)
        if 'error_string' not in args:
            presentation_type = args.get('presentation_type')
            amount_due = args.get('amount_due')
            service_date = args.get('service_date')
            return jsonify(dict({
                "invoice_number": args.get('prohibition_number'),
                "pbc_ref_number": "10008",
                "party_number": 0,
                "party_name": "RSI",
                "account_number": "0",
                "site_number": "0",
                "cust_trx_type": "Review Notice of Driving Prohibition",
                "term_due_date": service_date.isoformat(),
                "total": amount_due,
                "amount_due": amount_due,
                "attribute1": args.get('vips_data')['noticeTypeCd'],
                "attribute2": service_date.strftime("%b %-d, %Y"),
                "attribute3": presentation_type,
                "amount": amount_due
            }))
        return make_response({"error": args.get('error_string')}, 404)


@bp.route('/api_v2/receipt', methods=['POST'])
@require_oauth()
def receipt():
    """
    After PayBC verifies that the payment has been approved, it submits
    a list of invoices that have been paid (a user can pay multiple
    payments simultaneously), we'll notify VIPS of the payment and
    return the following to show that the receipt has been received.
    """
    if request.method == 'POST':
        payload = request.json

        if not validate(Config, 'receipt', payload):
            return make_response({"error": "failed validation"}, 400)

        # PayBC has the facility to pay multiple invoices in a single transaction
        # however we can assume there is only one transaction because this API only
        # returns a single invoice per prohibition number.
        prohibition_number = payload['invoices'][0]["trx_number"]

        date_object = pay_bc_date_to_datetime(payload['receipt_date'])

        correlation_id = vips.generate_correlation_id()
        is_successful, args = vips.payment_patch(prohibition_number,
                                                 Config,
                                                 correlation_id,
                                                 card_type=payload['cardtype'],
                                                 receipt_amount=payload['receipt_amount'],
                                                 receipt_date=date_object,
                                                 receipt_number=payload['receipt_number'])

        if not is_successful:
            return jsonify(dict({"status": "INCMP"}))

        # TODO - trigger a payment event which sends email to applicant
        #  with instructions to schedule

        return jsonify(dict({
            "status": "APP",
            "receipt_number": payload['receipt_number'],
            "receipt_date ": datetime.today().strftime('%d-%b-%Y'),
            "receipt_amount": payload['receipt_amount']
        }))


def validate(config, method_name: str, payload: dict) -> bool:
    schemas = load_json_into_dict(config.SCHEMA_PATH + config.SCHEMA_FILENAME)

    # check that that the method_name has an associated validation schema
    if method_name not in schemas:
        logging.critical('{} does not have an associated validation schema'.format(method_name))

    # return the validation error message from the associated schema
    schema = schemas[method_name]
    logging.debug('schema: {}'.format(json.dumps(schema)))
    logging.debug('payload: {}'.format(payload))
    cerberus = Cerberus(schema['cerberus_rules'])
    cerberus.allow_unknown = schema['allow_unknown']
    if cerberus.validate(payload):
        logging.info('payload passed validation')
        return True
    else:
        logging.warning('payload failed validation: {}'.format(json.dumps(cerberus.errors)))
        return False


def pay_bc_date_to_datetime(pay_bc_date: str) -> datetime:
    """
    Transform PayBC date format: 20-JUN-2017 datetime object
    """
    tz = pytz.timezone('America/Vancouver')
    date_object = datetime.strptime(pay_bc_date, "%d-%b-%Y")
    return tz.localize(date_object)
