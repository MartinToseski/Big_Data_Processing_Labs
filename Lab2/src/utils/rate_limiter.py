import requests
from Lab2.src.config import HEADERS
import time


def safe_request(url, method="GET", data=None, params=None, retries=5, delay=0.2):
    for i in range(retries):
        try:
            if method == "GET":
                r = requests.get(url, headers=HEADERS, params=params)
            else:
                r = requests.post(url, headers=HEADERS, data=data)

            if r.status_code == 200:
                return r.json()

            elif r.status_code in [429, 503]:
                time.sleep(2 ** i)

        except Exception:
            time.sleep(2 ** i)

    return None