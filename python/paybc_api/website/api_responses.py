import logging
import logging.config
from flask import make_response, jsonify
from python.paybc_api.website.config import Config

logging.config.dictConfig(Config.LOGGING)


def payment_incomplete(**args) -> tuple:
    args['response'] = make_response({'status': 'INCMP'}, 400)
    return True, args


def payment_success(**args) -> tuple:
    payload = args.get('payload')
    args['response'] = make_response(dict({
        "status": "APP",
        "receipt_number": payload['receipt_number'],
        "receipt_date": payload['receipt_date'],
        "receipt_amount": payload['receipt_amount']
    }), 200)
    return True, args


def get_prohibition_success(**args) -> tuple:
    presentation_type = args.get('presentation_type')
    amount_due = args.get('amount_due')
    service_date = args.get('service_date')
    args['response'] = make_response(dict({
                "invoice_number": args.get('prohibition_number'),
                "pbc_ref_number": "10008",
                "party_number": 0,
                "party_name": "n/a",
                "account_number": "n/a",
                "site_number": "0",
                "cust_trx_type": "Review Notice of Driving Prohibition",
                "term_due_date": service_date.isoformat(),
                "total": amount_due,
                "amount_due": amount_due,
                "attribute1": args.get('notice_type_verbose'),
                "attribute2": service_date.strftime("%b %-d, %Y"),
                "attribute3": presentation_type,
                "amount": amount_due
            }), 200)
    return True, args


def search_prohibition_success(**args) -> tuple:
    request = args.get('request')
    host_url = request.host_url.replace('http', 'https')
    args['response'] = jsonify({
                "items": [{"selected_invoice": {
                       "$ref": host_url + 'api_v2/invoice/' + args.get('prohibition_number')}
                    }
                ]
            })
    return True, args

