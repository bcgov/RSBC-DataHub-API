import pytest
import datetime
import python.common.helper as helper
import python.common.middleware as middleware
import python.ingestor.business as business
from python.ingestor.config import Config
import python.common.vips_api as vips


def status_gets(is_success, prohibition_type, date_served, is_paid, review_start_date, last_name, is_applied):
    data = {
            "resp": "success",
            "data": {
                "status": {
                    "noticeTypeCd": prohibition_type,
                    "noticeServedDt": date_served + " 00:00:00 -08:00",
                    "reviewFormSubmittedYn": "N",
                    "reviewCreatedYn": "N",
                    "originalCause": "IRP7",
                    "surnameNm": last_name,
                    "driverLicenceSeizedYn": "Y",
                    "disclosure": []
                }
            }
        }
    if len(review_start_date) > 0:
        data['data']['status']['reviewStartDtm'] = review_start_date + ' 09:30:00 -07:00'
    if is_paid == "True":
        data['data']['status']['receiptNumberTxt'] = 'AAABBB123'
    if is_applied == "True":
        data['data']['status']['applicationId'] = 'GUID-GUID-GUID-GUID'
    return is_success, data


submit_evidence_data = [
    # Type   Date Served   Today Is      IsPaid  LastName  IsValid IsApplied ReviewStartDt Expected

    # Happy path
    ["IRP", "2020-09-10", "2020-09-17 09:30", "True", "Gordon", "True", "True", "2020-09-21", "True"],

    # Not paid
    ["IRP", "2020-09-10", "2020-09-17 09:30", "False", "Gordon", "True", "True", "2020-09-21", "False"],

    # Wrong last name
    ["IRP", "2020-09-10", "2020-09-17 09:30", "True", "Smith", "True", "True", "2020-09-21", "False"],

    # Not found in VIPS
    ["IRP", "2020-09-10", "2020-09-17 09:30", "True", "Gordon", "False", "True", "2020-09-21", "False"],

    # Review date less than 48 hours in the future
    ["IRP", "2020-09-10", "2020-09-20 09:30", "True", "Gordon", "True", "True", "2020-09-21", "False"],
    ["IRP", "2020-09-10", "2020-09-19 09:30", "True", "Gordon", "True", "True", "2020-09-21", "False"],

    # Review has concluded
    ["IRP", "2020-09-10", "2020-09-22 09:30", "True", "Gordon", "True", "True", "2020-09-21", "False"],

    # Has not applied
    ["IRP", "2020-09-10", "2020-09-17 09:30", "True", "Gordon", "True", "False", "2020-09-21", "False"],

]


@pytest.mark.parametrize(
    "prohibition_type, date_served, today_is, is_paid, last_name, is_valid, is_applied, review_start_date, expected",
    submit_evidence_data)
def test_okay_to_submit_evidence(
        prohibition_type,
        date_served,
        today_is,
        is_paid,
        last_name,
        is_valid,
        is_applied,
        review_start_date,
        expected,
        monkeypatch):

    def mock_status_get(*args, **kwargs):
        print('inside mock_status_get()')
        return status_gets(is_valid == "True",
                           prohibition_type, date_served, is_paid, review_start_date, last_name, is_applied)

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime(today_is, "%Y-%m-%d %H:%M"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    monkeypatch.setattr(vips, "status_get", mock_status_get)

    results = helper.middle_logic(business.is_okay_to_submit_evidence(),
                                  prohibition_number="00123456",
                                  driver_last_name="Gordon",
                                  config=Config)

    if expected == "True":
        print("error string: {}".format(results.get('error_string')))
        assert 'error_string' not in results
    else:
        assert 'error_string' in results
