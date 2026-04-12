import math
from src.algorithms.k_means import load_feature_vectors, normalize, kmeans


def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def find_place_index(place_name, metadata):
    for i, m in enumerate(metadata):
        if m["name"].lower() == place_name.lower():
            return i
    return None


def find_cluster(query_idx, clusters):
    for cluster in clusters:
        if query_idx in cluster:
            return cluster
    return []


def knn_search(query_idx, cluster, data, metadata, k=5):
    query_vector = data[query_idx]
    query_city = metadata[query_idx]["city"]

    distances = []

    for idx in cluster:
        if idx == query_idx:
            continue

        # Only return places from OTHER cities
        if metadata[idx]["city"] == query_city:
            continue

        dist = euclidean(query_vector, data[idx])

        distances.append({
            "distance": dist,
            "id": metadata[idx]["id"],
            "name": metadata[idx]["name"],
            "city": metadata[idx]["city"]
        })

    # Sort by distance
    distances.sort(key=lambda x: x["distance"])

    return distances[:k]


def find_similar_places(place_name, clusters, data, metadata, k=5):
    query_idx = find_place_index(place_name, metadata)
    if query_idx is None:
        print(f"Place '{place_name}' not found.")
        return []

    cluster = find_cluster(query_idx, clusters)
    if not cluster:
        print("Cluster not found.")
        return []

    return knn_search(query_idx, cluster, data, metadata, k)


if __name__ == "__main__":
    data, metadata = load_feature_vectors(start_ind=5)
    normalized_data = normalize(data)
    for row in normalized_data[:5]:
        print(row)
    print("")
    clusters, _, _ = kmeans(normalized_data, k=8)
    for k in range(3, 15, 2):
        print("K=" + str(k))
        results = find_similar_places("EDEKA", clusters, normalized_data, metadata, k=k)
        for result in results:
            print(result)
        print("")

