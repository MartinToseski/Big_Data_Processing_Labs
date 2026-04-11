import json
from init_db import connect
from init_db import create_tables
from src.collectors.osm import fetch_osm_data

if __name__ == '__main__':
    #create_tables()

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

    conn.close()
    """

    data, raw_id = fetch_osm_data("London")
    with open("data/overpass_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)