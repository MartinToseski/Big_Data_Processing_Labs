import requests
import time
from src.config import NOMINATIM_API

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

    headers = {
        "User-Agent": "big-data-lab-project"
    }

    try:
        response = requests.get(NOMINATIM_API, params=params, headers=headers)

        if response.status_code != 200:
            return None

        data = response.json()

        if not data:
            return None

        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])

        _city_cache[city] = (lat, lon)

        time.sleep(1)  # respect API limits

        return lat, lon

    except:
        return None