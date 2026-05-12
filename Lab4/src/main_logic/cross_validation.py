import random

from src.database.database_manager import load_dataset
from src.algorithms.knn import compute_all_distances, sort_distances, get_k_neighbors, predict_class_closest
from matplotlib import pyplot as plt

random.seed(42)
NUMBER_OF_FOLDS = 5

dataset = load_dataset()
random.shuffle(dataset)

folds = []
fold_size = (len(dataset) // NUMBER_OF_FOLDS)
start_index = 0

for i in range(NUMBER_OF_FOLDS):
    end_index = (start_index + fold_size)
    fold = dataset[start_index:end_index]
    folds.append(fold)
    start_index = end_index


tested_k_values = []
average_accuracies = []

for K_NEIGHBORS in range(1, 16):
    print()
    print("===================================")
    print("TESTING K =", K_NEIGHBORS)
    print("===================================")

    # -----------------------------------
    # Cross Validation
    # -----------------------------------
    fold_accuracies = []
    for fold_index in range(NUMBER_OF_FOLDS):
        print()
        print("===================================")
        print("FOLD", fold_index + 1)
        print("===================================")

        testing_dataset = folds[fold_index]
        training_dataset = []

        for i in range(NUMBER_OF_FOLDS):
            if i != fold_index:
                for item in folds[i]:
                    training_dataset.append(item)

        correct_predictions = 0
        total_predictions = 0

        # -----------------------------------
        # Evaluate Fold
        # -----------------------------------
        for query_item in testing_dataset:
            query_vector = (query_item["feature_vector"])
            actual_class = (query_item["image_class"])

            distances = compute_all_distances(query_vector, training_dataset)
            sorted_distances = sort_distances(distances)

            neighbors = get_k_neighbors(sorted_distances, K_NEIGHBORS)
            predicted_class = predict_class_closest(neighbors)
            total_predictions = (total_predictions + 1)

            if predicted_class == actual_class:
                correct_predictions = (correct_predictions + 1)

        fold_accuracy = (correct_predictions / total_predictions)
        fold_accuracies.append(fold_accuracy)

        print()
        print("Fold Accuracy:")
        print(fold_accuracy)

    accuracy_sum = 0

    for value in fold_accuracies:
        accuracy_sum = accuracy_sum + value

    average_accuracy = accuracy_sum / len(fold_accuracies)
    tested_k_values.append(K_NEIGHBORS)
    average_accuracies.append(average_accuracy)

    print()
    print("===================================")
    print("AVERAGE ACCURACY FOR K =", K_NEIGHBORS)
    print(average_accuracy)
    print("===================================")


# -----------------------------------
# Final Results
# -----------------------------------
print()
print("===================================")
print("FINAL RESULTS")
print("===================================")

for i in range(len(tested_k_values)):
    print()
    print("K =", tested_k_values[i])
    print("Accuracy =", average_accuracies[i])


# -----------------------------------
# Elbow Method Plot
# -----------------------------------
plt.figure(figsize=(10, 6))
plt.plot(tested_k_values, average_accuracies, marker='o')
plt.xlabel("K Neighbors")
plt.ylabel("Average Cross Validation Accuracy")
plt.title("KNN Accuracy For Different K Values")
plt.xticks(tested_k_values)
plt.grid(True)
plt.show()
