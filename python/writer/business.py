import python.writer.database as database
import python.writer.middleware as middleware


def process_ekt_events() -> dict:
    """
    This function lists the business rules required when processing
    each etk payloads.
    """
    return {
        "evt_issuance": [
            {"try": middleware.get_address_from_message, "fail": []},
            {"try": middleware.clean_up_address, "fail": []},
            {"try": middleware.build_payload_to_send_to_geocoder, "fail": []},
            {"try": middleware.callout_to_geocoder_api, "fail": [
                # TODO - add error to message
                {"try": middleware.publish_to_fail_queue, "fail": []},
            ]},
            {"try": middleware.transform_geocoder_response, "fail": []},
            {"try": middleware.add_geolocation_data_to_message, "fail": []},
            {"try": database.write, "fail": [
                {"try": middleware.publish_to_fail_queue, "fail": []},
            ]},
        ],
        "vt_query": [
            {"try": database.write, "fail": [
                {"try": middleware.publish_to_fail_queue, "fail": []},
            ]},
        ],
        "vt_payment": [
            {"try": database.write, "fail": [
                {"try": middleware.publish_to_fail_queue, "fail": []},
            ]},
        ],
        "vt_dispute": [
            {"try": database.write, "fail": [
                {"try": middleware.publish_to_fail_queue, "fail": []},
            ]},
        ],
        "vt_dispute_status_update": [
            {"try": database.write, "fail": [
                {"try": middleware.publish_to_fail_queue, "fail": []},
            ]},
        ],
        "vt_dispute_finding": [
            {"try": database.write, "fail": [
                {"try": middleware.publish_to_fail_queue, "fail": []},
            ]},
        ],
    }
