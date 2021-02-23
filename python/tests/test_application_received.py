import pytest
import os
import pytz
import datetime
import logging
import python.common.helper as helper
import python.common.middleware as middleware
import python.common.actions as actions
import python.form_handler.business as business
from python.form_handler.config import Config as BaseConfig
import python.common.vips_api as vips
import python.common.common_email_services as common_email_services

os.environ['TZ'] = 'UTC'


def mock_status_not_found(*args, **kwargs):
    return True, dict({
        "resp": "fail",
        "error": {
            "message": "Record not found",
            "httpStatus": 404
        }
    })


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


def get_status_with_review_booked(date_served, prohibition_type):
    data = {
            "resp": "success",
            "data": {
                "status": {
                    "noticeTypeCd": prohibition_type,
                    "reviewStartDtm": "some-date",
                    "reviewEndDtm": "some-date",
                    "noticeServedDt": date_served + " 00:00:00 -07:00",
                    "reviewFormSubmittedYn": "N",
                    "reviewCreatedYn": "N",
                    "originalCause": "IRP90FAIL",
                    "surnameNm": "Gordon",
                    "driverLicenceSeizedYn": "Y",
                    "disclosure": []
                }
            }
        }
    return True, data


irp_or_adp = ["IRP", "ADP"]


@pytest.mark.parametrize("prohib", irp_or_adp)
def test_an_applicant_that_was_served_yesterday_but_not_in_vips_gets_not_yet_email(prohib, monkeypatch):

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Prohibition Not Yet Found - Driving Prohibition 21-999344" in args[1]
        assert "issued on September 22, 2020 isn't in our" in template_content
        assert "We'll check every 12 hours for 7 days from the prohibition issued date" in template_content
        assert "http://link-to-icbc" in template_content
        assert "http://link-to-service-bc" in template_content
        return True

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime("2020-09-23", "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    def mock_add_to_hold(**args):
        print('inside mock_add_to_hold()')
        return True, args

    monkeypatch.setattr(actions, "add_to_hold_queue", mock_add_to_hold)
    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    monkeypatch.setattr(vips, "status_get", mock_status_not_found)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission(prohib)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


@pytest.mark.parametrize("prohib", irp_or_adp)
def test_an_applicant_that_was_served_7_days_ago_but_not_in_vips_gets_still_not_found_email(prohib, monkeypatch):

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Prohibition Still Not Found - Driving Prohibition 21-999344" in args[1]
        assert "If it's not in our system by the next time we check, your online" in template_content
        assert "You can't get a review extension if you miss the deadline" in template_content
        assert "http://link-to-icbc" in template_content
        assert "http://link-to-service-bc" in template_content
        return True

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime("2020-09-29", "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    def mock_add_to_hold(**args):
        print('inside mock_add_to_hold()')
        return True, args

    monkeypatch.setattr(actions, "add_to_hold_queue", mock_add_to_hold)
    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    monkeypatch.setattr(vips, "status_get", mock_status_not_found)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission(prohib)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


@pytest.mark.parametrize("prohib", irp_or_adp)
def test_an_applicant_without_a_valid_prohibition_gets_appropriate_email(prohib, monkeypatch):
    """
    Applicant gets the "Not Found" email if the date served (as entered by the applicant)
    has allowed sufficient time for the prohibition to be entered into VIPS
    """
    global email_sent
    email_sent = False

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        assert "Prohibition Not Found and 7-day Application Window Missed - Driving Prohibition 21-999344 Review" in args[1]
        assert "Your application for a review of the prohibition can't be accepted." in template_content
        global email_sent
        email_sent = True
        return True

    monkeypatch.setattr(vips, "status_get", mock_status_not_found)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission(prohib)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)
    assert email_sent


@pytest.mark.parametrize("prohib", irp_or_adp)
def test_an_applicant_that_applies_using_incorrect_last_name_gets_appropriate_email(prohib, monkeypatch):

    def mock_status_get(*args, **kwargs):
        date_served = "2020-09-23"
        return status_gets(True, prohib, date_served, "NORRIS", "Y", "FAIL90", "N")

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Prohibition Number or Name Don't Match - Driving Prohibition 21-999344 Review" == args[1]
        assert "You must re-apply within 7 days from the date of prohibition issue." in template_content
        return True

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission(prohib)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


@pytest.mark.parametrize("prohib", irp_or_adp)
def test_an_applicant_that_has_not_surrendered_their_licence_gets_appropriate_email(prohib, monkeypatch):

    def mock_status_get(*args, **kwargs):
        # (is_success, prohibition_type, date_served, last_name, seized, cause, already_applied):
        date_served = datetime.datetime.now().strftime("%Y-%m-%d")
        return status_gets(True, prohib, date_served, "Gordon", "N", "FAIL90", "N")

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Licence Not Surrendered - Driving Prohibition 21-999344 Review" == args[1]
        assert "You're ineligible to apply online because your licence wasn't surrendered" in template_content
        return True

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission(prohib)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


@pytest.mark.parametrize("prohib", irp_or_adp)
def test_an_applicant_that_has_previously_applied_gets_appropriate_email(prohib, monkeypatch):

    def mock_status_get(*args, **kwargs):
        # (is_success, prohibition_type, date_served, last_name, seized, cause, already_applied):
        date_served = datetime.datetime.now().strftime("%Y-%m-%d")
        return status_gets(True, prohib, date_served, "Gordon", "Y", "FAIL90", "True")

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Already Applied – Driving Prohibition 21-999344 Review" == args[1]
        assert "An application to review prohibition 21999344 has already been submitted." in template_content
        assert "You must call to make changes to your application." in template_content
        return True

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission(prohib)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


@pytest.mark.parametrize("prohib", irp_or_adp)
def test_an_applicant_that_has_missed_the_window_to_apply_gets_appropriate_email(prohib, monkeypatch):

    def mock_status_get(*args, **kwargs):
        # (is_success, prohibition_type, date_served, last_name, seized, cause, already_applied):
        tz = pytz.timezone('America/Vancouver')
        date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=8)).strftime("%Y-%m-%d")
        return status_gets(True, prohib, date_served, "Gordon", "Y", "FAIL90", "False")

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "7-day Application Window Missed - Driving Prohibition 21-999344 Review" == args[1]
        assert "Your application for a review of driving prohibition 21999344 can't be accepted." in template_content
        assert "Our records show your Notice of Prohibition was issued more than 7 days ago." in template_content
        return True

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission(prohib)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


