from PIL import Image
import os


def save_palette_image(centroids, save_path, block_size=100):
    centroids = centroids.astype(int)

    palette_image = Image.new("RGB", (len(centroids) * block_size, block_size))

    for i, color in enumerate(centroids):
        color_block = Image.new("RGB", (block_size, block_size), tuple(color))
        palette_image.paste(color_block, (i * block_size, 0))

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    palette_image.save(save_path)