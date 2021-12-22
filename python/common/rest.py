from flask import jsonify
import logging


def failed_validation(**args) -> tuple:
    return _common_error_function(422, **args)


def server_error(**args) -> tuple:
    # override the error string, we don't want to share too much
    args['error_string'] = 'something went wrong'
    return _common_error_function(500, **args)


def okay(**args) -> tuple:
    config = args.get('config')
    if getattr(logging, config.LOG_LEVEL) < 30:
        args['response'] = jsonify(
            {
                "success": True,
                "payload": args.get('payload')
            }), 200
    else:
        args['response'] = jsonify({"success": True}), 200
    return True, args


def _common_error_function(http_status_code: int, **args) -> tuple:
    error_string = args.get('error_string')
    args['response'] = jsonify({"error": error_string}), http_status_code
    return False, args

