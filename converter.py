"""
Converter is used as a module for the Converter class. The Converter class is
used to convert an input (RD, WGS84 or Address)  to RD, WGS84 and an address.
"""
from locale import atof
import re
from geopy.geocoders import Nominatim

from epsg import RD_to_WGS84, WGS84_to_RD


class Converter:
    """
    Class to converter RD, WGS84 and address to RD, WGS84 and address.
    """
    geolocator = Nominatim(user_agent="sollicitatie")

    def __init__(self, raw_string: str):
        self._raw_string = raw_string
        self._input_string = raw_string.strip() \
            .replace(",", "")

        self._coords_compile = re.compile(
            r"\s*(\d+|\d+\.\d+)\s+(\d+|\d+\.\d+)\s*")

        self._input_is_rd = None
        self._input_is_wgs84 = None
        self._input_is_address = None

        # RD
        self._x = None
        self._y = None

        # WGS84
        self._lat = None
        self._lon = None

        self._address = None

        self._get_input_type_()

    @property
    def x(self) -> float:
        """
        Return x-coordinate for rd.
        :return:
        """
        return self._x

    @property
    def y(self) -> float:
        """
        Return y-coordinate for rd.
        :return:
        """
        return self._y

    @property
    def lat(self) -> float:
        """
        Return latituate for wgs84
        :return:
        """
        return self._lat

    @property
    def lon(self) -> float:
        """
        Return longitude for wgs84
        :return:
        """
        return self._lon

    @property
    def address(self) -> str:
        """
        Return the address.
        :return:
        """
        return self._address

    @property
    def input_string(self) -> str:
        "Return input_string"
        return self._input_string

    @input_string.setter
    def input_string(self, input_string: str):
        """
        When setting the input_string also update _get_input_type_
        :param input_string:
        :return:
        """
        self._input_string = input_string
        self._get_input_type_()

    @property
    def coords(self) -> (float, float):
        """
        Returns the 2 coordinates of the input_string if available. Otherwise
        returns the coordinates 0,0
        :return:
        """
        result = self._coords_compile.fullmatch(self._input_string)
        if result is None:
            return (0, 0)
        return tuple(atof(i) for i in result.groups())

    def _get_input_type_(self) -> None:
        """
        Validates what the input type is.
        :return:
        """
        coord_max = max(self.coords)
        coord_min = min(self.coords)

        is_rd = 650_000 > coord_max > 100 and 300_000 > coord_min > 100
        is_wgs_84 = 100 > coord_max > 10 and 10 > coord_min > 0
        is_address = coord_max == 0 and coord_min == 0

        if is_rd:
            self._input_is_rd = True
            self._input_is_wgs84 = False
            self._input_is_address = False
            # Coordinates
            self._x = coord_min
            self._y = coord_max

            self._lat, self._lon = RD_to_WGS84.transform(self._x, self._y)

            self._address = self.geolocator.reverse(
                f"{self._lat}, {self.lon}").address


        elif is_wgs_84:
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

        elif is_address:
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
            raise NotImplementedError("Could not determine time of input.")

    @property
    def input_is_rd(self) -> bool:
        "True if the input_string is rd"
        return self._input_is_rd

    @property
    def input_is_wgs84(self) -> bool:
        "True if the input_string is wgs84"
        return self._input_is_wgs84

    @property
    def input_is_address(self) -> bool:
        "True if the input_string is address"
        return self._input_is_address

    @property
    def dict(self) -> dict:
        """
        Returns a dictionary with the wgs84, rd and address values
        :return:
        """
        return {"wgs84": {
            "lat": self.lat,
            "lon": self.lon
        },
            "rd": {
                "x": self.x,
                "y": self.y
            },
            "address": self.address}
