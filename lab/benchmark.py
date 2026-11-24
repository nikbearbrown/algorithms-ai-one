"""Bounded, synthetic graph-frontier comparison; counts aren't bytes or timings."""
import argparse
import gc
import json
import platform
import statistics
import time
import tracemalloc

from lab.algorithms import make_tree, walk


def measure(tree, mode, repeats):
    expected = walk(tree, 0, mode=mode)
    deltas = []
    for _ in range(repeats):
        start = time.perf_counter_ns()
        trial = walk(tree, 0, mode=mode)
        delta = time.perf_counter_ns() - start
        if trial != expected:
            raise AssertionError("visit result changed")
        deltas.append(delta)
        del trial
    gc.collect()
    tracemalloc.start()
    try:
        profiled = walk(tree, 0, mode=mode)
        peak_bytes = tracemalloc.get_traced_memory()[1]
    finally:
        tracemalloc.stop()
    if profiled != expected:
        raise AssertionError("profile run changed the result")
    parents, peak, scans = expected
    return {"visited": len(parents), "scans": scans, "peak_frontier_items": peak,
            "median_duration_ns": statistics.median(deltas),
            "individual_duration_ns": deltas, "peak_traced_bytes": peak_bytes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=4095)
    parser.add_argument("--repeats", type=int, default=7)
    args = parser.parse_args()
    if not 2 <= args.n <= 20000 or not 3 <= args.repeats <= 25:
        parser.error("choose 2..20000 vertices and 3..25 repetitions")
    report = {"python": platform.python_version(), "system": platform.system(),
              "machine": platform.machine(), "n": args.n, "repeats": args.repeats,
              "measurement": "Traversal calls only; graph construction, warm-up, comparison and profiling excluded from wall time.",
              "cases": {}}
    for shape, fanout in [("chain", 1), ("binary", 2), ("star", args.n-1)]:
        tree = make_tree(args.n, fanout)
        report["cases"][shape] = {mode: measure(tree, mode, args.repeats)
                                   for mode in ("bfs", "frames")}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
