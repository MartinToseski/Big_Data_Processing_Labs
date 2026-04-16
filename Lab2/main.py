import os
import json
from init_db import connect, create_tables
from src.collectors.osm import fetch_osm_data
from src.config import CITIES, DB_PATH
from src.processing.process import process


if __name__ == '__main__':
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    create_tables()

    for city in CITIES:
        print("Processing:", city)
        osm_data, raw_id = fetch_osm_data(city)
        json_path = f"data/raw_{city.lower()}.json"

        if os.path.exists(json_path):
            os.remove(json_path)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(osm_data, f, ensure_ascii=False, indent=2)

        process(osm_data, raw_id, city)

 #   """
    conn = connect("")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM raw_data")
    print("Raw count:", c.fetchone()[0])
    c.execute("SELECT COUNT(*) FROM intermediate_data")
    print("Intermediate count:", c.fetchone()[0])
    c.execute("SELECT COUNT(*) FROM features")
    print("Features count:", c.fetchone()[0])
 #   """