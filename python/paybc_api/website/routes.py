from flask import Blueprint, request, session, url_for
from flask import render_template, redirect, jsonify
from python.paybc_api.website.oauth2 import authorization, require_oauth
import logging
import datetime

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
        return jsonify(search_for_invoice(
            request.args.get('invoice_number', None),
            request.args.get('pay_bc_reference', None),
            request.args.get('check_value', None)
        ))


@bp.route('/api_v2/invoice/<invoice_number>', methods=['GET'])
@require_oauth()
def show(invoice_number):
    """
    PayBC requests details on the item to be paid from this endpoint.
    :param invoice_number:
    :return:
    """
    if request.method == 'GET':
        # lookup the request using the VIPS API
        return jsonify(get_invoice(invoice_number))


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
        return jsonify(dict({
            "status": "APP",
            "receipt_number": "TEST_RECEIPT",
            # "receipt_date ": "28-NOV-2017",
            "receipt_date ": datetime.date.today().strftime('%d-%b-%Y'),
            "receipt_amount": 200.00
        }))


def search_for_invoice(invoice_number, pay_bc_reference, check_value):
    logging.warning('invoice_number: ' + invoice_number)
    logging.warning('pay_bc_reference: ' + pay_bc_reference)
    logging.warning('check_value: ' + check_value)
    if invoice_number is not None and check_value is not None and pay_bc_reference is not None:

        # TODO "request.host_url currently returns "http" (not https)
        # As a temporary workaround replace http with https

        # TODO - replace hard code data below with lookup from VIPS API
        if invoice_number == "1234" and check_value == "Smith":
            return dict({
                "items": [
                    {
                        "selected_invoice": {
                            "$ref": request.host_url.replace('http', 'https') + 'api_v2/invoice/1234'
                        }
                    }
                ]
            })
        else:
            return dict({
                "Error": 'An invoice by that number is not found'
            })
    else:
        return dict({
            "Error": 'insufficient data supplied'
        })


def get_invoice(invoice_number):
    if invoice_number == '1234':
        return dict({
            "invoice_number": "RSI_TEST_004",
            "pbc_ref_number": "10008",
            "party_number": 0,
            "party_name": "RSI",
            "account_number": "0",
            "site_number": "0",
            "cust_trx_type": "Review Notice of Driving Prohibition",
            "term_due_date": "2017-03-03T08:00:00Z",
            "total": 200.00,
            "amount_due": 200.00,
            "attribute1": "attribute one",
            "attribute2": "attribute two",
            "attribute3": "attribute three"
        })
    else:
        return dict({
            "error": 'We are unable to find invoice ' + invoice_number
        })
