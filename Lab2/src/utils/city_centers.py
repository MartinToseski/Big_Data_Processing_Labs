import requests
import time
from src.config import NOMINATIM_API, HEADERS


def get_city_center(city):
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
        time.sleep(1)

        return lat, lon
    except:
        return None