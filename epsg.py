"""
Helper module which makes reading conversions of RD and WGS84 easier.
"""
from pyproj import CRS, Transformer
from geopy.geocoders import Nominatim

WGS84 = CRS.from_epsg(4326)
RD = CRS.from_epsg(28992)

WGS84_to_RD = Transformer.from_crs(WGS84, RD)
RD_to_WGS84 = Transformer.from_crs(RD, WGS84)

if __name__ == "__main__":
    geolocator = Nominatim(user_agent="sollicitatie")
    location = geolocator.reverse("52.509669, 13.376294")
    print(location)
