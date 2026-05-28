import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(
    os.path.join(BASE_DIR, '..')
)
sys.path.append(PROJECT_ROOT)

from algorithms.image_knn import knn, similarity_score

DATABASE = 'database/website.db'

conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute(
    'DELETE FROM similar_places WHERE recommendation_type="image"'
)

cursor.execute('''
SELECT
    p.place_id,
    p.city_id,
    i.feature_vector
FROM places p
JOIN images i
ON p.place_id = i.place_id
WHERE i.feature_vector != ''
''')

rows = cursor.fetchall()


def parse_vector(text):
    return [float(x)/255 for x in text.split(',')]


dataset = []

for row in rows:

    dataset.append({
        'place_id': row['place_id'],
        'city_id': row['city_id'],
        'vector': parse_vector(row['feature_vector'])
    })


for item in dataset:

    query_vector = item['vector']

    neighbors = knn(
        query_vector,
        dataset,
        k=10
    )

    for neighbor in neighbors:

        if neighbor['place_id'] == item['place_id']:
            continue

        similarity = similarity_score(
            neighbor['distance']
        )

        cursor.execute('''
        INSERT INTO similar_places (
            source_place_id,
            target_place_id,
            similarity_score,
            recommendation_type
        )
        VALUES (?, ?, ?, ?)
        ''', (
            item['place_id'],
            neighbor['place_id'],
            similarity,
            'image'
        ))

conn.commit()
conn.close()

print('Real image recommendations built.')