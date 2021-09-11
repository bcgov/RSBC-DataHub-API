from flask import make_response


def successful_create_response(**kwargs) -> tuple:
    response_dict = kwargs.get('response_dict')
    kwargs['response'] = make_response(response_dict, 201)
    return True, kwargs


def successful_update_response(**kwargs) -> tuple:
    response_dict = kwargs.get('response_dict')
    kwargs['response'] = make_response(response_dict, 200)
    return True, kwargs


def server_error_response(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'server error'}, 500)
    return True, kwargs


def bad_request_response(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'bad request'}, 400)
    return True, kwargs