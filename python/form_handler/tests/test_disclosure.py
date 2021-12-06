import pytest
import datetime
import responses
import logging
import json
import pytz
import python.common.tests.vips_mock as vips_mock
import python.common.helper as helper
import python.common.middleware as middleware
import python.form_handler.business as business
from python.form_handler.config import Config
import python.common.vips_api as vips
from python.common.rabbitmq import RabbitMQ


def test_disclosure_that_has_not_reached_the_hold_until_datetime_is_placed_back_on_hold(monkeypatch):
    message_dict = helper.load_json_into_dict('python/common/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat()

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"
        return True

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)


@responses.activate
def test_when_an_applicants_review_has_concluded_the_disclosure_event_is_deleted(monkeypatch):
    message_dict = helper.load_json_into_dict('python/common/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()
    tz = pytz.timezone('America/Vancouver')
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) - datetime.timedelta(days=1))

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_paid_and_scheduled("IRP", review_start_date),
                  status=200, match_querystring=True)

    def mock_any_disclosure(*args, **kwargs):
        # We should never call this method
        assert False

    monkeypatch.setattr(middleware, "is_any_unsent_disclosure", mock_any_disclosure)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)


@responses.activate
def test_if_no_disclosure_add_back_to_hold_queue(monkeypatch):
    message_dict = helper.load_json_into_dict('python/common/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()
    tz = pytz.timezone('America/Vancouver')
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) - datetime.timedelta(days=1))

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_with_no_disclosure("IRP", review_start_date),
                  status=200, match_querystring=True)

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)


@responses.activate
def test_disclosure_documents_marked_sent_are_not_sent_again(monkeypatch):
    message_dict = helper.load_json_into_dict('python/common/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()
    tz = pytz.timezone('America/Vancouver')
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) - datetime.timedelta(days=1))

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_paid_and_scheduled("IRP", review_start_date),
                  status=200, match_querystring=True)

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)


@responses.activate
def test_when_one_document_not_disclosed_one_document_is_emailed_to_applicant(monkeypatch):
    message_dict = helper.load_json_into_dict('python/common/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()
    tz = pytz.timezone('America/Vancouver')
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) + datetime.timedelta(days=2))

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_with_one_sent_on_unsent_disclosure("IRP", review_start_date),
                  status=200, match_querystring=True)

    responses.add(responses.GET,
                  '{}/{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "111", "20123456"),
                  json=vips_mock.disclosure_get(),
                  status=200, match_querystring=True)

    responses.add(responses.PATCH,
                  '{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "20123456"),
                  json=vips_mock.disclosure_get(),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
         Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"sample": "test"}, status=200)

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"
        return True

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)

    email_payload = json.loads(responses.calls[3].request.body.decode())
    assert 'me@gov.bc.ca' in email_payload['to']
    assert len(email_payload['attachments']) == 1


@responses.activate
def test_when_two_documents_not_disclosed_two_documents_emailed_to_applicant(monkeypatch):
    message_dict = helper.load_json_into_dict('python/common/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()
    tz = pytz.timezone('America/Vancouver')
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) + datetime.timedelta(days=2))

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_with_two_unsent_disclosures("IRP", review_start_date),
                  status=200, match_querystring=True)

    responses.add(responses.GET,
                  '{}/{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "111", "20123456"),
                  json=vips_mock.disclosure_get(),
                  status=200, match_querystring=True)

    responses.add(responses.GET,
                  '{}/{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "222", "20123456"),
                  json=vips_mock.disclosure_get(),
                  status=200, match_querystring=True)

    responses.add(responses.PATCH,
                  '{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "20123456"),
                  json=dict({}),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
         Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"sample": "test"}, status=200)

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"
        return True

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)

    email_payload = json.loads(responses.calls[4].request.body.decode())
    assert 'me@gov.bc.ca' in email_payload['to']
    assert len(email_payload['attachments']) == 2


@responses.activate
def test_when_two_documents_previously_disclosed_two_documents_emailed_to_applicant(monkeypatch):
    message_dict = helper.load_json_into_dict('python/common/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()
    tz = pytz.timezone('America/Vancouver')
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) + datetime.timedelta(days=2))

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_with_two_disclosures_sent_last_month("UL", review_start_date),
                  status=200, match_querystring=True)

    responses.add(responses.GET,
                  '{}/{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "111", "20123456"),
                  json=vips_mock.disclosure_get(),
                  status=200, match_querystring=True)

    responses.add(responses.GET,
                  '{}/{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "222", "20123456"),
                  json=vips_mock.disclosure_get(),
                  status=200, match_querystring=True)

    responses.add(responses.PATCH,
                  '{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "20123456"),
                  json=dict({}),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
         Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"sample": "test"}, status=200)

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"
        return True

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)

    email_payload = json.loads(responses.calls[4].request.body.decode())
    assert 'me@gov.bc.ca' in email_payload['to']
    assert len(email_payload['attachments']) == 2


