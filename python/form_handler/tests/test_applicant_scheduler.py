import os
import datetime
import responses
import json
import logging
import python.common.tests.vips_mock as vips_mock
import python.common.helper as helper
import python.common.middleware as middleware
from python.common.rabbitmq import RabbitMQ
import python.form_handler.business as business
from python.form_handler.config import Config as BaseConfig
import python.common.vips_api as vips

os.environ['TZ'] = 'UTC'


@responses.activate
def test_an_applicant_can_schedule_an_oral_review(monkeypatch):
    today = "2020-09-23"
    payment_date = "2020-12-05"
    application_id = "bb71037c-f87b-0444-e054-00144ff95452"
    prohibtion_num = "21900040"
    time_slot = vips.encode_time_slot({
                "reviewStartDtm": "2020-12-09 11:00:00 -08:00",
                "reviewEndDtm": "2020-12-09 11:30:00 -08:00",
            })

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, prohibtion_num, prohibtion_num, prohibtion_num),
                  json=vips_mock.status_applied_and_paid_not_scheduled("IRP"),
                  status=404, match_querystring=True)

    responses.add(responses.GET,
                  '{}/{}/payment/status/{}'.format(
                      Config.VIPS_API_ROOT_URL, application_id , prohibtion_num),
                  json=vips_mock.payment_get(payment_date),
                  status=200)

    responses.add(responses.GET,
                  '{}/{}/application/{}'.format(
                      Config.VIPS_API_ROOT_URL, application_id, prohibtion_num),
                  json=vips_mock.application_get(),
                  status=200)

    responses.add(responses.POST,
                  '{}/{}/review/schedule/{}'.format(
                      Config.VIPS_API_ROOT_URL, application_id, prohibtion_num),
                  json={"timeSlot": time_slot},
                  status=200)

    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=201)

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime(today, "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"
        return True

    monkeypatch.setattr(BaseConfig, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    message_dict = get_sample_schedule_review_submission("21999344", "Gordon", time_slot)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)

    email_payload = json.loads(responses.calls[6].request.body.decode())
    assert "applicant_fake@gov.bc.ca" in email_payload['to']
    assert "Review Date Confirmed - Driving Prohibition 21-900040 Review" in email_payload['subject']
    assert "We can only change the review date or time in special situations." in email_payload['body']
    assert "Your oral review has been scheduled for:" in email_payload['body']
    assert "Wed, Dec 9, 2020 - 11:00AM to 11:30AM (Pacific Time)" in email_payload['body']
    assert "We'll call you at 2505551212, which is the number you provided." in email_payload['body']


@responses.activate
def test_an_applicant_can_schedule_a_written_review(monkeypatch):
    today = "2020-09-23"
    payment_date = "2020-12-05"
    application_id = "bb71037c-f87b-0444-e054-00144ff95452"
    prohibtion_num = "21900040"
    time_slot = vips.encode_time_slot({
                "reviewStartDtm": "2020-12-09 11:00:00 -08:00",
                "reviewEndDtm": "2020-12-09 11:30:00 -08:00",
            })

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, prohibtion_num, prohibtion_num, prohibtion_num),
                  json=vips_mock.status_applied_and_paid_not_scheduled("IRP"),
                  status=200, match_querystring=True)

    responses.add(responses.GET,
                  '{}/{}/payment/status/{}'.format(
                      Config.VIPS_API_ROOT_URL, application_id , prohibtion_num),
                  json=vips_mock.payment_get(payment_date),
                  status=200)

    responses.add(responses.GET,
                  '{}/{}/application/{}'.format(
                      Config.VIPS_API_ROOT_URL, application_id, prohibtion_num),
                  json=vips_mock.application_get("WRIT"),
                  status=200)

    responses.add(responses.POST,
                  '{}/{}/review/schedule/{}'.format(
                      Config.VIPS_API_ROOT_URL, application_id, prohibtion_num),
                  json={"timeSlot": time_slot},
                  status=201)

    responses.add(responses.POST, "{}:{}/services/collector".format(
        Config.SPLUNK_HOST, Config.SPLUNK_PORT), status=200)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
        Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"response": "ignored"}, status=201)

    def mock_datetime_now(**args):
        args['today_date'] = helper.localize_timezone(datetime.datetime.strptime(today, "%Y-%m-%d"))
        print('inside mock_datetime_now: {}'.format(args.get('today_date')))
        return True, args

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"
        return True

    monkeypatch.setattr(BaseConfig, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    monkeypatch.setattr(middleware, "determine_current_datetime", mock_datetime_now)
    message_dict = get_sample_schedule_review_submission("21999344", "Gordon", time_slot)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)

    email_payload = json.loads(responses.calls[6].request.body.decode())
    assert "applicant_fake@gov.bc.ca" in email_payload['to']
    assert "Review Date Confirmed - Driving Prohibition 21-900040 Review" in email_payload['subject']
    assert "We can only change the review date or time in special situations." in email_payload['body']
    assert "Your written review has been scheduled for:" in email_payload['body']
    assert "Wed, Dec 9, 2020 at 9:30AM (Pacific Time)" in email_payload['body']




def get_sample_schedule_review_submission(prohibition_number: str, last_name: str, time_slot: str) -> dict:
    message_dict = helper.load_json_into_dict('python/common/tests/sample_data/form/schedule_picker_submission.json')
    event_type = message_dict['event_type']
    message_dict[event_type]['form']['schedule-review-section']['prohibition_number'] = prohibition_number
    message_dict[event_type]['form']['schedule-review-section']['last-name'] = last_name
    message_dict[event_type]['form']['schedule-review-section']['timeslot-selected'] = time_slot
    return message_dict


class Config(BaseConfig):
    BCC_EMAIL_ADDRESSES = "someone@gov.bc.ca, another@gov.bc.ca"
    LINK_TO_PAYBC = 'http://link-to-paybc'
    LINK_TO_SCHEDULE_FORM = 'http://link-to-schedule-form'
    LINK_TO_EVIDENCE_FORM = 'http://link-to-evidence-form'
    LINK_TO_APPLICATION_FORM = 'http://link-to-application-form'
    LINK_TO_ICBC ='http://link-to-icbc'
    LINK_TO_SERVICE_BC = 'http://link-to-service-bc'
