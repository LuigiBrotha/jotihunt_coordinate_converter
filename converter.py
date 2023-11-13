from epsg import RD_to_WGS84, WGS84_to_RD
import pyproj
from locale import atof
import re
from geopy.geocoders import Nominatim


class Converter:
    geolocator = Nominatim(user_agent="sollicitatie")

    def __init__(self, input_string: str):
        self._input_string = input_string.strip() \
            .replace(",", "")

        self._coords_compile = re.compile(
            "\s*(\d+|\d+\.\d+)\s+(\d+|\d+\.\d+)\s*")

        self._input_is_rd = None
        self._input_is_wgs84 = None
        self._input_is_address = None

        # RD
        self._x = None
        self._y = None

        # WGS84
        self._lat = None
        self._lon = None

        self._get_input_type_

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def lat(self) -> float:
        return self._lat

    @property
    def lon(self) -> float:
        return self._lon

    @property
    def address(self) -> str:
        return self._address

    @property
    def input_string(self) -> str:
        return self._input_string

    @input_string.setter
    def input_string(self, input_string: str):
        self._input_string = input_string

    @property
    def coords(self) -> (float, float):
        result = self._coords_compile.fullmatch(self._input_string)
        if result is None:
            return (0, 0)
        else:
            return tuple(atof(i) for i in result.groups())

    @property
    def _get_input_type_(self):
        coord_max = max(self.coords)
        coord_min = min(self.coords)

        if 650_000 > coord_max > 100 and \
                300_000 > coord_min > 100:
            self._input_is_rd = True
            self._input_is_wgs84 = False
            self._input_is_address = False
            # Coordinates
            self._x = coord_min
            self._y = coord_max

            self._lat, self._lon = RD_to_WGS84.transform(self._x, self._y)

            self._address = self.geolocator.reverse(f"{self._lat}, {self.lon}")

        elif 100 > coord_max > 10 and 10 > coord_min > 0:
            self._input_is_rd = False
            self._input_is_wgs84 = True
            self._input_is_address = False
            # Coordinates
            self._lat = coord_max
            self._lon = coord_min

            self._x, self._y = WGS84_to_RD.transform(self._lat, self._lon)

            self._address = self.geolocator \
                .reverse(f"{self._lat}, {self.lon}") \
                .address

        elif coord_max == 0 and coord_min == 0:
            self._input_is_rd = False
            self._input_is_wgs84 = False
            self._input_is_address = True

            location = self.geolocator \
                .geocode(f"{self._input_string}")

            self._address = location.address

            self._lon = location.longitude
            self._lat = location.latitude

            self._x, self._y = WGS84_to_RD.transform(self._lat, self._lon)



        else:
            NotImplementedError

    @property
    def input_is_rd(self) -> bool:
        self._get_input_type_
        return self._input_is_rd

    @property
    def input_is_wgs84(self) -> bool:
        self._get_input_type_

        return self._input_is_wgs84

    @property
    def input_is_address(self) -> bool:
        return self._input_is_address

    @property
    def dict(self):
        return {"wgs84": {
            "lat": self.lat,
            "lon": self.lon
        },
            "rd": {
                "x": self.x,
                "y": self.y
            },
            "address": self.address}


if __name__ == "__main__":
    converter = Converter("192550, 443807")
    print(converter.dict)