@pytest.mark.parametrize("prohib", irp_or_adp)
def test_a_successful_applicant_gets_an_application_accepted_email(prohib, monkeypatch):

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime("2021-02-23", "%Y-%m-%d"))
        return True, args

    def mock_status_get(*args, **kwargs):
        # (is_success, prohibition_type, date_served, last_name, seized, cause, already_applied):
        date_served = "2021-02-19"
        return status_gets(True, prohib, date_served, "Gordon", "Y", "FAIL90", "False")

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Application Accepted - Driving Prohibition 21-999344 Review" == args[1]
        assert "Your application for a review of driving prohibition 21999344 has been accepted." in template_content
        assert "You must pay in full by credit card by February 27, 2021" in template_content
        assert "If you don't pay by February 27, 2021, your review will not go ahead." in template_content
        assert "http://link-to-paybc" in template_content
        return True

    def mock_save(*args, **kwargs):
        return True, dict({

        })

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "application_create", mock_save)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)
    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)

    message_dict = get_sample_application_submission(prohib)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


def test_a_unlicenced_applicant_that_was_served_yesterday_but_not_in_vips_gets_not_yet_email(monkeypatch):

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        assert "Prohibition Not Yet Found - Driving Prohibition 21-999344" in args[1]
        assert "issued on September 22, 2020 isn't in our" in template_content
        assert "We'll check every 12 hours for 7 days" in template_content
        assert "http://link-to-icbc" in template_content
        assert "http://link-to-service-bc" in template_content
        return True

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime("2020-09-23", "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    def mock_add_to_hold(**args):
        print('inside mock_add_to_hold()')
        return True, args

    monkeypatch.setattr(actions, "add_to_hold_queue", mock_add_to_hold)
    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    monkeypatch.setattr(vips, "status_get", mock_status_not_found)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


def test_a_unlicenced_applicant_that_was_served_7_days_ago_but_not_in_vips_gets_still_not_found_email(monkeypatch):

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        assert "Prohibition Still Not Found - Driving Prohibition 21-999344" in args[1]
        assert "If it's not in our system by the next time we check, your online application" in template_content
        assert "You may need to apply in-person." in template_content
        assert "http://link-to-icbc" in template_content
        assert "http://link-to-service-bc" in template_content
        return True

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime("2020-09-29", "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    def mock_add_to_hold(**args):
        return True, args

    monkeypatch.setattr(actions, "add_to_hold_queue", mock_add_to_hold)
    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    monkeypatch.setattr(vips, "status_get", mock_status_not_found)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


def test_an_unlicenced_applicant_without_a_valid_prohibition_gets_not_found_email(monkeypatch):
    """
    Applicant gets the "Not Found" email if the date served (as entered by the applicant)
    has allowed sufficient time for the prohibition to be entered into VIPS
    """

    def mock_status_get(*args, **kwargs):
        return True, dict({
            "resp": "fail",
            "error": {
                "message": "Record not found",
                "httpStatus": 404
            }
        })

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Prohibition Not Found – Driving Prohibition 21-999344 Review" in args[1]
        assert "You must apply in-person." in template_content
        return True

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


def test_an_unlicenced_applicant_that_applies_using_incorrect_last_name_gets_appropriate_email(monkeypatch):

    def mock_status_get(*args, **kwargs):
        date_served = "2020-09-23"
        return status_gets(True, "UL", date_served, "NORRIS", "Y", "FAIL90", "N")

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Prohibition Number or Name Don't Match - Driving Prohibition 21-999344 Review" == args[1]
        assert "You can re-apply at any time." in template_content
        return True

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


def test_an_unlicenced_applicant_has_no_licence_to_surrender_get_accepted_email(monkeypatch):

    def mock_status_get(*args, **kwargs):
        # (is_success, prohibition_type, date_served, last_name, seized, cause, already_applied):
        date_served = datetime.datetime.now().strftime("%Y-%m-%d")
        return status_gets(True, "UL", date_served, "Gordon", "N", "FAIL90", "N")

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Application Accepted - Driving Prohibition 21-999344 Review" == args[1]
        assert "Your application for a review of driving prohibition 21999344 has been accepted." in template_content
        return True

    def mock_save(*args, **kwargs):
        return True, dict({

        })

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "application_create", mock_save)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


def test_an_unlicenced_applicant_that_has_previously_applied_gets_already_applied_email(monkeypatch):

    def mock_status_get(*args, **kwargs):
        # (is_success, prohibition_type, date_served, last_name, seized, cause, already_applied):
        date_served = datetime.datetime.now().strftime("%Y-%m-%d")
        return status_gets(True, "UL", date_served, "Gordon", "Y", "FAIL90", "True")

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Previous Review on File – Driving Prohibition 21-999344 Review" == args[1]
        assert "You're unable to apply online because there is a previous review on file" in template_content
        assert "You'll need to apply in person for a review." in template_content
        assert "You must apply in person." in template_content
        return True

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


def test_an_unlicenced_applicant_can_apply_anytime_and_get_application_accepted_email(monkeypatch):

    def mock_status_get(*args, **kwargs):
        # (is_success, prohibition_type, date_served, last_name, seized, cause, already_applied):
        date_served = (datetime.datetime.now() - datetime.timedelta(days=8)).strftime("%Y-%m-%d")
        return status_gets(True, "UL", date_served, "Gordon", "Y", "FAIL90", "False")

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Application Accepted - Driving Prohibition 21-999344 Review" == args[1]
        assert "Your application for a review of driving prohibition 21999344 has been accepted." in template_content
        return True

    def mock_save(*args, **kwargs):
        return True, dict({

        })

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "application_create", mock_save)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


