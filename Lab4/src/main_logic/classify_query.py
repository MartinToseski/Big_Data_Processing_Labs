import os
from src.main_logic.process_image import process_single_image
from src.database.database_manager import load_dataset
from src.algorithms.knn import compute_all_distances, sort_distances, get_k_neighbors, predict_class_closest
from src.utils.palette_visualization import save_palette_image

QUERY_IMAGE = "../../sample.jpg"
K_NEIGHBORS = 5

full_dataset = load_dataset()
dataset = []

# -----------------------------------
# Process Query Image
# -----------------------------------
feature_vector = None
query_file_name = os.path.basename(QUERY_IMAGE)
for item in full_dataset:
    database_file_name = os.path.basename(item["image_path"])
    if database_file_name == query_file_name:
        feature_vector = item["feature_vector"]
    else:
        dataset.append(item)

if feature_vector is None:
    sorted_centroids, feature_vector = process_single_image(QUERY_IMAGE)
    save_palette_image(sorted_centroids, "../../sample_palette.png")

# -----------------------------------
# KNN
# -----------------------------------
distances = compute_all_distances(feature_vector, dataset)
sorted_distances = sort_distances(distances)
neighbors = get_k_neighbors(sorted_distances, K_NEIGHBORS)
predicted_class = predict_class_closest(neighbors)

# -----------------------------------
# Results
# -----------------------------------
print()
print("QUERY IMAGE:")
print(QUERY_IMAGE)

print()
print("PREDICTED CLASS:")
print(predicted_class)

print()
print("NEAREST NEIGHBORS:")

for neighbor in neighbors:
    print()
    print("Image:", neighbor["image_name"])
    print("Class:", neighbor["image_class"])
    print("Distance:", neighbor["distance"])
