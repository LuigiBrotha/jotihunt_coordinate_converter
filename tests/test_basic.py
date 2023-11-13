import pytest
from converter import Converter
from temp.test_fixtures import rd

def test_happy():
    assert True

# class TestConverter:
#     def test_is_rd(self):
#         assert True
#
#     def test_is_wgs84(self):
#         assert True

@pytest.fixture
def make_converter():
    def _make_converter(converter_sample):
        return converter_sample
    return _make_converter

def test_converters(make_converter):
    make_converter(rd)

# class CONVERTER():
#     def __init__(self,
#                  input_string: str,
#                  input_is_rd: bool,
#                  input_is_wgs84: bool,
#                  input_is_address: str,
#                  x: float,
#                  y: float,
#                  lat: float,
#                  lon: float,
#                  address: str):
#             self.input_string=input_string
#
#             self.input_is_rd=input_is_rd
#             self.input_is_wgs84=input_is_wgs84
#             self.input_is_address=input_is_address
#
#             self.x=x
#             self.y=y
#
#             self.lat=lat
#             self.lon=lon
#
#             self.address=address
#
#
# @pytest.fixture
# def rd():
#     return CONVERTER(input_string="192550 443807",
#                      input_is_rd=True,
#                      input_is_wgs84=False,
#                      input_is_address=False,
#                      x=192550,
#                      y=443807,
#                      lat=51.98138,
#                      lon=5.93388,
#                      address="André de Thaye, 41, Voetiuslaan, Statenkwartier, "
#                              "Arnhem, Gelderland, Nederland, 6828 TD, Nederland")
#
#
# @pytest.mark.usefixtures("rd")
# class TestClass():
#     def test_input_string(self):
#         self.converter = Converter(rd.input_string)
#         assert self.converter.input_string == rd.input_string
#
#     def test_is_rd(self):
#         assert self.converter.input_is_rd == rd.input_is_rd

# class TestClass():
#     def test_is_rd(self, rd):
#         self.converter = Converter(rd.input_string)
#         assert self.converter.input_is_rd == rd.input_is_rd
#
#     def test_is_wgs84(self, rd):
#         self.converter = Converter(rd.input_string)
#         assert self.converter.input_is_wgs84 == rd.input_is_wgs84
#
#
#
#
#





