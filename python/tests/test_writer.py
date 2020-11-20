import pytest
import python.writer.middleware as middleware


address_sample_data = [
    ["914 Yates Street", "914 Yates Street"],
    ["E/B 914 Yates Street", "914 Yates Street"],
]


@pytest.mark.parametrize("address_in, expected_output", address_sample_data)
def test_clean_address_method(address_in, expected_output):
    data = {"address_raw": address_in}
    is_success, data = middleware.clean_up_address(**data)
    assert data['address_clean'] == expected_output
