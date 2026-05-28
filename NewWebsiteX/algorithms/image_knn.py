import math


# ------------------------------------------------
# Euclidean Distance
# ------------------------------------------------
def compute_distance(vector1, vector2):
    distance_sum = 0

    for i in range(len(vector1)):
        difference = (vector1[i] - vector2[i])
        squared = difference * difference
        distance_sum += squared

    return math.sqrt(distance_sum)


# ------------------------------------------------
# Sort Distances
# ------------------------------------------------
def sort_distances(distances):
    distances.sort(key=lambda item: item["distance"])
    return distances


# ------------------------------------------------
# Get K Neighbors
# ------------------------------------------------
def get_k_neighbors(sorted_distances, k=5):
    return sorted_distances[:k]


# ------------------------------------------------
# Find Nearest Neighbors
# ------------------------------------------------
def knn(query_vector, dataset, k=5):
    distances = []

    for item in dataset:
        vector = item["vector"]
        d = compute_distance(query_vector, vector)

        distances.append({
            "place_id": item["place_id"],
            "distance": d
        })

    sorted_distances = sort_distances(distances)
    neighbors = get_k_neighbors(sorted_distances, k)
    return neighbors


# ------------------------------------------------
# Similarity Score
# ------------------------------------------------
def similarity_score(distance):
    return 1 / (1 + distance)