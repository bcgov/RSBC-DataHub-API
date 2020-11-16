import pytest
import datetime
import python.common.helper as helper
import python.common.middleware as middleware
import python.common.actions as actions
import python.form_handler.business as business
from python.form_handler.config import Config as BaseConfig
import python.common.vips_api as vips
import python.common.common_email_services as common_email_services


def status_gets(is_success, prohibition_type, date_served, last_name, seized, cause, already_applied):
    data = {
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
    if already_applied == "True":
        data['data']['status']['applicationId'] = 'GUID-GUID-GUID-GUID'
    if is_success:
        data['resp'] = "success"
    else:
        data['resp'] = 'error'
    return True, data


@pytest.mark.parametrize(
    "prohibition_type, date_served, today_is, seized, last_name, is_valid, is_applied, email_text",
    helper.get_csv_test_data('./python/tests/test_application_data.csv'))
def test_application_form_received(
        prohibition_type, date_served, today_is, seized, last_name, is_valid, is_applied, email_text, monkeypatch):

    def mock_status_get(*args, **kwargs):
        print('inside mock_status_get()')
        is_response_successful, data = status_gets(is_valid == "True", prohibition_type, date_served, last_name, seized, "N/A", is_applied)
        if is_response_successful and 'resp' in data:
            return True, data
        return False, dict({})

    def mock_send_email(*args, **kwargs):
        print('inside mock_send_email()')
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert email_text in args[3]
        return True

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime(today_is, "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    def mock_application_save(**args):
        print('inside mock_application_save()')
        return True, args

    def mock_add_to_hold(**args):
        print('inside mock_add_to_hold()')
        return True, args

    monkeypatch.setattr(actions, "add_to_hold_queue", mock_add_to_hold)
    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    monkeypatch.setattr(middleware, "save_application_to_vips", mock_application_save)
    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = helper.load_json_into_dict('python/tests/sample_data/form/irp_form_submission.json')

    # For the prohibition_not_found and the prohibition_not_found_yet emails, we rely on users entering
    # correct prohibition number prefix to determine the correct letter type.
    if prohibition_type == "UL":
        message_dict['prohibition_review']['form']['prohibition-information']['control-is-ul'] = "true"
        message_dict['prohibition_review']['form']['prohibition-information']['control-is-irp'] = "false"

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


class Config(BaseConfig):
    LINK_TO_PAYBC = 'http://link-to-paybc'
    LINK_TO_SCHEDULE_FORM = 'http://link-to-schedule-form'
    LINK_TO_EVIDENCE_FORM = 'http://link-to-evidence-form'
    LINK_TO_APPLICATION_FORM = 'http://link-to-application-form'
    LINK_TO_ICBC ='http://link-to-icbc'
    LINK_TO_SERVICE_BC = 'http://link-to-service-bc'