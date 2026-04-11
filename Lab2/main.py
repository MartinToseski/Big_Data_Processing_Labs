import json

from Tools.scripts.fixdiv import report

from init_db import connect
from init_db import create_tables
from src.collectors.osm import fetch_osm_data
from src.config import CITIES
from src.processing.process import process

if __name__ == '__main__':
    create_tables()

    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    print("Tables:", tables)

    c.execute("PRAGMA table_info(raw_data);")
    columns = c.fetchall()
    for col in columns:
        print(col)
    print("\n")

    c.execute("PRAGMA table_info(intermediate_data);")
    columns = c.fetchall()
    for col in columns:
        print(col)
    print("\n")

    c.execute("PRAGMA table_info(features);")
    columns = c.fetchall()
    for col in columns:
        print(col)
    
    c.execute("SELECT COUNT(*) FROM raw_data")
    print("Raw count:", c.fetchone()[0])
    
    conn.close()
    """

    for city in CITIES:
        print("Processing:", city)
        osm_data, raw_id = fetch_osm_data(city)
        path = f"data/raw_{city.lower()}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(osm_data, f, ensure_ascii=False, indent=2)
        process(osm_data, raw_id, city)

 #   """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM raw_data")
    print("Raw count:", c.fetchone()[0])
    c.execute("SELECT COUNT(*) FROM intermediate_data")
    print("Intermediate count:", c.fetchone()[0])
    c.execute("SELECT COUNT(*) FROM features")
    print("Features count:", c.fetchone()[0])
 #   """