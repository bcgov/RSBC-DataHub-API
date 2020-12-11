import pytest
import pytz
import datetime
import logging
import python.common.helper as helper
import python.common.middleware as middleware
import python.paybc_api.business as business
from python.paybc_api.website.config import Config
import python.common.vips_api as vips


test_search_method_data = [
    # Type, ServiceDate   TodayIs       Paid     LastName  InVips  Error
    ('IRP', "2020-09-10", "2020-09-15", False,   "Norris", True,  "The last name doesn't match a driving prohibition in the system."),
    ('IRP', "2020-09-10", "2020-09-18", False,   "Gordon", True,  "The Notice of Prohibition was issued more than 7 days ago."),
    ('IRP', "2020-09-10", "2020-09-16", False,   "Gordon", True,  None),
    ('IRP', "2020-09-10", "2020-09-14", False,   "Gordon", False, "The driving prohibition isn't in the system."),
    ('IRP', "2020-09-10", "2020-09-14", True,    "Gordon", True,  "The application review fee has already been paid."),
    ('IRP', "2020-09-10", "2020-09-14", False,   "Gordon", True,  None),

    ('ADP', "2020-09-10", "2020-09-15", False,   "Norris", True,  "The last name doesn't match a driving prohibition in the system."),
    ('ADP', "2020-09-10", "2020-09-18", False,   "Gordon", True,  "The Notice of Prohibition was issued more than 7 days ago."),
    ('ADP', "2020-09-10", "2020-09-16", False,   "Gordon", True,  None),
    ('ADP', "2020-09-10", "2020-09-14", False,   "Gordon", False, "The driving prohibition isn't in the system."),
    ('ADP', "2020-09-10", "2020-09-14", True,    "Gordon", True,  "The application review fee has already been paid."),
    ('ADP', "2020-09-10", "2020-09-14", False,   "Gordon", True,  None),

    ('UL',  "2020-09-10", "2020-09-15", False,   "Norris", True,  "The last name doesn't match a driving prohibition in the system."),
    ('UL',  "2020-09-10", "2020-09-14", False,   "Gordon", False, "The driving prohibition isn't in the system."),
    ('UL',  "2020-09-10", "2020-09-14", True,    "Gordon", True,  "The application review fee has already been paid."),
    ('UL',  "2020-09-10", "2020-09-14", False,   "Gordon", True,  None),
]


@pytest.mark.parametrize(
    "prohibition_type, date_served, today_is, is_paid, last_name, is_in_vips, error", test_search_method_data)
