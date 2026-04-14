import random
import math
from init_db import connect
from matplotlib import pyplot as plt


random.seed(42)
def print_cluster_stats(clusters, metadata):
    print("\n===== CLUSTER ANALYSIS =====")

    for i, cluster in enumerate(clusters):
        print(f"\nCluster {i + 1}")
        print(f"Size: {len(cluster)}")

        city_counts = {}

        for idx in cluster:
            city = metadata[idx]["city"]
            city_counts[city] = city_counts.get(city, 0) + 1

        print("City distribution:")
        for city, count in city_counts.items():
            print(f"  {city}: {count}")
    print("")


def load_feature_vectors(start_ind=3):
    conn = connect("")
    c = conn.cursor()

    c.execute("""
    SELECT id, name, city,
           lat, lon, distance_to_center,
           category_encoded, tags_count,
           description_length,
           has_website, has_wikipedia,
           is_tourism_place, has_phone
    FROM features
    """)

    rows = c.fetchall()
    conn.close()

    data = []
    metadata = []

    for row in rows:
        vector = list(row[start_ind:])
        data.append(vector)

        metadata.append({
            "id": row[0],
            "name": row[1],
            "city": row[2]
        })

    return data, metadata


def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def normalize(data):
    cols = list(zip(*data))
    min_vals = [min(col) for col in cols]
    max_vals = [max(col) for col in cols]

    normalized = []

    for row in data:
        normalized.append([
            (row[i] - min_vals[i]) / (max_vals[i] - min_vals[i] + 1e-9)
            for i in range(len(row))
        ])

    return normalized


def centroid_shift(old, new):
    return sum(euclidean(o, n) for o, n in zip(old, new))


def compute_wcss(data, clusters, centroids):
    wcss = 0

    for cluster_id, cluster in enumerate(clusters):
        centroid = centroids[cluster_id]

        for idx in cluster:
            wcss += euclidean(data[idx], centroid) ** 2

    return wcss


def elbow_method(data, k_range=range(2, 11), runs=3):
    wcss_values = []

    for k in k_range:
        print(f"\nRunning K={k}")

        wcss_sum = 0

        for run in range(runs):
            clusters, centroids, iter_cnt = kmeans(data, k=k)

            wcss = compute_wcss(data, clusters, centroids)
            wcss_sum += wcss

            print(f"  Run {run + 1}: WCSS={wcss:.2f}, iterations={iter_cnt}")

        avg_wcss = wcss_sum / runs
        wcss_values.append(avg_wcss)

        print(f"  → Avg WCSS for K={k}: {avg_wcss:.2f}")

    # -----------------------------
    # PLOT
    # -----------------------------
    plt.figure()
    plt.plot(list(k_range), wcss_values, marker='o')
    plt.xlabel("Number of clusters (K)")
    plt.ylabel("WCSS (Average)")
    plt.title(f"Elbow Method (Averaged over {runs} runs)")
    plt.grid()

    plt.show()

    return wcss_values


def kmeans(data, k=5, max_iters=50, tol=1e-4):
    centroids = random.sample(data, k)
    iter_cnt = 0

    for iteration in range(max_iters):
        clusters = [[] for _ in range(k)]

        # assign step
        for idx, point in enumerate(data):
            distances = [euclidean(point, c) for c in centroids]
            cluster_id = distances.index(min(distances))
            clusters[cluster_id].append(idx)

        # update step
        new_centroids = []
        for cluster in clusters:
            if not cluster:
                new_centroids.append(random.choice(data))
                continue

            mean = [
                sum(data[i][dim] for i in cluster) / len(cluster)
                for dim in range(len(data[0]))
            ]
            new_centroids.append(mean)

        # convergence check
        shift = centroid_shift(centroids, new_centroids)
        if shift < tol:
            break

        centroids = new_centroids
        iter_cnt = iter_cnt+1

    return clusters, centroids, iter_cnt


if __name__ == "__main__":
    data, metadata = load_feature_vectors()
    normalized_data = normalize(data)
    #elbow_method(normalized_data, k_range=range(2, 21), runs=1)
    elbow_method(normalized_data, k_range=range(2, 21), runs=3)
    #elbow_method(normalized_data, k_range=range(2, 21), runs=5)
