import sqlite3
from src.config import DB_NAME

DB = f"{DB_NAME}.db"

def connect():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_tables():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS raw_data (
        id INTEGER PRIMARY KEY,
        source TEXT,
        city TEXT,
        raw_json TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS intermediate_data (
        id INTEGER PRIMARY KEY,
        raw_data_id INTEGER,
        name TEXT,
        city TEXT,
        lat REAL,
        lon REAL,
        category TEXT,
        tags_json TEXT,
        wikidata_id TEXT,
        FOREIGN KEY (raw_data_id) REFERENCES raw_data(id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS features (
        id INTEGER PRIMARY KEY,
        intermediate_id INTEGER,
        name TEXT,
        city TEXT,
        lat REAL,
        lon REAL,
        distance_to_center REAL,
        category_encoded INTEGER,
        tags_count INTEGER,
        description_length INTEGER,
        has_website INTEGER,
        has_wikipedia INTEGER,
        is_tourism_place INTEGER,
        has_phone INTEGER,
        FOREIGN KEY (intermediate_id) REFERENCES intermediate_data(id)
    )
    """)

    conn.commit()
    conn.close()