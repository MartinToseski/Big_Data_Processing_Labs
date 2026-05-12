from src.database.database_manager import load_dataset
from src.algorithms.knn import compute_all_distances, sort_distances, get_k_neighbors, predict_class_closest
from matplotlib import pyplot as plt


K_NEIGHBORS = 5
dataset = load_dataset()

correct_predictions = 0
total_predictions = 0

# -----------------------------------
# Class Labels
# -----------------------------------
class_labels = [
    "bridge",
    "garden",
    "mountains",
    "seaside",
    "sunset"
]


# -----------------------------------
# Create Confusion Matrix
# -----------------------------------
confusion_matrix = []

for i in range(len(class_labels)):

    row = []

    for j in range(len(class_labels)):

        row.append(0)

    confusion_matrix.append(row)


# -----------------------------------
# Evaluate Dataset
# -----------------------------------
for i in range(len(dataset)):

    print()
    print("Evaluating Image:")
    print(dataset[i]["image_name"])

    query_item = dataset[i]

    query_vector = query_item["feature_vector"]
    print(query_vector)

    actual_class = query_item["image_class"]

    # -----------------------------------
    # Build Training Dataset
    # -----------------------------------
    training_dataset = []

    for j in range(len(dataset)):

        if i != j:

            training_dataset.append(dataset[j])

    # -----------------------------------
    # KNN
    # -----------------------------------
    distances = compute_all_distances(
        query_vector,
        training_dataset
    )

    sorted_distances = sort_distances(distances)

    neighbors = get_k_neighbors(
        sorted_distances,
        K_NEIGHBORS
    )

    predicted_class = predict_class_closest(neighbors)

    # -----------------------------------
    # Print Results
    # -----------------------------------
    print("Actual:", actual_class)

    print("Predicted:", predicted_class)

    # -----------------------------------
    # Accuracy
    # -----------------------------------
    total_predictions = (
        total_predictions + 1
    )

    if predicted_class == actual_class:

        correct_predictions = (
            correct_predictions + 1
        )

    # -----------------------------------
    # Update Confusion Matrix
    # -----------------------------------
    actual_index = class_labels.index(actual_class)

    predicted_index = class_labels.index(predicted_class)

    confusion_matrix[actual_index][predicted_index] += 1


# -----------------------------------
# Final Accuracy
# -----------------------------------
accuracy = (
    correct_predictions /
    total_predictions
)

print()
print("===================================")

print("FINAL ACCURACY:")

print(accuracy)

print("===================================")


# -----------------------------------
# Print Confusion Matrix
# -----------------------------------
print()
print("CONFUSION MATRIX")

for row in confusion_matrix:

    print(row)


# -----------------------------------
# Plot Confusion Matrix
# -----------------------------------
plt.figure(figsize=(8, 6))

plt.imshow(
    confusion_matrix,
    cmap="Blues"
)

plt.colorbar()

plt.xticks(
    range(len(class_labels)),
    class_labels
)

plt.yticks(
    range(len(class_labels)),
    class_labels
)

plt.xlabel("Predicted Class")

plt.ylabel("Actual Class")

plt.title("KNN Confusion Matrix")


# -----------------------------------
# Show Values Inside Matrix
# -----------------------------------
for i in range(len(class_labels)):

    for j in range(len(class_labels)):

        value = confusion_matrix[i][j]

        plt.text(
            j,
            i,
            str(value),
            ha='center',
            va='center'
        )

plt.show()
