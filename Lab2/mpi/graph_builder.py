import os
import sys
from mpi4py import MPI

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

from init_db import connect
from src.collectors.wiki import get_wikipedia_title
from src.utils.rate_limiter import safe_request


def normalize_title(t):
    return t.replace("_", " ").strip().lower() if t else None


# Get Wikipedia links
def get_wikipedia_links(title):
    if not title:
        return []
    try:
        formatted = title.replace(" ", "_")
        url = "https://en.wikipedia.org/w/api.php"

        params = {
            "action": "query",
            "titles": formatted,
            "prop": "links",
            "pllimit": "max",
            "format": "json"
        }

        data = safe_request(url, params=params)

        if not data:
            return []

        pages = data.get("query", {}).get("pages", {})

        links = []
        for page in pages.values():
            for link in page.get("links", []):
                links.append(link["title"])

        return links

    except:
        return []


def load_data():
    conn = connect("")
    c = conn.cursor()

    c.execute("""
    SELECT f.id, i.wikidata_id
    FROM features f
    JOIN intermediate_data i ON f.intermediate_id = i.id
    WHERE f.has_wikipedia = 1
    """)

    data = c.fetchall()
    conn.close()
    return data


def split_data(data, size):
    return [data[i::size] for i in range(size)]


def build_edges(local_data, titles_map, title_to_id, rank):
    edges = []

    for i, (fid, wikidata_id) in enumerate(local_data):
        title = titles_map.get(fid)

        if not title:
            continue

        links = get_wikipedia_links(title)

        for link in links:
            target_id = title_to_id.get(normalize_title(link))

            if target_id:
                edges.append((fid, target_id, 1.0))  # directed

    print(f"Rank {rank}: finished {len(local_data)} items", flush=True)
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
            except:
                pass

    conn.commit()
    conn.close()


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        data = load_data()

        titles_map = {}
        title_to_id = {}

        for i, (fid, wikidata_id) in enumerate(data):
            title = get_wikipedia_title(wikidata_id) if wikidata_id else None
            titles_map[fid] = title

            if title:
                title_to_id[normalize_title(title)] = fid

        chunks = split_data(data, size)

    else:
        data = None
        chunks = None
        titles_map = None
        title_to_id = None

    local_data = comm.scatter(chunks, root=0)

    titles_map = comm.bcast(titles_map, root=0)
    title_to_id = comm.bcast(title_to_id, root=0)

    local_edges = build_edges(local_data, titles_map, title_to_id, rank)
    gathered_edges = comm.gather(local_edges, root=0)

    if rank == 0:
        save_edges(gathered_edges)
        print("Graph built using Wikipedia links.", flush=True)