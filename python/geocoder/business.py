import python.geocoder.middleware as middleware
import python.common.middleware as tools
import python.geocoder.databc as databc
import python.geocoder.google as google
import python.common.rest as rest


def geocode_address() -> list:
    """

    """
    return [
        {"try": tools.content_type_is_json, "fail": [{"try": rest.failed_validation, "fail": []}]},
        {"try": middleware.retrieve_address_data, "fail": [{"try": rest.failed_validation, "fail": []}]},
        {"try": middleware.clean_up_address, "fail": []},
        {"try": databc.send_query, "fail": []},
        {"try": databc.is_response_valid, "fail": []},
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

