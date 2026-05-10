from process_image import process_single_image
from database_manager import load_dataset
from knn import compute_all_distances, sort_distances, get_k_neighbors, predict_class


QUERY_IMAGE = "raw_data/sunset/sunset_1.jpg"
K_NEIGHBORS = 5
dataset = load_dataset()

# -----------------------------------
# Process Query Image
# -----------------------------------
sorted_centroids, feature_vector = (process_single_image(QUERY_IMAGE, k=10))

# -----------------------------------
# KNN
# -----------------------------------
distances = compute_all_distances(feature_vector, dataset)
sorted_distances = sort_distances(distances)
neighbors = get_k_neighbors(sorted_distances, K_NEIGHBORS)
predicted_class = predict_class(neighbors)

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
