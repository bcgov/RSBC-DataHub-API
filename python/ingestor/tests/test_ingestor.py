import pytest
import json
import datetime
import base64
import logging
import logging.config
import responses
import os
import pytz
import python.common.rsi_email as rsi_email
import python.common.tests.vips_mock as vips_mock
from python.ingestor.config import Config
import python.common.vips_api as vips
import python.common.middleware as middleware
import python.ingestor.routes as routes

os.environ['TZ'] = 'UTC'

@pytest.fixture
def client():
    routes.application.config['TESTING'] = True
    with routes.application.test_client() as client:
        yield client


def mock_rabbitmq(*args):
    print("mocking RabbitMQ")


def test_form_endpoint_rejects_json_payload(client, monkeypatch):
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)
    payload = dict({"data": "json"})
    response = client.post('/v1/publish/event/form', json=payload)
    json_data = response.json

    assert "received content type is not XML" in json_data['error']
    assert response.status_code == 422


def test_form_endpoint_rejects_payloads_that_exceed_max_length(client, monkeypatch):
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    payload = "<xml>" + "long_string" * 10000 + "</xml>"
    header = dict({"Content-Type": "application/xml"})
    response = client.post('/v1/publish/event/form', data=payload, headers=header)
    logging.warning(response.json)
    assert response.status_code == 422


def test_form_endpoint_rejects_submissions_with_incorrect_query_parameter(client, monkeypatch):
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    payload = "<xml>" + "long_string" * 100 + "</xml>"
    header = dict({"Content-Type": "application/xml"})
    params = dict({"form_name": "prohibition_review"})
    response = client.post('/v1/publish/event/form', data=payload, headers=header, query_string=params)
    logging.warning(response.json)
    json_data = response.json
    assert "missing key query parameter: form" in json_data['error']
    assert response.status_code == 422


def test_form_endpoint_rejects_submissions_with_bad_xml_payload(client, monkeypatch):
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)
    bad_payload = "<xml>" + "long_string" * 100
    header = dict({"Content-Type": "application/xml"})
    params = dict({"form": "prohibition_review"})
    response = client.post('/v1/publish/event/form', data=bad_payload, headers=header, query_string=params)
    logging.warning(response.json)
    json_data = response.json
    assert "something went wrong" in json_data['error']
    assert response.status_code == 500


def test_form_endpoint_returns_500_when_rabbitmq_not_available(client, monkeypatch):

    class RabbitMQ:
        def __init__(self, *args):
            pass

        def publish(*args):
            return False

    monkeypatch.setattr(routes, "RabbitMQ", RabbitMQ)

    payload = "<xml>" + "long_string" * 100 + "</xml>"
    header = dict({"Content-Type": "application/xml"})
    params = dict({"form": "prohibition_review"})
    response = client.post('/v1/publish/event/form', data=payload, headers=header, query_string=params)
    logging.warning(response.json)
    assert response.status_code == 500


def test_form_endpoint_saves_submissions_to_rabbitmq(client, monkeypatch):

    class RabbitMQ:
        def __init__(self, *args):
            pass

        def publish(*args):
            return True

    monkeypatch.setattr(routes, "RabbitMQ", RabbitMQ)

    payload = "<xml>" + "long_string" * 100 + "</xml>"
    header = dict({"Content-Type": "application/xml"})
    params = dict({"form": "prohibition_review"})
    response = client.post('/v1/publish/event/form', data=payload, headers=header, query_string=params)
    logging.warning(response.json)
    assert response.status_code == 200


def test_check_templates_endpoint(client, monkeypatch):

    monkeypatch.setattr(Config, "ENVIRONMENT", "dev")
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.get('/check_templates')
    assert "Email Templates" in str(response.data)
    assert response.status_code == 200


@pytest.mark.parametrize("environment", [('prod', 'test')])
def test_check_templates_endpoint_responds_only_in_dev(environment, client, monkeypatch):

    monkeypatch.setattr(Config, "ENVIRONMENT", environment)
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    with pytest.raises(TypeError):
        client.get('/check_templates')


