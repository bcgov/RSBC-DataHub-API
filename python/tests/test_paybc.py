from python.paybc_api.website.routes import pay_bc_date_to_datetime
from python.common.vips_api import vips_datetime
import pytest
import pytz
from iso8601 import parse_date
from datetime import datetime, timezone


class TestPayBC:

    vips_date_strings = [
        ("20-JUN-2017", "2017-06-20 00:00:00 -07:00"),
    ]

    @pytest.mark.parametrize("pay_bc_date, expected", vips_date_strings)
    def test_pay_bc_date_transformation(self, pay_bc_date, expected):
        date_object = pay_bc_date_to_datetime(pay_bc_date)
        print(date_object)
        actual = vips_datetime(date_object)
        assert actual == expected

