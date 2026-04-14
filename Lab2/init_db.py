import sqlite3
from Lab2.src.config import DB_PATH


def connect(path=""):
    conn = sqlite3.connect(path+DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_tables():
    conn = connect("")
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

    c.execute("""
    CREATE TABLE IF NOT EXISTS relevance (
        id INTEGER PRIMARY KEY,
        feature_id INTEGER,
        score REAL,
        FOREIGN KEY (feature_id) REFERENCES features(id) ON DELETE CASCADE
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS graph_edges (
        id INTEGER PRIMARY KEY,
        source_id INTEGER,
        target_id INTEGER,
        FOREIGN KEY (source_id) REFERENCES features(id) ON DELETE CASCADE,
        FOREIGN KEY (target_id) REFERENCES features(id) ON DELETE CASCADE,
        UNIQUE(source_id, target_id)
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS pagerank (
        id INTEGER PRIMARY KEY,
        node_id INTEGER,
        score REAL,
        FOREIGN KEY (node_id) REFERENCES features(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()