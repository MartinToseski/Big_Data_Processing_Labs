from mpi4py import MPI
from init_db import connect


DAMPING = 0.85
ITERATIONS = 20


def load_graph():
    conn = connect("")
    c = conn.cursor()

    c.execute("SELECT source_id, target_id FROM graph_edges")
    edges = c.fetchall()

    conn.close()
    return edges


def build_adjacency(edges):
    adj = {}

    for src, tgt in edges:
        if src not in adj:
            adj[src] = []
        adj[src].append(tgt)

    nodes = list(adj.keys())

    return adj, nodes


def split_nodes(nodes, size):
    return [nodes[i::size] for i in range(size)]


def initialize_pagerank(nodes):
    N = len(nodes)
    return {node: 1.0 / N for node in nodes}


def compute_local_pagerank(local_nodes, adj, pr, N):
    new_pr = {}

    for node in local_nodes:
        rank_sum = 0.0

        for src in adj:
            if node in adj[src]:
                out_degree = len(adj[src])
                if out_degree > 0:
                    rank_sum += pr[src] / out_degree

        new_pr[node] = (1 - DAMPING) / N + DAMPING * rank_sum

    return new_pr


def merge_dicts(dicts):
    result = {}
    for d in dicts:
        result.update(d)
    return result


def save_pagerank(pr):
    conn = connect("")
    c = conn.cursor()

    c.execute("DELETE FROM pagerank")

    for node, score in pr.items():
        c.execute("""
            INSERT INTO pagerank (node_id, score)
            VALUES (?, ?)
        """, (node, score))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Load graph
    if rank == 0:
        edges = load_graph()
        adj, nodes = build_adjacency(edges)
        chunks = split_nodes(nodes, size)
        pr = initialize_pagerank(nodes)
    else:
        adj = None
        nodes = None
        chunks = None
        pr = None

    # Broadcast adjacency + pagerank
    adj = comm.bcast(adj, root=0)
    pr = comm.bcast(pr, root=0)

    # Scatter nodes
    local_nodes = comm.scatter(chunks, root=0)

    N = len(pr)

    for _ in range(ITERATIONS):
        local_pr = compute_local_pagerank(local_nodes, adj, pr, N)

        gathered = comm.gather(local_pr, root=0)

        if rank == 0:
            pr = merge_dicts(gathered)

        pr = comm.bcast(pr, root=0)

    if rank == 0:
        save_pagerank(pr)
        print("PageRank computed and stored.")