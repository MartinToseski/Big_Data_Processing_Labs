import json
from Lab2.init_db import connect
from Lab2.src.config import OVERPASS_API
from Lab2.src.utils.rate_limiter import safe_request


# Collect Raw Data
def fetch_osm_data(city, timeout=60):
    query = f"""
    [out:json][timeout:{timeout}];
    area[name="{city}"]->.searchArea;
    (
        node["historic"="monument"](area.searchArea);
        node["shop"](area.searchArea);
        node["tourism"="artwork"](area.searchArea);
    );
    out body 300;
    """

    data = safe_request(OVERPASS_API, method="POST", data=query)
    if not data:
        print("Failed to fetch data")
        return None, None

    conn = connect("")
    c = conn.cursor()

    c.execute(
        "INSERT INTO raw_data (source, city, raw_json) VALUES (?, ?, ?)",
        ("osm", city, json.dumps(data))
    )
    raw_id = c.lastrowid
    conn.commit()
    conn.close()

    return data, raw_id