from mpi4py import MPI
from init_db import connect


def load_data():
    conn = connect("")
    c = conn.cursor()

    c.execute("""
    SELECT id,
        city,
        category_encoded,
        description_length,
        tags_count,
        has_wikipedia,
        distance_to_center
    FROM features
    """)

    data = c.fetchall()
    conn.close()
    return data


def split_data(data, size):
    return [data[i::size] for i in range(size)]


def build_edges(local_data, full_data):
    edges = []

    for row_i in local_data:
        id_i, city_i, cat_i, desc_i, tags_i, wiki_i, dist_i = row_i

        candidates = []

        for row_j in full_data:
            id_j, city_j, cat_j, desc_j, tags_j, wiki_j, dist_j = row_j

            if id_i == id_j:
                continue

            same_category = (cat_i == cat_j)

            if same_category:
                similar_tags = abs(tags_i - tags_j) <= 3
            else:
                similar_tags = abs(tags_i - tags_j) <= 10

            if desc_i == 0 and desc_j == 0:
                similar_desc = False
            else:
                if same_category:
                    similar_desc = abs(desc_i - desc_j) <= 100
                else:
                    similar_desc = abs(desc_i - desc_j) <= 350

            if not (similar_tags and similar_desc):
                continue

            # Weight calculation
            weight = 1.0

            # Category influence
            if same_category:
                weight += 0.25
            else:
                weight -= 0.15

            # Geographic boost
            if city_i == city_j:
                weight += 0.2

            # Wikipedia boost
            if wiki_i == 1 and wiki_j == 1:
                weight += 0.3

            # Distance-to-center similarity
            if abs(dist_i - dist_j) <= 0.1:
                weight += 0.2

            # Prevent invalid edges
            if weight <= 0:
                continue

            candidates.append((id_j, weight))

        K = 150
        candidates.sort(key=lambda x: x[1], reverse=True)
        top_neighbors = candidates[:K]

        for target_id, weight in top_neighbors:
            edges.append((id_i, target_id, weight))

    return edges


def save_edges(all_edges):
    conn = connect("")
    c = conn.cursor()

    c.execute("DELETE FROM graph_edges")

    for chunk in all_edges:
        for source, target, weight in chunk:
            try:
                c.execute("""
                    INSERT OR IGNORE INTO graph_edges (source_id, target_id, weight)
                    VALUES (?, ?, ?)
                """, (source, target, weight))
            except Exception:
                pass

    conn.commit()
    conn.close()


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        data = load_data()
        chunks = split_data(data, size)
    else:
        data = None
        chunks = None

    local_data = comm.scatter(chunks, root=0)
    full_data = comm.bcast(data, root=0)
    local_edges = build_edges(local_data, full_data)
    gathered_edges = comm.gather(local_edges, root=0)

    # Save results
    if rank == 0:
        save_edges(gathered_edges)
        print("Graph edges created and stored.")