@pytest.mark.parametrize("prohibition_type", ['IRP', 'ADP'])
@responses.activate
def test_disclosure_email_template_has_unique_text_for_irp_and_adp_prohibitions(prohibition_type, monkeypatch):
    message_dict = helper.load_json_into_dict('python/common/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()
    tz = pytz.timezone('America/Vancouver')
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) + datetime.timedelta(days=2))

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_with_two_unsent_disclosures(prohibition_type, review_start_date),
                  status=200, match_querystring=True)

    responses.add(responses.GET,
                  '{}/{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "111", "20123456"),
                  json=vips_mock.disclosure_get(),
                  status=200, match_querystring=True)

    responses.add(responses.GET,
                  '{}/{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "222", "20123456"),
                  json=vips_mock.disclosure_get(),
                  status=200, match_querystring=True)

    responses.add(responses.PATCH,
                  '{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "20123456"),
                  json=dict({}),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
         Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"sample": "test"}, status=200)

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"
        return True

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)

    email_payload = json.loads(responses.calls[4].request.body.decode())
    assert 'me@gov.bc.ca' in email_payload['to']
    assert email_payload['subject'] == "Disclosure Documents Attached - Driving Prohibition 20-123456 Review"
    assert "Attached is the police evidence the adjudicator will consider in your review." in email_payload['body']
    assert "Make sure you can open the attachments." in email_payload['body']


@responses.activate
def test_disclosure_email_template_has_unique_text_for_ul_prohibitions(monkeypatch):
    message_dict = helper.load_json_into_dict('python/common/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()
    tz = pytz.timezone('America/Vancouver')
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) + datetime.timedelta(days=2))

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_with_two_unsent_disclosures("UL", review_start_date),
                  status=200, match_querystring=True)

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"
        return True
    #
    # def mock_send_email(*args, **kwargs):
    #     print('inside mock_send_email()')
    #     assert "me@gov.bc.ca" in args[0]
    #     assert "Disclosure Documents Attached - Driving Prohibition 20-123456 Review" in args[1]
    #     assert "Attached is the police evidence the RoadSafetyBC adjudicator will consider in your review." in args[3]
    #     assert '<a href="http://localhost">get a copy from ICBC</a>' in args[3]
    #     return True

    responses.add(responses.GET,
                  '{}/{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "111", "20123456"),
                  json=vips_mock.disclosure_get(),
                  status=200, match_querystring=True)

    responses.add(responses.GET,
                  '{}/{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "222", "20123456"),
                  json=vips_mock.disclosure_get(),
                  status=200, match_querystring=True)

    responses.add(responses.PATCH,
                  '{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "20123456"),
                  json=dict({}),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
         Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"sample": "test"}, status=200)

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)

    email_payload = json.loads(responses.calls[4].request.body.decode())
    assert 'me@gov.bc.ca' in email_payload['to']
    assert email_payload['subject'] == "Disclosure Documents Attached - Driving Prohibition 20-123456 Review"
    assert "Attached is the police evidence the RoadSafetyBC adjudicator will consider in your review." in email_payload['body']
    assert '<a href="http://localhost">get a copy from ICBC</a>' in email_payload['body']


@responses.activate
def test_adp_disclosure_includes_blood_alcohol_pdf_document_during_initial_disclosure(monkeypatch):
    message_dict = helper.load_json_into_dict('python/common/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()
    tz = pytz.timezone('America/Vancouver')
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) + datetime.timedelta(days=2))
    number_of_attachments_expected = 3

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_with_two_unsent_disclosures("ADP", review_start_date),
                  status=200, match_querystring=True)

    responses.add(responses.GET,
                  '{}/{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "111", "20123456"),
                  json=vips_mock.disclosure_get(),
                  status=200, match_querystring=True)

    responses.add(responses.GET,
                  '{}/{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "222", "20123456"),
                  json=vips_mock.disclosure_get(),
                  status=200, match_querystring=True)

    responses.add(responses.PATCH,
                  '{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "20123456"),
                  json=dict({}),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
         Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"sample": "test"}, status=200)

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"
        return True

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)

    email_payload = json.loads(responses.calls[4].request.body.decode())
    assert 'me@gov.bc.ca' in email_payload['to']
    assert email_payload['subject'] == "Disclosure Documents Attached - Driving Prohibition 20-123456 Review"
    assert number_of_attachments_expected == len(email_payload['attachments'])


@responses.activate
def test_subsequent_adp_disclosure_does_not_include_blood_alcohol_pdf_document(monkeypatch):
    message_dict = helper.load_json_into_dict('python/common/tests/sample_data/form/disclosure_payload.json')
    message_dict['hold_until'] = (datetime.datetime.now() - datetime.timedelta(hours=1)).isoformat()
    tz = pytz.timezone('America/Vancouver')
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) + datetime.timedelta(days=2))
    number_of_attachments_expected = 1

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_with_one_sent_on_unsent_disclosure("ADP", review_start_date),
                  status=200, match_querystring=True)

    responses.add(responses.GET,
                  '{}/{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "111", "20123456"),
                  json=vips_mock.disclosure_get(),
                  status=200, match_querystring=True)

    responses.add(responses.PATCH,
                  '{}/disclosure/{}'.format(Config.VIPS_API_ROOT_URL, "20123456"),
                  json=dict({}),
                  status=200, match_querystring=True)

    responses.add(responses.POST, '{}/realms/{}/protocol/openid-connect/token'.format(
         Config.COMM_SERV_AUTH_URL, Config.COMM_SERV_REALM), json={"access_token": "token"}, status=200)

    responses.add(responses.POST, '{}/api/v1/email'.format(
        Config.COMM_SERV_API_ROOT_URL), json={"sample": "test"}, status=200)

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"
        return True

    monkeypatch.setattr(Config, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=Config,
                                  writer=RabbitMQ)

    email_payload = json.loads(responses.calls[3].request.body.decode())
    assert 'me@gov.bc.ca' in email_payload['to']
    assert email_payload['subject'] == "Disclosure Documents Attached - Driving Prohibition 20-123456 Review"
    assert number_of_attachments_expected == len(email_payload['attachments'])
