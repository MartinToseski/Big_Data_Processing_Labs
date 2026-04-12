import requests
import urllib.parse
import time
from src.config import HEADERS
from src.utils.rate_limiter import safe_request


"""
def safe_get(url, retries=5):
    for i in range(retries):
        try:
            r = requests.get(url, headers=HEADERS)

            if r.status_code == 200:
                return r.json()

        except Exception as e:
            time.sleep(2 ** i)

    return None
"""


def get_wikipedia_title(wikidata_id):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"

    data = safe_request(url)

    if not data:
        return None

    try:
        entity = data["entities"].get(wikidata_id, {})
        sitelinks = entity.get("sitelinks", {})

        if "enwiki" in sitelinks:
            return sitelinks["enwiki"]["title"]

    except Exception as e:
        print("Wikidata error:", e)

    return None


def get_description_length(title):
    if not title:
        return 0

    try:
        formatted_title = urllib.parse.quote(title.replace(" ", "_"))
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_title}"

        data = safe_request(url)

        if not data:
            return 0

        return len(data.get("extract", ""))

    except Exception as e:
        print("Wiki error:", e)
        return 0


def enrich(tags):
    wikidata_id = tags.get("wikidata") or tags.get("brand:wikidata")

    if not wikidata_id:
        return None, 0

    title = get_wikipedia_title(wikidata_id)
    desc_len = get_description_length(title)

    time.sleep(0.2)

    return wikidata_id, desc_len