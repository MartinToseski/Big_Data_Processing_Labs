import math


def compute_pagerank(nodes, links, iterations=20, damping=0.85):
    ranks = {}

    for node in nodes:
        ranks[node] = 1 / len(nodes)

    for _ in range(iterations):
        new_ranks = {}
        for node in nodes:
            incoming_sum = 0
            for other in nodes:
                if node in links.get(other, []):
                    outgoing = len(links.get(other, []))

                    if outgoing > 0:
                        incoming_sum += ranks[other] / outgoing

            new_ranks[node] = ((1 - damping) / len(nodes)) + damping * incoming_sum

        ranks = new_ranks

    return ranks
