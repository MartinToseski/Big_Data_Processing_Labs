import os
import random

import numpy as np
import matplotlib.pyplot as plt
from src.utils.image_loader import load_image_pixels
from src.algorithms.k_means import initialize_centroids, assign_pixels_to_clusters, recompute_centroids, centroids_are_equal, euclidean_distance


random.seed(42)
np.random.seed(42)

RAW_DATA_FOLDER = "../../raw_data"
K_CLUSTERS = 10
MAX_ITERATIONS = 20
RESIZE_SIZE = (50, 50)
IMAGE_SELECTION_STEP = 6

category_names = []
category_averages = []
all_category_scores = []


# -----------------------------------
# Process Each Category
# -----------------------------------
for image_class in os.listdir(RAW_DATA_FOLDER):
    image_class_path = os.path.join(RAW_DATA_FOLDER, image_class)

    if os.path.isdir(image_class_path):
        print()
        print("===================================")
        print("CATEGORY:", image_class)
        print("===================================")

        image_files = []
        for file_name in os.listdir(image_class_path):
            lower_name = file_name.lower()
            valid_image = False

            if lower_name.endswith(".jpg"):
                valid_image = True

            if lower_name.endswith(".jpeg"):
                valid_image = True

            if lower_name.endswith(".png"):
                valid_image = True

            if valid_image:
                image_files.append(file_name)

        image_files.sort()

        selected_images = []
        for i in range(0, len(image_files), IMAGE_SELECTION_STEP):
            selected_images.append(image_files[i])

        category_scores = []


        # -----------------------------------
        # Process Selected Images
        # -----------------------------------
        for file_name in selected_images:
            image_path = os.path.join(image_class_path, file_name)
            print()
            print("Processing:")
            print(image_path)

            pixels, image_shape = load_image_pixels(image_path, resize=RESIZE_SIZE)

            # -----------------------------------
            # K-Means
            # -----------------------------------
            centroids = initialize_centroids(pixels, K_CLUSTERS)
            iteration = 0
            while iteration < MAX_ITERATIONS:
                cluster_indices = assign_pixels_to_clusters(pixels, centroids)
                new_centroids = recompute_centroids(pixels, cluster_indices, K_CLUSTERS)
                finished = centroids_are_equal(centroids, new_centroids)

                if finished:
                    break

                centroids = new_centroids
                iteration = iteration + 1

            # -----------------------------------
            # Silhouette Calculation
            # -----------------------------------
            silhouette_scores = []
            for i in range(len(pixels)):
                current_pixel = pixels[i]
                current_cluster = cluster_indices[i]

                # -----------------------------------
                # a(i)
                # -----------------------------------
                intra_cluster_distances = []
                for j in range(len(pixels)):
                    if i != j:
                        comparison_cluster = cluster_indices[j]

                        if comparison_cluster == current_cluster:
                            distance = euclidean_distance(current_pixel, pixels[j])
                            intra_cluster_distances.append(distance)

                if len(intra_cluster_distances) == 0:
                    a_i = 0
                else:
                    intra_sum = 0
                    for value in intra_cluster_distances:
                        intra_sum = intra_sum + value
                    a_i = (intra_sum / len(intra_cluster_distances))

                # -----------------------------------
                # b(i)
                # -----------------------------------
                inter_cluster_averages = []
                for cluster_id in range(K_CLUSTERS):
                    if cluster_id != current_cluster:
                        cluster_distances = []

                        for j in range(len(pixels)):
                            comparison_cluster = cluster_indices[j]

                            if comparison_cluster == cluster_id:
                                distance = euclidean_distance(current_pixel, pixels[j])
                                cluster_distances.append(distance)

                        if len(cluster_distances) > 0:
                            cluster_sum = 0
                            for value in cluster_distances:
                                cluster_sum = cluster_sum + value

                            cluster_average = cluster_sum / len(cluster_distances)
                            inter_cluster_averages.append(cluster_average)

                b_i = inter_cluster_averages[0]

                for value in inter_cluster_averages:
                    if value < b_i:
                        b_i = value

                # -----------------------------------
                # Silhouette Formula
                # -----------------------------------
                maximum_value = a_i

                if b_i > maximum_value:
                    maximum_value = b_i

                if maximum_value == 0:
                    silhouette = 0
                else:
                    silhouette = ((b_i - a_i) / maximum_value)

                silhouette_scores.append(silhouette)


            # -----------------------------------
            # Average Silhouette For Image
            # -----------------------------------
            silhouette_sum = 0

            for value in silhouette_scores:
                silhouette_sum = silhouette_sum + value

            average_silhouette = silhouette_sum / len(silhouette_scores)
            category_scores.append(average_silhouette)

            print()
            print("Silhouette Coefficient:")
            print(average_silhouette)

        # -----------------------------------
        # Average Category Score
        # -----------------------------------
        category_sum = 0

        for value in category_scores:
            category_sum = category_sum + value

        category_average = category_sum / len(category_scores)
        category_names.append(image_class)
        category_averages.append(category_average)
        all_category_scores.append(category_scores)

        print()
        print("-----------------------------------")
        print("CATEGORY AVERAGE:")
        print(image_class)
        print(category_average)
        print("-----------------------------------")


# -----------------------------------
# Final Summary
# -----------------------------------
print()
print("===================================")
print("FINAL CATEGORY AVERAGES")
print("===================================")

for i in range(len(category_names)):
    print()
    print(category_names[i])
    print(category_averages[i])


# -----------------------------------
# Bar Graph
# -----------------------------------
plt.figure(figsize=(10, 6))
bars = plt.bar(category_names, category_averages)
plt.xlabel("Category")
plt.ylabel("Average Silhouette Coefficient")
plt.title("Average Silhouette Coefficient Per Category")
plt.ylim(0, 1)
plt.grid(True)

for i in range(len(bars)):
    bar = bars[i]
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.01,
        round(height, 3),
        ha='center'
    )

plt.grid(False)
plt.show()


# -----------------------------------
# Scatter Plot
# -----------------------------------
plt.figure(figsize=(10, 6))

for i in range(len(category_names)):
    scores = all_category_scores[i]
    x_values = []

    for j in range(len(scores)):
        x_values.append(category_names[i])

    plt.scatter(x_values, scores)

plt.xlabel("Category")
plt.ylabel("Silhouette Coefficient")
plt.title("Silhouette Coefficients Per Image")
plt.ylim(0, 1)
plt.grid(True)
plt.show()


# -----------------------------------
# Box Plot
# -----------------------------------
plt.figure(figsize=(10, 6))
plt.boxplot(all_category_scores, tick_labels=category_names)
plt.xlabel("Category")
plt.ylabel("Silhouette Coefficient")
plt.title("Distribution of Silhouette Coefficients")
plt.ylim(0, 1)
plt.grid(True)
plt.show()