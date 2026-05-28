import sqlite3
import random

LAB2_DB = '../Lab2/db/lab2.db'
IMAGE_DB = '../Lab4/database/image_database.db'
FINAL_DB = '../Website/database/website.db'
BAD_KEYWORDS = [
    'supermarket',
    'pharmacy',
    'mall',
    'convenience',
    'shop',
    'grocery'
]


lab2_conn = sqlite3.connect(LAB2_DB)
lab2_cursor = lab2_conn.cursor()
image_conn = sqlite3.connect(IMAGE_DB)
image_cursor = image_conn.cursor()
final_conn = sqlite3.connect(FINAL_DB)
final_cursor = final_conn.cursor()

# ------------------------------------------------
# LOAD PLACES
# ------------------------------------------------
lab2_cursor.execute('''
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
''')

places = lab2_cursor.fetchall()

# ------------------------------------------------
# LOAD IMAGES
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
# CITY CACHE
# ------------------------------------------------
city_map = {}

# ------------------------------------------------
# INSERT PLACES
# ------------------------------------------------
for place in places:
    place_id = place[0]
    name = place[1]
    city = place[2]
    if not city:
        continue

    name_lower = name.lower()
    if any(word in name_lower for word in BAD_KEYWORDS):
        continue
    lat = place[3]
    lon = place[4]
    category = str(place[5])
    tourism = place[6]
    relevance = place[7] if place[7] else 0
    pagerank = place[8] if place[8] else 0

    # --------------------------------------------
    # INSERT CITY
    # --------------------------------------------
    if city not in city_map:
        final_cursor.execute('''
         INSERT OR IGNORE INTO cities (name)
         VALUES (?)
         ''', (city,))

        final_conn.commit()

        final_cursor.execute('''
         SELECT city_id
         FROM cities
         WHERE name=?
         ''', (city,))

        city_id = final_cursor.fetchone()[0]
        city_map[city] = city_id

    city_id = city_map[city]
    description = (f'{name} is a place of interest in {city}.')

    # --------------------------------------------
    # INSERT PLACE
    # --------------------------------------------
    final_cursor.execute('''
     INSERT OR REPLACE INTO places (
        place_id,
        city_id,
        name,
        lat,
        lon,
        description,
        pagerank_score,
        relevance_score,
        has_image
     )
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
     ''', (
        place_id,
        city_id,
        name,
        lat,
        lon,
        description,
        pagerank,
        relevance,
        tourism
    ))

    # --------------------------------------------
    # CATEGORY
    # --------------------------------------------
    final_cursor.execute('''
     INSERT OR IGNORE INTO categories (name)
     VALUES (?)
     ''', (category,))

    final_conn.commit()
    final_cursor.execute('''
     SELECT category_id
     FROM categories
     WHERE name=?
     ''', (category,))

    category_id = final_cursor.fetchone()[0]
    final_cursor.execute('''
     INSERT INTO place_categories (
         place_id,
         category_id
     )
     VALUES (?, ?)
     ''', (
        place_id,
        category_id
    ))

    # --------------------------------------------
    # IMAGE ASSIGNMENT
    # --------------------------------------------
    if tourism == 1:
        image = random.choice(images)
        image_path = image[1].replace('\\', '/')
        palette_path = image[3].replace('\\', '/')

        final_cursor.execute('''
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
final_conn.commit()
lab2_conn.close()
image_conn.close()
final_conn.close()
print('Data merged successfully.')
