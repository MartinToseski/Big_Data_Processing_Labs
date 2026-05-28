import math


# ------------------------------------------------
# Euclidean Distance
# ------------------------------------------------
def euclidean(a, b):
    total = 0
    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2
    return math.sqrt(total)


# ------------------------------------------------
# KNN
# ------------------------------------------------
def knn(query_vector, dataset, k=5):
    distances = []

    for item in dataset:
        d = euclidean(query_vector, item["vector"])

        distances.append({
            "id": item["id"],
            "distance": d
        })

    distances.sort(key=lambda x: x["distance"])

    return distances[:k]