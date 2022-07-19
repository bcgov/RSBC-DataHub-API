from flask import make_response
import logging


def successful_create_response(**kwargs) -> tuple:
    response_dict = kwargs.get('response_dict', {
        "message": "create successful"
    })
    kwargs['response'] = make_response(response_dict, 201)
    return True, kwargs


def successful_update_response(**kwargs) -> tuple:
    response_dict = kwargs.get('response_dict', {
        "message": "update successful"
    })
    kwargs['response'] = make_response(response_dict, 200)
    return True, kwargs


def server_error_response(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'server error'}, 500)
    return True, kwargs


def bad_request_response(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'bad request'}, 400)
    return True, kwargs


def record_not_found(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'record not found'}, 404)
    return True, kwargs


def unauthorized(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'unauthorized'}, 401)
    return True, kwargs


def unable_to_retrieve_keycloak_certificates(**kwargs) -> tuple:
    logging.warning("unable to retrieve keycloak certificates")
    kwargs['response'] = make_response({'error': 'unable to retrieve keycloak certificates'}, 500)
    return True, kwargs


def keycloak_token_not_valid(**kwargs) -> tuple:
    logging.warning("keycloak access token not valid")
    kwargs['response'] = make_response({'error': 'token not valid'}, 401)
    return True, kwargs


def keycloak_no_username(**kwargs) -> tuple:
    logging.warning("decoded keycloak token has no username")
    kwargs['response'] = make_response({'error': 'server error'}, 500)
    return True, kwargs


def no_user_guid(**kwargs) -> tuple:
    logging.warning("decoded keycloak token has no user_guid")
    kwargs['response'] = make_response({'error': 'server error'}, 500)
    return True, kwargs


def role_already_exists(**kwargs) -> tuple:
    logging.warning("role for {} already exists".format(kwargs.get('username')))
    kwargs['response'] = make_response({'error': 'role already exists'}, 400)
    return True, kwargs


def user_already_exists(**kwargs) -> tuple:
    logging.warning("user for {} already exists".format(kwargs.get('username')))
    kwargs['response'] = make_response({'error': 'user already exists'}, 400)
    return True, kwargs


def payload_missing(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'missing payload'}, 403)
    return True, kwargs


def failed_validation(**kwargs) -> tuple:
    kwargs['response'] = make_response({
        'message': 'failed validation',
        'errors': kwargs.get('validation_errors')
    }, 400)
    return True, kwargs


def no_payload(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'no payload'}, 400)
    return True, kwargs


def cannot_access_users_at_another_agency(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'you cannot access or update users at a different agency'}, 400)
    return True, kwargs


def cannot_create_user_roles(**kwargs) -> tuple:
    roles = kwargs.get('requested_roles')
    kwargs['response'] = make_response({
        'error': 'insufficient permissions to create user with these roles: {}'.format(", ".join(roles))
    }, 400)
    return True, kwargs


def cannot_access_another_user_data(**kwargs) -> tuple:
    kwargs['response'] = make_response({"error": "you cannot access another user's data"}, 400)
    return True, kwargs


def cannot_change_user_guid(**kwargs) -> tuple:
    kwargs['response'] = make_response({"error": "You cannot change the user guid; create a new user instead"}, 400)
    return True, kwargs


def cannot_change_business_guid(**kwargs) -> tuple:
    kwargs['response'] = make_response({"error": "You cannot change the business guid; create a new user instead"}, 400)
    return True, kwargs