@pytest.mark.parametrize("template", rsi_email.content_data().keys())
def test_check_endpoint(template, client, monkeypatch):

    monkeypatch.setattr(Config, "ENVIRONMENT", "dev")
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.get('/check?template=' + template)
    assert response.status_code == 200


@pytest.mark.parametrize("template", rsi_email.content_data())
def test_check_endpoint_does_not_respond_in_test(template, client, monkeypatch):

    monkeypatch.setattr(Config, "ENVIRONMENT", "test")
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    with pytest.raises(TypeError):
        client.get('/check?template=' + template[0])


@pytest.mark.parametrize("template", rsi_email.content_data())
def test_check_endpoint_does_not_respond_in_prod(template, client, monkeypatch):

    monkeypatch.setattr(Config, "ENVIRONMENT", "prod")
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    with pytest.raises(TypeError):
        client.get('/check?template=' + template[0])


def test_the_evidence_endpoint_requires_basic_auth(client, monkeypatch):

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence', data=dict({
        "prohibition_number": "99999",
        "last_name": "smith"
    }))
    assert response.status_code == 401  # Unauthorized


def test_an_applicant_cannot_submit_evidence_with_prohibition_number_that_is_too_short(client, monkeypatch):

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data('99999'))
    json_data = response.json
    assert response.status_code == 200
    assert 'You have entered an invalid prohibition number, please try again.' in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


@responses.activate
def test_an_applicant_cannot_submit_evidence_after_their_review_has_concluded(client, monkeypatch):

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_review_concluded("IRP"),
                  status=200)

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    assert response.status_code == 200
    assert "You can't submit evidence less than 48 hours before your review." in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


@responses.activate
def test_an_applicant_cannot_submit_evidence_if_they_have_not_applied(client, monkeypatch):

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_has_never_applied("IRP"),
                  status=200)

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    assert response.status_code == 200
    assert "You must apply before you can submit evidence." in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


@responses.activate
def test_an_applicant_cannot_submit_evidence_if_they_have_not_paid(client, monkeypatch):

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid("IRP"),
                  status=200)

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    assert response.status_code == 200
    assert "You must pay before you can submit evidence." in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


@responses.activate
def test_an_applicant_cannot_submit_evidence_if_their_last_name_does_not_match_vips(client, monkeypatch):

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_and_paid_not_scheduled("IRP"),
                  status=200)

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data(last_name="Wrong"))
    json_data = response.json
    assert response.status_code == 200
    assert "The last name doesn't match a driving prohibition in the system." in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


@responses.activate
def test_an_applicant_cannot_submit_evidence_if_no_matching_prohibition_in_vips(client, monkeypatch):

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_not_found(),
                  status=404)

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    assert response.status_code == 200
    assert "The driving prohibition isn't in the system." in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


@responses.activate
def test_an_applicant_cannot_submit_evidence_if_the_review_date_is_less_than_48hrs_from_now(client, monkeypatch):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=7)).strftime(iso_format)
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) + datetime.timedelta(hours=47))

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_paid_and_scheduled("IRP", review_start_date),
                  status=200)
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    logging.warning("review start date and time: {}".format(review_start_date))
    assert response.status_code == 200
    assert "You can't submit evidence less than 48 hours before your review." in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


@responses.activate
def test_an_applicant_cannot_submit_evidence_if_the_review_date_has_not_been_scheduled(client, monkeypatch):
    iso_format = "%Y-%m-%d"
    date_served = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime(iso_format)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_and_paid_not_scheduled("IRP"),
                  status=200)

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    assert response.status_code == 200
    assert "You must book a review date before you can submit evidence for the review." in json_data['data']['error']
    assert json_data['data']['is_valid'] is False


@responses.activate
def test_an_applicant_can_submit_evidence_happy_path(client, monkeypatch):
    tz = pytz.timezone('America/Vancouver')
    review_start_date = vips.vips_datetime(datetime.datetime.now(tz) + datetime.timedelta(days=3))

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_paid_and_scheduled("IRP", review_start_date),
                  status=200)

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/evidence',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    assert response.status_code == 200
    assert json_data['data']['is_valid'] is True


