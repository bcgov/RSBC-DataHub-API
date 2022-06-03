from python.prohibition_web_svc.middleware.form_middleware import convert_vancouver_to_utc
from datetime import datetime


def test_datetime_conversion():
    datetime_result = convert_vancouver_to_utc("2022-06-02T12:31:41-07:00")
    assert datetime_result == datetime(
        year=2022,
        month=6,
        day=2,
        hour=19,
        minute=31,
        second=41
        )
