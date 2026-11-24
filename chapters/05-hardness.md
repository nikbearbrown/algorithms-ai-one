# Chapter 5 — Explain why a choice is hard

*An instance can be difficult for you without its problem being hard in the mathematical sense.*

Suppose clubs request repair-station support. Some requests conflict because two clubs need the same volunteers, even when their reservation times are disjoint. The operations team now asks for at least $k$ clubs with no conflicts. The interval scheduler has lost its reason to work. A list of conflict pairs can connect almost any two requests; time order no longer describes compatibility. Before reaching for a heuristic, ask exactly what the decision version promises.

You should finish able to write and check a certificate, state a reduction and its direction, distinguish proof of hardness from timeout, and construct an approximation with a stated bound.

## A witness answers a different question from a search

Use a simple undirected graph $G=(V,E)$, with vertices for clubs and an edge for a conflicting pair. A subset $I$ of vertices is *independent* if it contains no edge's two endpoints. The decision problem asks whether such an $I$ of size at least $k$ exists. A yes-certificate is the subset. Check that it contains valid distinct vertices, meets the threshold, and has no conflict edge internal to it. With direct membership flags indexed by vertex and an edge list, you can check a presented subset by scanning its entries and the edges. This does not say how to find a subset. For no-cases, the absence of a witnessed subset does not by itself prove a no answer.

Instead imagine the operations team wants to assign conflict mediation. A *vertex cover* $C$ contains at least one endpoint of every edge; here the decision asks whether a cover of size at most $b$ exists. The complement of an independent set is a cover, because every edge fails to lie entirely inside that independent set. The complement of a cover is independent, because otherwise some edge would have both endpoints outside the cover. The two implications matter equally. With $n=|V|$ and $0\le k\le n$, send the independent-set instance $(G,k)$ to the cover instance $(G,n-k)$ without changing the graph:

$$\exists I: |I|\ge k \text{ and } I \text{ independent}
\quad\Longleftrightarrow\quad
\exists C: |C|\le n-k \text{ and } C \text{ a cover}.$$

This transformation and its correspondence have polynomial cost in the ordinary encoded input length. At extreme thresholds, $k=0$ maps to budget $n$ (yes), and $k=n$ maps to zero (yes precisely when $E$ is empty). The diagram goes from the known source problem to the candidate target problem. An exact efficient solver for the target would solve the source after the transformation. Reversing a different reduction and hoping the same conclusion follows is a common error; in this example complements happen to give both directions, but a reduction need not be reversible in general.

| Fictional conflicts | $k$ | One independent set | Complement cover and budget |
| --- | ---: | --- | --- |
| AB, BC, CD, BD | 2 | A, C | B, D; budget 2 |
| same graph | 3 | none | no cover of size at most 1 |

For the no-instance, AB and CD are disjoint. A cover needs at least one endpoint per edge and cannot cover both using one vertex. The specific witness gives a clean local lower bound. It does not turn every no-case into an easy proof.

## What NP-completeness does and does not buy

P is the class of decision problems solvable in deterministic polynomial time under the usual encoded-input model. NP is the class of decision problems whose yes-instances have polynomial-length certificates checkable in polynomial time. NP-hard means every problem in NP reduces to the target by the adopted polynomial-time reduction. NP-complete means both NP-hard and in NP. In this chapter we take the standard NP-completeness starting point of decision Clique and show the short chain: a clique in a simple graph is an independent set of the same size in the graph complement, then use the cover transformation above. Building the complement uses at most quadratically many unordered pairs, polynomial for explicitly supplied vertices. Both target decision problems have direct certificate checkers. [Karp's original reduction paper](https://www2.seas.gwu.edu/~simhaweb/champalg/tsp/papers/KarpOriginal.pdf) gives the classic definitions and names vertex cover “node cover”; the toy case above is original.

Showing NP-completeness does not prove a particular graph will take a long time, that no finite algorithm exists, or that P and NP differ. A solver that returns “did not finish within 2 seconds” gives a resource observation. It has not returned a no-certificate and has not proved a lower bound on every algorithm for the problem. Likewise a quick run on the example does not refute hardness. Restricting structure changes the problem class: for conflicts exactly from overlapping intervals and maximum count, the efficient method in Chapter 3 already answers whether the count is at least $k$. The bare phrase “selection problem” identifies neither setting.

## A guarantee can be useful without an exact answer

Construct a matching: greedily add an edge only if neither endpoint is already matched. A *maximal* matching cannot accept any extra edge; it need not have the largest possible size. Select both endpoints of every matched edge. If some original edge were still uncovered, neither endpoint would have been matched and that edge could have been added, contradicting maximality. The selected endpoints therefore form a cover.

Let $m$ be the number of matched edges. Any cover needs at least one vertex from each, and because matched edges have disjoint endpoints those contributions are distinct. So $\mathrm{OPT}\ge m$. The algorithm picks exactly $2m$ vertices, at most $2\,\mathrm{OPT}$. For no edges it returns the empty optimum. In our graph the lab's sorted order takes AB, then CD. The returned cover is all four vertices, though B and D suffice. The output is valid, the bound is tight on this fixture, and the solution is not optimal. This particular implementation sorts edges for determinism; a scan of a given edge list needs only one pass if the edge order itself is an acceptable choice rule and membership checks are cheap. Sorted deterministic output and asymptotic time are different design requests.

This is an approximation for *minimum cover*, not automatically a multiplicative approximation for maximum independent set. When a cover size is subtracted from $n$, an additive error in the cover can consume the entire independent set. In our example the complement of the four-vertex cover is empty while optimum independent-set size is 2. Exact reductions transfer decisions; approximation transfer needs a separate argument.

## Optional model switch: when a flow certificate fits

Suppose two clerks A and B must hand off tasks X and Y. Each clerk can serve one task; X and Y each accept one clerk. A can serve X or Y; B can serve X only. This is a bipartite matching model, not arbitrary conflict selection. Encode a source edge to each clerk, an edge for each permissible assignment, and an edge from each task to the sink, all of capacity one. Route one unit through A→X. Now B appears stuck. A residual edge X→A of capacity one denotes permission to undo the current A→X unit, not an original assignment. The augmenting path source→B→X→A→Y→sink replaces A→X with B→X and A→Y. Two units reach the sink, and there can be no third: the cut leaving the source has capacity two. This pair of witness and upper bound proves optimality for the toy instance. Flow can model alternatives and reversible choices when capacities capture the contract; it does not by itself capture arbitrary incompatibilities. See [MIT's flow and cut lectures](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/lecture-videos/) for the general theorem.

## Exercises

- **Warm-up, certificates:** On the four-club graph, confirm why B,D covers every listed edge and A,C is independent.
- **Warm-up, direction:** Label the source and target in the transformation when a new solver is available only for Vertex Cover.
- **Application, boundary:** Try empty, complete and disconnected graphs. Check that both implications still hold at $k=0$ and $k=n$.
- **Application, approximation:** Give an edge order that changes the size of a maximal matching. Explain why the lower-bound inequality remains true.
- **Synthesis, remedy:** Describe how you would separately label a feasible cover, an exact optimal cover, and a timeout with no verified cover.
- **Challenge, modeling:** Add a third clerk and task to the flow case. Provide a candidate assignment and a cut upper bound; note which change would make this model insufficient again.

You can now discuss what kind of evidence a claim about hardness needs, and what an approximation actually guarantees. The last chapter takes the implementation in hand and measures costs outside the proof model.

[Back to the contents](../README.md)
