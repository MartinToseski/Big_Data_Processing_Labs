from init_db import connect
import matplotlib.pyplot as plt
import numpy as np
import math


def plot_city_distribution():
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT city, COUNT(*) FROM features GROUP BY city")
    data = c.fetchall()
    conn.close()

    cities = [row[0] for row in data]
    counts = [row[1] for row in data]

    plt.figure()
    bars = plt.bar(cities, counts)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(height),
            ha='center',
            va='bottom'
        )

    plt.show()


def plot_category_distribution():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    SELECT category_encoded, COUNT(*)
    FROM features
    GROUP BY category_encoded
    """)
    data = c.fetchall()
    conn.close()

    labels = ["Monuments (1)", "Shops (2)"]
    counts = [row[1] for row in sorted(data)]

    plt.figure()
    bars = plt.bar(labels, counts)
    plt.title("Category Distribution")
    plt.ylabel("Count")

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(height),
            ha='center',
            va='bottom'
        )

    plt.show()


def plot_description_length_hist():
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT description_length FROM features")
    values = [row[0] for row in c.fetchall()]
    conn.close()

    plt.figure()
    plt.hist(values, bins=30)
    plt.title("Description Length Distribution")
    plt.xlabel("Description Length")
    plt.ylabel("Frequency")
    plt.show()


def plot_tags_count_hist():
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT tags_count FROM features")
    values = [row[0] for row in c.fetchall()]
    conn.close()

    plt.figure()
    plt.hist(values, bins=30)
    plt.title("Tags Count Distribution")
    plt.xlabel("Tags Count")
    plt.ylabel("Frequency")
    plt.show()


def plot_distance_to_center():
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT distance_to_center FROM features")
    values = [row[0] for row in c.fetchall() if row[0]]
    conn.close()

    values = [np.log1p(v) for v in values]

    plt.figure()
    plt.hist(values, bins=30)
    plt.title("Log Distance to City Center Distribution")
    plt.xlabel("Distance")
    plt.ylabel("Frequency")
    plt.show()


def plot_cluster_distribution(clusters, metadata):
    import collections

    # Collect all cities
    cities = sorted(set(m["city"] for m in metadata))

    # Prepare data
    cluster_counts = []

    for cluster in clusters:
        counts = collections.Counter(metadata[i]["city"] for i in cluster)
        cluster_counts.append([counts.get(city, 0) for city in cities])

    # Transpose for stacking
    cluster_counts = list(zip(*cluster_counts))

    # Plot
    plt.figure()

    bottom = [0] * len(clusters)

    for i, city in enumerate(cities):
        values = cluster_counts[i]

        plt.bar(range(len(clusters)), values, bottom=bottom, label=city)

        # Update bottom for stacking
        bottom = [bottom[j] + values[j] for j in range(len(values))]

    plt.title("Cluster City Distribution")
    plt.xlabel("Cluster")
    plt.ylabel("Number of Places")
    plt.xticks(range(len(clusters)), [f"C{i + 1}" for i in range(len(clusters))])
    plt.legend()
    plt.show()


def plot_pagerank_vs_relevance():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    SELECT p.score, r.score
    FROM pagerank p
    JOIN relevance r ON p.node_id = r.feature_id
    """)

    data = c.fetchall()
    conn.close()

    pagerank = [row[0] for row in data]
    relevance = [row[1] for row in data]

    plt.figure()
    plt.scatter(relevance, pagerank)
    plt.title("PageRank vs Relevance")
    plt.xlabel("Relevance")
    plt.ylabel("PageRank")
    plt.show()


import matplotlib.pyplot as plt
import collections


def plot_cluster_distribution_percent(clusters, metadata):
    cities = sorted(set(m["city"] for m in metadata))
    num_clusters = len(clusters)
    num_cities = len(cities)

    # Prepare data matrix: clusters x cities
    data = []

    for cluster in clusters:
        counts = collections.Counter(metadata[i]["city"] for i in cluster)
        total = len(cluster)

        percentages = [
            (counts.get(city, 0) / total) * 100 if total > 0 else 0
            for city in cities
        ]

        data.append(percentages)

    data = np.array(data)

    # X positions
    x = np.arange(num_clusters)
    width = 0.8 / num_cities  # total width split among cities

    plt.figure(figsize=(12, 6))

    colors = ["#8FBBD9", "#A8D5BA", "#F4A7A7", "#C3AED6"]

    for i, city in enumerate(cities):
        bars = plt.bar(
            x + i * width,
            data[:, i],
            width,
            label=city,
            color=colors[i % len(colors)]
        )

        # Labels on top
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.1f}%",
                ha='center',
                va='bottom',
                fontsize=8
            )

    # Labels and formatting
    plt.xlabel("Cluster")
    plt.ylabel("Percentage (%)")
    plt.title("Cluster City Distribution (%)")
    plt.xticks(x + width * (num_cities - 1) / 2, [f"C{i + 1}" for i in range(num_clusters)])
    plt.legend()
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    #plot_city_distribution()
    #plot_category_distribution()
    #plot_description_length_hist()
    #plot_tags_count_hist()
    #plot_distance_to_center()
    plot_pagerank_vs_relevance()