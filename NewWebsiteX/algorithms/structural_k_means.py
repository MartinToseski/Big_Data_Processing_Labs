import random
import math


# ------------------------------------------------
# Euclidean Distance
# ------------------------------------------------
def euclidean_distance(a, b):
    total = 0
    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2
    return math.sqrt(total)


# ------------------------------------------------
# Normalize
# ------------------------------------------------
def normalize(data):
    mins = [min(col) for col in zip(*data)]
    maxs = [max(col) for col in zip(*data)]
    normalized = []

    for row in data:
        norm = []

        for i in range(len(row)):
            denominator = maxs[i] - mins[i]

            if denominator == 0:
                norm.append(0)
            else:
                value = (row[i] - mins[i]) / denominator
                norm.append(value)

        normalized.append(norm)

    return normalized


# ------------------------------------------------
# Assign Clusters
# ------------------------------------------------
def assign_clusters(data, centroids):
    clusters = [[] for _ in centroids]

    for index, point in enumerate(data):
        distances = []

        for centroid in centroids:
            d = euclidean_distance(point, centroid)
            distances.append(d)

        closest = distances.index(min(distances))
        clusters[closest].append(index)

    return clusters


# ------------------------------------------------
# Recompute Centroids
# ------------------------------------------------
def recompute_centroids(data, clusters):
    centroids = []

    for cluster in clusters:
        if len(cluster) == 0:
            centroids.append([0] * len(data[0]))
            continue

        centroid = []

        for dimension in range(len(data[0])):
            values = []

            for index in cluster:
                values.append(data[index][dimension])

            centroid.append(sum(values) / len(values))

        centroids.append(centroid)

    return centroids


# ------------------------------------------------
# KMeans
# ------------------------------------------------
def kmeans(data, k=5, max_iterations=100):
    centroids = random.sample(data, k)

    for _ in range(max_iterations):
        clusters = assign_clusters(data, centroids)
        new_centroids = recompute_centroids(data, clusters)

        if new_centroids == centroids:
            break

        centroids = new_centroids

    return clusters, centroids