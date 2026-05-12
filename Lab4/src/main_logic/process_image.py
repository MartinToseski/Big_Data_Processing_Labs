from src.utils.image_loader import load_image_pixels
from src.algorithms.k_means import initialize_centroids, assign_pixels_to_clusters, recompute_centroids, centroids_are_equal, count_cluster_sizes
from src.utils.feature_vector import sort_clusters_by_size, create_feature_vector


def process_single_image(image_path, k=10, resize_size=(200, 200), max_iterations=20):
    pixels, image_shape = load_image_pixels(image_path, resize_size)
    centroids = initialize_centroids(pixels, k)
    iteration = 0

    while iteration < max_iterations:
        cluster_indices = assign_pixels_to_clusters(pixels, centroids)
        new_centroids = recompute_centroids(pixels, cluster_indices, k)
        finished = centroids_are_equal(centroids, new_centroids)

        if finished:
            break

        centroids = new_centroids
        iteration = iteration + 1

    cluster_sizes = count_cluster_sizes(cluster_indices, k)
    sorted_centroids, sorted_sizes = sort_clusters_by_size(centroids, cluster_sizes)
    feature_vector = create_feature_vector(sorted_centroids)

    return sorted_centroids, feature_vector