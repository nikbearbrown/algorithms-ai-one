"""Run the examples quoted in the compact draft."""
from lab.algorithms import (
    CONFLICTS, GRAPH, PAIR, SLOTS, closest, earliest_finish, inversion_count,
    make_tree, matching_cover, route, shortest_weight, walk, weighted_slots,
)


def examples():
    graph = {u: [v for v, _ in edges] for u, edges in GRAPH.items()}
    parents, peak, scanned = walk(graph, "desk")
    distances, cost_parent = shortest_weight(GRAPH, "desk")
    cover, witness = matching_cover(CONFLICTS)
    return {
        "closest_baseline": closest(PAIR),
        "closest_sorted": closest(PAIR, scan_sorted=True),
        "bfs": (route(parents, "lab"), peak, scanned),
        "dijkstra": (route(cost_parent, "lab"), distances["lab"]),
        "interval_count": earliest_finish(SLOTS),
        "interval_value": weighted_slots(SLOTS),
        "inversions": inversion_count([5, 1, 4, 1]),
        "cover": (sorted(cover), witness),
        "frontiers": {shape: (walk(tree, 0)[1], walk(tree, 0, mode="frames")[1])
                      for shape, tree in [("chain", make_tree(31, 1)),
                                          ("binary", make_tree(31, 2)),
                                          ("star", make_tree(31, 30))]},
    }


if __name__ == "__main__":
    for key, value in examples().items():
        print(f"{key}: {value}")
