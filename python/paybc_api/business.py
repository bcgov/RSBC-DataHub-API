import python.common.middleware as middleware
import python.common.rsi_email as rsi_email
import python.paybc_api.website.api_responses as api


def search_for_invoice() -> list:
    """
    An application is ready for payment when the:
        - the prohibition is found in VIPS
        - the name provided by the user matches the driver's name in VIPS
        - an application has been saved in VIPS
        - the window to apply (if applicable) has not expired
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
        {"try": middleware.application_not_paid, "fail": []},
        {"try": middleware.is_applicant_within_window_to_apply, "fail": []},
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
        {"try": middleware.create_correlation_id, "fail": []},
        {"try": middleware.determine_current_datetime, "fail": []},
        {"try": middleware.clean_prohibition_number, "fail": []},
        {"try": middleware.validate_prohibition_number, "fail": []},
        {"try": middleware.get_vips_status, "fail": []},
        {"try": middleware.prohibition_exists_in_vips, "fail": []},
        {"try": middleware.application_has_been_saved_to_vips, "fail": []},
        {"try": middleware.application_not_paid, "fail": []},
        {"try": middleware.is_applicant_within_window_to_apply, "fail": []},
        {"try": middleware.get_application_details, "fail": []},
        {"try": middleware.valid_application_received_from_vips, "fail": []},
        {"try": middleware.get_invoice_details, "fail": []},
    ]


def save_payment() -> list:
    """
    PayBC has successfully processed the applicant's credit card details and
    is now posting the payment details to our API.  In the event that PayBC
    does not receive a successful response, PayBC will try again indefinitely.
    """
    return [
        {"try": middleware.create_correlation_id, "fail": []},
        {"try": middleware.validate_pay_bc_post_receipt, "fail": []},
        {"try": middleware.get_vips_status, "fail": []},
        {"try": middleware.prohibition_exists_in_vips, "fail": []},
        {"try": middleware.application_not_paid, "fail": [
            # If VIPS says the application is paid, tell PayBC that the payment was successful.
            # Likely PayBC didn't receive the initial successful response and is trying again
            # TODO - send email to applicant to schedule review
            #  needs to be tested to make sure all information has been received for the email
            {"try": middleware.payment_success, "fail": []},
        ]},
        {"try": middleware.application_has_been_saved_to_vips, "fail": []},
        {"try": middleware.get_application_details, "fail": []},
        {"try": middleware.valid_application_received_from_vips, "fail": []},
        {"try": middleware.get_invoice_details, "fail": []},
        {"try": middleware.transform_receipt_date_from_pay_bc_format, "fail": []},
        {"try": middleware.save_payment_to_vips, "fail": []},
        {"try": middleware.payment_success, "fail": []},
        {"try": rsi_email.applicant_to_schedule_review, "fail": []},
        {"try": api.payment_success, "fail": []},
    ]
