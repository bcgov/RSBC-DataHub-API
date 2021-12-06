import python.prohibition_web_service.middleware.role_middleware as role_middleware
import python.prohibition_web_service.middleware.form_middleware as form_middleware
import python.prohibition_web_service.middleware.keycloak_middleware as keycloak_middleware
import python.prohibition_web_service.business.keycloak_logic as keycloak_logic
import python.prohibition_web_service.http_responses as http_responses


def list_any_users_roles() -> list:
    """
    List all user-roles for the admin user
    :return:
    """
    return keycloak_logic.get_keycloak_user() + [
        {"try": keycloak_middleware.load_roles_and_permissions_from_static_file, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": keycloak_middleware.query_database_for_users_permissions, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": keycloak_middleware.check_user_is_authorized, "fail": [
            {"try": http_responses.unauthorized, "fail": []},
        ]},
        {"try": role_middleware.query_all_users_roles, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]}
    ]


def list_my_roles() -> list:
    """
    List the user-roles for the authorized user
    :return:
    """
    return keycloak_logic.get_authorized_keycloak_user() + [
        {"try": role_middleware.query_current_users_roles, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]}
    ]


def create_a_role() -> list:
    """
    Create a new "role-user" for an unauthorized keycloak user.
    :return:
    """
    return keycloak_logic.get_keycloak_user() + [
        {"try": role_middleware.officer_has_not_applied_previously, "fail": [
            {"try": http_responses.role_already_exists, "fail": []},
        ]},
        {"try": role_middleware.create_a_role, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]}
        # TODO - email admin with notice that user has applied
    ]


def update_a_role() -> list:
    """
    Only administrators can update a role-user
    :return:
    """
    return keycloak_logic.get_keycloak_user() + [
        {"try": keycloak_middleware.load_roles_and_permissions_from_static_file, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": keycloak_middleware.query_database_for_users_permissions, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": keycloak_middleware.check_user_is_authorized, "fail": [
            {"try": http_responses.unauthorized, "fail": []},
        ]},
        {"try": role_middleware.approve_officers_role, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
    ]


def admin_create_a_role() -> list:
    """
    Only administrators can update a role-user
    :return:
    """
    return keycloak_logic.get_keycloak_user() + [
        {"try": keycloak_middleware.load_roles_and_permissions_from_static_file, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": keycloak_middleware.query_database_for_users_permissions, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": keycloak_middleware.check_user_is_authorized, "fail": [
            {"try": http_responses.unauthorized, "fail": []},
        ]},
        {"try": form_middleware.request_contains_a_payload, "fail": [
            {"try": http_responses.payload_missing, "fail": []},
        ]},
        {"try": role_middleware.admin_create_role, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
    ]


def delete_a_role() -> list:
    """
    Only administrators can delete a role-user
    :return:
    """
    return keycloak_logic.get_keycloak_user() + [
        {"try": keycloak_middleware.load_roles_and_permissions_from_static_file, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": keycloak_middleware.query_database_for_users_permissions, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": keycloak_middleware.check_user_is_authorized, "fail": [
            {"try": http_responses.unauthorized, "fail": []},
        ]},
        {"try": role_middleware.delete_a_role, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
    ]


def list_all_users() -> list:
    """
    Only administrators list all users
    :return:
    """
    return keycloak_logic.get_keycloak_user() + [
        {"try": keycloak_middleware.load_roles_and_permissions_from_static_file, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": keycloak_middleware.query_database_for_users_permissions, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
        {"try": keycloak_middleware.check_user_is_authorized, "fail": [
            {"try": http_responses.unauthorized, "fail": []},
        ]},
        {"try": role_middleware.query_all_users, "fail": [
            {"try": http_responses.server_error_response, "fail": []},
        ]},
    ]