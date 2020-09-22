import python.common.middleware as middleware
import python.common.rsi_email as rsi_email


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
        {"try": middleware.validate_prohibition_number, "fail": []},
        {"try": middleware.update_vips_status, "fail": []},
        {"try": middleware.prohibition_exists_in_vips, "fail": []},
        {"try": middleware.user_submitted_last_name_matches_vips, "fail": []},
        {"try": middleware.application_has_been_saved_to_vips, "fail": []},
        {"try": middleware.application_not_paid, "fail": []},
        {"try": middleware.date_served_not_older_than_one_week, "fail": []},
    ]


def generate_invoice() -> list:
    """
    An application is ready for invoicing when it's ready for payment plus:
        -
    """
    return [
        {"try": middleware.create_correlation_id, "fail": []},
        {"try": middleware.validate_prohibition_number, "fail": []},
        {"try": middleware.update_vips_status, "fail": []},
        {"try": middleware.prohibition_exists_in_vips, "fail": []},
        {"try": middleware.application_has_been_saved_to_vips, "fail": []},
        {"try": middleware.application_not_paid, "fail": []},
        {"try": middleware.date_served_not_older_than_one_week, "fail": []},
        {"try": middleware.get_application_details, "fail": []},
        {"try": middleware.valid_application_received_from_vips, "fail": []},
        {"try": middleware.get_invoice_details, "fail": []},
    ]


def save_payment() -> list:
    return [
        {"try": middleware.create_correlation_id, "fail": []},
        {"try": middleware.validate_pay_bc_post_receipt, "fail": []},
        {"try": middleware.update_vips_status, "fail": []},
        {"try": middleware.prohibition_exists_in_vips, "fail": []},
        {"try": middleware.application_has_been_saved_to_vips, "fail": []},
        {"try": middleware.application_not_paid, "fail": []},
        {"try": middleware.get_application_details, "fail": []},
        {"try": middleware.valid_application_received_from_vips, "fail": []},
        {"try": middleware.get_invoice_details, "fail": []},
        {"try": middleware.transform_receipt_date_from_pay_bc_format, "fail": []},
        {"try": middleware.save_payment_to_vips, "fail": []},
        {"try": rsi_email.applicant_to_schedule_review, "fail": []},
        ]
