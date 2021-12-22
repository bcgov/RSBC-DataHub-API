import logging
from flask import make_response, jsonify
from python.paybc_api.website.config import Config

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


def payment_incomplete(**args):
    return make_response(dict({"status": "INCMP"}), 400)


def payment_success(**args):
    payload = args.get('payload')
    return jsonify(dict({
        "status": "APP",
        "receipt_number": payload['receipt_number'],
        "receipt_date": payload['receipt_date'],
        "receipt_amount": payload['receipt_amount']
    }))
