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
    out_adj = {}
    in_adj = {}
    nodes = set()

    for src, tgt in edges:
        nodes.add(src)
        nodes.add(tgt)

        # Outgoing
        if src not in out_adj:
            out_adj[src] = []
        out_adj[src].append(tgt)

        # Incoming
        if tgt not in in_adj:
            in_adj[tgt] = []
        in_adj[tgt].append(src)

    # Ensure all nodes exist in both dicts
    for node in nodes:
        out_adj.setdefault(node, [])
        in_adj.setdefault(node, [])

    return out_adj, in_adj, list(nodes)


def split_nodes(nodes, size):
    return [nodes[i::size] for i in range(size)]


def initialize_pagerank(nodes):
    N = len(nodes)
    return {node: 1.0 / N for node in nodes}


def compute_local_pagerank(local_nodes, out_adj, in_adj, pr, N):
    new_pr = {}

    # Precompute dangling mass
    dangling_sum = sum(pr[node] for node in pr if len(out_adj[node]) == 0)

    for node in local_nodes:
        rank_sum = 0.0

        for src in in_adj[node]:
            out_degree = len(out_adj[src])
            if out_degree > 0:
                rank_sum += pr[src] / out_degree

        # Add dangling contribution
        rank_sum += dangling_sum / N

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

        out_adj, in_adj, nodes = build_adjacency(edges)

        chunks = split_nodes(nodes, size)
        pr = initialize_pagerank(nodes)
    else:
        out_adj = None
        in_adj = None
        nodes = None
        chunks = None
        pr = None

    out_adj = comm.bcast(out_adj, root=0)
    in_adj = comm.bcast(in_adj, root=0)
    pr = comm.bcast(pr, root=0)

    local_nodes = comm.scatter(chunks, root=0)

    N = len(pr)

    for i in range(ITERATIONS):
        if rank == 0:
            print(f"Iteration {i+1}/{ITERATIONS}", flush=True)

        local_pr = compute_local_pagerank(local_nodes, out_adj, in_adj, pr, N)
        gathered = comm.gather(local_pr, root=0)

        if rank == 0:
            pr = merge_dicts(gathered)

        pr = comm.bcast(pr, root=0)

    if rank == 0:
        save_pagerank(pr)
        print("PageRank computed and stored.", flush=True)