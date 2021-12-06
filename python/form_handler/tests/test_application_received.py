import pytest
import os
import pytz
import datetime
import responses
import json
import python.common.tests.vips_mock as vips_mock
import python.common.helper as helper
import python.common.middleware as middleware
import python.common.actions as actions
import python.form_handler.business as business
from python.form_handler.config import Config as BaseConfig
import python.common.vips_api as vips

os.environ['TZ'] = 'UTC'


@pytest.mark.parametrize("prohib", ["IRP", "ADP"])
@responses.activate
def test_an_applicant_that_was_served_yesterday_but_not_in_vips_gets_not_yet_email(prohib, monkeypatch):

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344", "21999344"),
                  json=vips_mock.status_not_found(),
                  status=404, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime("2020-09-23", "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    def mock_add_to_hold(**args):
        print('inside mock_add_to_hold()')
        return True, args

    monkeypatch.setattr(actions, "add_to_hold_queue", mock_add_to_hold)
    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    message_dict = get_sample_application_submission(prohib)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[2].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Prohibition Not Yet Found - Driving Prohibition 21-999344" in email_payload['subject']
    assert "issued on September 22, 2020 isn't in our" in email_payload['body']
    assert "We'll check every 12 hours for 7 days from the prohibition issued date" in email_payload['body']
    assert "http://link-to-icbc" in email_payload['body']
    assert "http://link-to-service-bc" in email_payload['body']


@pytest.mark.parametrize("prohib", ["IRP", "ADP"])
@responses.activate
def test_an_applicant_that_was_served_7_days_ago_but_not_in_vips_gets_still_not_found_email(prohib, monkeypatch):

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime("2020-09-29", "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    def mock_add_to_hold(**args):
        print('inside mock_add_to_hold()')
        return True, args

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344", "21999344"),
                  json=vips_mock.status_not_found(),
                  status=404, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    monkeypatch.setattr(actions, "add_to_hold_queue", mock_add_to_hold)
    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    message_dict = get_sample_application_submission(prohib)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[2].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Prohibition Still Not Found - Driving Prohibition 21-999344" in email_payload['subject']
    assert "If it's not in our system by the next time we check, your online" in email_payload['body']
    assert "You can't get a review extension if you miss the deadline" in email_payload['body']
    assert "http://link-to-icbc" in email_payload['body']
    assert "http://link-to-service-bc" in email_payload['body']


@pytest.mark.parametrize("prohib", ["IRP", "ADP"])
@responses.activate
def test_an_applicant_without_a_valid_prohibition_gets_appropriate_email(prohib, monkeypatch):
    """
    Applicant gets the "Not Found" email if the date served (as entered by the applicant)
    has allowed sufficient time for the prohibition to be entered into VIPS
    """

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_not_found(),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    message_dict = get_sample_application_submission(prohib)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[2].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Prohibition Not Found and 7-day Application Window Missed - Driving Prohibition 21-999344 Review" in email_payload['subject']
    assert "Your application for a review of the prohibition can't be accepted." in email_payload['body']


@pytest.mark.parametrize("prohib", ["IRP", "ADP"])
@responses.activate
def test_an_applicant_that_applies_using_incorrect_last_name_gets_appropriate_email(prohib, monkeypatch):
    date_served = "2020-09-23"

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_has_never_applied(prohib, date_served, "Wrong"),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    message_dict = get_sample_application_submission(prohib)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[2].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Prohibition Number or Name Don't Match - Driving Prohibition 21-999344 Review" == email_payload['subject']
    assert "You must re-apply within 7 days from the date of prohibition issue." in email_payload['body']


@pytest.mark.parametrize("prohib", ["IRP", "ADP"])
@responses.activate
def test_an_applicant_that_has_not_surrendered_their_licence_gets_appropriate_email(prohib, monkeypatch):
    date_served = datetime.datetime.now().strftime("%Y-%m-%d")

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_has_never_applied(prohib, date_served, "Gordon", "N"),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    message_dict = get_sample_application_submission(prohib)
    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[2].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Licence Not Surrendered - Driving Prohibition 21-999344 Review" == email_payload['subject']
    assert "You're ineligible to apply online because your licence wasn't surrendered" in email_payload['body']


@pytest.mark.parametrize("prohib", ["IRP", "ADP"])
@responses.activate
def test_an_irp_or_adp_applicant_that_has_previously_applied_gets_appropriate_email(prohib, monkeypatch):
    date_served = datetime.datetime.now().strftime("%Y-%m-%d")
    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_applied_not_paid(prohib, date_served),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)


    message_dict = get_sample_application_submission(prohib)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[2].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Already Applied – Driving Prohibition 21-999344 Review" == email_payload['subject']
    assert "An application to review prohibition 21999344 has already been submitted." in email_payload['body']
    assert "You must call to make changes to your application." in email_payload['body']


@pytest.mark.parametrize("prohib", ["IRP", "ADP"])
@responses.activate
def test_an_applicant_that_has_missed_the_window_to_apply_gets_appropriate_email(prohib, monkeypatch):
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=8)).strftime("%Y-%m-%d")

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_has_never_applied(prohib, date_served),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    message_dict = get_sample_application_submission(prohib)
    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[2].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "7-day Application Window Missed - Driving Prohibition 21-999344 Review" == email_payload['subject']
    assert "Your application for a review of driving prohibition 21999344 can't be accepted." in email_payload['body']
    assert "Our records show your Notice of Prohibition was issued more than 7 days ago." in email_payload['body']


