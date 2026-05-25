import sqlite3
import math

DATABASE = 'database/website.db'

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute('''
SELECT
    id,
    lat,
    lon,
    pagerank_score,
    relevance_score
FROM places
''')

rows = cursor.fetchall()

# ------------------------------------------------
# Build vectors
# ------------------------------------------------
place_ids = []
vectors = []

for row in rows:
    place_ids.append(row[0])
    vectors.append([
        row[1] if row[1] else 0,
        row[2] if row[2] else 0,
        row[3] if row[3] else 0,
        row[4] if row[4] else 0
    ])

# ------------------------------------------------
# Normalize
# ------------------------------------------------
mins = [min(col) for col in zip(*vectors)]
maxs = [max(col) for col in zip(*vectors)]
normalized = []

for vector in vectors:
    norm = []
    for i in range(len(vector)):
        denominator = maxs[i] - mins[i]
        if denominator == 0:
            norm.append(0)
        else:
            norm.append((vector[i] - mins[i]) / denominator)
    normalized.append(norm)

# ------------------------------------------------
# Distance Function
# ------------------------------------------------

def euclidean(a, b):

    total = 0

    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2

    return math.sqrt(total)

# ------------------------------------------------
# Recommendations
# ------------------------------------------------
for i in range(len(normalized)):
    source_id = place_ids[i]
    distances = []

    for j in range(len(normalized)):
        if i == j:
            continue

        target_id = place_ids[j]
        distance = euclidean(normalized[i], normalized[j])
        distances.append((target_id, distance))

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