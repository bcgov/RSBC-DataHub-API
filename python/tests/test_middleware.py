import pytest
from datetime import datetime, timedelta
import python.form_handler.middleware as middleware
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
    sample_data = dict()
    vips_data = dict()
    vips_data['surnameNm'] = last_name_from_vips
    sample_data = load_json_into_dict('python/tests/sample_data/form/irp_form_submission.json')
    sample_data['form_submission']['form']['identification-information']['driver-last-name'] = user_entered_last_name
    result, args = middleware.user_submitted_last_name_matches_vips(message=sample_data, vips_data=vips_data)
    assert result is expected


should_have_been_entered_into_vips_data = [
    (False, 0, False),
    (False, 2, False),
    (False, 3, True),
    (True, 0, True),
    (True, 2, True),
    (True, 3, True)
]


@pytest.mark.parametrize("is_vips_status_successful, date_offset, expected", should_have_been_entered_into_vips_data)
def test_prohibition_should_have_been_entered_in_vips_method(is_vips_status_successful, date_offset, expected):
    days = timedelta(date_offset)
    new_date = datetime.today() - days
    date_under_test = new_date.strftime("%Y-%m-%d")
    sample_data = load_json_into_dict('python/tests/sample_data/form/irp_form_submission.json')
    sample_data['form_submission']['form']['prohibition-information']['date-of-service'] = date_under_test
    result, args = middleware.prohibition_should_have_been_entered_in_vips(
        message=sample_data,
        delay_days='3',
        vips_data_success=is_vips_status_successful)
    assert result is expected


exists_in_vips_data = [
    (True, True),
    (False, False)
]


@pytest.mark.parametrize("vips_data_success, expected", exists_in_vips_data)
def test_prohibition_exists_in_vips_method(vips_data_success, expected):
    # I know not worth testing, but for completeness ...
    result, args = middleware.prohibition_exists_in_vips(vips_data_success=vips_data_success)
    assert result is expected


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
    vips_status = response_from_api['data']['status']
    result, args = middleware.has_drivers_licence_been_seized(message=sample_data, vips_status=vips_status)
    assert result is expected


applicant_roles = [
    ("driver", True),
    ("lawyer", False),
    ("advocate", False)
]

