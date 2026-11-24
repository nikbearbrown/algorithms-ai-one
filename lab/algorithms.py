"""Plain, deterministic teaching implementations. Python 3.10+, standard library."""
from collections import deque
from bisect import bisect_right
from heapq import heappop, heappush
from itertools import combinations


def closest(values, *, scan_sorted=False):
    """Return (gap, lower, upper) for closest distinct positions, and comparison count."""
    seq = sorted(values) if scan_sorted else list(values)
    if len(seq) < 2:
        raise ValueError("at least two positions required")
    pairs = zip(seq, seq[1:]) if scan_sorted else combinations(seq, 2)
    best, count = None, 0
    for a, b in pairs:
        candidate = (abs(a-b), min(a, b), max(a, b))
        if best is None or candidate < best:
            best = candidate
        count += 1
    return best, count


def walk(graph, start, *, mode="bfs"):
    """Return (parents, peak frontier items, scanned edges) for one reachable component."""
    if mode not in {"bfs", "frames"}:
        raise ValueError("mode must be bfs or frames")
    parents, peak, scans = {start: None}, 1, 0
    if mode == "bfs":
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                scans += 1
                if v not in parents:
                    parents[v] = u
                    queue.append(v)
                    peak = max(peak, len(queue))
    else:
        frames = [(start, iter(graph[start]))]
        while frames:
            u, neighbors = frames[-1]
            try:
                v = next(neighbors)
            except StopIteration:
                frames.pop()
                continue
            scans += 1
            if v not in parents:
                parents[v] = u
                frames.append((v, iter(graph[v])))
                peak = max(peak, len(frames))
    return parents, peak, scans


def route(parents, goal):
    """Reconstruct a parent chain from walk/shortest_weight, including both ends."""
    if goal not in parents:
        return None
    result = []
    while goal is not None:
        result.append(goal)
        goal = parents[goal]
    return result[::-1]


def shortest_weight(graph, start):
    """Teaching domain: string vertices, nonnegative integer weights, all endpoints declared."""
    if start not in graph:
        raise ValueError("unknown start")
    for u, edges in graph.items():
        if not isinstance(u, str):
            raise ValueError("vertex names must be strings")
        for v, w in edges:
            if v not in graph or type(w) is not int or w < 0:
                raise ValueError("edge must name a vertex and a nonnegative integer weight")
    distance, parent = {start: 0}, {start: None}
    heap = [(0, start)]
    while heap:
        d, u = heappop(heap)
        if d != distance[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if v not in distance or nd < distance[v]:
                distance[v] = nd
                parent[v] = u
                heappush(heap, (nd, v))
    return distance, parent


def ordered_slots(rows):
    """Each row is a distinct (label, start, finish, integer value)."""
    seq = list(rows)
    if len({r[0] for r in seq}) != len(seq) or any(r[1] >= r[2] for r in seq):
        raise ValueError("unique IDs and positive-length intervals required")
    return sorted(seq, key=lambda r: (r[2], r[1], r[0]))


def earliest_finish(rows):
    out, cutoff = [], None
    for row in ordered_slots(rows):
        if cutoff is None or cutoff <= row[1]:
            out.append(row[0])
            cutoff = row[2]
    return out


def weighted_slots(rows):
    """Skip on equal value. Return optimum value and one feasible selection."""
    seq = ordered_slots(rows)
    finishes = [r[2] for r in seq]
    predecessor = [bisect_right(finishes, r[1], hi=i) for i, r in enumerate(seq)]
    best = [0]
    for i, r in enumerate(seq):
        best.append(max(best[i], r[3] + best[predecessor[i]]))
    out, j = [], len(seq)
    while j:
        i = j-1
        if seq[i][3] + best[predecessor[i]] > best[i]:
            out.append(seq[i][0])
            j = predecessor[i]
        else:
            j -= 1
    return best[-1], out[::-1]


def inversion_count(values):
    """Return (sorted copy, count of strict inversions)."""
    if len(values) < 2:
        return list(values), 0
    mid = len(values)//2
    left, lc = inversion_count(values[:mid])
    right, rc = inversion_count(values[mid:])
    cross, i, j, result = 0, 0, 0, []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            cross += len(left)-i
    result.extend(left[i:])
    result.extend(right[j:])
    return result, lc+rc+cross


def matching_cover(edges):
    """For a simple undirected graph, return cover set and disjoint witness edges."""
    cover, witness = set(), []
    for a, b in sorted(tuple(sorted(edge)) for edge in edges):
        if a == b:
            raise ValueError("no self-loops")
        if a not in cover and b not in cover:
            cover.update((a, b))
            witness.append((a, b))
    return cover, witness


def make_tree(n, fanout):
    """Create an outward rooted tree with exactly n vertices."""
    if not (1 <= n <= 200000 and 1 <= fanout):
        raise ValueError("n must be 1..200000 and fanout positive")
    graph = {v: [] for v in range(n)}
    for v in range(1, n):
        graph[(v-1)//fanout].append(v)
    return graph


PAIR = [42, 19, 67, 26, 85, 29, 54, 70]
GRAPH = {
    "desk": [("lift", 4), ("west", 1), ("ramp", 1)],
    "lift": [("lab", 7)],
    "west": [("gallery", 1)],
    "ramp": [("lift", 1), ("lab", 9)],
    "gallery": [("lab", 2)],
    "lab": [],
    "annex": [],
}
SLOTS = [("long", 0, 7, 15), ("morning", 1, 3, 4),
         ("browse", 2, 4, 9), ("noon", 3, 5, 3), ("late", 5, 7, 4)]
CONFLICTS = [("A", "B"), ("B", "C"), ("C", "D"), ("B", "D")]
