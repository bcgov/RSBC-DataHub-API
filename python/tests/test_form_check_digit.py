from python.common.helper import validate_form_number
import pytest


class TestIrpCheckDigit:

    testdata = [
        '221633429',
        '221549593',
        '221633395',
        '218303283',
        '217813144',
        '217813076',
        '221633395',
        '303342348',
        '303474246',
        '303474299',
    ]

    @staticmethod
    @pytest.mark.parametrize("param", testdata)
    def test_check_digit(param):
        assert validate_form_number(param) is True
