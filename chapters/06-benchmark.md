# Chapter 6 — Benchmark what the proof does not predict

*Two algorithms can do the same number of edge scans and leave different amounts of work in flight.*

Suppose the exchange must find every reachable bin before opening. The routing graph is already loaded. The programmer presents a proof of linear time and says it answers a question about the peak frontier on the busiest input. It does not. The bound lumps together enough different input shapes that two different designs can satisfy it and allocate memory in different places.

This chapter gives you a controlled graph family, makes the code run the same reachability contract, and then separates deterministic counts, measured timing and observed allocations. You will design a capacity recommendation that could survive a changed fixture.

## Change one property without secretly changing the work

The benchmark generates three directed trees with the same number of vertices $n$. For each vertex index $v$ from 1 to $n-1$, insert one edge from parent $\lfloor(v-1)/b\rfloor$ to $v$, where $b$ is the fanout. Indices increase along every edge, and repeated parenting eventually reaches zero, so all vertices are reachable from zero and no edge makes a directed cycle. Using $b=1$ produces a chain; $b=2$ gives a binary tree filled in level order; $b=n-1$ produces a star. At any fixed $n$, all have $n-1$ edges and every traversal must see all vertices under the given contract.

Check not just the count of visited vertices but the correctness of the returned parents. In a rooted tree, every reachable non-root vertex has exactly one parent, so both policies must return the same map. In graphs with joins, different valid parent maps can represent the same reachable set while only BFS guarantees minimum-hop parents. Do not compare policies by an equality rule that rejects an intentional contract difference. Do not allow a faulty traversal to stop at its first leaf and win the timing race.

| Shape, $n=31$ | BFS maximum queue items | DFS maximum suspended/current frames | Scanned edges, both |
| --- | ---: | ---: | ---: |
| chain | 1 | 31 | 30 |
| complete binary tree | 16 | 5 | 30 |
| star | 30 | 2 | 30 |

On a chain the queue never holds more than the next vertex, while the DFS frames wait on every ancestor before reaching the bottom. On a star the BFS queue fills with all children immediately after the root scan, but the DFS iterator holds one position in the root's neighbor list and at most one live child frame. On a complete binary tree with 31 vertices the deepest level contains 16 leaves and has edge depth four; four edges mean five vertex frames, not four. Reading the table as “DFS uses two units of memory on a star” confuses a logical frontier peak with the full storage bill. Both implementations also allocate a visited parent map and have access to the prebuilt adjacency lists. A deque entry is not the same size as a frame with an iterator, and the peaks are not measured bytes.

## Make each measurement answer one question

Run the lab initially with `--n 31 --repeats 3` so you can predict all reported counts. For a second run, choose a larger size with the same shapes, such as 4095; observe rather than assume that finite-size timing preserves the ratios of the frontier table. The benchmark caps size and repetition count to keep it suited to an ordinary machine. It does not require internet or a model.

```sh
python3 -B -m lab.benchmark --n 31 --repeats 3
python3 -B -m lab.benchmark --n 4095 --repeats 7
```

The harness generates the graph before either measurement, warms each traversal once, and takes individual deltas from `perf_counter_ns` only over the traversal call. It saves each duration and the median and checks each result after the clock stops. It then runs a separate profiled traversal with `tracemalloc` for peak traced bytes during that run. Profiling overhead is not blended into the timing numbers. See the standard-library documentation for [performance counters](https://docs.python.org/3/library/time.html#time.perf_counter_ns) and [allocation tracing](https://docs.python.org/3/library/tracemalloc.html). Neither measurement includes the graph construction cost. The allocation measurement excludes the already-built graph and does not measure total process resident memory or arbitrary native allocations outside its tracing scope. The environment printout records Python version, platform and architecture but not all background load or allocator history.

The order is currently BFS then DFS for each graph. If your recommendation depends on small timing differences, repeat with independently varied or counterbalanced order in a separate experimental copy, keep the fixture identical, record raw measurements and explain a plausible order effect. A median of seven values is not a confidence interval and is not a safe tail-latency estimate. A measured peak is not a proven ceiling for hostile or simply different inputs. Use the mathematical invariants to predict where the costs might rise, then deliberately test another shape. For example, compare equal-size trees of fanouts 3 and 7 as held-out shapes. A real multigraph can produce different duplicate work; validate production-like input without exposing any personal records.

## Evidence can disagree without either instrument being broken

Suppose DFS has fewer frontier items than BFS on the star but takes longer in your run. This is not a refutation of the count. The iterator state, Python loop overhead, branch behavior and allocation machinery all contribute to measured time. The correct next step is to name one measurable mechanism, vary it in isolation and rerun. For instance, compare an isolated change to frontier representation with the same output map and count. Don't change the graph and the policy and then credit the faster result to the library type. On another graph DFS may return a different valid parent map; compare reachability to align the contract unless path semantics are part of the decision.

As a second workload example, consider a hypothetical cache of capacity two, initially empty, and the request trace `A B A C A B`. FIFO eviction remembers when an item was inserted; hits do not change that order. LRU eviction moves a hit to the most recent position. The third request hits in both. The fourth request C displaces A under FIFO and B under LRU. The fifth hits under LRU but misses under FIFO; the sixth misses in both. FIFO gets one hit, LRU gets two. This result describes a six-request trace, not a claim that LRU dominates FIFO on all traces. Even a higher hit rate might fail to improve latency if maintaining the policy costs more than its saved misses. Record the workload construction, capacity and per-operation cost before claiming that a cache policy “wins.”

## Exercises

- **Warm-up, trace:** Draw the frontier for both traversals on a star with seven vertices. Write the peak queue size and frame count before running code.
- **Warm-up, units:** Give one thing included in “peak traced bytes during the run” and one thing deliberately excluded.
- **Application, benchmark:** Choose sizes and a counterbalanced ordering. Report medians and individual durations for equal-work cases and say what effect could still explain differences.
- **Application, proof and test:** Add a graph where the same vertex can be discovered from two different parents. Test the reachable set and minimum hops without requiring the DFS parent map to match BFS.
- **Synthesis, capacity:** Your service accepts both deep chains and broad roots. Propose a memory risk policy using an input contract, a worst-case bound, measured evidence and a stop signal. State which quantities you do not yet know.
- **Challenge, cache:** Find or construct a trace on which FIFO has more hits than LRU at capacity two, or explain why your proposed example does not suffice. Keep the comparison tied to the trace, not a universal speed claim.

You can now defend a recommendation without confusing proof, implementation check, measurement and context. The [capstone](../practice/capstone.md) asks you to put all four in one decision record.

[Back to the contents](../README.md)
