import pytest
import datetime
import python.common.helper as helper
import python.common.middleware as middleware
import python.form_handler.business as business
from python.form_handler.config import Config
import python.common.vips_api as vips
import python.common.common_email_services as common_email_services


def status_gets(is_success, prohibition_type, date_served, last_name, seized, cause, already_applied):
    data = {
            "resp": "success",
            "data": {
                "status": {
                    "noticeTypeCd": prohibition_type,
                    "noticeServedDt": date_served + " 00:00:00 -07:00",
                    "reviewFormSubmittedYn": "N",
                    "reviewCreatedYn": "N",
                    "reviewStartDtm": "2020-09-20 09:30:00 -08:00",
                    "originalCause": cause,
                    "surnameNm": last_name,
                    "driverLicenceSeizedYn": seized,
                    "receiptNumberTxt": "AAABBB123",
                    "disclosure": []
                }
            }
        }
    if already_applied == "True":
        data['data']['status']['applicationId'] = 'GUID-GUID-GUID-GUID'
    return is_success, data


def application_get():
    return True, {
            "resp": "success",
            "data": {
                "applicationInfo": {
                    "email": "me@lost.com",
                    "firstGivenNm": "Bob",
                    "noticeSubjectCd": "string",
                    "noticeTypeCd": "string",
                    "phoneNo": "string",
                    "presentationTypeCd": "string",
                    "prohibitionNoticeNo": "string",
                    "reviewApplnTypeCd": "string",
                    "reviewRoleTypeCd": "",
                    "surnameNm": "Gordon"
                }
            }
        }



@pytest.mark.parametrize(
    "prohibition_type, date_served, today_is, seized, last_name, is_valid, is_applied, email_text",
    helper.get_csv_test_data('./python/tests/test_document_submission_data.csv'))
def test_evidence_form_received(
        prohibition_type, date_served, today_is, seized, last_name, is_valid, is_applied, email_text, monkeypatch):

    def mock_status_get(*args, **kwargs):
        print('inside mock_status_get()')
        return status_gets(is_valid == "True", prohibition_type, date_served, last_name, seized, "N/A", is_applied)

    def mock_application_get(*args, **kwargs):
        print('inside mock_application_get()')
        return application_get()

    def mock_send_email(*args, **kwargs):
        print('inside mock_send_email()')
        assert "me@gov.bc.ca" in args[0]
        print("Subject: {}".format(args[1]))
        assert email_text in args[3]
        return True

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime(today_is, "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "application_get", mock_application_get)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = helper.load_json_into_dict('python/tests/sample_data/form/document_submission.json')

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                        message=message_dict,
                        config=Config,
                        writer=None)

    if "error_string" in results:
        print(results.get('error_string'))
    assert 'error_string' not in results
