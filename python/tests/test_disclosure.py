import pytest
import datetime
import python.common.helper as helper
import python.common.middleware as middleware
import python.common.actions as actions
import python.form_handler.business as business
from python.form_handler.config import Config as BaseConfig
import python.common.vips_api as vips
import python.common.common_email_services as common_email_services


class Config(BaseConfig):
    VIPS_API_ROOT_URL = 'https://vips_url'

def status_gets(is_success, prohibition_type, review_start_date, disclosure):
    data = {
            "resp": "success",
            "data": {
                "status": {
                    "noticeTypeCd": prohibition_type,
                    "noticeServedDt": "2020-09-10 00:00:00 -08:00",
                    "reviewStartDtm": review_start_date + ' 09:30:00 -07:00',
                    "reviewFormSubmittedYn": "N",
                    "reviewCreatedYn": "Y",
                    "originalCause": "IRP7",
                    "surnameNm": "Gordon",
                    "driverLicenceSeizedYn": "Y",
                    "receiptNumberTxt": "AAABBB123",
                    "applicationId": 'GUID-GUID-GUID-GUID',
                }
            }
        }
    if disclosure == "No":
        data['data']['status']['disclosure'] = []
    elif disclosure == "2":
        data['data']['status']['disclosure'] = [
            {
                "documentId": "1491"
            },
            {
                "documentId": "1490"
            }
        ]
    elif disclosure == "1":
        data['data']['status']['disclosure'] = [
            {
                "documentId": "1491",
                "disclosedDtm": "some-date",
            },
            {
                "documentId": "1490"
            }
        ]
    elif disclosure == "none-unsent":
        data['data']['status']['disclosure'] = [
            {
                "documentId": "1491",
                "disclosedDtm": "some-date",
            },
            {
                "documentId": "1490",
                "disclosedDtm": "some-date",
            }
        ]
    return is_success, data


disclosure_test_data = [
    # Type   Today is     ReviewStartDt  IsValid   Disclosure     AttachmentsExpected
    ["IRP", "2020-10-20", "2020-10-22", "True",    "none-unsent", 0],
    ["IRP", "2020-10-20", "2020-10-22", "True",    "no",          0],
    ["IRP", "2020-10-20", "2020-10-22", "True",    "1",           1],
    ["IRP", "2020-10-20", "2020-10-22", "True",    "2",           2],

    # ADP's include an additional static document as an attachment
    ["ADP", "2020-10-20", "2020-10-22", "True",    "2",           3],

]


@pytest.mark.parametrize("prohibition_type, today_is, review_start_date, is_valid, disclosure, attachments_expected",
                         disclosure_test_data)
def test_disclosure_event_processing(
        prohibition_type, today_is, review_start_date, is_valid, disclosure, attachments_expected, monkeypatch):

    def mock_status_get(*args, **kwargs):
        print('inside mock_status_get()')
        return status_gets(is_valid == "True", prohibition_type, review_start_date, disclosure)

    def mock_send_email(*args, **kwargs):
        print('inside mock_send_email()')
        assert "me@gov.bc.ca" in args[0]
        print("Subject: {}".format(args[1]))
        return True

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime(today_is, "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    def mock_add_to_hold(**args):
        print("inside mock_add_to_hold")
        return True, args

    def mock_disclosure_get(*args):
        print("inside mock_disclosure_get()")
        data = dict({
                "resp": "success",
                "data": {
                    "document": {
                        "document": "base64_string_of_encoded_document",
                        "mimeType": "application/pdf"
                    }
                }
            })
        return True, data

    def mock_patch(*args):
        return True, dict({})

    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "patch", mock_patch)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)
    monkeypatch.setattr(actions, "add_to_hold_queue", mock_add_to_hold)
    monkeypatch.setattr(vips, "disclosure_get", mock_disclosure_get)

    message_dict = helper.load_json_into_dict('python/tests/sample_data/form/disclosure_payload.json')

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                        message=message_dict,
                        config=Config,
                        writer=None)

    if attachments_expected > 0:
        assert 'disclosure_for_applicant' in results
        assert len(results.get('disclosure_for_applicant')) == attachments_expected
    else:
        assert 'disclosure_for_applicant' not in results
