import numpy as np


def sort_clusters_by_size(centroids, cluster_sizes):
    paired = list(zip(centroids, cluster_sizes))
    paired.sort(key=lambda x: x[1], reverse=True)
    sorted_centroids = [item[0] for item in paired]
    sorted_sizes = [item[1] for item in paired]
    return np.array(sorted_centroids), sorted_sizes


def create_feature_vector(sorted_centroids):
    feature_vector = sorted_centroids.flatten()
    return feature_vector