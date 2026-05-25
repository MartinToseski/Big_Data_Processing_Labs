import sqlite3
import math

DATABASE = 'database/website.db'

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute('''
SELECT
    place_id,
    feature_vector
FROM images
''')

rows = cursor.fetchall()

# ------------------------------------------------
# Parse vectors
# ------------------------------------------------
dataset = []
for row in rows:
    place_id = row[0]

    vector = [
        float(x)
        for x in row[1].split(',')
    ]

    dataset.append({
        'place_id': place_id,
        'vector': vector
    })

# ------------------------------------------------
# Distance
# ------------------------------------------------

def distance(a, b):

    total = 0

    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2

    return math.sqrt(total)

# ------------------------------------------------
# Recommendations
# ------------------------------------------------
for item in dataset:
    source_id = item['place_id']
    distances = []

    for other in dataset:
        if source_id == other['place_id']:
            continue
        d = distance(item['vector'], other['vector'])
        distances.append((other['place_id'], d))

    distances.sort(key=lambda x: x[1])
    top_k = distances[:5]

    for target_id, d in top_k:
        similarity = 1 / (1 + d)
        cursor.execute('''
        INSERT INTO image_recommendations (
            source_place_id,
            recommended_place_id,
            similarity_score
        )
        VALUES (?, ?, ?)
        ''', (
            source_id,
            target_id,
            similarity
        ))

conn.commit()
conn.close()

print('Image recommendations generated.')