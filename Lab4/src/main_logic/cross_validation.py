import random

from src.database.database_manager import load_dataset
from src.algorithms.knn import compute_all_distances, sort_distances, get_k_neighbors, predict_class

random.seed(42)

K_NEIGHBORS = 5
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
        predicted_class = predict_class(neighbors)
        total_predictions = (total_predictions + 1)

        if predicted_class == actual_class:
            correct_predictions = (correct_predictions + 1)

    fold_accuracy = (correct_predictions / total_predictions)
    fold_accuracies.append(fold_accuracy)

    print()
    print("Fold Accuracy:")
    print(fold_accuracy)

# -----------------------------------
# Final Cross Validation Accuracy
# -----------------------------------
accuracy_sum = 0

for value in fold_accuracies:
    accuracy_sum = (accuracy_sum + value)

final_accuracy = (accuracy_sum / len(fold_accuracies))

print()
print("===================================")
print("FINAL CROSS VALIDATION ACCURACY:")
print(final_accuracy)
print("===================================")