def test_an_unlicenced_successful_applicant_gets_an_application_accepted_email(monkeypatch):

    def mock_status_get(*args, **kwargs):
        # (is_success, prohibition_type, date_served, last_name, seized, cause, already_applied):
        date_served = (datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y-%m-%d")
        return status_gets(True, "UL", date_served, "Gordon", "Y", "FAIL90", "False")

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Application Accepted - Driving Prohibition 21-999344 Review" == args[1]
        assert "Your application for a review of driving prohibition 21999344 has been accepted." in template_content
        assert "You must pay in full by credit card within 7 days of applying for this review." in template_content
        assert "http://link-to-paybc" in template_content
        return True

    def mock_save(*args, **kwargs):
        return True, dict({

        })

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(vips, "application_create", mock_save)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


def test_a_ul_applicant_that_applies_at_icbc_gets_already_applied_email(monkeypatch):

    def mock_status_get(*args, **kwargs):
        date_served = datetime.datetime.now().strftime("%Y-%m-%d")
        return get_status_with_review_booked(date_served, "UL")

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Previous Review on File – Driving Prohibition 21-999344 Review" == args[1]
        assert "You're unable to apply online because there is a previous review on file" in template_content
        assert "You'll need to apply in person for a review." in template_content
        assert "You must apply in person." in template_content
        return True

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


def test_an_irp_applicant_that_applies_at_icbc_gets_already_applied_email(monkeypatch):

    def mock_status_get(*args, **kwargs):
        date_served = datetime.datetime.now().strftime("%Y-%m-%d")
        return get_status_with_review_booked(date_served, "IRP")

    def mock_send_email(*args, **kwargs):
        template_content = args[3]
        assert "me@lost.com" in args[0]
        print("Subject: {}".format(args[1]))
        assert "Already Applied – Driving Prohibition 21-999344 Review" == args[1]
        assert "An application to review prohibition 21999344 has already been submitted." in template_content
        assert "You must call to make changes to your application." in template_content
        assert "Disregard this email if you applied in person after submitting your online application." in template_content
        return True

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(common_email_services, "send_email", mock_send_email)

    message_dict = get_sample_application_submission("IRP")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)


