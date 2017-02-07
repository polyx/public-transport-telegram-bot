from pprint import pprint

import requests
import utm
import arrow

HOME = 'Solvang'


# {'latitude': 59.95414, 'longitude': 10.729933},
def get_utm_location(x, y):
    """
    :param x: latitude in decimal degrees
    :param y: longitude in decimal degrees
    :return: x, y converted to the UTM format
    """
    x, y, _, _ = utm.from_latlon(x, y)
    return int(x), int(y)


