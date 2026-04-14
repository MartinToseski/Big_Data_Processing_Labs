import os
import sys
from mpi4py import MPI

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)
from src import config
config.DB_PATH = os.path.join(PROJECT_ROOT, "db", "lab2.db")
from init_db import connect


def load_data():
    conn = connect("")
    c = conn.cursor()

    c.execute("""
    SELECT id,
           description_length,
           tags_count,
           has_wikipedia,
           has_website,
           is_tourism_place,
           category_encoded
    FROM features
    """)

    data = c.fetchall()
    conn.close()
    return data


def split_data(data, size):
    return [data[i::size] for i in range(size)]


def compute_relevance(row, max_desc, max_tags):
    fid, desc_len, tags_count, has_wiki, has_web, is_tourism, category = row

    # --- Normalization ---
    norm_desc = desc_len / (max_desc + 1e-9)
    norm_tags = tags_count / (max_tags + 1e-9)

    # --- Weighted relevance ---
    base_score = (
        0.4 * norm_desc +
        0.2 * norm_tags +
        0.2 * has_wiki +
        0.1 * has_web +
        0.1 * is_tourism
    )

    category_weight = {
        1: 1.0,   # monument
        2: 0.7,   # shop
        0: 0.5
    }.get(category, 0.5)

    score = base_score * category_weight
    return fid, score


def save_results(results):
    conn = connect("")
    c = conn.cursor()
    c.execute("DELETE FROM relevance")

    for chunk in results:
        for fid, score in chunk:
            c.execute(
                "INSERT INTO relevance (feature_id, score) VALUES (?, ?)",
                (fid, score)
            )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Load data (rank == 0)
    if rank == 0:
        data = load_data()

        # Compute normalization values
        max_desc = max(row[1] for row in data)
        max_tags = max(row[2] for row in data)
        chunks = split_data(data, size)
    else:
        data = None
        chunks = None
        max_desc = None
        max_tags = None

    # Distribute data
    local_data = comm.scatter(chunks, root=0)

    # Broadcast normalization values
    max_desc = comm.bcast(max_desc, root=0)
    max_tags = comm.bcast(max_tags, root=0)

    # Local processing
    local_results = []

    for row in local_data:
        fid, score = compute_relevance(row, max_desc, max_tags)
        local_results.append((fid, score))

    # Gather results
    gathered = comm.gather(local_results, root=0)

    # Save results
    if rank == 0:
        save_results(gathered)
        print("Relevance scores computed and stored.")