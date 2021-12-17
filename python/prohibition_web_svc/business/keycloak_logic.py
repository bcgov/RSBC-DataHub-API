import python.prohibition_web_svc.middleware.keycloak_middleware as keycloak_middleware
import python.prohibition_web_svc.http_responses as http_responses
from python.prohibition_web_svc.config import Config


def get_keycloak_user() -> list:
    return [
        {"try": keycloak_middleware.get_authorization_header_from_request, "fail": [
            {"try": http_responses.unauthorized, "fail": []},
        ]},
        {"try": keycloak_middleware.get_token_from_authorization_header, "fail": [
            {"try": http_responses.unauthorized, "fail": []},
        ]},
        {"try": keycloak_middleware.get_keycloak_certificates, "fail": [
            {"try": http_responses.unable_to_retrieve_keycloak_certificates, "fail": []},
        ]},
        {"try": keycloak_middleware.decode_keycloak_access_token, "fail": [
            {"try": http_responses.keycloak_token_not_valid, "fail": []},
        ]},
        {"try": keycloak_middleware.get_username_from_decoded_access_token, "fail": [
            {"try": http_responses.keycloak_no_username, "fail": []},
        ]},
    ]


def get_authorized_keycloak_user() -> list:
    return get_keycloak_user() + [
        {"try": keycloak_middleware.load_roles_and_permissions_from_static_file, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": keycloak_middleware.query_database_for_users_permissions, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": keycloak_middleware.check_user_is_authorized, "fail": [
            {"try": http_responses.unauthorized, "fail": []},
        ]},
    ]


def user_is_an_administrator() -> list:
    return get_keycloak_user() + [

    ]

