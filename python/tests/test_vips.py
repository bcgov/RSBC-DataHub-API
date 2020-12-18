import python.common.vips_api as vips
import logging
import json
from unittest.mock import MagicMock
from python.common.helper import load_json_into_dict, localize_timezone
import pytest
import pytz
from iso8601 import parse_date
from datetime import datetime, timezone


class TestConfig:
    VIPS_API_ROOT_URL           = 'https://someserver.gov.bc.ca/endpoint'
    VIPS_API_USERNAME           = 'username'
    VIPS_API_PASSWORD           = 'password'


class TestVips:

    CORRELATION_ID = 'ABC'

    @staticmethod
    def test_build_endpoint_method():
        prohibition_number = "1234"
        endpoint = vips.build_endpoint(TestConfig.VIPS_API_ROOT_URL, prohibition_number, 'status')
        assert isinstance(endpoint, str)
        assert TestConfig.VIPS_API_ROOT_URL + '/' + prohibition_number + '/status' == endpoint

    @staticmethod
    def test_health_check_method():
        response = load_json_into_dict('python/tests/sample_data/vips/vips_health_check_200.json')
        vips.get = MagicMock(return_value=(True, response))
        endpoint = TestConfig.VIPS_API_ROOT_URL + '/api/utility/ping'
        vips.get(endpoint, TestConfig.VIPS_API_USERNAME, TestConfig.VIPS_API_PASSWORD)
        is_success, actual = vips.health_get(TestConfig)
        vips.get.assert_called_with(endpoint, TestConfig.VIPS_API_USERNAME, TestConfig.VIPS_API_PASSWORD)
        print(json.dumps(actual))
        assert is_success is True
        assert "responseMessage" in actual

    @staticmethod
    def test_query_get_method_success():
        response_from_api = load_json_into_dict('python/tests/sample_data/vips/vips_query_200.json')
        vips.get = MagicMock(return_value=(True, response_from_api))
        endpoint = TestConfig.VIPS_API_ROOT_URL + '/12345/status/' + TestVips.CORRELATION_ID
        vips.get(endpoint, TestConfig.VIPS_API_USERNAME, TestConfig.VIPS_API_PASSWORD)
        is_success, actual = vips.status_get("12345", TestConfig, TestVips.CORRELATION_ID)
        vips.get.assert_called_with(
            endpoint,
            TestConfig.VIPS_API_USERNAME,
            TestConfig.VIPS_API_PASSWORD,
            TestVips.CORRELATION_ID)
        print(json.dumps(actual))
        assert is_success is True
        assert "driverLicenceSeizedYn" in actual['data']['status']
        assert "surnameNm" in actual['data']['status']
        assert "disclosure" in actual['data']['status']

    @staticmethod
    def test_query_get_method_failure():
        response_from_api = load_json_into_dict('python/tests/sample_data/vips/vips_query_404.json')
        vips.get = MagicMock(return_value=(True, response_from_api))
        endpoint = TestConfig.VIPS_API_ROOT_URL + '/12345/status/' + TestVips.CORRELATION_ID
        vips.get(endpoint, TestConfig.VIPS_API_USERNAME, TestConfig.VIPS_API_PASSWORD)
        is_success, actual = vips.status_get("12345", TestConfig, TestVips.CORRELATION_ID)
        vips.get.assert_called_with(
            endpoint,
            TestConfig.VIPS_API_USERNAME,
            TestConfig.VIPS_API_PASSWORD,
            TestVips.CORRELATION_ID)
        print(json.dumps(actual))
        assert is_success is True
        assert "fail" in actual['resp']

    @staticmethod
    def test_query_get_method_bad_response():
        response_from_api = dict({"offline": True})
        vips.get = MagicMock(return_value=(False, response_from_api))
        endpoint = TestConfig.VIPS_API_ROOT_URL + '/12345/status/' + TestVips.CORRELATION_ID
        vips.get(endpoint, TestConfig.VIPS_API_USERNAME, TestConfig.VIPS_API_PASSWORD)
        is_success, actual = vips.status_get("12345", TestConfig, TestVips.CORRELATION_ID)
        vips.get.assert_called_with(
            endpoint,
            TestConfig.VIPS_API_USERNAME,
            TestConfig.VIPS_API_PASSWORD,
            TestVips.CORRELATION_ID)
        print(json.dumps(actual))
        assert is_success is False

    @staticmethod
    def test_disclosure_get_method():
        response_from_api = load_json_into_dict('python/tests/sample_data/vips/vips_disclosure_200.json')
        vips.get = MagicMock(return_value=(True, response_from_api))
        endpoint = TestConfig.VIPS_API_ROOT_URL + '/1234/disclosure/' + TestVips.CORRELATION_ID
        vips.get(endpoint, TestConfig.VIPS_API_USERNAME, TestConfig.VIPS_API_PASSWORD)
        is_success, actual = vips.disclosure_get("1234", TestConfig, TestVips.CORRELATION_ID)
        vips.get.assert_called_with(
            endpoint,
            TestConfig.VIPS_API_USERNAME,
            TestConfig.VIPS_API_PASSWORD,
            TestVips.CORRELATION_ID)
        assert is_success is True
        assert "document" in actual['data']

    @staticmethod
    def test_payment_get_method():
        response_from_api = load_json_into_dict('python/tests/sample_data/vips/vips_payment_200.json')
        vips.get = MagicMock(return_value=(True, response_from_api))
        endpoint = TestConfig.VIPS_API_ROOT_URL + '/1234/payment/status/' + TestVips.CORRELATION_ID
        vips.get(endpoint, TestConfig.VIPS_API_USERNAME, TestConfig.VIPS_API_PASSWORD)
        is_success, actual = vips.payment_get("1234", TestConfig, TestVips.CORRELATION_ID)
        vips.get.assert_called_with(
            endpoint,
            TestConfig.VIPS_API_USERNAME,
            TestConfig.VIPS_API_PASSWORD,
            TestVips.CORRELATION_ID)
        assert is_success is True
        assert "transactionInfo" in actual['data']

    vips_date_strings = [
        ("2019-01-02 17:30:00 -08:00", "2019-01-02 17:30:00-0800"),
        ("2019-01-02 17:30:00 -07:00", "2019-01-02 17:30:00-0700"),
    ]

    @pytest.mark.parametrize("vips_datetime, expected", vips_date_strings)
    def test_vips_datetime_conversion(self, vips_datetime, expected):
        actual = vips.vips_str_to_datetime(vips_datetime)
        assert actual == parse_date(expected)

    @staticmethod
    def test_datetime_to_vips_string():
        tz = pytz.timezone('America/Vancouver')
        date_under_test = localize_timezone(datetime.strptime("2020-11-22", "%Y-%m-%d"))
        vips_date_string = vips.vips_datetime(date_under_test)
        components = vips_date_string.split(":")
        print(date_under_test.strftime("%z"))
        print(vips_date_string)
        assert len(components) == 4
        assert vips_date_string[0:22] == '2020-11-22 00:00:00 -0'

    @staticmethod
    def test_transform_schedule_to_local_friendly_times():
        vips_response = load_json_into_dict('python/tests/sample_data/vips/vips_schedule_200.json')
        time_slots = vips_response['data']['timeSlots']
        print(json.dumps(time_slots[0]))
        print(str(type(time_slots[0])))
        friendly_times_list = vips.time_slots_to_friendly_times(time_slots, "ORAL")
        expected = list(["Fri, Sep 4, 2020 - 9:00AM to 9:30AM", "Fri, Sep 4, 2020 - 10:00AM to 10:30AM",
                         "Fri, Sep 4, 2020 - 11:00AM to 11:30AM", "Fri, Sep 4, 2020 - 12:00PM to 12:30PM",
                         "Fri, Sep 4, 2020 - 1:00PM to 1:30PM"])
        for index, item in enumerate(expected):
            assert friendly_times_list[index]['label'] == item

    @staticmethod
    def test_list_of_weekday_dates_between_method():
        start_date = datetime.strptime("2020-09-01", "%Y-%m-%d")
        end_date = datetime.strptime("2020-09-07", "%Y-%m-%d")
        expected = list(["2020-09-01", "2020-09-02", "2020-09-03", "2020-09-04", "2020-09-07"])
        list_of_date_times = vips.list_of_weekdays_dates_between(start_date, end_date)
        assert list(map(iso_date_string, list_of_date_times)) == expected

    @staticmethod
    def test_last_name_match():
        response_from_api = load_json_into_dict('python/tests/sample_data/vips/vips_query_200.json')
        is_success = vips.is_last_name_match(response_from_api['data']['status'], "Norris")
        assert is_success is True

    dates_to_test = [
        ("2020-11-02", "2020-11-03"),
        ("2020-11-03", "2020-11-04"),
        ("2020-11-06", "2020-11-09"),
        ("2020-11-07", "2020-11-09"),
        ("2020-11-08", "2020-11-09"),
        ("2020-11-09", "2020-11-10"),
    ]

    @staticmethod
    @pytest.mark.parametrize("date_under_test, next_business_date", dates_to_test)
    def test_next_business_date(date_under_test, next_business_date):
        iso = "%Y-%m-%d"
        date_time = datetime.strptime(date_under_test, iso)
        expected = datetime.strptime(next_business_date, iso)
        assert vips.next_business_date(date_time) == expected

    get_schedule_data = [
        ("IRP", "ORAL", "2020-11-02", "2020-11-03", 1, 2),
        ("IRP", "ORAL", "2020-11-02", "2020-11-07", 1, 5),
        ("IRP", "ORAL", "2020-11-02", "2020-11-10", 2, 7),
        ("IRP", "ORAL", "2020-11-02", "2020-11-08", 0, 0)
    ]

    @staticmethod
    @pytest.mark.parametrize(
        "prohibition_type, review_type, first_date, last_date, get_time_slots, count_days", get_schedule_data)
    def test_schedule_get_method(
            prohibition_type, review_type, first_date, last_date, get_time_slots, count_days, monkeypatch):

        correlation_id = 'abcdef'
        iso = "%Y-%m-%d"

        def mock_vips_get(*args):
            endpoint_list = args[0].split("/")
            query_date = endpoint_list[6]
            print(query_date)

            assert args[0] == vips.build_endpoint(
                TestConfig.VIPS_API_ROOT_URL,
                prohibition_type,
                review_type,
                query_date,
                "review",
                "availableTimeSlot",
                correlation_id
            )

            endpoint_list = args[0].split("/")
            print(endpoint_list)

            return mock_schedule_get(get_time_slots, query_date)

        first_datetime = datetime.strptime(first_date, iso)
        last_datetime = datetime.strptime(last_date, iso)

        monkeypatch.setattr(vips, "get", mock_vips_get)

        is_successful, data = vips.schedule_get(
            prohibition_type,
            review_type,
            first_datetime,
            last_datetime,
            TestConfig,
            correlation_id)

        assert is_successful
        print(data)
        assert data['number_review_days_offered'] == count_days


def iso_date_string(date_time: datetime) -> str:
    return date_time.strftime("%Y-%m-%d")


def mock_schedule_get(time_slots: int, query_date: str) -> tuple:
    if time_slots == 0:
        return False, dict({
          "resp": "fail",
          "error": {
            "message": "Requested data not found",
            "httpStatus": 404
          }
        })
    elif 0 < time_slots < 7:
        items = list()
        for item in range(time_slots):
            hour = str(time_slots + 9)
            items.append({
                "reviewStartDtm": query_date + ' ' + hour.zfill(2) + ":00:00 -08:00",
                "reviewEndDtm": query_date + ' ' + hour.zfill(2) + ":30:00 -08:00",
            })
        logging.info("items: {}".format(json.dumps(items)))
        return True, dict({
            "resp": "success",
            "data": {
                "timeSlots": items
            }
        })
    else:
        logging.warning('too many time slots requested')
        return True, dict()
