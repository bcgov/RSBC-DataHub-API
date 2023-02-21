from flask import jsonify, make_response
from cerberus import Validator
from cerberus import errors
import logging
import json
from datetime import datetime
import pytz
from python.prohibition_web_svc.models import db, User, UserRole

class CustomErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.REGEX_MISMATCH.code] = "must be 2 letters + 2-4 digits OR 6 digits (HRMIS)"

def user_has_not_applied_previously(**kwargs) -> tuple:
    try:
        user_count = db.session.query(User) \
            .filter(User.user_guid == kwargs.get('user_guid')) \
            .count()
        logging.debug("inside user_has_not_applied_previously(): " + str(user_count))
        if user_count:
            logging.warning('user already exists: ' + str(user_count))
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return user_count == 0, kwargs


def does_role_already_exist(**kwargs) -> tuple:
    try:
        user_role_count = db.session.query(UserRole) \
            .filter(UserRole.user_guid == kwargs.get('user_guid')) \
            .count()
        logging.debug("inside does_role_already_exist(): " + str(user_role_count))
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return user_role_count != 0, kwargs


def update_the_user(**kwargs) -> tuple:
    try:
        user = db.session.query(User) \
            .filter(User.user_guid == kwargs.get('user_guid')) \
            .first()
        user.username = kwargs.get('username')
        user.user_guid = kwargs.get('user_guid')
        user.badge_number = kwargs.get('payload')['badge_number']
        user.agency = kwargs.get('payload')['agency']
        user.first_name = kwargs.get('payload')['first_name']
        user.last_name = kwargs.get('payload')['last_name']
        db.session.commit()
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def create_a_user(**kwargs) -> tuple:
    try:
        user = User(
            username=kwargs.get('username'),
            user_guid=kwargs.get('user_guid'),
            business_guid=kwargs.get('business_guid'),
            badge_number=kwargs.get('payload')['badge_number'],
            agency=kwargs.get('payload')['agency'],
            first_name=kwargs.get('payload')['first_name'],
            last_name=kwargs.get('payload')['last_name']
        )
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def create_user_role(**kwargs) -> tuple:
    tz = pytz.timezone("America/Vancouver")
    now = datetime.now(tz)
    try:
        requested_role = UserRole(
            user_guid=kwargs.get('user_guid'),
            role_name="officer",
            submitted_dt=now
        )
        db.session.add(requested_role)
        db.session.commit()
        kwargs['response'] = make_response(jsonify(UserRole.serialize(requested_role)), 201)
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def request_contains_a_payload(**kwargs) -> tuple:
    request = kwargs.get('request')
    try:
        payload = request.get_json()
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    kwargs['payload'] = payload
    logging.warning("payload: " + json.dumps(payload))
    return payload is not None, kwargs

def validate_create_user_payload(**kwargs) -> tuple:
    schema = {
        "badge_number": {
            "type": "string",
            "regex": "^([A-Z]{2}\d{2,4})|(\d{6})$",
            "required": True
        },
        "agency": {
            "type": "string",
            'minlength': 5,
            'maxlength': 30,
            "required": True
        },
        "first_name": {
            "type": "string",
            'minlength': 2,
            'maxlength': 30,
            "required": True
        },
        "last_name": {
            "type": "string",
            'minlength': 2,
            'maxlength': 30,
            "required": True
        }
    }
    cerberus = Validator(schema, error_handler=CustomErrorHandler)
    cerberus.allow_unknown = False
    if cerberus.validate(kwargs.get('payload')):
        return True, kwargs
    logging.warning("validation error: " + json.dumps(cerberus.errors))
    kwargs['validation_errors'] = cerberus.errors
    return False, kwargs

def get_user(**kwargs) -> tuple:
    try:
        user = db.session.query(User) \
            .filter(User.user_guid == kwargs.get('user_guid')) \
            .first()
        db.session.commit()
        kwargs['response'] = make_response(jsonify(User.serialize(user)), 200)
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs
