import python.common.middleware as middleware
import python.common.actions as actions
import python.common.rsi_email as rsi_email
import python.common.rest as rest


def get_available_time_slots() -> list:
    """
    An application is ready for scheduling when all the payment rules are satisfied plus:
        - the application has been paid
        - the window to schedule the review has not elapsed
    """
    return [
        {"try": middleware.create_correlation_id, "fail": []},
        {"try": middleware.determine_current_datetime, "fail": []},
        {"try": middleware.clean_prohibition_number, "fail": []},
        {"try": middleware.validate_prohibition_number, "fail": []},
        {"try": middleware.get_vips_status, "fail": []},
        {"try": middleware.prohibition_exists_in_vips, "fail": []},
        {"try": middleware.user_submitted_last_name_matches_vips, "fail": []},
        {"try": middleware.application_has_been_saved_to_vips, "fail": []},

        {"try": middleware.get_payment_status, "fail": []},
        {"try": middleware.received_valid_payment_status, "fail": []},
        {"try": middleware.paid_not_more_than_24hrs_ago, "fail": []},

        {"try": middleware.application_has_been_paid, "fail": []},
        {"try": middleware.review_has_not_been_scheduled, "fail": []},
        {"try": middleware.get_application_details, "fail": []},
        {"try": middleware.valid_application_received_from_vips, "fail": []},
        {"try": middleware.get_invoice_details, "fail": []},
        {"try": middleware.calculate_schedule_window, "fail": []},
        {"try": middleware.query_review_times_available, "fail": []},
        {"try": middleware.does_applicant_have_enough_review_options, "fail": [
            {"try": middleware.query_for_additional_review_times, "fail": []},
            {"try": middleware.does_applicant_have_enough_review_options, "fail": [
                {"try": rsi_email.insufficient_reviews_available, "fail": []},
            ]}
        ]},
       ]


def ingest_form() -> list:
    return [
        {"try": middleware.content_type_is_xml, "fail": [
            {"try": rest.failed_validation, "fail": []},
        ]},
        {"try": middleware.content_length_within_bounds, "fail": [
            {"try": rest.failed_validation, "fail": []},
        ]},
        {"try": middleware.form_name_provided, "fail": [
            {"try": rest.failed_validation, "fail": []},
        ]},
        {"try": middleware.validate_form_name, "fail": [
            {"try": rest.failed_validation, "fail": []},
        ]},
        {"try": middleware.add_encrypt_at_rest_attribute, "fail": []},
        {"try": middleware.convert_xml_to_dictionary_object, "fail": [
            {"try": rest.server_error, "fail": []},
        ]},
        {"try": middleware.get_xml_from_request, "fail": []},
        {"try": middleware.base_64_encode_xml, "fail": []},
        {"try": middleware.create_form_payload, "fail": []},
        {"try": middleware.encode_payload, "fail": []},
        {"try": middleware.get_queue_name_from_parameters, "fail": []},
        {"try": actions.add_to_rabbitmq_queue, "fail": [
            {"try": rest.server_error, "fail": []},
        ]},
        # Useful for debugging: {"try": rsi_email.send_form_xml_to_admin, "fail": []},
        {"try": rest.okay, "fail": []}
       ]


def is_okay_to_submit_evidence() -> list:
    """
    Check to determine if an applicant can upload / submit evidence.
    To submit evidence an applicant must have:
     - submitted an application,
     - paid for a review,
     - scheduled a review date and
     - the review date must be at 24 hours in the future
    """
    return [
        {"try": middleware.create_correlation_id, "fail": []},
        {"try": middleware.determine_current_datetime, "fail": []},
        {"try": middleware.clean_prohibition_number, "fail": []},
        {"try": middleware.validate_prohibition_number, "fail": []},
        {"try": middleware.get_vips_status, "fail": []},
        {"try": middleware.prohibition_exists_in_vips, "fail": []},
        {"try": middleware.user_submitted_last_name_matches_vips, "fail": []},
        {"try": middleware.application_has_been_saved_to_vips, "fail": []},
        {"try": middleware.application_has_been_paid, "fail": []},
        {"try": middleware.review_has_been_scheduled, "fail": []},
        {"try": middleware.is_review_more_than_48_hours_in_the_future, "fail": []}
       ]
