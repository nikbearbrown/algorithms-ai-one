# Chapter 2 — Represent reachability and cost

*The shortest trip depends on what your ruler measures.*

Suppose the library exchange is moving a padded crate from the service desk to a repair lab. The lift route has two links. The western corridor has three. With no other information the shorter route is the first. Once the staff supply travel minutes, the ranking reverses. The algorithms do not disagree about arithmetic. They were given different questions.

In this chapter, choose a graph representation, trace discovery with a queue and branch exploration with frames, prove a weighted answer under its input promise, and recognize when an edge breaks the proof.

## Store directions, not wishful thinking

A vertex is a named place. A directed edge $u\to v$ is a permissible move from $u$ to $v$. The reverse move is not implied. A weight is a cost on one such move; here its unit is minutes and path cost is a sum. In this teaching fixture the costs are static nonnegative integers. These data do not represent changing access, a lift timetable or route reliability.

| From | Outgoing links and minutes in input order |
| --- | --- |
| desk | lift: 4; west: 1; ramp: 1 |
| lift | lab: 7 |
| west | gallery: 1 |
| ramp | lift: 1; lab: 9 |
| gallery | lab: 2 |
| lab | none |
| annex | none |

An adjacency list stores the outgoing neighbors for each vertex, including an empty list where no edge leaves. With $V$ vertices and $E$ directed edges it takes $O(V+E)$ space, excluding the memory for variable-size labels if treated separately. An adjacency matrix uses $O(V^2)$ entries but can test a particular edge in constant time with integer indices. On a sparse graph, scanning a whole matrix row to find the two neighbors is wasted work. On a dense fixed graph with many point queries, constant-time lookup may be the useful feature. No result about frontier memory substitutes for storage of the input representation.

## One frontier, two different intentions

Breadth-first search, or BFS, puts the source into a first-in, first-out queue. Mark a neighbor discovered at enqueue time and store its parent. Marking when it leaves the queue permits duplicate enqueues in a graph where branches meet. The queue processes vertices in nondecreasing hop distance: when a vertex at distance $d$ discovers a vertex, that edge extends the stored route to length $d+1$; anything reachable with fewer hops would have been encountered through an earlier layer. So the first parent is a witness for the minimum number of edges. BFS doesn't settle ties by total minutes because minutes do not enter its decision.

Pop desk and schedule lift, west and ramp. Pop lift and discover lab. Other links reach lab but cannot make it a new BFS discovery. The returned route desk → lift → lab has two hops and would take 11 minutes. In the full traversal, every outgoing edge of the six reachable vertices is examined once: eight scans. The annex remains absent rather than receiving a made-up zero or infinite route. Reconstruct a route by following parent entries from goal to source and reversing. With parallel links, a list of vertices alone does not say which edge was chosen. The toy example has at most one edge per ordered pair; a route audit for a multigraph should also store edge IDs.

Depth-first search, or DFS, instead takes a child and finishes exploring that branch before resuming the parent's neighbor iterator. The lab represents each suspended position as a frame. You can use a stack of vertices for a different traversal implementation, but storing one pending sibling per slot is not the same as storing one frame per current ancestor. Chapter 6 measures that difference. Both traversals can decide reachability with an adjacency list by visiting and scanning the reachable part. In the worst case the traversal takes $O(V+E)$ time and $O(V)$ extra space including visited information. A DFS parent chain is a route, not a proof that the route minimizes hops. If the fixture is deep, using explicit frames avoids reliance on the host's recursion limit.

## Why Dijkstra gets to stop worrying about a vertex

Keep an upper bound $d[u]$ from a discovered route to $u$; treat a missing label as infinity. Initially $d[\text{desk}]=0$. Extract the smallest tentative distance, and for every outgoing edge of weight $w$ offer a candidate $d[u]+w$ to the endpoint. Accept only strict improvements. This operation is called *relaxation*. A binary min heap answers “which bound should we examine next?” In the toy implementation improvements insert a second heap entry instead of editing the first. If the popped value no longer equals the stored bound, discard it. No stale price is allowed to establish anything. Among equal values the lab uses its string keys as a deterministic heap tie-break; it does not promise the lexicographically earliest complete route.

After the desk, the candidates are lift at 4, ramp at 1 and west at 1. The ramp can improve lift to 2 and supply a candidate 10 for lab. The west supplies gallery at 2, and gallery offers lab at 4. The lift route from the ramp offers 9. The final minimum route is desk → west → gallery → lab at 4 minutes. Notice why saving only a parent from the first encounter would fail: the earliest shown upper bound need not be the final value.

Here is the correctness hinge. Assume the vertices already settled have correct distances. Suppose the current minimum live label belongs to $u$, but a shorter route to $u$ exists. Walk along that route and find the first unsettled vertex $x$. Its predecessor was settled unless $x$ is the source. The predecessor's relaxation made the label at $x$ no larger than the prefix cost to $x$. With nonnegative weights that prefix costs no more than the complete supposed shorter route to $u$. Then an unsettled vertex had a smaller tentative label than $u$, contradicting the choice. This argument settles the next vertex, including zero-weight edges. When the heap empties, a reachable unsettled vertex would imply a first unsettled vertex with a finite candidate, another contradiction. For the method in its historical setting see [Dijkstra's paper](https://doi.org/10.1007/BF01386390) and for the directed case see the [MIT lecture on Dijkstra](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-13-dijkstra/index.html).

For an example that breaks the assumption, take edges $s\to a$ of cost 2, $s\to b$ of cost 5, and $b\to a$ of cost −4. First finalizing $a$ at 2 is wrong: the later route costs 1. A negative edge is not necessarily a negative cycle. The example is acyclic, and the labels can be computed in topological order. More generally, use a method whose contract handles negative edges and identifies relevant negative cycles, rather than quietly treating a stop-at-first-extraction rule as valid. The lab checks all edges, including disconnected ones, before running; its promise is about the supplied graph. For this lazy heap there are at most $E+1$ inserted entries because each settled outgoing edge is examined once. Under the unit-cost assumption a conservative time bound, including validation, is $O(V+E+(E+1)\log(E+2))$; stale entries can make heap space $O(E+1)$, in addition to input, distances and parents. An indexed decrease-key heap has a different representation and bound.

## Exercises

- **Warm-up, representation:** In the table, which edge allows movement from lab back to desk? What would a code helper have to change to make all links bidirectional?
- **Warm-up, trace:** Trace BFS and record the first parent of every reachable vertex and the queue immediately after each pop-and-scan.
- **Application, weights:** Change the lift-to-lab edge to cost 1. Explain why shortest hops stays the same and calculate the new cheapest route including ties, if any.
- **Application, correctness:** On the negative-edge example, write the exact inequality in the settled-label proof that is no longer justified.
- **Synthesis, contract:** If a path is ordered first by minutes, then by number of lifts, explain what data the state or ranking needs and which version of relaxation still requires proof.
- **Challenge, test:** Construct a directed cyclic fixture with a parallel edge and an unreachable vertex. Explain what a vertex-only witness cannot certify and propose an edge-aware witness.

You can now distinguish adjacency, the policy for choosing frontier work, and the objective that policy justifies. Chapter 3 asks the same question in a different costume: when can early commitment, not just early discovery, be safe?

[Back to the contents](../README.md)
