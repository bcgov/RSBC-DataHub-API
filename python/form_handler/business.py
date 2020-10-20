import python.common.middleware as middleware
import python.common.actions as actions
import python.common.rsi_email as rsi_email


def process_incoming_form() -> dict:
    return {
        "unknown_event": [
            {"try": actions.add_unknown_event_error_to_message, "fail": []},
            {"try": actions.add_to_failed_queue, "fail": []},
            {"try": rsi_email.admin_unknown_event_type, "fail": []}
        ],
        "send_disclosure": [
            {
                "try": actions.is_not_on_hold,
                "fail": [
                    {"try": actions.add_to_hold_queue, "fail": []}
                ]
            },
            {"try": middleware.get_data_from_disclosure_event, "fail": []},
            {"try": middleware.determine_current_datetime, "fail": []},

            {"try": middleware.create_correlation_id, "fail": []},
            {"try": middleware.determine_current_datetime, "fail": []},
            {"try": middleware.get_vips_status, "fail": []},
            {"try": middleware.prohibition_exists_in_vips, "fail": []},
            {"try": middleware.is_review_in_the_future, "fail": [
                # No further disclosure will be sent. The review has concluded.
            ]},
            {"try": middleware.is_any_unsent_disclosure, "fail": [
                # No new disclosure to send at present, try again later
                {"try": actions.add_hold_before_sending_disclosure, "fail": []},
                {"try": actions.add_to_hold_queue, "fail": []}
            ]},
            {"try": middleware.retrieve_unsent_disclosure, "fail": []},
            {"try": middleware.if_required_add_adp_disclosure, "fail": []},
            {"try": rsi_email.applicant_disclosure, "fail": [
                # if send is not successful, add back to hold queue
            ]},
            {"try": middleware.mark_disclosure_as_sent, "fail": []},
            {"try": actions.add_hold_before_sending_disclosure, "fail": []},
            {"try": actions.add_to_hold_queue, "fail": []}

        ],
        "review_schedule_picker": [
            {"try": middleware.create_correlation_id, "fail": []},
            {"try": middleware.determine_current_datetime, "fail": []},
            {"try": middleware.get_data_from_schedule_form, "fail": []},
            {"try": middleware.clean_prohibition_number, "fail": []},
            {"try": middleware.validate_prohibition_number, "fail": []},
            {"try": middleware.validate_drivers_last_name, "fail": []},
            {"try": middleware.get_vips_status, "fail": []},
            {"try": middleware.prohibition_exists_in_vips, "fail": []},
            {"try": middleware.user_submitted_last_name_matches_vips, "fail": []},
            {"try": middleware.application_has_been_saved_to_vips, "fail": []},

            {"try": middleware.get_payment_status, "fail": []},
            {"try": middleware.received_valid_payment_status, "fail": []},
            {"try": middleware.paid_not_more_than_24hrs_ago, "fail": []},

            {"try": middleware.application_has_been_paid, "fail": []},
            {"try": middleware.get_application_details, "fail": []},
            {"try": middleware.valid_application_received_from_vips, "fail": []},
            {"try": middleware.get_invoice_details, "fail": []},
            {"try": middleware.calculate_schedule_window, "fail": []},
            {"try": middleware.decode_selected_timeslot, "fail": []},
            {"try": middleware.is_selected_timeslot_inside_schedule_window, "fail": []},
            {"try": middleware.get_human_friendly_time_slot_string, "fail": []},

            {"try": middleware.save_schedule_to_vips, "fail": [
                # Consider sending a message to the applicant in the unlikely
                # event that the schedule save operation is unsuccessful
            ]},
            {"try": rsi_email.applicant_schedule_confirmation, "fail": []},
            {"try": rsi_email.applicant_evidence_instructions, "fail": []},
            {"try": middleware.create_disclosure_event, "fail": []},
            {"try": actions.add_hold_before_sending_disclosure, "fail": []},
            {"try": actions.add_to_hold_queue, "fail": []}
        ],
        "prohibition_review": [
            {
                "try": actions.is_not_on_hold,
                "fail": [
                    {"try": actions.add_to_hold_queue, "fail": []}
                ]
            },
            {"try": middleware.get_data_from_application_form, "fail": []},
            {"try": middleware.clean_prohibition_number, "fail": []},
            {"try": middleware.populate_driver_name_fields_if_null, "fail": []},
            {"try": middleware.create_correlation_id, "fail": []},
            {"try": middleware.determine_current_datetime, "fail": []},
            {
                "try": middleware.get_vips_status,
                "fail": [
                    {"try": actions.add_to_hold_queue, "fail": []}
                ]
            },
            {
                "try": middleware.prohibition_exists_in_vips,
                "fail": [
                    {
                        "try": middleware.prohibition_served_recently,
                        "fail": [
                            {"try": rsi_email.applicant_prohibition_not_found, "fail": []}
                        ]
                    },
                    {"try": rsi_email.applicant_prohibition_not_found_yet, "fail": []},
                    {"try": actions.add_hold_before_trying_vips_again, "fail": []},
                    {"try": actions.add_to_hold_queue, "fail": []}
                ]
            },
            {
                "try": middleware.application_not_previously_saved_to_vips,
                "fail": [
                    {"try": rsi_email.already_applied, "fail": []},
                ]},
            {
                "try": middleware.user_submitted_last_name_matches_vips,
                "fail": [
                    {"try": rsi_email.applicant_last_name_mismatch, "fail": []}
                ]
            },
            {
                "try": middleware.date_served_not_older_than_one_week,
                "fail": [
                    {"try": rsi_email.applicant_prohibition_served_more_than_7_days_ago, "fail": []}
                ]
            },
            {
                "try": middleware.has_drivers_licence_been_seized,
                "fail": [
                    {"try": rsi_email.applicant_licence_not_seized, "fail": []}
                ]
            },
            {"try": middleware.transform_hearing_request_type, "fail": []},
            {"try": middleware.force_presentation_type_to_written_if_ineligible_for_oral, "fail": []},
            {"try": middleware.transform_applicant_role_type, "fail": []},
            {"try": middleware.compress_form_data_xml, "fail": []},
            {
                "try": middleware.save_application_to_vips,
                "fail": [
                    {"try": actions.add_to_failed_queue, "fail": []},
                    {"try": rsi_email.admin_unable_to_save_to_vips, "fail": []}
                ]
            },
            {"try": rsi_email.application_accepted, "fail": []}
        ],
    }
