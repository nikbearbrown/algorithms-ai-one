"""Checks against independent tiny enumerations; no third-party dependencies."""
import itertools
import json
import random
import subprocess
import sys
import unittest

from lab.algorithms import (
    earliest_finish, closest, inversion_count, make_tree, matching_cover,
    route, shortest_weight, walk, weighted_slots,
)
from lab.check_examples import examples


def subsets(seq):
    return (s for k in range(len(seq)+1) for s in itertools.combinations(seq, k))


def feasible(slots):
    return all(x[2] <= y[1] or y[2] <= x[1] for x, y in itertools.combinations(slots, 2))


class Examples(unittest.TestCase):
    def test_exact_printed_examples(self):
        e = examples()
        self.assertEqual(e["closest_baseline"], ((3, 26, 29), 28))
        self.assertEqual(e["closest_sorted"], ((3, 26, 29), 7))
        self.assertEqual(e["bfs"], (["desk", "lift", "lab"], 3, 8))
        self.assertEqual(e["dijkstra"], (["desk", "west", "gallery", "lab"], 4))
        self.assertEqual(e["interval_count"], ["morning", "noon", "late"])
        self.assertEqual(e["interval_value"], (15, ["long"]))
        self.assertEqual(e["inversions"], ([1, 1, 4, 5], 4))
        self.assertEqual(e["cover"], (["A", "B", "C", "D"], [("A", "B"), ("C", "D")]))
        self.assertEqual(e["frontiers"], {"chain": (1, 31), "binary": (16, 5), "star": (30, 2)})

    def test_counts_and_ties_at_more_than_one_size(self):
        rng = random.Random(19)
        for n in [2, 3, 8, 16, 33]:
            seq = [rng.randrange(-5, 15) for _ in range(n)]
            a, count = closest(seq)
            b, scan = closest(seq, scan_sorted=True)
            self.assertEqual(a, b)
            self.assertEqual(count, n*(n-1)//2)
            self.assertEqual(scan, n-1)
        self.assertEqual(closest([7, 2, 7, 2], scan_sorted=True)[0], (0, 2, 2))
        with self.assertRaises(ValueError):
            closest([2])

    def test_graph_cycle_disconnected_and_zero(self):
        graph = {"a": [("b", 4), ("c", 0)], "b": [("a", 2)], "c": [("b", 0)], "x": []}
        d, p = shortest_weight(graph, "a")
        self.assertEqual(d, {"a": 0, "b": 0, "c": 0})
        self.assertEqual(route(p, "b"), ["a", "c", "b"])
        self.assertIsNone(route(p, "x"))
        simple = {u: [v for v, _ in edges] for u, edges in graph.items()}
        for mode in ["bfs", "frames"]:
            parents, _, scans = walk(simple, "a", mode=mode)
            self.assertEqual(set(parents), {"a", "b", "c"})
            self.assertEqual(scans, 4)

    def test_global_negative_promise_and_undeclared_target(self):
        for graph in [{"root": [], "x": [("x", -1)]}, {"root": [("x", 1)]},
                      {"root": [("root", True)]}]:
            with self.subTest(graph=graph), self.assertRaises(ValueError):
                shortest_weight(graph, "root")

    def test_dijkstra_vs_full_relaxations(self):
        rng = random.Random(27)
        names = tuple("abcde")
        for _ in range(65):
            graph = {a: [(b, rng.randrange(10)) for b in names if rng.random()<0.35]
                     for a in names}
            ref = {"a": 0}
            for _ in range(len(names)-1):
                nxt = ref.copy()
                for u, d in ref.items():
                    for v, w in graph[u]:
                        nxt[v] = min(nxt.get(v, float("inf")), d+w)
                ref = nxt
            observed, p = shortest_weight(graph, "a")
            self.assertEqual(ref, observed)
            for v in ref:
                path = route(p, v)
                self.assertEqual(len(path), len(set(path)))
                self.assertEqual(sum(dict(graph[a])[b] for a,b in zip(path,path[1:])), ref[v])

    def test_schedules_against_exhaustive_oracle(self):
        rng = random.Random(29)
        for _ in range(80):
            slots = [(str(i), a, a+rng.randrange(1, 6), rng.randrange(-5, 19))
                     for i, a in enumerate(rng.choices(range(-2, 10), k=7))]
            keep = [s for s in subsets(slots) if feasible(s)]
            by_id = {s[0]:s for s in slots}
            count_set = [by_id[i] for i in earliest_finish(slots)]
            val, ids = weighted_slots(slots)
            val_set = [by_id[i] for i in ids]
            self.assertTrue(feasible(count_set) and feasible(val_set))
            self.assertEqual(len(count_set), max(map(len, keep)))
            self.assertEqual(val, max(sum(s[3] for s in k) for k in keep))
            self.assertEqual(val, sum(s[3] for s in val_set))

    def test_touching_and_weight_tie(self):
        slots = [("a", 0, 2, 4), ("b", 2, 4, 4), ("c", 0, 4, 8)]
        self.assertEqual(earliest_finish(slots), ["a", "b"])
        self.assertEqual(weighted_slots(slots), (8, ["c"]))
        self.assertEqual(weighted_slots([("negative", 0, 1, -1)]), (0, []))
        self.assertEqual(weighted_slots([]), (0, []))

    def test_inversions_count_strict_only(self):
        for n in range(6):
            for seq in itertools.product(range(3), repeat=n):
                direct = sum(x>y for i,x in enumerate(seq) for y in seq[i+1:])
                self.assertEqual(inversion_count(seq), (sorted(seq), direct))

    def test_vertex_cover_witness_and_complement_vs_exhaustive(self):
        all_edges = list(itertools.combinations("abcd", 2))
        for edges in subsets(all_edges):
            cover, witness = matching_cover(edges)
            optimal = 4
            vertices = set("abcd")
            for s in subsets("abcd"):
                cover_ok = all(a in s or b in s for a,b in edges)
                indep = vertices - set(s)
                self.assertEqual(cover_ok, not any({a,b}<=indep for a,b in edges))
                if cover_ok:
                    optimal = min(optimal, len(s))
            self.assertTrue(all(a in cover or b in cover for a,b in edges))
            self.assertEqual(len(cover), 2*len(witness))
            self.assertEqual(len(set(itertools.chain.from_iterable(witness))), 2*len(witness))
            self.assertLessEqual(len(witness), optimal)
            self.assertLessEqual(len(cover), 2*optimal)

    def test_walk_join_different_valid_parents(self):
        graph = {"start": ["long", "short"], "long": ["mid"], "mid": ["goal"],
                 "short": ["goal"], "goal": ["start"], "isolated": []}
        bfs, _, bfs_scans = walk(graph, "start")
        dfs, _, dfs_scans = walk(graph, "start", mode="frames")
        self.assertEqual(set(bfs), set(dfs))
        self.assertNotIn("isolated", bfs)
        self.assertEqual(route(bfs, "goal"), ["start", "short", "goal"])
        self.assertEqual(route(dfs, "goal"), ["start", "long", "mid", "goal"])
        self.assertEqual((bfs_scans, dfs_scans), (6, 6))

    def test_parallel_weights_decrease_key_course_contract(self):
        graph = {"a": [("b", 7), ("b", 2), ("b", 5)], "b": [("c", 0)], "c": []}
        expected = {"a": 0, "b": 2, "c": 2}
        self.assertEqual(shortest_weight(graph, "a")[0], expected)
        graph["a"].reverse()
        self.assertEqual(shortest_weight(graph, "a")[0], expected)

    def test_benchmark_cli_and_all_shapes(self):
        args = [sys.executable, "-B", "-m", "lab.benchmark"]
        output = subprocess.check_output(args+["--n","31","--repeats","3"], text=True)
        report = json.loads(output)
        self.assertEqual(set(report["cases"]), {"chain","binary","star"})
        expected = examples()["frontiers"]
        for shape, runs in report["cases"].items():
            for i, mode in enumerate(("bfs","frames")):
                case = runs[mode]
                self.assertEqual((case["visited"],case["scans"]),(31,30))
                self.assertEqual(case["peak_frontier_items"],expected[shape][i])
                self.assertEqual(len(case["individual_duration_ns"]),3)
                self.assertGreater(case["peak_traced_bytes"],0)
        error = subprocess.run(args+["--n","20001"], capture_output=True)
        self.assertNotEqual(error.returncode,0)


if __name__ == "__main__":
    unittest.main()
