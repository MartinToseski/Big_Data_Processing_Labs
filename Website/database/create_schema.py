import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'website.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ------------------------------------------------
# Places
# ------------------------------------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS places (
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    lat REAL,
    lon REAL,
    category TEXT,
    description TEXT,
    pagerank_score REAL,
    relevance_score REAL,
    has_image INTEGER DEFAULT 0
)
''')

# ------------------------------------------------
# Images
# ------------------------------------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id INTEGER,
    image_name TEXT,
    image_path TEXT,
    palette_path TEXT,
    feature_vector TEXT,
    image_class TEXT,
    FOREIGN KEY(place_id) REFERENCES places(id)
)
''')

# ------------------------------------------------
# Structural Recommendations
# ------------------------------------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS structural_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_place_id INTEGER,
    recommended_place_id INTEGER,
    similarity_score REAL
)
''')

# ------------------------------------------------
# Image Recommendations
# ------------------------------------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS image_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_place_id INTEGER,
    recommended_place_id INTEGER,
    similarity_score REAL
)
''')

conn.commit()
conn.close()

print('Database schema created successfully.')