import pytest
from python.form_handler.config import Config
import python.common.vips_api as vips
from datetime import datetime, timedelta
import python.common.middleware as middleware
from python.common.helper import load_json_into_dict

date_served_data = [
    ('IRP', 0, True),
    ('IRP', 1, True),
    ('IRP', 7, True),
    ('IRP', 8, False),
    ('IRP', 9, False),
    ('UL', 0, True),
    ('UL', 1, True),
    ('UL', 7, True),
    ('UL', 8, True),
    ('UL', 9, True),
    ('ADP', 0, True),
    ('ADP', 1, True),
    ('ADP', 7, True),
    ('ADP', 8, False),
    ('ADP', 9, False)
]


@pytest.mark.parametrize("prohibition_type, date_offset, expected", date_served_data)
def test_date_served_not_older_than_one_week_method(prohibition_type, date_offset, expected):
    vips_date_time_string = (datetime.today() - timedelta(days=date_offset)).strftime("%Y-%m-%d %H:%M:%S -08:00")
    vips_data = dict()
    vips_data['noticeTypeCd'] = prohibition_type
    vips_data['effectiveDt'] = vips_date_time_string
    (result, args) = middleware.date_served_not_older_than_one_week(vips_data=vips_data)
    assert result is expected


last_name_match_data = [
    ('Jones', 'Jones', True),
    ('Jones', 'JONES', True),
    ('Coté', 'Cote', True),  # note the accent on the "e"
    ('Jones', 'Other', False)
]


@pytest.mark.parametrize("user_entered_last_name, last_name_from_vips, expected", last_name_match_data)
def test_user_submitted_last_name_matches_vips_method(user_entered_last_name, last_name_from_vips, expected):
    vips_status = load_json_into_dict("python/tests/sample_data/vips/vips_query_200.json")
    vips_status['data']['status']['surnameNm'] = last_name_from_vips
    result, args = middleware.user_submitted_last_name_matches_vips(
        driver_last_name=user_entered_last_name,
        vips_data=vips_status['data']['status'])
    assert result is expected


served_recently_data = [
    (0, True),
    (1, True),
    (2, True),
    (3, False),
    (4, False)
]


@pytest.mark.parametrize("date_offset, expected", served_recently_data)
def test_prohibition_served_recently_method(date_offset, expected):
    days = timedelta(date_offset)
    new_date = datetime.today() - days
    date_under_test = new_date.strftime("%Y-%m-%d")
    result, args = middleware.prohibition_served_recently(
        date_of_service=date_under_test,
        config=Config)
    assert result is expected


exists_in_vips_data = [
    ("vips_query_404.json", False),
    ("vips_query_200.json", True)
]


@pytest.mark.parametrize("response_from_vips, expected", exists_in_vips_data)
def test_prohibition_exists_in_vips_method(response_from_vips, expected):
    vips_status = load_json_into_dict("python/tests/sample_data/vips/{}".format(response_from_vips))
    result, data = middleware.prohibition_exists_in_vips(vips_status=vips_status)
    assert result is expected
    if result:
        assert 'vips_data' in data


licence_seized = [
    ("UL", "Y", True),
    ("UL", "N", True),
    ("IRP", "Y", True),
    ("IRP", "N", False),
    ("ADP", "Y", True),
    ("ADP", "N", False)
]


@pytest.mark.parametrize("prohibition_type, test_condition, expected", licence_seized)
def test_has_drivers_licence_been_seized_method(prohibition_type, test_condition, expected):
    sample_data = load_json_into_dict('python/tests/sample_data/form/irp_form_submission.json')
    response_from_api = load_json_into_dict('python/tests/sample_data/vips/vips_query_200.json')
    response_from_api['data']['status']['driverLicenceSeizedYn'] = test_condition
    response_from_api['data']['status']['noticeTypeCd'] = prohibition_type
    vips_data = response_from_api['data']['status']
    result, args = middleware.has_drivers_licence_been_seized(message=sample_data, vips_data=vips_data)
    assert result is expected


applicant_roles = [
    ("driver", True),
    ("lawyer", False),
    ("advocate", False)
]

vips_date_strings = [
    ("20-JUN-2017", "2017-06-20 00:00:00 -07:00"),
]


@pytest.mark.parametrize("pay_bc_date, expected", vips_date_strings)
def test_pay_bc_date_transformation(pay_bc_date, expected):
    payload = dict()
    payload['receipt_date'] = pay_bc_date
    is_success, args = middleware.transform_receipt_date_from_pay_bc_format(payload=payload)
    date_object = args.get('receipt_date')
    actual = vips.vips_datetime(date_object)
    assert actual == expected

