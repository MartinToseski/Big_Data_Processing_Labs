import os
import numpy as np
from PIL import Image
import random


# ----------------------------
# Load image
# ----------------------------
def load_image_path(image_path, resize=None):
    img = Image.open(image_path).convert("RGB")

    if resize:
        img = img.resize(resize)

    image_array = np.array(img)
    pixels = image_array.reshape(-1, 3).astype(float)

    return pixels, image_array.shape


# ----------------------------
# Euclidean distance
# ----------------------------
def compute_distance(a, b):
    return np.linalg.norm(a - b)


# ----------------------------
# K-Means
# ----------------------------
def initialize_centroids(pixels, k):
    return pixels[random.sample(range(len(pixels)), k)]


def assign_clusters(pixels, centroids):
    clusters = [[] for _ in range(len(centroids))]

    for pixel in pixels:
        distances = [compute_distance(pixel, c) for c in centroids]
        idx = np.argmin(distances)
        clusters[idx].append(pixel)

    return clusters


def update_centroids(clusters):
    new_centroids = []

    for cluster in clusters:
        if len(cluster) == 0:
            new_centroids.append(np.zeros(3))
        else:
            new_centroids.append(np.mean(cluster, axis=0))

    return np.array(new_centroids)


def kmeans(pixels, k=5, max_iters=20):
    centroids = initialize_centroids(pixels, k)

    for _ in range(max_iters):
        clusters = assign_clusters(pixels, centroids)
        new_centroids = update_centroids(clusters)

        if np.allclose(centroids, new_centroids):
            break

        centroids = new_centroids

    return centroids


# ----------------------------
# KNN
# ----------------------------
def knn_classify(pixel, centroids):
    distances = [compute_distance(pixel, c) for c in centroids]
    return np.argmin(distances)


def apply_palette(pixels, centroids):
    return np.array([centroids[knn_classify(p, centroids)] for p in pixels])


# ----------------------------
# Visualization
# ----------------------------
def visualize_palette(centroids, save_path, swatch_size=100):
    centroids = centroids.astype(int)
    k = len(centroids)

    img = Image.new("RGB", (k * swatch_size, swatch_size))

    for i, color in enumerate(centroids):
        block = Image.new("RGB", (swatch_size, swatch_size), tuple(color))
        img.paste(block, (i * swatch_size, 0))

    # Create folder if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    img.save(save_path)


# ----------------------------
# Pipeline
# ----------------------------
def extract_dominant_colors(image_path, k=10, size=None):
    pixels, shape = load_image_path(image_path, size=size)

    centroids = kmeans(pixels, k)
    new_pixels = apply_palette(pixels, centroids)

    quantized_img = new_pixels.reshape(shape).astype(np.uint8)

    return centroids.astype(int), quantized_img


# ----------------------------
# Process all images
# ----------------------------
def process_raw_data(
    raw_data_folder="raw_data",
    palettes_folder="palettes",
    k=10,
    size=(200, 200)
):
    print("Current working directory:")
    print(os.getcwd())

    print("\nLooking for raw data folder at:")
    print(os.path.abspath(raw_data_folder))

    if not os.path.exists(raw_data_folder):
        print("\nERROR: raw_data folder not found!")
        return

    found_images = False

    for root, dirs, files in os.walk(raw_data_folder):

        print(f"\nChecking folder: {root}")
        print(f"Files: {files}")

        for file in files:

            if file.lower().endswith((".jpg", ".jpeg", ".png")):

                found_images = True

                image_path = os.path.join(root, file)

                relative_path = os.path.relpath(root, raw_data_folder)

                output_folder = os.path.join(palettes_folder, relative_path)
                os.makedirs(output_folder, exist_ok=True)

                file_name = os.path.splitext(file)[0]

                palette_path = os.path.join(
                    output_folder,
                    f"{file_name}_palette.png"
                )

                print(f"\nProcessing: {image_path}")

                palette, _ = extract_dominant_colors(
                    image_path,
                    k=k,
                    size=size
                )

                visualize_palette(
                    palette,
                    save_path=palette_path
                )

                print(f"Saved palette: {palette_path}")

    if not found_images:
        print("\nNo images found!")


# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    process_raw_data(
        raw_data_folder="raw_data",
        palettes_folder="palettes",
        k=10,
        size=(200, 200)
    )