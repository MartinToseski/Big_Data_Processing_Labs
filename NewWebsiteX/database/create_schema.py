import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "website.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# ------------------------------------------------
# Cities
# ------------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS cities (
    city_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")

# ------------------------------------------------
# Places
# ------------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS places (
    place_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_id INTEGER,
    name TEXT,
    description TEXT,
    lat REAL,
    lon REAL,
    wiki_url TEXT,
    wiki_summary TEXT,
    wiki_links TEXT,
    image_url TEXT,
    pagerank_score REAL,
    relevance_score REAL,
    has_image INTEGER,
    FOREIGN KEY(city_id) REFERENCES cities(city_id)
)
""")

# ------------------------------------------------
# Categories
# ------------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")

# ------------------------------------------------
# Place Categories
# ------------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS place_categories (
    place_id INTEGER,
    category_id INTEGER,
    FOREIGN KEY(place_id) REFERENCES places(place_id),
    FOREIGN KEY(category_id) REFERENCES categories(category_id)
)
""")

# ------------------------------------------------
# Images
# ------------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS images (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id INTEGER,
    image_name TEXT,
    image_path TEXT,
    palette_path TEXT,
    feature_vector TEXT,
    image_class TEXT,
    FOREIGN KEY(place_id) REFERENCES places(place_id)
)
""")

# ------------------------------------------------
# Similar Places
# ------------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS similar_places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_place_id INTEGER,
    target_place_id INTEGER,
    similarity_score REAL,
    recommendation_type TEXT
)
""")

conn.commit()
conn.close()
print("Schema created.")
