import requests
import time
from Lab2.src.config import NOMINATIM_API, HEADERS


# Cache to avoid repeated API calls
_city_cache = {}


def get_city_center(city):
    if city in _city_cache:
        return _city_cache[city]

    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }

    try:
        response = requests.get(NOMINATIM_API, params=params, headers=HEADERS)
        if response.status_code != 200:
            return None

        data = response.json()
        if not data:
            return None

        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        _city_cache[city] = (lat, lon)
        time.sleep(1)

        return lat, lon
    except:
        return None