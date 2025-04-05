# -*- coding: utf-8 -*-
from __future__ import absolute_import

import flask_restful as restful
import logging
import os
from flask import request, jsonify
from flask_restful import abort
from functools import wraps

from python.vips_mock_svc.vips_mock_svc.config import Config
from python.vips_mock_svc.vips_mock_svc.helper import load_json_into_dict
from ..validators import request_validate, response_filter
from cerberus import Validator


def valid_credentials(username, password) -> bool:
    logging.warning("inside valid_credentials() {} {}".format(username, password))
    return username == Config.BASIC_AUTH_USER and password == Config.BASIC_AUTH_PASS


def require_basic_authentication(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if auth and valid_credentials(auth.username, auth.password):
            return f(*args, **kwargs)
        return abort(401, message="unauthorized")
    return wrapper


def validate(schema):
    def validate_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cerberus = Validator(schema)
            cerberus.allow_unknown = False
            if cerberus.validate(request.json):
                return f(*args, **kwargs)
            logging.warning('payload failed validation')
            return abort(400, message=cerberus.errors)
        return wrapper
    return validate_decorator


class Resource(restful.Resource):

    @staticmethod
    def get_json_data(resource):
        root = os.path.dirname(os.path.abspath(__file__))
        return load_json_into_dict(root + "/data/{}.json".format(resource))

