import requests
import json
from db.init_db import connect
from src.config import OVERPASS_API
import time


def safe_request(query, retries=5):
    for i in range(retries):
        try:
            r = requests.post(OVERPASS_API, data=query)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 429:
                time.sleep(2 ** i)
        except:
            time.sleep(2 ** i)
    return None


# Collect Raw Data
def fetch_osm_data(city, timeout=60):
    query = f"""
    [out:json][timeout:{timeout}];
    area[name="{city}"]->.searchArea;
    (
        node["tourism"](area.searchArea);
        node["amenity"](area.searchArea);
    );
    out body 400;
    """

    data = safe_request(query)
    conn = connect()
    c = conn.cursor()

    c.execute(
        "INSERT INTO raw_data (source, city, raw_json) VALUES (?, ?, ?)",
        ("osm", city, json.dumps(data))
    )
    raw_id = c.lastrowid
    conn.commit()
    conn.close()

    return data, raw_id

