import python.common.middleware as middleware
import python.common.rsi_email as rsi_email
import python.common.actions as actions
import python.paybc_api.website.api_responses as api_responses
import python.common.splunk_application_for_review as splunk
import python.common.splunk as common_splunk


def search_for_invoice() -> list:
    """
    An application is ready for payment when the:
        - the prohibition is found in VIPS
        - the name provided by the user matches the driver's name in VIPS
        - an application has been saved in VIPS
        - the window to apply (if applicable) has not expired
    """
    return [
        {"try": middleware.determine_current_datetime, "fail": []},
        {"try": middleware.clean_prohibition_number, "fail": []},
        {"try": middleware.validate_prohibition_number, "fail": []},
        {"try": splunk.paybc_lookup, "fail": []},
        {"try": common_splunk.log_to_splunk, "fail": []},
        {"try": middleware.get_vips_status, "fail": []},
        {"try": middleware.prohibition_exists_in_vips, "fail": []},
        {"try": middleware.user_submitted_last_name_matches_vips, "fail": []},
        {"try": middleware.application_has_been_saved_to_vips, "fail": []},
        {"try": middleware.application_not_paid, "fail": []},
        {"try": middleware.is_applicant_within_window_to_pay, "fail": []},
        {"try": api_responses.search_prohibition_success, "fail": []},
    ]


def generate_invoice() -> list:
    """
    An application is ready for payment when the:
        - the prohibition is found in VIPS
        - the name provided by the user matches the driver's name in VIPS
        - an application has been saved in VIPS
        - the window to apply (if applicable) has not expired
    """
    return [
        {"try": middleware.determine_current_datetime, "fail": []},
        {"try": middleware.clean_prohibition_number, "fail": []},
        {"try": middleware.validate_prohibition_number, "fail": []},
        {"try": middleware.get_vips_status, "fail": []},
        {"try": middleware.prohibition_exists_in_vips, "fail": []},
        {"try": middleware.application_has_been_saved_to_vips, "fail": []},
        {"try": middleware.application_not_paid, "fail": []},
        {"try": middleware.is_applicant_within_window_to_pay, "fail": []},
        {"try": middleware.get_application_details, "fail": []},
        {"try": middleware.valid_application_received_from_vips, "fail": []},
        {"try": middleware.get_invoice_details, "fail": []},
        {"try": api_responses.get_prohibition_success, "fail": []},
        {"try": splunk.paybc_invoice_generated, "fail": []},
        {"try": common_splunk.log_to_splunk, "fail": []},
    ]


def save_payment() -> list:
    """
    PayBC has successfully processed the applicant's credit card details and
    is now posting the payment details to our API.  In the event that PayBC
    does not receive a successful response, PayBC will try again indefinitely.
    """
    return [
        {"try": middleware.validate_pay_bc_post_receipt, "fail": []},
        {"try": middleware.get_vips_status, "fail": []},
        {"try": middleware.prohibition_exists_in_vips, "fail": []},
        {"try": middleware.application_has_been_saved_to_vips, "fail": []},
        {"try": middleware.application_not_paid, "fail": [
            # If VIPS says the application is paid, tell PayBC that the payment was successful.
            # Likely PayBC didn't receive the initial successful response and is trying again
            {"try": middleware.get_application_details, "fail": []},
            {"try": middleware.valid_application_received_from_vips, "fail": []},
            {"try": middleware.get_invoice_details, "fail": []},
            {"try": middleware.transform_receipt_date_from_pay_bc_format, "fail": []},
            {"try": middleware.payment_success, "fail": []},
            {"try": splunk.review_fee_paid, "fail": []},
            {"try": rsi_email.applicant_to_schedule_review, "fail": []},
            {"try": middleware.create_verify_schedule_event, "fail": []},
            {"try": actions.add_hold_to_verify_schedule, "fail": []},
            {"try": actions.add_to_hold_queue, "fail": []},
            {"try": api_responses.payment_success, "fail": []}
        ]},
        {"try": middleware.get_application_details, "fail": []},
        {"try": middleware.valid_application_received_from_vips, "fail": []},
        {"try": middleware.get_invoice_details, "fail": []},
        {"try": middleware.transform_receipt_date_from_pay_bc_format, "fail": []},
        {"try": middleware.save_payment_to_vips, "fail": []},
        {"try": middleware.payment_success, "fail": []},
        {"try": splunk.review_fee_paid, "fail": []},
        {"try": common_splunk.log_to_splunk, "fail": []},
        {"try": rsi_email.applicant_to_schedule_review, "fail": []},
        {"try": middleware.create_verify_schedule_event, "fail": []},
        {"try": actions.add_hold_to_verify_schedule, "fail": []},
        {"try": actions.add_to_hold_queue, "fail": []},
        {"try": api_responses.payment_success, "fail": []}
    ]
