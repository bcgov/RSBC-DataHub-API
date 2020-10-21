import python.common.helper as helper
import python.common.message as message
import python.form_handler.business as business
import pytest
import json


def test_helper_has_add_error_to_message_method():
    message_dict = json.loads('{"event_type": "some invalid event"}')
    expected_error_message = 'error message'
    error_dict = json.loads('{"isSuccess": false, "errors": "error message"}')
    modified_message = message.add_error_to_message(message_dict, error_dict['errors'])
    assert isinstance(modified_message, dict)
    assert 'errors' in modified_message
    assert 'timestamp' in modified_message['errors'][0]
    assert 'description' in modified_message['errors'][0]
    assert modified_message['errors'][0]['description'] == expected_error_message


def test_add_error_to_message_method_handles_cerberus_errors():
    error_message = json.loads('{"fieldA": ["required", "must be string"]}')
    message_dict = 'some string that is not valid JSON'
    error_dict = {'isSuccess': False, 'errors': error_message}
    modified_message = message.add_error_to_message(message_dict, error_dict['errors'])
    assert isinstance(modified_message, dict)
    assert 'errors' in modified_message
    assert 'timestamp' in modified_message['errors'][0]
    assert 'description' in modified_message['errors'][0]


def test_get_listener_functions():
    functions = helper.get_listeners(business.process_incoming_form(), 'prohibition_review')
    assert len(functions) == 19