def test_search_method(
        prohibition_type, date_served, today_is, is_paid, last_name, is_in_vips, error, monkeypatch):

    def mock_status_get(*args, **kwargs):
        print('inside mock_status_get()')
        return status_get(is_in_vips, prohibition_type, date_served, last_name, is_paid, True)

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime(today_is, "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    monkeypatch.setattr(vips, "status_get", mock_status_get)

    results = helper.middle_logic(business.search_for_invoice(),
                                  prohibition_number="20-123456",
                                  driver_last_name="Gordon",
                                  config=Config)

    print(results.get('error_string'))
    if error is None:
        assert "error_string" not in results
    else:
        assert "error_string" in results
        assert results.get('error_string') == error


test_show_method_data = [
    # Type, Application  Error
    ('IRP', True,        None),
    ('IRP', False,       "You must submit an application before you can pay."),

]


@pytest.mark.parametrize("prohibition_type, application_created, error", test_show_method_data)
def test_pay_bc_generate_invoice_method(prohibition_type, application_created, error, monkeypatch):
    is_in_vips = True
    prohibition_type = "ADP"
    today_is = "2020-09-14"
    last_name = "Gordon"
    date_served = "2020-09-10"
    is_paid = False

    def mock_status_get(*args, **kwargs):
        print('inside mock_status_get()')
        return status_get(is_in_vips, prohibition_type, date_served, last_name, is_paid, application_created)

    def mock_application_get(*args, **kwargs):
        print('inside mock_application_get()')
        return application_get()

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime(today_is, "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "application_get", mock_application_get)

    results = helper.middle_logic(business.generate_invoice(),
                                  prohibition_number="20-123456",
                                  config=Config)

    print(results.get('error_string'))
    if error is None:
        assert "error_string" not in results
    else:
        assert "error_string" in results
        assert results.get('error_string') == error


def test_an_applicant_must_apply_for_a_review_before_paying_the_application_fee(monkeypatch):
    is_in_vips = True
    prohibition_type = "ADP"
    last_name = "Gordon"
    date_served = datetime.datetime.now().strftime("%Y-%m-%d")
    application_created = False
    is_paid = False
    expected_error = "You must submit an application before you can pay."

    def mock_status_get(*args, **kwargs):
        return status_get(is_in_vips, prohibition_type, date_served, last_name, is_paid, application_created)

    monkeypatch.setattr(vips, "status_get", mock_status_get)

    results = helper.middle_logic(business.search_for_invoice(),
                                  driver_last_name="Gordon",
                                  prohibition_number="20-123456",
                                  config=Config)
    error = results.get('error_string')
    logging.warning(error)
    assert error == expected_error


def test_an_applicant_must_enter_a_last_name_that_matches_vips(monkeypatch):
    is_in_vips = True
    prohibition_type = "ADP"
    last_name = "Smith"
    date_served = "2020-09-10"
    application_created = True
    is_paid = False
    expected_error = "The last name doesn't match a driving prohibition in the system."

    def mock_status_get(*args, **kwargs):
        return status_get(is_in_vips, prohibition_type, date_served, last_name, is_paid, application_created)

    monkeypatch.setattr(vips, "status_get", mock_status_get)

    results = helper.middle_logic(business.search_for_invoice(),
                                  driver_last_name="Gordon",
                                  prohibition_number="20-123456",
                                  config=Config)
    error = results.get('error_string')
    logging.warning(error)
    assert error == expected_error


def test_an_applicant_must_pay_before_application_window_has_expired(monkeypatch):
    is_in_vips = True
    prohibition_type = "IRP"
    last_name = "Gordon"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=8)).strftime("%Y-%m-%d")
    application_created = True
    is_paid = False
    expected_error = "The Notice of Prohibition was issued more than 7 days ago."

    def mock_status_get(*args, **kwargs):
        return status_get(is_in_vips, prohibition_type, date_served, last_name, is_paid, application_created)

    monkeypatch.setattr(vips, "status_get", mock_status_get)

    results = helper.middle_logic(business.search_for_invoice(),
                                  driver_last_name="Gordon",
                                  prohibition_number="20-123456",
                                  config=Config)
    error = results.get('error_string')
    logging.warning(error)
    assert error == expected_error


def test_an_applicant_must_not_have_paid_previously(monkeypatch):
    is_in_vips = True
    prohibition_type = "IRP"
    last_name = "Gordon"
    date_served = datetime.datetime.now().strftime("%Y-%m-%d")
    application_created = True
    is_paid = True
    expected_error = "The application review fee has already been paid."

    def mock_status_get(*args, **kwargs):
        return status_get(is_in_vips, prohibition_type, date_served, last_name, is_paid, application_created)

    monkeypatch.setattr(vips, "status_get", mock_status_get)

    results = helper.middle_logic(business.search_for_invoice(),
                                  driver_last_name="Gordon",
                                  prohibition_number="20-123456",
                                  config=Config)
    error = results.get('error_string')
    logging.warning(error)
    assert error == expected_error


def status_get(is_success, prohibition_type, date_served, last_name, is_paid, application_saved):
    if is_success:
        status = {
            "noticeTypeCd": prohibition_type,
            "noticeServedDt": date_served + " 00:00:00 -07:00",
            "reviewFormSubmittedYn": "N",
            "reviewCreatedYn": "N",
            "originalCause": "N/A",
            "surnameNm": last_name,
            "driverLicenceSeizedYn": "Y",
            "disclosure": []
        }
        if is_paid:
            status['receiptNumberTxt'] = "ABC"
        if application_saved:
            status['applicationId'] = "ABC-ABC-ABC"
        return True, {
                "resp": "success",
                "data": {
                    "status": status
                }
            }
    else:
        return True, {
                  "resp": "fail",
                  "error": {
                    "message": "Record not found",
                    "httpStatus": 404
                  }
               }


def application_get():
    return True, {
          "data": {
                "applicationInfo": {
                      "email": "string",
                      "firstGivenNm": "string",
                      "manualEntryYN": "N",
                      "noticeSubjectCd": "string",
                      "noticeTypeCd": "string",
                      "phoneNo": "string",
                      "presentationTypeCd": "string",
                      "prohibitionNoticeNo": "string",
                      "reviewApplnTypeCd": "string",
                      "reviewRoleTypeCd": "string",
                      "secondGivenNm": "string",
                      "surnameNm": "string"
                }
          },
          "resp": "success"
          }
