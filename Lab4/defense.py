import numpy as np
import random
import math
import os

from PIL import Image

random.seed(42)
np.random.seed(42)


def load_image(image_path, resize_size=(200, 200)):
    image = Image.open(image_path).convert("RGB")
    image = image.resize(resize_size)
    image_array = np.array(image)
    pixels = image_array.reshape(-1, 3).astype(float)
    return pixels


def compute_distance(vector1, vector2):
    distance_sum = 0

    for i in range(len(vector1)):
        difference = vector1[i] - vector2[i]
        squared = difference * difference
        distance_sum = distance_sum + squared

    distance = math.sqrt(distance_sum)
    return distance


def initialize_centroids(pixels, k):
    centroids = []
    random_indices = random.sample(range(len(pixels)), k)

    for index in random_indices:
        centroids.append(pixels[index].astype(float))

    return centroids


def assign_clusters(pixels, centroids):
    cluster_indices = []

    for pixel in pixels:
        best_distance = None
        best_cluster = None

        for centroid_index in range(len(centroids)):
            centroid = centroids[centroid_index]
            distance = compute_distance(pixel, centroid)

            if best_distance is None:
                best_distance = distance
                best_cluster = centroid_index
            elif distance < best_distance:
                best_distance = distance
                best_cluster = centroid_index

        cluster_indices.append(best_cluster)

    return cluster_indices


def recompute_centroids(pixels, cluster_indices, k):
    new_centroids = []

    for cluster_id in range(k):
        red_sum = 0
        green_sum = 0
        blue_sum = 0
        pixel_count = 0

        for i in range(len(pixels)):
            if cluster_indices[i] == cluster_id:
                red_sum = red_sum + pixels[i][0]
                green_sum = green_sum + pixels[i][1]
                blue_sum = blue_sum + pixels[i][2]
                pixel_count = pixel_count + 1

        if pixel_count == 0:
            centroid = np.array([0, 0, 0])
        else:
            centroid = np.array([red_sum/pixel_count, green_sum/pixel_count, blue_sum / pixel_count])

        new_centroids.append(centroid)

    return new_centroids


def centroids_equal(old_centroids, new_centroids):
    for i in range(len(old_centroids)):
        for j in range(3):
            difference = abs(old_centroids[i][j] - new_centroids[i][j])
            if difference > 0.001:
                return False
    return True


def count_cluster_sizes(cluster_indices, k):
    cluster_sizes = []

    for cluster_id in range(k):
        count = 0

        for value in cluster_indices:
            if value == cluster_id:
                count = count + 1

        cluster_sizes.append(count)

    return cluster_sizes


def sort_clusters_by_size(centroids, cluster_sizes):
    for i in range(len(cluster_sizes)):
        largest_index = i

        for j in range(i + 1, len(cluster_sizes)):
            if cluster_sizes[j] > cluster_sizes[largest_index]:
                largest_index = j

        temporary_size = cluster_sizes[i]
        cluster_sizes[i] = cluster_sizes[largest_index]
        cluster_sizes[largest_index] = temporary_size

        temporary_centroid = centroids[i]
        centroids[i] = centroids[largest_index]
        centroids[largest_index] = temporary_centroid

    return centroids


def create_feature_vector(sorted_centroids):
    feature_vector = []

    for centroid in sorted_centroids:
        feature_vector.append(centroid[0])
        feature_vector.append(centroid[1])
        feature_vector.append(centroid[2])

    return feature_vector


def process_image(image_path, k=10, max_iterations=20):
    pixels = load_image(image_path)
    centroids = initialize_centroids(pixels, k)
    iteration = 0

    while iteration < max_iterations:
        cluster_indices = assign_clusters(pixels, centroids)
        new_centroids = recompute_centroids(pixels, cluster_indices, k)
        finished = centroids_equal(centroids, new_centroids)
        centroids = new_centroids

        if finished:
            break

        iteration = iteration + 1

    cluster_sizes = count_cluster_sizes(cluster_indices, k)
    sorted_centroids = sort_clusters_by_size(centroids, cluster_sizes)
    feature_vector = create_feature_vector(sorted_centroids)
    return sorted_centroids, feature_vector


def save_palette(centroids, save_path, block_size=100):
    palette_width = len(centroids) * block_size

    palette_image = Image.new("RGB", (palette_width, block_size))

    for i in range(len(centroids)):
        centroid = centroids[i]

        red = int(centroid[0])
        green = int(centroid[1])
        blue = int(centroid[2])

        color = (red, green, blue)
        block = Image.new("RGB", (block_size, block_size), color)
        palette_image.paste(block, (i * block_size, 0))

    palette_image.save(save_path)


def compute_all_distances(query_vector, dataset):
    distances = []

    for item in dataset:
        feature_vector = item["feature_vector"]
        distance = compute_distance(query_vector, feature_vector)

        result = {
            "image_path": item["image_path"],
            "image_class": item["image_class"],
            "distance": distance
        }

        distances.append(result)

    return distances

