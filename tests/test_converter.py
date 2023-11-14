from time import sleep
from math import isclose
import pytest
import json
from pathlib import Path
from converter import Converter


def create_test_converter(json_path: Path):
    input_dict = json.load(Path(json_path).open(encoding="UTF-8"))
    input_dict["converter"] = Converter(input_dict["input_string"])
    sleep(1)
    return input_dict


rd = create_test_converter("json/rd.json")
address = create_test_converter("json/address.json")
rd_no_comma = create_test_converter("json/rd_no_comma.json")
rd_no_comma_reversed = create_test_converter("json/rd_no_comma_reversed.json")
wgs84 = create_test_converter("json/wgs84.json")


def test_happy():
    assert True


@pytest.fixture(params=[address,
                        rd,
                        rd_no_comma,
                        rd_no_comma_reversed,
                        wgs84
                        ])
def data_set(request):
    return request.param


class TestConverter:
    def test_is_rd(self, data_set):
        assert data_set["converter"].input_is_rd == \
               data_set["input_is_rd"]

    def test_is_wgs84(self, data_set):
        assert data_set["converter"].input_is_wgs84 == \
               data_set["input_is_wgs84"]

    def test_is_address(self, data_set):
        assert data_set["converter"].input_is_address == \
               data_set["input_is_address"]

    def test_x(self, data_set):
        assert isclose(data_set["converter"].x,
                       data_set["rd"]["x"], abs_tol=1)

    def test_y(self, data_set):
        assert isclose(data_set["converter"].y,
                       data_set["rd"]["y"], abs_tol=1)

    def test_lat(self, data_set):
        assert isclose(data_set["converter"].lat,
                       data_set["wgs84"]["lat"],abs_tol=1)

    def test_lon(self, data_set):
        assert isclose(data_set["converter"].lon,
                       data_set["wgs84"]["lon"],abs_tol=1)

    def test_address(self, data_set):
        assert data_set["converter"].address == data_set["address"]
