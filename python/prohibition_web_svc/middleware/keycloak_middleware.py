import logging
import jwt
import json
from python.common.helper import load_json_into_dict
from python.prohibition_web_svc.models import db, UserRole
from python.prohibition_web_svc.config import Config


def get_authorization_header_from_request(**kwargs) -> tuple:
    request = kwargs.get('request')
    try:
        kwargs['auth_header'] = request.headers.get('Authorization').split(" ")
    except Exception as e:
        return False, kwargs
    return len(kwargs.get('auth_header')) == 2, kwargs


def get_token_from_authorization_header(**kwargs) -> tuple:
    auth_header = kwargs.get('auth_header')
    try:
        kwargs['access_token'] = auth_header[1]
    except Exception as e:
        kwargs['error'] = "keycloak authorization header is not valid: " + str(e)
        return False, kwargs
    return auth_header[0] == 'Bearer' and kwargs['access_token'] is not None, kwargs


def get_keycloak_certificates(**kwargs) -> tuple:
    try:
        jwks_client = jwt.PyJWKClient(Config.KEYCLOAK_CERTS_URL)
        kwargs['signing_key'] = jwks_client.get_signing_key_from_jwt(kwargs.get('access_token')).key
    except Exception as e:
        kwargs['error'] = str(e)
        return False, kwargs
    return True, kwargs


def decode_keycloak_access_token(**kwargs) -> tuple:
    access_token = kwargs.get('access_token')
    signing_key = kwargs.get('signing_key')
    try:
        kwargs['decoded_access_token'] = jwt.decode(access_token,
                                                    signing_key,
                                                    algorithms=[Config.KEYCLOAK_ALGORITHM],
                                                    audience=Config.KEYCLOAK_CLIENT_ID)
    except Exception as e:
        logging.warning(str(e))
        return False, kwargs
    return True, kwargs


def get_username_from_decoded_access_token(**kwargs) -> tuple:
    decoded_access_token = kwargs.get('decoded_access_token')
    try:
        kwargs['username'] = decoded_access_token['preferred_username']
        kwargs['display_name'] = decoded_access_token['display_name']
        kwargs['identity_provider'] = decoded_access_token['identity_provider']
        logging.debug("username and identity_provider from access token: " +  kwargs.get('username') + kwargs.get('identity_provider'))
        if decoded_access_token.get('bceid_user_guid'):
            logging.debug('BCeID user')
            kwargs['bceid_username'] = decoded_access_token['bceid_username']
            kwargs['login'] = str(kwargs.get('bceid_username', '')) + '@' + str(kwargs.get('identity_provider', ''))
        if decoded_access_token.get('idir_user_guid'):
            logging.debug('IDIR user')
            kwargs['idir_username'] = decoded_access_token['idir_username']
            kwargs['login'] = str(kwargs.get('idir_username', '')) + '@' + str(kwargs.get('identity_provider', ''))
        logging.debug("login id from access token: " +  kwargs.get('login'))
    except Exception as e:
        kwargs['error'] = "preferred_username or login not present in decoded access token: " + str(e)
        return False, kwargs
    return True, kwargs


def get_user_guid_from_decoded_access_token(**kwargs) -> tuple:
    decoded_access_token = kwargs.get('decoded_access_token')
    if decoded_access_token.get('bceid_user_guid'):
        logging.debug('BCeID user')
        kwargs['business_guid'] = decoded_access_token.get('bceid_business_guid')
        kwargs['user_guid'] = kwargs.get('username')
        # kwargs['user_guid'] = decoded_access_token.get('bceid_user_guid')
        return True, kwargs
    if decoded_access_token.get('idir_user_guid'):
        logging.debug('IDIR user')
        kwargs['user_guid'] = kwargs.get('username')
        # kwargs['user_guid'] = decoded_access_token.get('idir_user_guid')
        return True, kwargs
    logging.debug('Github user? - no user GUID')
    kwargs['user_guid'] = kwargs.get('username')
    if kwargs['user_guid']:
        return True, kwargs
    return False, kwargs


def load_roles_and_permissions_from_static_file(**kwargs) -> tuple:
    permissions = load_json_into_dict("python/prohibition_web_svc/data/permissions.json")
    kwargs['permissions'] = permissions
    return permissions is not None, kwargs


def check_user_is_authorized(**kwargs) -> tuple:
    username = kwargs.get('username')
    required_permission = kwargs.get('required_permission', None)
    permissions = kwargs.get('permissions')
    user_roles = kwargs.get('user_roles')
    logging.debug("inside check_user_is_authorized() {} {} {}".format(username, required_permission, "|".join(user_roles)))
    for role in user_roles:
        logging.debug("if {} in {}".format(required_permission, json.dumps(permissions[role])))
        if required_permission in permissions[role]['permissions']:
            return True, kwargs
    return False, kwargs


def query_database_for_users_permissions(**kwargs) -> tuple:
    logging.debug("inside query_database_for_users_permissions()")
    try:
        kwargs['user_roles'] = UserRole.get_roles(kwargs.get('user_guid'))
    except Exception as e:
        logging.warning("error while querying database for user permissions: " + str(e))
        return False, kwargs
    return True, kwargs

