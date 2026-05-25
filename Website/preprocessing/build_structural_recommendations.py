import sqlite3
import math

from algorithms.structural_k_means import (
    kmeans,
    normalize
)

DATABASE = 'database/website.db'

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute('''
SELECT
    id,
    city,
    lat,
    lon,
    pagerank_score,
    relevance_score
FROM places
''')

rows = cursor.fetchall()

place_ids = []
cities = []
vectors = []

for row in rows:

    place_ids.append(row[0])
    cities.append(row[1])

    vectors.append([
        row[2] if row[2] else 0,
        row[3] if row[3] else 0,
        row[4] if row[4] else 0,
        row[5] if row[5] else 0
    ])

normalized = normalize(vectors)

# ------------------------------------------------
# KMEANS
# ------------------------------------------------

clusters, centroids = kmeans(
    normalized,
    k=6
)

# ------------------------------------------------
# Distance
# ------------------------------------------------

def euclidean(a, b):

    total = 0

    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2

    return math.sqrt(total)

# ------------------------------------------------
# KNN INSIDE CLUSTER
# ------------------------------------------------

for cluster in clusters:

    for source_index in cluster:

        source_id = place_ids[source_index]

        source_vector = normalized[source_index]

        distances = []

        for target_index in cluster:

            if source_index == target_index:
                continue

            target_id = place_ids[target_index]

            target_vector = normalized[target_index]

            distance = euclidean(
                source_vector,
                target_vector
            )

            distances.append((
                target_id,
                distance
            ))

        distances.sort(key=lambda x: x[1])

        top_k = distances[:5]

        for target_id, distance in top_k:
            similarity = 1 / (1 + distance)

            cursor.execute('''
            INSERT INTO structural_recommendations (
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

print('Structural recommendations generated.')