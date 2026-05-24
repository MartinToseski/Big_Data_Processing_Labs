import sqlite3

conn = sqlite3.connect('database/website.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS places (
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    category TEXT,
    description TEXT,
    image_path TEXT,
    palette_path TEXT,
    pagerank_score REAL,
    feature_vector TEXT
)
''')

sample_places = [
    (
        1,
        'Kaunas Castle',
        'Kaunas',
        'Historical',
        'Historic castle in Kaunas.',
        'images/castle.jpg',
        'palettes/castle_palette.png',
        0.92,
        '[1,2,3]'
    ),
    (
        2,
        'Liberty Avenue',
        'Kaunas',
        'Street',
        'Popular walking street.',
        'images/street.jpg',
        'palettes/street_palette.png',
        0.87,
        '[4,5,6]'
    )
]

cur.executemany(
    '''
    INSERT OR REPLACE INTO places
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''',
    sample_places
)

conn.commit()
conn.close()