@pytest.mark.parametrize("prohib", ["IRP", "ADP"])
@responses.activate
def test_a_successful_applicant_gets_an_application_accepted_email(prohib, monkeypatch):
    date_served = "2021-02-19"

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_has_never_applied(prohib, date_served),
                  status=200, match_querystring=True)

    responses.add(responses.POST,
                  '{}/{}/{}/application/{}'.format(Config.VIPS_API_ROOT_URL, prohib, "21999344", "21999344"),
                  json={},
                  status=200)

    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime("2021-02-23", "%Y-%m-%d"))
        return True, args

    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    message_dict = get_sample_application_submission(prohib)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[4].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Application Accepted - Driving Prohibition 21-999344 Review" == email_payload['subject']
    assert "Your application for a review of driving prohibition 21999344 has been accepted." in email_payload['body']
    assert "You must pay in full by credit card by February 27, 2021" in email_payload['body']
    assert "If you don't pay by February 27, 2021, your review will not go ahead." in email_payload['body']
    assert "http://link-to-paybc" in email_payload['body']


@responses.activate
def test_a_unlicenced_applicant_that_was_served_yesterday_but_not_in_vips_gets_not_yet_email(monkeypatch):

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime("2020-09-23", "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    def mock_add_to_hold(**args):
        print('inside mock_add_to_hold()')
        return True, args

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_not_found(),
                  status=404, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    monkeypatch.setattr(actions, "add_to_hold_queue", mock_add_to_hold)
    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)

    message_dict = get_sample_application_submission("UL")
    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[2].request.body.decode())
    assert "Prohibition Not Yet Found - Driving Prohibition 21-999344" in email_payload['subject']
    assert "issued on September 22, 2020 isn't in our" in email_payload['body']
    assert "We'll check every 12 hours for 7 days" in email_payload['body']
    assert "http://link-to-icbc" in email_payload['body']
    assert "http://link-to-service-bc" in email_payload['body']


@responses.activate
def test_a_unlicenced_applicant_that_was_served_7_days_ago_but_not_in_vips_gets_still_not_found_email(monkeypatch):

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime("2020-09-29", "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    def mock_add_to_hold(**args):
        return True, args

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_not_found(),
                  status=404, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    monkeypatch.setattr(actions, "add_to_hold_queue", mock_add_to_hold)
    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[2].request.body.decode())
    assert "Prohibition Still Not Found - Driving Prohibition 21-999344" in email_payload['subject']
    assert "If it's not in our system by the next time we check, your online application" in email_payload['body']
    assert "You may need to apply in-person." in email_payload['body']
    assert "http://link-to-icbc" in email_payload['body']
    assert "http://link-to-service-bc" in email_payload['body']


@responses.activate
def test_an_unlicenced_applicant_without_a_valid_prohibition_gets_not_found_email():
    """
    Applicant gets the "Not Found" email if the date served (as entered by the applicant)
    has allowed sufficient time for the prohibition to be entered into VIPS
    """

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_not_found(),
                  status=404, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)


    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[2].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Prohibition Not Found – Driving Prohibition 21-999344 Review" in email_payload['subject']
    assert "You must apply in-person." in email_payload['body']


@responses.activate
def test_an_unlicenced_applicant_that_applies_using_incorrect_last_name_gets_appropriate_email():
    date_served = "2020-09-23"
    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_has_never_applied("UL", date_served, "Wrong"),
                  status=404, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[2].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Prohibition Number or Name Don't Match - Driving Prohibition 21-999344 Review" == email_payload['subject']
    assert "You can re-apply at any time." in email_payload['body']


@responses.activate
def test_an_unlicenced_applicant_has_no_licence_to_surrender_gets_accepted_email():
    date_served = datetime.datetime.now().strftime("%Y-%m-%d")
    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_has_never_applied("UL", date_served, "Gordon", "N"),
                  status=200, match_querystring=True)

    responses.add(responses.POST,
                  '{}/{}/{}/application/{}'.format(Config.VIPS_API_ROOT_URL, "UL", "21999344", "21999344"),
                  json={},
                  status=200)

    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[4].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Application Accepted - Driving Prohibition 21-999344 Review" == email_payload['subject']
    assert "Your application for a review of driving prohibition 21999344 has been accepted." in email_payload['body']


