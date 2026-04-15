import os
import sys
from mpi4py import MPI
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)
from src import config
config.DB_PATH = os.path.join(PROJECT_ROOT, "db", "lab2.db")
from init_db import connect
import math
from src.collectors.wiki import get_wikipedia_title
from src.utils.rate_limiter import safe_request


def get_pageviews(title):
    if not title:
        return 0

    try:
        formatted_title = title.replace(" ", "_")
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{formatted_title}/daily/20260301/20260331"
        data = safe_request(url)

        if not data:
            return 0

        views = sum(item["views"] for item in data.get("items", []))
        return views
    except:
        return 0


def load_data():
    conn = connect("")
    c = conn.cursor()

    c.execute("""
    SELECT f.id,
           i.wikidata_id,
           f.has_wikipedia
    FROM features f
    JOIN intermediate_data i ON f.intermediate_id = i.id
    """)

    data = c.fetchall()
    conn.close()
    return data


def split_data(data, size):
    return [data[i::size] for i in range(size)]


def compute_relevance(local_data, titles_map):
    results = []

    for fid, wikidata_id, has_wiki in local_data:

        if has_wiki == 0:
            results.append((fid, 0))
            continue

        title = titles_map.get(fid)

        if not title:
            results.append((fid, 0))
            continue

        views = get_pageviews(title)

        # log scaling
        score = math.log(1 + views)
        results.append((fid, score))

    return results


def save_results(all_results):
    conn = connect("")
    c = conn.cursor()

    c.execute("DELETE FROM relevance")

    flat = [item for chunk in all_results for item in chunk]

    max_score = max(score for _, score in flat) + 1e-9

    for fid, score in flat:
        normalized = score / max_score

        c.execute(
            "INSERT INTO relevance (feature_id, score) VALUES (?, ?)",
            (fid, normalized)
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

        titles_map = {}

        for fid, wikidata_id, has_wiki in data:
            if has_wiki and wikidata_id:
                title = get_wikipedia_title(wikidata_id)
            else:
                title = None

            titles_map[fid] = title

        chunks = split_data(data, size)
    else:
        data = None
        chunks = None
        titles_map = None

    # Distribute data
    local_data = comm.scatter(chunks, root=0)

    # broadcast title mapping
    titles_map = comm.bcast(titles_map, root=0)

    # Local processing
    local_results = compute_relevance(local_data, titles_map)

    # Gather results
    gathered = comm.gather(local_results, root=0)

    # Save results
    if rank == 0:
        save_results(gathered)
        print("Relevance scores computed and stored.")