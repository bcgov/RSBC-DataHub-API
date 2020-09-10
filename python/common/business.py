import python.common.middleware as middleware


def basic_middleware_checks() -> list:
    return [
        {"try": middleware.create_correlation_id, "fail": []},
        {"try": middleware.validate_prohibition_number, "fail": []},
        {"try": middleware.update_vips_status, "fail": []},
        {"try": middleware.prohibition_exists_in_vips, "fail": []},
    ]


def ready_for_payment() -> list:
    """
    An application is ready for payment when the:
        - the prohibition is found in VIPS
        - the name provided by the user matches the driver's name in VIPS
        - an application has been saved in VIPS
        - the window to apply (if applicable) has not expired
    """
    return basic_middleware_checks() + [
        {"try": middleware.user_submitted_last_name_matches_vips, "fail": []},
        {"try": middleware.application_has_been_submitted, "fail": []},
        {"try": middleware.application_not_paid, "fail": []},
        {"try": middleware.date_served_not_older_than_one_week, "fail": []},
    ]


def ready_for_invoicing() -> list:
    """
    An application is ready for invoicing when it's ready for payment plus:
        -
    """
    return basic_middleware_checks() + [
        {"try": middleware.application_has_been_submitted, "fail": []},
        {"try": middleware.application_not_paid, "fail": []},
        {"try": middleware.date_served_not_older_than_one_week, "fail": []},
        {"try": middleware.get_application_details, "fail": []},
        {"try": middleware.valid_application_received_from_vips, "fail": []},
        {"try": middleware.get_invoice_details, "fail": []},
    ]


def ready_for_scheduling() -> list:
    """
    An application is ready for scheduling when all the payment rules are satisfied plus:
        - the application has been paid
        - the window to schedule the review has not elapsed
    """
    return ready_for_payment() + [
        {"try": middleware.application_has_been_paid, "fail": []},
        {"try": middleware.get_application_details, "fail": []},
        {"try": middleware.valid_application_received_from_vips, "fail": []},
        {"try": middleware.get_invoice_details, "fail": []},
       # {"try": middleware.calculate_schedule_window, "fail": []},
       # {"try": middleware.max_schedule_date_has_not_elapsed, "fail": []},
        ]