@responses.activate
def test_an_applicant_can_can_receive_schedule_options_happy_path(client, monkeypatch):
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    date_served = (datetime.datetime.now(tz) - datetime.timedelta(days=5)).strftime(iso_format)
    payment_date = datetime.datetime.now(tz).strftime(iso_format)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_and_paid_not_scheduled("IRP", date_served),
                  status=200)

    responses.add(responses.GET,
                  '{}/{}/payment/status/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.payment_get(payment_date),
                  status=200)

    responses.add(responses.GET,
                  '{}/{}/application/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.application_get(),
                  status=200)

    for x in [4, 5, 6, 7, 8, 9]:
        query_date = (datetime.datetime.now(tz) + datetime.timedelta(days=x)).strftime(iso_format)
        responses.add(responses.GET,
                      '{}/{}/{}/{}/review/availableTimeSlot/{}'.format(
                          Config.VIPS_API_ROOT_URL, "IRP", "ORAL", query_date, "20123456"),
                      json=vips_mock.schedule_get(query_date),
                      status=200)

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/schedule',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    logging.warning(json_data)
    assert response.status_code == 200
    assert json_data['data']['is_valid'] is True
    assert "time_slots" in json_data['data']


@responses.activate
def test_system_queries_for_additional_time_slots_if_insufficient_review_date_available(client, monkeypatch):
    date_served = "2020-12-02"
    payment_date = "2020-12-05"
    iso_format = "%Y-%m-%d"
    tz = pytz.timezone('America/Vancouver')
    expected_query_dates = ['2020-12-17']

    def mock_today_date(**args):
        tz = pytz.timezone('America/Vancouver')
        local_time = datetime.datetime.now(tz)
        args['today_date'] = local_time.replace(year=2020, month=12, day=5)
        return True, args

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_and_paid_not_scheduled("IRP", date_served),
                  status=200)

    responses.add(responses.GET,
                  '{}/{}/payment/status/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.payment_get(payment_date),
                  status=200)

    responses.add(responses.GET,
                  '{}/{}/application/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.application_get(),
                  status=200)

    query_date = expected_query_dates.pop()
    responses.add(responses.GET,
                  '{}/{}/{}/{}/review/availableTimeSlot/{}'.format(
                      Config.VIPS_API_ROOT_URL, "IRP", "ORAL", query_date, "20123456"),
                  json=vips_mock.schedule_get(query_date),
                  status=200)

    def mock_query_review_times(**args):
        """
        This method only returns only 2 review dates.  This is insufficient according
        to business rules so mock schedule get is queried for additional review dates.
        """
        args['time_slots'] = []
        args['number_review_days_offered'] = 2
        return True, args


    def mock_insufficient_dates_email(**args):
        # send email to Appeals to let them know to add more dates
        return True, args

    monkeypatch.setattr(middleware, "query_review_times_available", mock_query_review_times)
    monkeypatch.setattr(middleware, "determine_current_datetime", mock_today_date)
    monkeypatch.setattr(rsi_email, "insufficient_reviews_available", mock_insufficient_dates_email)
    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)
    monkeypatch.setattr(rsi_email, "insufficient_reviews_available", mock_insufficient_dates_email)

    response = client.post('/schedule',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    logging.warning(json_data)
    assert response.status_code == 200
    assert json_data['data']['is_valid'] is True
    assert "time_slots" in json_data['data']
    assert isinstance(json_data['data']['time_slots'], list)
    assert len(expected_query_dates) == 0


@responses.activate
def test_an_applicant_that_has_not_paid_cannot_schedule(client, monkeypatch):
    iso_format = "%Y-%m-%d"
    date_served = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime(iso_format)
    payment_date = datetime.datetime.now().strftime(iso_format)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid("IRP", date_served),
                  status=200)

    responses.add(responses.GET,
                  '{}/{}/payment/status/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.payment_get(payment_date),
                  status=200)

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/schedule',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    logging.warning(json_data)
    assert response.status_code == 200
    assert json_data['data']['is_success'] is False
    assert json_data['data']['error'] == "The application review fee must be paid to continue."