def get_sample_application_submission(prohibition_type: str = "IRP") -> dict:
    message_dict = helper.load_json_into_dict('python/tests/sample_data/form/irp_form_submission.json')
    event_type = message_dict['event_type']
    if prohibition_type == "UL":
        message_dict[event_type]['form']['prohibition-information']['control-is-adp'] = "false"
        message_dict[event_type]['form']['prohibition-information']['control-is-irp'] = "false"
        message_dict[event_type]['form']['prohibition-information']['control-is-ul'] = "true"
    elif prohibition_type == "ADP":
        message_dict[event_type]['form']['prohibition-information']['control-is-adp'] = "true"
        message_dict[event_type]['form']['prohibition-information']['control-is-irp'] = "false"
        message_dict[event_type]['form']['prohibition-information']['control-is-ul'] = "false"
    return message_dict


class Config(BaseConfig):
    LINK_TO_PAYBC = 'http://link-to-paybc'
    LINK_TO_SCHEDULE_FORM = 'http://link-to-schedule-form'
    LINK_TO_EVIDENCE_FORM = 'http://link-to-evidence-form'
    LINK_TO_APPLICATION_FORM = 'http://link-to-application-form'
    LINK_TO_ICBC ='http://link-to-icbc'
    LINK_TO_SERVICE_BC = 'http://link-to-service-bc'
