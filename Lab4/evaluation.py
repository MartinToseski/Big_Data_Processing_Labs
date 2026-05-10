from database_manager import load_dataset
from knn import compute_all_distances, sort_distances, get_k_neighbors, predict_class


K_NEIGHBORS = 5
dataset = load_dataset()

correct_predictions = 0
total_predictions = 0

for i in range(len(dataset)):
    print()
    print("Evaluating Image:")
    print(dataset[i]["image_name"])

    query_item = dataset[i]
    query_vector = (query_item["feature_vector"])
    actual_class = (query_item["image_class"])

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
    distances = compute_all_distances(query_vector, training_dataset)
    sorted_distances = sort_distances(distances)
    neighbors = get_k_neighbors(sorted_distances, K_NEIGHBORS)
    predicted_class = predict_class(neighbors)

    # -----------------------------------
    # Compare Prediction
    # -----------------------------------
    print("Actual:", actual_class)
    print("Predicted:", predicted_class)

    total_predictions = (total_predictions + 1)
    if predicted_class == actual_class:
        correct_predictions = (correct_predictions + 1)

# -----------------------------------
# Final Accuracy
# -----------------------------------
accuracy = (correct_predictions / total_predictions)

print()
print("===================================")
print("FINAL ACCURACY:")
print(accuracy)
print("===================================")
