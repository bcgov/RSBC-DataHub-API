import pytest
import datetime
import python.common.helper as helper
import python.common.middleware as middleware
import python.common.actions as actions
import python.form_handler.business as business
from python.form_handler.config import Config
import python.common.vips_api as vips
import python.common.common_email_services as common_email_services


def status_gets(is_success, prohibition_type, date_served, last_name, seized, cause):
    return is_success, {
            "resp": "success",
            "data": {
                "status": {
                    "noticeTypeCd": prohibition_type,
                    "noticeServedDt": date_served + " 00:00:00 -07:00",
                    "reviewFormSubmittedYn": "N",
                    "reviewCreatedYn": "N",
                    "originalCause": cause,
                    "surnameNm": last_name,
                    "driverLicenceSeizedYn": seized,
                    "disclosure": []
                }
            }
        }


vips_status_application_received = [
    # Type, ServiceDate   TodayIs       Seized   LastName  Valid EmailTemplate
    ('IRP', "2020-09-10", "2020-09-11", "Y",     "Norris", True,  "last_name_mismatch.html"),
    ('IRP', "2020-09-10", "2020-09-15", "N",     "Gordon", True,  "licence_not_seized.html"),
    ('IRP', "2020-09-10", "2020-09-18", "Y",     "Gordon", True,  "not_received_in_time.html"),
    ('IRP', "2020-09-10", "2020-09-17", "Y",     "Gordon", True,  "not_received_in_time.html"),
    ('IRP', "2020-09-10", "2020-09-16", "Y",     "Gordon", True,  "application_accepted.html"),
    ('IRP', "2020-09-10", "2020-09-15", "Y",     "Gordon", True,  "application_accepted.html"),

    # When the prohibition is not found in VIPS, we rely on the service date as entered by the applicant
    # to determine which template to use.  For the tests below we use a service date of 2020-09-22
    ('IRP', "          ", "2020-09-23", "Y",     "Gordon", False, "application_not_yet_in_vips.html"),
    ('IRP', "          ", "2020-09-24", "Y",     "Gordon", False, "application_not_yet_in_vips.html"),
    ('IRP', "          ", "2020-09-25", "Y",     "Gordon", False, "application_not_found.html"),
    ('ADP', "          ", "2020-09-23", "Y",     "Gordon", False, "application_not_yet_in_vips.html"),
    ('ADP', "          ", "2020-09-24", "Y",     "Gordon", False, "application_not_yet_in_vips.html"),
    ('ADP', "          ", "2020-09-25", "Y",     "Gordon", False, "application_not_found.html"),
    ('UL',  "          ", "2020-09-23", "Y",     "Gordon", False, "application_not_yet_in_vips.html"),
    ('UL',  "          ", "2020-09-24", "Y",     "Gordon", False, "application_not_yet_in_vips.html"),
    ('UL',  "          ", "2020-09-25", "Y",     "Gordon", False, "application_not_found.html"),

    ('ADP', "2020-09-10", "2020-09-11", "Y",     "Norris", True,  "last_name_mismatch.html"),
    ('ADP', "2020-09-10", "2020-09-15", "N",     "Gordon", True,  "licence_not_seized.html"),
    ('ADP', "2020-09-10", "2020-09-18", "Y",     "Gordon", True,  "not_received_in_time.html"),
    ('ADP', "2020-09-10", "2020-09-17", "Y",     "Gordon", True,  "not_received_in_time.html"),
    ('ADP', "2020-09-10", "2020-09-16", "Y",     "Gordon", True,  "application_accepted.html"),
    ('ADP', "2020-09-10", "2020-09-11", "Y",     "Norris", True,  "last_name_mismatch.html"),
    ('ADP', "2020-09-10", "2020-09-15", "Y",     "Gordon", True,  "application_accepted.html"),

    ('UL',  "2020-09-10", "2020-09-18", "N",     "Gordon", True,  "application_accepted.html"),
    ('UL',  "2020-09-10", "2020-09-11", "Y",     "Norris", True,  "last_name_mismatch.html"),

]


@pytest.mark.parametrize(
    "prohibition_type, date_served, today_is, seized, last_name, is_valid, template", vips_status_application_received)
def test_application_form_received(
        prohibition_type, date_served, today_is, seized, last_name, is_valid, template, monkeypatch):

    def mock_status_get(*args, **kwargs):
        print('inside mock_status_get()')
        return status_gets(True, prohibition_type, date_served, last_name, seized, "N/A")

    def mock_send_email(*args):
        print('inside mock_send_email()')
        return True

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime(today_is, "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    def mock_application_save(**args):
        print('inside mock_application_save()')
        return True, args

    def mock_prohibition_exists(**args):
        print('inside mock_prohibition_exists()')
        vips_status = args.get('vips_status')
        args['vips_data'] = vips_status['data']['status']
        return is_valid, args

    def mock_add_to_hold(**args):
        print('inside mock_add_to_hold()')
        return True, args

    monkeypatch.setattr(actions, "add_to_hold_queue", mock_add_to_hold)
    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    monkeypatch.setattr(middleware, "save_application_to_vips", mock_application_save)
    monkeypatch.setattr(middleware, "prohibition_exists_in_vips", mock_prohibition_exists)
    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = helper.load_json_into_dict('python/tests/sample_data/form/irp_form_submission.json')

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)
    assert results.get('email_template') == template

