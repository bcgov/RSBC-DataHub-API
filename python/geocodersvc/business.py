import python.geocodersvc.middleware as middleware
import python.geocodersvc.middleware as tools
import python.geocodersvc.databc as databc
import python.geocodersvc.google as google
import python.geocodersvc.rest as rest


def geocode_address() -> list:
    """

    """
    return [
        {"try": tools.content_type_is_json, "fail": [
            {"try": rest.not_json, "fail": []}
        ]},
        {"try": middleware.retrieve_address_data, "fail": [
            {"try": rest.failed_validation, "fail": []}
        ]},
        {"try": databc.send_query, "fail": [
            {"try": middleware.generate_error_response, "fail": []}
        ]},
        {"try": databc.is_response_valid, "fail": [
            {"try": middleware.generate_error_response, "fail": []}
        ]},
        {"try": databc.is_confidence_too_low, "fail": [
            {"try": middleware.generate_data_bc_only_response, "fail": []},
        ]},
        {"try": middleware.is_google_fail_over_enabled, "fail": [
            {"try": middleware.generate_data_bc_only_response, "fail": []},
        ]},
        {"try": middleware.is_google_api_key_provided, "fail": []},

        {"try": google.send_query, "fail": []},
        {"try": google.is_response_valid, "fail": []},
        {"try": google.is_confidence_too_low, "fail": [
            {"try": middleware.generate_data_bc_revert_response, "fail": []},
        ]},
        {"try": middleware.generate_google_and_data_bc_response, "fail": []},
       ]


def determine_ready_status() -> list:
    """
    Business rules to determine if the Geocoder service is ready
    """
    return [
        {"try": databc.send_query, "fail": [
            {"try": middleware.generate_error_response, "fail": []}
        ]},
        {"try": databc.is_response_valid, "fail": [
            {"try": rest.geocoder_error, "fail": []}
        ]},
        {"try": rest.ready_response, "fail": []}
       ]

