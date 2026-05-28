import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

import sqlite3
import math
from algorithms.structural_k_means import normalize, kmeans
from algorithms.pagerank import compute_pagerank


DATABASE = 'database/website.db'
conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# ------------------------------------------------
# LOAD PLACES
# ------------------------------------------------
cursor.execute('''
SELECT
    place_id,
    city_id,
    lat,
    lon,
    pagerank_score,
    relevance_score
FROM places
''')

rows = cursor.fetchall()
place_ids = []
vectors = []

for row in rows:
    place_ids.append(row['place_id'])
    vectors.append([
        row['lat'] if row['lat'] else 0,
        row['lon'] if row['lon'] else 0,
        row['pagerank_score'] if row['pagerank_score'] else 0,
        row['relevance_score'] if row['relevance_score'] else 0
    ])

normalized = normalize(vectors)

# ------------------------------------------------
# KMEANS
# ------------------------------------------------
clusters, centroids = kmeans(normalized, k=6)

# ------------------------------------------------
# DISTANCE
# ------------------------------------------------
def euclidean(a, b):
    total = 0
    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2
    return math.sqrt(total)

# ------------------------------------------------
# PAGERANK GRAPH
# ------------------------------------------------
links = {}
for i in range(len(place_ids)):
    links[place_ids[i]] = []
    for j in range(len(place_ids)):
        if i == j:
            continue

        d = euclidean(normalized[i], normalized[j])
        similarity = 1 / (1 + d)
        if similarity > 0.5:
            links[place_ids[i]].append(place_ids[j])

pagerank_scores = compute_pagerank(place_ids, links)

# ------------------------------------------------
# UPDATE PAGERANK
# ------------------------------------------------
for place_id, score in pagerank_scores.items():
    cursor.execute('''
     UPDATE places
     SET pagerank_score=?
     WHERE place_id=?
    ''', (
        score,
        place_id
    ))

# ------------------------------------------------
# STRUCTURAL RECOMMENDATIONS
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
            distance = euclidean(source_vector, target_vector)
            distances.append((target_id, distance))

        distances.sort(key=lambda x: x[1])
        top_k = distances[:5]

        for target_id, distance in top_k:
            similarity = 1 / (1 + distance)

            cursor.execute('''
             INSERT INTO similar_places (
                source_place_id,
                target_place_id,
                similarity_score,
                recommendation_type
             )
             VALUES (?, ?, ?, ?)
             ''', (
                source_id,
                target_id,
                similarity,
            'structural'
            ))

conn.commit()
conn.close()
print('Data processing complete.')