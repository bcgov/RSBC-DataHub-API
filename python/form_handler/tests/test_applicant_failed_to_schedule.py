import datetime
import responses
import python.common.tests.vips_mock as vips_mock
import python.common.helper as helper
import python.form_handler.business as business
from python.form_handler.config import Config as BaseConfig
import python.common.common_email_services as common_email
from python.common.rabbitmq import RabbitMQ


def test_verify_schedule_event_that_has_not_reached_the_hold_until_datetime_is_placed_back_on_hold(monkeypatch):
    future_date = datetime.datetime.now() + datetime.timedelta(hours=1)
    message_dict = get_verify_schedule_event(future_date)

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"
        return True

    monkeypatch.setattr(BaseConfig, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=BaseConfig,
                                  writer=RabbitMQ)


@responses.activate
def test_verify_schedule_event_sends_email_to_business_if_applicant_has_not_scheduled(monkeypatch):
    past_date = datetime.datetime.now() - datetime.timedelta(hours=1)
    message_dict = get_verify_schedule_event(past_date)
    business_email_address = "business-address@gov.bc.ca"

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(BaseConfig.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_and_paid_not_scheduled("IRP"),
                  status=200, match_querystring=True)

    def mock_send_business_email(*args, **kwargs):
        assert "Did Not Schedule - Driving Prohibition 20-123456 Review" in args[0]
        assert "Appeals Registry," in args[2]
        assert "Charlie Brown, the applicant of prohibition 20123456," in args[2]
        assert "did not schedule the review within 24 hours of payment." in args[2]
        assert "Number: ABCD-1234" in args[2]
        assert "Amount: 50.00" in args[2]
        assert "Date: 2020-10-22" in args[2]
        assert "Order Number: 1010100" in args[2]
        return True

    monkeypatch.setattr(BaseConfig, "BCC_EMAIL_ADDRESSES", business_email_address)
    monkeypatch.setattr(common_email, "send_to_business", mock_send_business_email)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=BaseConfig,
                                  writer=RabbitMQ)


@responses.activate
def test_verify_no_email_sent_to_business_if_applicant_scheduled(monkeypatch):
    past_date = datetime.datetime.now() - datetime.timedelta(hours=1)
    message_dict = get_verify_schedule_event(past_date)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(BaseConfig.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_applied_paid_and_scheduled("IRP", "2021-03-24 12:00:00 -0700"),
                  status=200, match_querystring=True)

    def mock_send_business_email(*args, **kwargs):
        # this method should never be called
        assert False

    monkeypatch.setattr(common_email, "send_to_business", mock_send_business_email)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=BaseConfig,
                                  writer=RabbitMQ)


def test_verify_schedule_check_placed_back_on_hold_if_vips_not_available(monkeypatch):
    past_date = datetime.datetime.now() + datetime.timedelta(hours=1)
    message_dict = get_verify_schedule_event(past_date)

    responses.add(responses.GET,
                  '{}/{}/status/{}'.format(BaseConfig.VIPS_API_ROOT_URL, "20123456", "20123456"),
                  json=vips_mock.status_returns_html_response(),
                  status=200, match_querystring=True)

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"
        return True

    monkeypatch.setattr(BaseConfig, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=BaseConfig,
                                  writer=RabbitMQ)


def get_verify_schedule_event(hold_until_date_time: datetime) -> dict:
    return {
          "event_version": "1.5",
          "event_date_time": "2020-10-28T04:50:35.202805",
          "event_type": "verify_schedule",
          "verify_schedule": {
              "applicant_name": "Charlie Brown",
              "receipt_date": "2020-10-22",
              "receipt_amount": "50.00",
              "receipt_number": "ABCD-1234",
              "prohibition_number": "20123456",
              "order_number": "1010100"
          },
          "hold_until": hold_until_date_time.isoformat()
    }
