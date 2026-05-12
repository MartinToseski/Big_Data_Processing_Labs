import math


# -----------------------------------
# Euclidean Distance
# -----------------------------------
def compute_distance(vector1, vector2):
    distance_sum = 0

    for i in range(len(vector1)):
        difference = (vector1[i] - vector2[i])
        squared = (difference * difference)
        distance_sum = (distance_sum + squared)

    return math.sqrt(distance_sum)



# -----------------------------------
# Compute Distances To Dataset
# -----------------------------------
def compute_all_distances(query_vector, dataset):
    distances = []

    for item in dataset:
        feature_vector = item["feature_vector"]
        image_class = item["image_class"]
        image_name = item["image_name"]

        distance = compute_distance(query_vector, feature_vector)
        result = {
            "image_name": image_name,
            "image_class": image_class,
            "distance": distance
        }
        distances.append(result)

    return distances


# -----------------------------------
# Sort By Distance
# -----------------------------------
def sort_distances(distances):
    distances.sort(key=lambda item: item["distance"])
    return distances


# -----------------------------------
# Get K Nearest Neighbors
# -----------------------------------
def get_k_neighbors(sorted_distances, k=5):
    return sorted_distances[:k]


# -----------------------------------
# Majority Voting
# -----------------------------------
def predict_class(neighbors):
    class_counts = {}
    best_class = None
    best_count = -1

    for neighbor in neighbors:
        image_class = (neighbor["image_class"])

        if image_class not in class_counts:
            class_counts[image_class] = 0
        class_counts[image_class] = (class_counts[image_class] + 1)

    for image_class in class_counts:
        count = class_counts[image_class]
        if count > best_count:
            best_count = count
            best_class = image_class

    return best_class


# -----------------------------------
# Majority Voting + Closest Neighbour
# -----------------------------------
def predict_class_closest(neighbors):
    class_counts = {}

    for neighbor in neighbors:
        image_class = (neighbor["image_class"])

        if image_class not in class_counts:
            class_counts[image_class] = 0
        class_counts[image_class] = (class_counts[image_class] + 1)

    class_counts = sorted(class_counts.items(), key=lambda item: item[1], reverse=True)

    if len(class_counts) == 1:
        return class_counts[0][0]

    if class_counts[0][1] == class_counts[1][1]:
        return neighbors[0]["image_class"]

    return class_counts[0][0]