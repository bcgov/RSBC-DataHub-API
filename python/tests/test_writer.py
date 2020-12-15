import pytest
import python.writer.middleware as middleware


address_sample_data = [
    ["914 Yates Street", "914 Yates Street, BC"],
    ["E/B 914 Yates Street", "914 Yates Street, BC"],
    ["HWY # 1 / CLEARBROOK ON RAMP, ABBOTSFORD", "TRANS-CANADA HWY AND CLEARBROOK ON RAMP, ABBOTSFORD, BC"],
    ["HWY ONE - WELLSWOOD RD, MALAHAT", "TRANS-CANADA HWY AND WELLSWOOD RD, MALAHAT, BC"],
    ["HWY 97N AT HOFERKAMP, PRINCE GEORGE", "HWY-97 AND HOFERKAMP, PRINCE GEORGE, BC"],
    ["1100 BLK HIGHWAY ONE, SAANICH", "1100 TRANS-CANADA HWY, SAANICH, BC"],
    ["BLANSHARD ST SOUTH OF FINLAYSON, VICTORIA", "BLANSHARD ST AND FINLAYSON, VICTORIA, BC"],
    ["HWY 17 N/O ELK LAKE DR, SAANICH", "HWY-17 AND ELK LAKE DR, SAANICH, BC"],
    ["HWY 97SOUTH / BOYKO RD, PRINCE GEORGE", "HWY-97 AND BOYKO RD, PRINCE GEORGE, BC"],
    ["1200  HWY 16 E, PRINCE GEORGE", "1200 HWY-16 , PRINCE GEORGE, BC"],
    ["ISLAND HWY / ATKINS RD, COLWOOD", "ISLAND HWY AND ATKINS RD, COLWOOD, BC"]
]


@pytest.mark.parametrize("address_in, expected_output", address_sample_data)
def test_clean_address_method(address_in, expected_output):
    data = {"address_raw": address_in}
    is_success, data = middleware.clean_up_address(**data)
    assert data['address_clean'] == expected_output