def sort_distances(distances):
    for i in range(len(distances)):
        smallest_index = i

        for j in range(i + 1, len(distances)):
            current_distance = distances[j]["distance"]
            smallest_distance = distances[smallest_index]["distance"]

            if current_distance < smallest_distance:
                smallest_index = j

        temporary = distances[i]
        distances[i] = distances[smallest_index]
        distances[smallest_index] = temporary

    return distances

def get_k_neighbors(sorted_distances, k=5):
    neighbors = []

    for i in range(k):
        neighbors.append(sorted_distances[i])

    return neighbors

def get_best_k_neighbors(query_vector, dataset, k=5):
    best_neighbors = []

    for item in dataset:
        feature_vector = item["feature_vector"]

        distance = compute_distance(query_vector, feature_vector)

        result = {
            "image_path": item["image_path"],
            "image_class": item["image_class"],
            "distance": distance
        }

        # -----------------------------------
        # Insert Into Sorted Position
        # -----------------------------------
        inserted = False
        for i in range(len(best_neighbors)):
            current_distance = best_neighbors[i]["distance"]

            if distance < current_distance:
                best_neighbors.insert(i, result)
                inserted = True
                break

        if inserted is False:
            best_neighbors.append(result)

        if len(best_neighbors) > k:
            best_neighbors.pop()

    return best_neighbors

def predict_class(neighbors):
    class_counts = {}

    for neighbor in neighbors:
        image_class = neighbor["image_class"]

        if image_class not in class_counts:
            class_counts[image_class] = 0

        class_counts[image_class] = class_counts[image_class] + 1

    best_class = None
    best_count = -1
    tie = False

    for image_class in class_counts:
        count = class_counts[image_class]

        if count > best_count:
            best_count = count
            best_class = image_class
            tie = False
        elif count == best_count:
            tie = True

    if tie:
        return neighbors[0]["image_class"]

    return best_class


'''
###### EXAMPLE DATASET ###### 
dataset = [
    {
        "image_path": "bridge_1.jpg",
        "image_class": "bridge",
        "feature_vector": [100, 120, 140]
    },

    {
        "image_path": "garden_1.jpg",
        "image_class": "garden",
        "feature_vector": [30, 150, 40]
    },

    {
        "image_path": "sunset_1.jpg",
        "image_class": "sunset",
        "feature_vector": [220, 120, 40]
    }
]
'''

QUERY_IMAGE = "sample.png"

sorted_centroids, feature_vector = process_image(QUERY_IMAGE, k=10)
save_palette(sorted_centroids, "sample_palette.png")

distances = compute_all_distances(feature_vector, dataset)
sorted_distances = sort_distances(distances)
neighbors = get_k_neighbors(sorted_distances, k=3)
predicted_class = predict_class(neighbors)

print()
print("FEATURE VECTOR:")
print(feature_vector)

print()
print("PREDICTED CLASS:")
print(predicted_class)

print()
print("NEAREST NEIGHBORS:")

for neighbor in neighbors:
    print()
    print("Image:")
    print(neighbor["image_path"])

    print("Class:")
    print(neighbor["image_class"])

    print("Distance:")
    print(neighbor["distance"])

dataset = []
DATASET_FOLDER = "dataset"

for file_name in os.listdir(DATASET_FOLDER):
    if file_name.endswith(".png"):
        image_path = os.path.join(DATASET_FOLDER, file_name)
        print("Processing:")
        print(image_path)

        centroids, feature_vector = process_image(image_path, k=10)
        item = {
            "image_name": file_name,
            "feature_vector": feature_vector
        }

        dataset.append(item)

'''
for image_class in os.listdir(DATASET_FOLDER):
    class_folder = os.path.join(DATASET_FOLDER, image_class)

    if os.path.isdir(class_folder):
        for file_name in os.listdir(class_folder):
            if file_name.endswith(".png"):
                image_path = os.path.join(class_folder, file_name)
                centroids, feature_vector = process_image(image_path, k=10)
                item = {
                    "image_path": image_path,
                    "image_class": image_class,
                    "feature_vector": feature_vector
                }

                dataset.append(item)
'''

'''
PALETTE_FOLDER = "palettes"

for image_class in os.listdir(DATASET_FOLDER):
    class_folder = os.path.join(DATASET_FOLDER, image_class)

    if os.path.isdir(class_folder):
        palette_class_folder = os.path.join(PALETTE_FOLDER, image_class)

        if os.path.exists(palette_class_folder) is False:
            os.makedirs(palette_class_folder)

        for file_name in os.listdir(class_folder):
            if file_name.endswith(".png"):
                image_path = os.path.join(class_folder, file_name)

                centroids, feature_vector = process_image(image_path, k=10)

                file_name_without_extension = os.path.splitext(file_name)[0]
                palette_file_name = (file_name_without_extension + "_palette.png")
                palette_path = os.path.join(palette_class_folder, palette_file_name)

                save_palette(centroids, palette_path)
                item = {
                    "image_path": image_path,
                    "image_class": image_class,
                    "feature_vector": feature_vector
                }
                dataset.append(item)
'''