@responses.activate
def test_an_applicant_that_paid_more_than_24hrs_ago_cannot_schedule(client, monkeypatch):
    iso_format = "%Y-%m-%d"
    date_served = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime(iso_format)
    payment_date = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime(iso_format)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid("IRP", date_served),
                  status=200)

    responses.add(responses.GET,
                  '{}/{}/payment/status/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.payment_get(payment_date),
                  status=200)


    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/schedule',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    logging.warning(json_data)
    assert response.status_code == 200
    assert json_data['data']['is_success'] is False
    assert json_data['data']['error'] == "You are outside the 24-hour time allowed to schedule the review. " \
                                         "Please call Appeals at 250-356-6573."


@responses.activate
def test_an_applicants_last_name_must_match_vips_to_schedule(client, monkeypatch):
    iso_format = "%Y-%m-%d"
    date_served = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime(iso_format)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_not_paid("IRP", date_served),
                  status=200)

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/schedule',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data(last_name="Wrong"))
    json_data = response.json
    logging.warning(json_data)
    assert response.status_code == 200
    assert json_data['data']['is_success'] is False
    assert json_data['data']['error'] == "The last name doesn't match a driving prohibition in the system."


@responses.activate
def test_an_applicant_must_have_applied_before_scheduling(client, monkeypatch):
    iso_format = "%Y-%m-%d"

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_has_never_applied("IRP"),
                  status=200)

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/schedule',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    logging.warning(json_data)
    assert response.status_code == 200
    assert json_data['data']['is_success'] is False
    assert json_data['data']['error'] == "You must submit an application before you can schedule."


@responses.activate
def test_an_applicant_must_not_have_already_scheduled_a_review(client, monkeypatch):
    iso_format = "%Y-%m-%d"
    date_served = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime(iso_format)
    payment_date = datetime.datetime.now().strftime(iso_format)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(Config.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_paid_and_scheduled("IRP", date_served),
                  status=200)

    responses.add(responses.GET,
                  '{}/{}/payment/status/{}'.format(
                      Config.VIPS_API_ROOT_URL, "bb71037c-f87b-0444-e054-00144ff95452", "20123456"),
                  json=vips_mock.payment_get(payment_date),
                  status=200)

    monkeypatch.setattr(routes, "RabbitMQ", mock_rabbitmq)

    response = client.post('/schedule',
                           headers=get_basic_authentication_header(monkeypatch),
                           data=get_evidence_form_data())
    json_data = response.json
    logging.warning(json_data)
    assert response.status_code == 200
    assert json_data['data']['is_success'] is False
    assert json_data['data']['error'] == 'A review has already been scheduled for this prohibition.'


def get_basic_authentication_header(monkeypatch, username="name", password="secret") -> dict:
    monkeypatch.setattr(Config, "FLASK_BASIC_AUTH_USER", username)
    monkeypatch.setattr(Config, "FLASK_BASIC_AUTH_PASS", password)
    credentials = base64.b64encode((username + ":" + password).encode('utf-8')).decode('utf-8')
    headers = dict({"Authorization": "Basic {}".format(credentials)})
    logging.debug(headers)
    return headers


def get_evidence_form_data(prohibition_number='20123456', last_name='Gordon'):
    return dict({
        "prohibition_number": prohibition_number,
        "last_name": last_name
    })


def schedule_get(days_offered=3) -> tuple:

    return True, dict({
        "time_slots": list([
            {
                "label": "Fri, Sep 4, 2020 - 10:00am to 11:30am",
                "value": "ZGF0YSB0byBiZSBlbmNvZGVk"
            },
            {
                "label": "Mon, Sep 7, 2020 - 10:00am to 11:30am",
                "value": "ZGF0YSB0byBiZSBlbmNvZGVk"
            },
            {
                "label": "Tue, Sep 8, 2020 - 10:00am to 11:30am",
                "value": "ZGF0YSB0byBiZSBlbmNvZGVk"
            }
        ]),
        "number_review_days_offered": days_offered
    })
