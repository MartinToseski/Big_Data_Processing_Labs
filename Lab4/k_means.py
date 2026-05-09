import numpy as np
import random


random.seed(42)


def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))


def initialize_centroids(pixels, k):
    random_indices = random.sample(range(len(pixels)), k)
    centroids = pixels[random_indices]
    return centroids


def assign_pixels_to_clusters(pixels, centroids):
    cluster_indices = []

    for pixel in pixels:
        distances = []

        for centroid in centroids:
            distance = euclidean_distance(pixel, centroid)
            distances.append(distance)

        closest_cluster = np.argmin(distances)
        cluster_indices.append(closest_cluster)

    return np.array(cluster_indices)


def recompute_centroids(pixels, cluster_indices, k):
    new_centroids = []

    for cluster_id in range(k):
        cluster_pixels = pixels[cluster_indices == cluster_id]

        if len(cluster_pixels) == 0:
            new_centroid = np.array([0, 0, 0])
        else:
            new_centroid = np.mean(cluster_pixels, axis=0)

        new_centroids.append(new_centroid)

    return np.array(new_centroids)


def centroids_are_equal(old_centroids, new_centroids):
    for i in range(len(old_centroids)):
        for j in range(3):
            difference = abs(old_centroids[i][j] - new_centroids[i][j])
            if difference > 0.001:
                return False
    return True


def count_cluster_sizes(cluster_indices, k):
    counts = []

    for cluster_id in range(k):
        count = np.sum(cluster_indices == cluster_id)
        counts.append(count)

    return counts