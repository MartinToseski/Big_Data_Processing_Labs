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
    name,
    wiki_links
FROM places
''')

rows = cursor.fetchall()
place_ids = []
titles = {}
links = {}

for row in rows:
    place_id = row['place_id']
    title = row['name']
    titles[title] = place_id
    place_ids.append(place_id)

for row in rows:
    source_id = row['place_id']
    raw_links = row['wiki_links']
    links[source_id] = []

    if not raw_links:
        continue

    split_links = raw_links.split('|')
    for link in split_links:
        if link in titles:
            links[source_id].append(titles[link])

pagerank_scores = compute_pagerank(place_ids, links)

for place_id, score in pagerank_scores.items():
    cursor.execute('''
         UPDATE places
         SET pagerank_score=?
         WHERE place_id=?
     ''', (
        score,
        place_id
    ))

cursor.execute('''
SELECT
     place_id,
     pagerank_score,
     relevance_score
FROM places
''')

feature_rows = cursor.fetchall()
vectors = []
feature_place_ids = []

for row in feature_rows:
    vectors.append([
        row['pagerank_score'],
        row['relevance_score']
    ])
    feature_place_ids.append(row['place_id'])

normalized = normalize(vectors)
clusters, centroids = kmeans(normalized, k=6)


def euclidean(a, b):
    total = 0
    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2
    return math.sqrt(total)


cursor.execute(
    'DELETE FROM similar_places WHERE recommendation_type="structural"'
)
for cluster in clusters:
    for source_index in cluster:
        source_id = feature_place_ids[source_index]
        source_vector = normalized[source_index]
        distances = []

        for target_index in cluster:
            if source_index == target_index:
                continue

            target_id = feature_place_ids[target_index]
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
print('Processing complete.')