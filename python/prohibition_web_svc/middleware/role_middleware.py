from flask import jsonify, make_response
import pytz
from datetime import datetime
import logging
from python.prohibition_web_svc.config import Config
from python.prohibition_web_svc.models import db, UserRole


def query_current_users_roles(**kwargs) -> tuple:
    try:
        my_roles = db.session.query(UserRole) \
            .filter(UserRole.username == kwargs['username']) \
            .filter(UserRole.approved_dt != None) \
            .all()
        kwargs['response'] = make_response(jsonify(UserRole.collection_to_dict(my_roles)))
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def query_all_users_roles(**kwargs) -> tuple:
    try:
        user_role = db.session.query(UserRole) \
            .filter(UserRole.username == kwargs.get('requested_username')) \
            .limit(Config.MAX_RECORDS_RETURNED).all()
        kwargs['response'] = make_response(jsonify(UserRole.collection_to_dict(user_role)))
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def officer_has_not_applied_previously(**kwargs) -> tuple:
    try:
        roles = db.session.query(UserRole) \
            .filter(UserRole.role_name == 'officer') \
            .filter(UserRole.username == kwargs.get('username')) \
            .count()
        logging.debug("inside officer_has_not_applied_previously(): " + str(roles))
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return roles == 0, kwargs


def create_a_role(**kwargs) -> tuple:
    tz = pytz.timezone('America/Vancouver')
    try:
        role_user = UserRole("officer", kwargs.get('username'), datetime.now(tz))
        db.session.add(role_user)
        db.session.commit()
        kwargs['response'] = make_response(jsonify(UserRole.serialize(role_user)), 201)
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def approve_officers_role(**kwargs) -> tuple:
    try:
        user_role = db.session.query(UserRole) \
            .filter(UserRole.role_name == 'officer') \
            .filter(UserRole.username == kwargs.get('requested_username')) \
            .first()
        tz = pytz.timezone('America/Vancouver')
        user_role.approved_dt = datetime.now(tz)
        db.session.commit()
        kwargs['response'] = make_response(jsonify(UserRole.serialize(user_role)), 200)
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def delete_a_role(**kwargs) -> tuple:

    try:
        user_role = db.session.query(UserRole) \
            .filter(UserRole.role_name == kwargs.get('role_name')) \
            .filter(UserRole.username == kwargs.get('requested_username')) \
            .first()
        db.session.delete(user_role)
        db.session.commit()
        kwargs['response'] = make_response("okay", 200)
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def admin_create_role(**kwargs) -> tuple:
    payload = kwargs.get('payload')
    try:
        tz = pytz.timezone('America/Vancouver')
        current_dt = datetime.now(tz)
        role_user = UserRole(payload.get('role_name'),
                             kwargs.get('requested_username'),
                             current_dt,
                             current_dt)
        db.session.add(role_user)
        db.session.commit()
        kwargs['response'] = make_response(jsonify(UserRole.serialize(role_user)), 201)
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def query_all_users(**kwargs) -> tuple:
    try:
        user_role = db.session.query(UserRole).limit(Config.MAX_RECORDS_RETURNED).all()
        kwargs['response'] = make_response(jsonify(UserRole.collection_to_dict(user_role)))
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs
