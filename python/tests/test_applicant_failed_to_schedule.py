import pytest
import datetime
import python.common.helper as helper
import python.form_handler.business as business
from python.form_handler.config import Config as BaseConfig
import python.common.vips_api as vips
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


def test_verify_schedule_event_sends_email_to_business_if_applicant_has_not_scheduled(monkeypatch):
    past_date = datetime.datetime.now() - datetime.timedelta(hours=1)
    message_dict = get_verify_schedule_event(past_date)
    business_email_address = "business-address@gov.bc.ca"

    def mock_status_get(*args, **kwargs):
        return status_gets_success("")

    def mock_send_business_email(*args, **kwargs):
        assert "Did Not Schedule - Driving Prohibition 21-258852 Review" in args[0]
        assert "Appeals Registry," in args[2]
        assert "Charlie Brown, the applicant of prohibition 21258852," in args[2]
        assert "did not schedule the review within 24 hours of payment." in args[2]
        assert "Number: ABCD-1234" in args[2]
        assert "Amount: 50.00" in args[2]
        assert "Date: 2020-10-22" in args[2]
        return True

    monkeypatch.setattr(BaseConfig, "BCC_EMAIL_ADDRESSES", business_email_address)
    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(common_email, "send_to_business", mock_send_business_email)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=BaseConfig,
                                  writer=RabbitMQ)


def test_verify_no_email_sent_to_business_if_applicant_scheduled(monkeypatch):
    past_date = datetime.datetime.now() - datetime.timedelta(hours=1)
    message_dict = get_verify_schedule_event(past_date)

    def mock_status_get(*args, **kwargs):
        return status_gets_success("2020-10-01")

    def mock_send_business_email(*args, **kwargs):
        # this method should never be called
        assert False

    monkeypatch.setattr(vips, "status_get", mock_status_get)
    monkeypatch.setattr(common_email, "send_to_business", mock_send_business_email)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=BaseConfig,
                                  writer=RabbitMQ)


def test_verify_schedule_check_placed_back_on_hold_if_vips_not_available(monkeypatch):
    past_date = datetime.datetime.now() + datetime.timedelta(hours=1)
    message_dict = get_verify_schedule_event(past_date)

    def mock_status_get(*args, **kwargs):
        return status_get_fail(False)

    def mock_publish(queue_name: str, payload: bytes):
        assert queue_name == "DF.hold"
        return True

    monkeypatch.setattr(BaseConfig, "ENCRYPT_KEY", "something-secret")
    monkeypatch.setattr(RabbitMQ, "publish", mock_publish)
    monkeypatch.setattr(vips, "status_get", mock_status_get)

    results = helper.middle_logic(helper.get_listeners(business.process_incoming_form(), message_dict['event_type']),
                                  message=message_dict,
                                  config=BaseConfig,
                                  writer=RabbitMQ)


def status_gets_success(review_start_date) -> tuple:
    data = {
            "resp": "success",
            "data": {
                "status": {
                    "noticeTypeCd": "IRP",
                    "noticeServedDt": "2020-09-10 00:00:00 -08:00",
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
    if len(review_start_date) > 0:
        data['data']['status']['reviewStartDtm'] = review_start_date + ' 09:30:00 -07:00'
    return True, data


def status_get_fail(is_success=True):
    return is_success, {
          "resp": "fail",
          "error": {
            "message": "Record not found",
            "httpStatus": 404
          }
    }


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
            "prohibition_number": "21258852"
          },
          "hold_until": hold_until_date_time.isoformat()
    }
