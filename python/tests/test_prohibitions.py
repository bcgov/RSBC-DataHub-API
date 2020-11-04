import pytest
import pytz
import python.common.helper as helper
from datetime import datetime, timedelta
import python.common.prohibitions as pro


review_date_times = [
    # Applicant applies on the same day as the date of service
    # Type, ServiceDate   TodayIs       MinReviewDt   MaxReviewDt
    ('IRP', "2020-09-10", "2020-09-10", "2020-09-18", "2020-09-25"),
    ('ADP', "2020-09-10", "2020-09-10", "2020-09-18", "2020-09-25"),

    # Applicant applies the day after date of service
    # Type, ServiceDate   TodayIs       MinReviewDt   MaxReviewDt
    ('IRP', "2020-09-10", "2020-09-11", "2020-09-18", "2020-09-25"),
    ('ADP', "2020-09-10", "2020-09-11", "2020-09-18", "2020-09-25"),

    # Applicant waits and applies on the fifth date
    # Type, ServiceDate   TodayIs       MinReviewDt   MaxReviewDt
    ('IRP', "2020-09-10", "2020-09-15", "2020-09-19", "2020-09-25"),
    ('ADP', "2020-09-10", "2020-09-15", "2020-09-19", "2020-09-25"),

    # Applicant waits and applies on the last possible date
    # Type, ServiceDate   TodayIs       MinReviewDt   MaxReviewDt
    ('IRP', "2020-09-10", "2020-09-16", "2020-09-20", "2020-09-25"),
    ('ADP', "2020-09-10", "2020-09-16", "2020-09-20", "2020-09-25"),

    # ULs are a special case, earliest possible date doesn't change
    # but there is no legislated max review date. As per business
    # rule, set max review date to two weeks from today.
    # Type, ServiceDate   TodayIs       MinReviewDt   MaxReviewDt
    ('UL', "2020-09-10", "2020-09-11", "2020-09-15", "2020-09-26"),
    ('UL', "2020-09-10", "2020-09-15", "2020-09-19", "2020-09-30"),
]


@pytest.mark.parametrize("prohib_type, date_served, today_is, min_expected, max_expected", review_date_times)
def test_get_application_window(prohib_type: str, date_served: str, today_is: str, min_expected: str, max_expected: str):
    iso = "%Y-%m-%d"
    date_served_object = helper.localize_timezone(datetime.strptime(date_served, iso))
    today_object = helper.localize_timezone(datetime.strptime(today_is, iso))
    prohibition = pro.prohibition_factory(prohib_type)
    result = prohibition.get_min_max_review_dates(date_served_object, today_object)
    assert result[0] == helper.localize_timezone(datetime.strptime(min_expected, iso))
    assert result[1] == helper.localize_timezone(datetime.strptime(max_expected, iso))


prohibition_types = [
    ('IRP', "ImmediateRoadside", "Immediate roadside prohibition"),
    ('ADP', "AdministrativeDriving", "Administrative driving prohibition"),
    ('UL', "UnlicencedDriver", "Unlicensed driver prohibition"),
]


@pytest.mark.parametrize("prohib_type, class_expected, verbose_type", prohibition_types)
def test_prohibition_factory(prohib_type: str, class_expected: str, verbose_type: str):
    prohibition = pro.prohibition_factory(prohib_type)
    assert class_expected in str(prohibition.__class__)


@pytest.mark.parametrize("prohib_type, class_expected, verbose_type", prohibition_types)
def test_prohibition_type_verbose(prohib_type: str, class_expected: str, verbose_type: str):
    prohibition = pro.prohibition_factory(prohib_type)
    assert verbose_type == prohibition.type_verbose()


def test_prohibition_unknown_factory():
    prohibition = pro.prohibition_factory('')
    assert prohibition is None


oral_eligible = [

    # Type, originalCause   Pass?
    ('IRP', "IRP90ANY",     True),
    ('IRP', "IRP90FAIL",    True),
    ('IRP', "IRP90REFUSE",  True),
    ('IRP', "IRP30ANY",     True),
    ('IRP', "IRP90",        True),
    ('IRP', "IRP30",        True),
    ('IRP', "IRP30WARN",    True),
    ('IRP', "IRP7",         False),
    ('IRP', "IRP3",         False),
    ('IRP', "IRP3ANY",      False),
    ('IRP', "IRP7ANY",      False),
    ('ADP', "BREATHSAMP",   True),
    ('UL',  "",             False),
]


@pytest.mark.parametrize("prohibition_type, original_cause, expected", oral_eligible)
def test_is_oral_review_eligible(prohibition_type: str, original_cause: str, expected):
    vips_data = {
        "originalCause": original_cause
    }
    prohibition = pro.prohibition_factory(prohibition_type)
    result = prohibition.is_eligible_for_oral_review(vips_data=vips_data)
    assert result == expected


@pytest.mark.parametrize("today_is, prohibition_type, service_date, okay_to_apply, okay_to_pay, min_expected, max_expected, comments",
                         helper.get_csv_test_data('./python/tests/test_prohibition_data.csv'))
def test_key_prohibition_functions_window(today_is: str,
                                          prohibition_type: str,
                                          service_date: str,
                                          okay_to_apply: str,
                                          okay_to_pay: str,
                                          min_expected: str,
                                          max_expected: str,
                                          comments: str):
    iso = "%Y-%m-%d"
    date_served_object = helper.localize_timezone(datetime.strptime(service_date, iso))
    today_object = helper.localize_timezone(datetime.strptime(today_is, iso))
    first_review_date = helper.localize_timezone(datetime.strptime(min_expected, iso))
    last_review_date = helper.localize_timezone(datetime.strptime(max_expected, iso))
    prohibition = pro.prohibition_factory(prohibition_type)
    result = prohibition.get_min_max_review_dates(date_served_object, today_object)
    assert prohibition.is_okay_to_apply(date_served_object, today_object) is (okay_to_apply == "Yes")
    assert prohibition.is_okay_to_apply(date_served_object, today_object) is (okay_to_pay == "Yes")
    assert result[0] == first_review_date
    assert result[1] == last_review_date



