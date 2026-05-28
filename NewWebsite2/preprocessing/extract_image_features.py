import sqlite3
import os
import sys
import numpy as np
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(
    os.path.join(BASE_DIR, '..')
)
sys.path.append(PROJECT_ROOT)

from algorithms.structural_k_means import kmeans

DATABASE = 'database/website.db'

conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('''
SELECT
    image_id,
    image_path
FROM images
''')

rows = cursor.fetchall()

PALETTE_FOLDER = 'static/palettes'
os.makedirs(PALETTE_FOLDER, exist_ok=True)


for row in rows:
    image_id = row['image_id']
    image_path = os.path.join(
        'static',
        row['image_path']
    )

    if not os.path.exists(image_path):
        continue

    try:
        image = Image.open(image_path).convert('RGB')

        image = image.resize((150, 150))

        pixels = list(image.getdata())

        pixels = [list(pixel) for pixel in pixels]

        clusters, centroids = kmeans(
            pixels,
            k=10,
            max_iterations=15
        )

        cluster_sizes = []

        for i, cluster in enumerate(clusters):
            cluster_sizes.append((i, len(cluster)))

        cluster_sizes.sort(
            key=lambda x: x[1],
            reverse=True
        )

        ordered_centroids = []

        for cluster_index, _ in cluster_sizes:
            ordered_centroids.append(
                centroids[cluster_index]
            )

        feature_vector = []

        for centroid in ordered_centroids:
            feature_vector.extend(centroid)

        vector_text = ','.join(
            str(round(v, 2))
            for v in feature_vector
        )

        palette = Image.new('RGB', (800, 100))
        draw = ImageDraw.Draw(palette)

        width = 80

        for i, centroid in enumerate(ordered_centroids):
            color = tuple(
                int(v)
                for v in centroid
            )

            draw.rectangle(
                [i * width, 0, (i + 1) * width, 100],
                fill=color
            )

        palette_name = f'palette_{image_id}.png'

        palette_path = os.path.join(
            PALETTE_FOLDER,
            palette_name
        )

        palette.save(palette_path)

        relative_palette_path = (
            f'palettes/{palette_name}'
        )

        cursor.execute('''
        UPDATE images
        SET
            palette_path=?,
            feature_vector=?
        WHERE image_id=?
        ''', (
            relative_palette_path,
            vector_text,
            image_id
        ))

    except:
        continue

conn.commit()
conn.close()

print('Image features extracted.')