from python.prohibition_web_svc.business.keycloak_logic import get_authorized_keycloak_user
import python.prohibition_web_svc.middleware.icbc_middleware as icbc_middleware
import python.prohibition_web_svc.http_responses as http_responses
import python.common.splunk as splunk


def get_driver() -> list:
    return get_authorized_keycloak_user() + [
        {"try": icbc_middleware.get_icbc_api_authorization_header, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": icbc_middleware.get_icbc_driver, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": splunk.icbc_get_driver, "fail": []},
    ]


def get_vehicle() -> list:
    return get_authorized_keycloak_user() + [
        {"try": icbc_middleware.get_icbc_api_authorization_header, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": icbc_middleware.is_request_not_seeking_test_plate, "fail": [
            {"try": http_responses.respond_test_vehicle, "fail": []},
        ]},
        {"try": icbc_middleware.get_icbc_vehicle, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": splunk.icbc_get_vehicle, "fail": []}
    ]