# Chapter 4 — Combine solutions across subproblems

*Recursion splits instructions. A recurrence explains why the pieces still answer the question.*

Suppose the exchange records checkouts in the order they were entered, but each checkout has a rank from a separately audited shelf ordering. You want to know how much ordering disagreement is present without generating every disagreeing pair in memory. Then the schedule team asks for a different kind of combination: room requests with unequal value. Both problems have parts. Only one permits you to forget each half once it has been summarized.

By the end, build a merge recurrence and count inversions without counting ties, define a state around a compatible prefix, reconstruct an optimum, and identify what evidence an implementation test does not supply.

## Sorting as an accounting device

An inversion in a sequence is a pair of positions $i<j$ with value at $i$ strictly greater than value at $j$. Equal values do not count. The unsorted positions, not the final values, determine which item came first. Split a sequence into left and right halves by position. Every inversion belongs to exactly one bin: entirely left, entirely right, or a left position paired with a right position. There is no fourth bin. This partition is the core of the proof.

Imagine the original sequence `[5,1,4,1]`. The left half contributes the inversion `(5,1)`; the right contributes `(4,1)`. Each recursive call also hands back its values in sorted order, so the merger sees `[1,5]` and `[1,4]`. First take the left 1. With equality, choosing left first preserves stability of the merge and, importantly for the counting rule, does not add an inversion. Now the right 1 is smaller than the left 5: take it and add one. Right 4 is also smaller than left 5: take it and add one. Append the 5. Total inversions: $1+1+2=4$; merged sequence: `[1,1,4,5]`.

If the current right value is less than the current left value, it is less than *every remaining* value in the sorted left half. All those positions originally preceded every position in the right half. Add the number of remaining left entries at once. Conversely, when the left value is no greater than the right head, this left value cannot form a strict inversion with any remaining right value; advancing it loses nothing. Every cross inversion is counted exactly when its right endpoint is taken while the larger left endpoint remains. The induction uses the empty/singleton base case, the disjoint bins, and the combine rule. “I sorted the data and the counts looked right” uses none of them.

For a power-of-two length $n$, the total time $T(n)$ obeys $T(n)=2T(n/2)+O(n)$: split, count separately, merge by advancing one pointer per emitted value. There are logarithmically many levels, at most a linear amount of nonrecursive work per level, and linearly many leaves. The usual near-halves for other lengths give the same bound. The sliced teaching code is not in-place; it allocates list storage, uses logarithmic call depth and has linear peak auxiliary live sequence storage under the usual reference-counted invocation model, because list sizes along a recursive path form a geometric series plus saved sibling results. Linear peak does not mean linear total allocation traffic. If all intermediate arrays were retained for tracing, the space claim would need to change.

## Weighted intervals: keep two histories alive

Return to the [room requests](03-greedy.md). The objective is now total value, with an empty schedule allowed. Use the same finish order, with ties by start and identifier. Define $B_j$ as the best total value obtainable using only the first $j$ sorted requests. $B_0=0$. For request $j$, let $p(j)$ be the length of the earlier prefix whose finishes are no later than its start. Because finish times are sorted, that is a prefix, and the boundary is found by binary search over earlier entries only. Searching the entire list instead hides a dependency on future items and makes the proof harder to enforce. Here positive interval length rules out the interval itself being compatible.

An optimum over the first $j$ requests either excludes $j$, in which case the best possible value is $B_{j-1}$, or includes it, in which case every selected earlier request fits in the compatible prefix and the best remaining value is $B_{p(j)}$. If $v_j$ is the value of request $j$:

$$B_j=\max\{B_{j-1},v_j+B_{p(j)}\}.$$

The state is not “whatever choices we made up to now.” It is the optimum over a particular subproblem independent of which future interval calls it. The same prefix result can be reused by many callers. This is a dynamic program: an ordering of state dependencies plus stored summaries. The state would be insufficient if adding an interval spent a separate quota by room user, because future feasibility would then depend on which user allocations the earlier optimum had consumed.

| $j$ | Request | $p(j)$ | Take value | Skip value | $B_j$ |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0 | none | — | — | — | 0 |
| 1 | morning | 0 | 4 | 0 | 4 |
| 2 | browse | 0 | 9 | 4 | 9 |
| 3 | noon | 1 | 7 | 9 | 9 |
| 4 | long | 0 | 15 | 9 | 15 |
| 5 | late | 3 | 13 | 15 | 15 |

To reconstruct, begin at $j=5$. Skipping late is best, so go to 4. Taking long is best, so add its ID and jump to $p(4)=0$. The selected value is 15. This is a different optimum from the greedy *count* result. In the lab, equality skips the current interval. In a tie fixture `a=[0,2)` worth 4, `b=[2,4)` worth 4, and `c=[0,4)` worth 8, sort as a, c, b; then skip b on the last tie. The optimum value is 8 and the reported selection is c. The alternatives a and b are also a valid witness. Requiring the lexicographically first optimum or the largest number of intervals among weight ties would be a new objective, so express it inside the state comparison.

Each predecessor binary search takes logarithmic time; sorting also takes $O(n\log n)$, filling the value table is linear, and reconstruction moves strictly to smaller prefixes. This implementation uses linear auxiliary storage. Retaining only the last optimum value cannot implement this recurrence: $p(j)$ may point arbitrarily far back. Separately, a value-only interface would not establish that the IDs reconstructed by a second function form the promised shipment. Validate both reported value and feasible certificate against a tiny exhaustive oracle. Larger fixtures are useful for speed and memory, not a substitute for checking the small cases in which all answers fit on one page.

## Which kind of split did you buy?

The merge's two half problems are independent once you know how to combine them. No later half needs a prefix optimum from the other. The weighted schedule repeatedly asks for earlier prefixes; without reuse, recursive “take or skip” can expand many repeated subproblems. Caching a state is safe only if the same state really has the same permitted futures and objective. Divide-and-conquer and dynamic programming can both use recursion; recursion alone identifies neither strategy. [MIT's lectures on merge-style design and dynamic programming](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/lecture-videos/) offer formulations beyond these toy cases.

## Exercises

- **Warm-up, merge:** Compute strict inversions of `[3, 2, 2, 1]` by bins from a split in the middle. Track the equality branch.
- **Warm-up, state:** State what $B_2$ means in words that do not assume which two requests get accepted.
- **Application, reconstruction:** Use requests with equal finishes and at least two distinct optimal sets. Give the prefix table and one witness under the book tie convention.
- **Application, proof:** Explain exactly how the combine operation would change to count pairs with greater *or equal* order.
- **Synthesis, representation:** Give two feasible prefix schedules with the same value but different numbers of a particular user's reservations. Use the comparison to explain why a per-user quota can invalidate the old state.
- **Challenge, complexity:** Distinguish time measured by total recurrence work from maximum simultaneous storage in a version that logs every recursive result.

You can now say what the subanswer means and why an optimum survives being decomposed. Next, change the shape of the constraints and inspect what happens when this neat decomposition is no longer available.

[Back to the contents](../README.md)
