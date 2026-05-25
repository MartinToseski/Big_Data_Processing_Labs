import sqlite3
import random

LAB2_DB = '../Lab2/db/lab2.db'
IMAGE_DB = '../Lab4/database/image_database.db'
WEBSITE_DB = '../Website/database/website.db'

lab2_conn = sqlite3.connect(LAB2_DB)
lab2_cursor = lab2_conn.cursor()

image_conn = sqlite3.connect(IMAGE_DB)
image_cursor = image_conn.cursor()

website_conn = sqlite3.connect(WEBSITE_DB)
website_cursor = website_conn.cursor()

# ------------------------------------------------
# Load Lab2 POIs
# ------------------------------------------------
query = '''
SELECT
    f.id,
    f.name,
    f.city,
    f.lat,
    f.lon,
    f.category_encoded,
    f.is_tourism_place,
    r.score,
    p.score
FROM features f
LEFT JOIN relevance r
ON f.id = r.feature_id
LEFT JOIN pagerank p
ON f.id = p.node_id
'''

lab2_cursor.execute(query)
places = lab2_cursor.fetchall()

# ------------------------------------------------
# Load Lab4 Images
# ------------------------------------------------
image_cursor.execute('''
SELECT
    image_name,
    image_path,
    image_class,
    palette_path,
    feature_vector
FROM images
''')

images = image_cursor.fetchall()

# ------------------------------------------------
# Insert Places
# ------------------------------------------------
for place in places:
    place_id = place[0]
    name = place[1]
    city = place[2]
    lat = place[3]
    lon = place[4]

    category = str(place[5])
    tourism = place[6]

    relevance = place[7] if place[7] else 0
    pagerank = place[8] if place[8] else 0

    description = f'{name} is a place of interest in {city}.'

    website_cursor.execute('''
    INSERT OR REPLACE INTO places (
        id,
        name,
        city,
        lat,
        lon,
        category,
        description,
        pagerank_score,
        relevance_score,
        has_image
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        place_id,
        name,
        city,
        lat,
        lon,
        category,
        description,
        pagerank,
        relevance,
        tourism
    ))

# ------------------------------------------------
# Assign Images ONLY to Tourism Places
# ------------------------------------------------
tourism_places = [p for p in places if p[6] == 1]

for place in tourism_places:
    place_id = place[0]
    image = random.choice(images)

    image_path = image[1].replace("\\", "/")
    palette_path = image[3].replace("\\", "/")
    website_cursor.execute('''
    INSERT INTO images (
        place_id,
        image_name,
        image_path,
        palette_path,
        feature_vector,
        image_class
    )
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        place_id,
        image[0],
        image_path,
        palette_path,
        image[4],
        image[2]
    ))

website_conn.commit()
lab2_conn.close()
image_conn.close()
website_conn.close()

print('Databases merged successfully.')