@responses.activate
def test_an_unlicenced_applicant_that_has_previously_applied_gets_application_accepted():
    """
    UL applicants can apply multiple times, other prohibition types can only apply once
    """

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_previously_applied_review_unsuccessful("UL"),
                  status=200, match_querystring=True)

    responses.add(responses.POST,
                  '{}/{}/{}/application/{}'.format(Config.VIPS_API_ROOT_URL, "UL", "21999344", "21999344"),
                  json={},
                  status=200)

    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[4].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Application Accepted - Driving Prohibition 21-999344 Review" == email_payload['subject']


@responses.activate
def test_an_unlicenced_applicant_that_had_a_successful_review_cannot_apply_again():

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_previously_applied_review_successful("UL"),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[2].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Previous Review on File – Driving Prohibition 21-999344 Review" == email_payload['subject']


@responses.activate
def test_an_unlicenced_applicant_who_has_never_previously_applied_gets_application_accepted_email():
    date_served = (datetime.datetime.now() - datetime.timedelta(days=8)).strftime("%Y-%m-%d")
    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_has_never_applied("UL", date_served),
                  status=200, match_querystring=True)

    responses.add(responses.POST,
                  '{}/{}/{}/application/{}'.format(Config.VIPS_API_ROOT_URL, "UL", "21999344", "21999344"),
                  json={},
                  status=200)

    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)


    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[4].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Application Accepted - Driving Prohibition 21-999344 Review" == email_payload['subject']
    assert "Your application for a review of driving prohibition 21999344 has been accepted." in email_payload['body']


@responses.activate
def test_an_unlicenced_successful_applicant_gets_an_application_accepted_email():
    date_served = (datetime.datetime.now() - datetime.timedelta(days=6)).strftime("%Y-%m-%d")
    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_has_never_applied("UL", date_served),
                  status=200, match_querystring=True)

    responses.add(responses.POST,
                  '{}/{}/{}/application/{}'.format(Config.VIPS_API_ROOT_URL, "UL", "21999344", "21999344"),
                  json={},
                  status=200)

    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[4].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Application Accepted - Driving Prohibition 21-999344 Review" == email_payload['subject']
    assert "Your application for a review of driving prohibition 21999344 has been accepted." in email_payload['body']
    assert "You must pay in full by credit card within 7 days of applying for this review." in email_payload['body']
    assert "http://link-to-paybc" in email_payload['body']


@responses.activate
def test_a_ul_applicant_that_applies_at_icbc_gets_already_applied_email():
    tz = pytz.timezone('America/Vancouver')
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) + datetime.timedelta(days=2))
    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_applied_at_icbc("UL", review_start_date),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
         Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    message_dict = get_sample_application_submission("UL")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[2].request.body.decode())
    assert 'me@lost.com' in email_payload['to']
    assert "Applied at ICBC - Driving Prohibition 21-999344 Review" == email_payload['subject']
    assert "Dear Applicant," in email_payload['body']
    assert "Our records show that an application to review prohibition 21999344" in email_payload['body']
    assert "has been paid and scheduled at ICBC" in email_payload['body']
    assert "Please do not respond to this email." in email_payload['body']


@responses.activate
def test_an_irp_applicant_that_applies_at_icbc_gets_already_applied_email():
    tz = pytz.timezone('America/Vancouver')
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) + datetime.timedelta(days=2))
    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "21999344", "21999344"),
                  json=vips_mock.status_applied_at_icbc("IRP", review_start_date),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=200)

    message_dict = get_sample_application_submission("IRP")

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=None)

    email_payload = json.loads(responses.calls[2].request.body.decode())
    assert "me@lost.com" in email_payload['to']
    assert "Dear Applicant," in email_payload['body']
    assert "Applied at ICBC - Driving Prohibition 21-999344 Review" == email_payload['subject']
    assert "Our records show that an application to review prohibition 21999344" in email_payload['body']
    assert "has been paid and scheduled at ICBC" in email_payload['body']
    assert "Please do not respond to this email." in email_payload['body']


def get_sample_application_submission(prohibition_type: str = "IRP") -> dict:
    message_dict = helper.load_json_into_dict('python/common/tests/sample_data/form/irp_form_submission.json')
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
    BCC_EMAIL_ADDRESSES = "someone@gov.bc.ca, another@gov.bc.ca"
    LINK_TO_PAYBC = 'http://link-to-paybc'
    LINK_TO_SCHEDULE_FORM = 'http://link-to-schedule-form'
    LINK_TO_EVIDENCE_FORM = 'http://link-to-evidence-form'
    LINK_TO_APPLICATION_FORM = 'http://link-to-application-form'
    LINK_TO_ICBC ='http://link-to-icbc'
    LINK_TO_SERVICE_BC = 'http://link-to-service-bc'
