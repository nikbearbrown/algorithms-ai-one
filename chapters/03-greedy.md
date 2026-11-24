# Chapter 3 — Earn the greedy choice

*A rule is not greedy because it is quick. It is greedy because it commits.*

Suppose several repair groups request exclusive rehearsal time in one room. The staff can grant at most one request at any instant. An appealing policy takes whoever starts first. One group requests the whole day; taking it consumes all remaining choices. “First” was easy to compute. It wasn't what the staff wanted to optimize.

By the end, trace an earliest-finish schedule, prove why it preserves an optimum, produce a minimal useful counterexample to an alternative, and identify the assumption lost when slots have unequal value.

## The small contract that makes the proof work

Each request has a start and a strictly later finish. It occupies a half-open interval $[s,f)$: present at the start, absent at the finish. Finishing at time 3 and starting at time 3 is allowed. The room cannot move or divide an interval. Reject duplicate identifiers in the lab. We maximize how many intervals are accepted, not the total time used, requester priority, profit, or room utilization. If safety requires a turnover gap, change the model and then test whether the proof still applies.

| Request | Start | Finish | Value for the separate weighted problem |
| --- | ---: | ---: | ---: |
| long | 0 | 7 | 15 |
| morning | 1 | 3 | 4 |
| browse | 2 | 4 | 9 |
| noon | 3 | 5 | 3 |
| late | 5 | 7 | 4 |

Sort by finish, then start and identifier for deterministic ties. Walk the list. Accept the next compatible interval and advance the cutoff to its finish. The live cutoff begins absent; this also works for negative coordinate values. Choose morning (finish 3), skip browse (start 2), choose noon (starts 3), choose late (starts 5). Early start instead chooses long and gets one. A three-request structural counterexample consists of the long slot plus two back-to-back interior slots; two requests could tie at one, but cannot demonstrate first start getting one when a feasible two-request schedule exists. If you want a strictly earlier start for the bad long slot, make it begin before both short slots.

A good fixture tests the finish/start equality. Quietly using strict inequality for compatibility rejects back-to-back bookings. An assistant might insist that adding a tiny numerical tolerance solves the issue. Here the scale is integer and the definition is exact. If input times really are noisy, that is a policy change, not a one-character repair to the algorithm.

## Exchange a decision without shrinking the result

Let $g$ be an earliest-finishing interval. Take any optimal nonempty feasible schedule and consider its first interval $o$. By definition, $f(g)\le f(o)$. Replace $o$ with $g$. Every later request in that schedule starts no earlier than $f(o)$, so all are still compatible. The schedule has the same count, and now begins with the greedy choice. What remains is the same optimization question on requests starting no earlier than $f(g)$. Repeating the argument proves the entire schedule optimal. Empty input is the stopping case. Ties pose no difficulty here: equality preserves compatibility. It would pose difficulty if the output contract demanded a particular global tie-break not captured by local ordering.

This is stronger than “the chosen interval leaves the room open longer.” It identifies an optimal schedule that survives the choice. It is weaker than “the exchange preserves any measure of success.” In the same fixture the greedy count schedule has value $4+3+4=11$, but long alone has value 15. The exchange argument preserved the *number of intervals*, not their total value. A superficially similar rule choosing highest-value intervals first is also unproved; two nonoverlapping requests worth 8 each beat one conflicting request worth 15. Chapter 4 builds the state needed to preserve alternatives.

The sorted implementation takes $O(n\log n)$ time for sorting and $O(n)$ time for the scan. The answer list can grow to $n$. There is a simpler $O(n)$ scan when finishing order is provided and guaranteed. Compare against a tiny exhaustive oracle, not against a second implementation built from the exact same rule. The [MIT course's interval scheduling lecture](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/resources/lecture-videos/) offers a further proof-oriented reference.

## Transfer: preferences are not times

An optional design comparison helps separate greedy proof forms. In one-to-one deferred acceptance, each proposer tentatively asks receivers in preference order; each receiver retains the best proposer seen so far and releases the previous one if necessary. This does not “pick the top edge and freeze it.” Under complete strict rankings and equally sized sides, a rejected proposal never needs repeating, and a receiver's tentative partner only improves by that receiver's ranking. This is the hinge of a stability argument: if a proposer prefers a different receiver to the final partner, that receiver was asked earlier and either rejected the proposer or later released the proposer for someone preferred. The receiver cannot form a mutually preferred pair at the end. With $n$ on each side there are at most $n^2$ distinct requests, and an implementation using inverse ranking tables can compare receiver preferences in constant time per request after preprocessing.

For a fictional two-by-two example, both proposers rank Q above R, Q prefers the second proposer, and R prefers the first. Q ends with the second and R with the first. Stability means absence of a blocking pair, not maximum summed rank or fairness. If data include ties, incomplete lists, quotas or unsuitable matches, the contract and proof must be restated. See [Gale and Shapley's original paper](https://doi.org/10.1080/00029890.1962.11989827) for the source model, not a claim about how a real admissions process should work.

## Exercises

- **Warm-up, trace:** Trace the room policy if browse finishes exactly at 3. Include your deterministic ordering rule and prove why maximum count is unaffected by a valid finish tie-break, even if the chosen IDs change.
- **Warm-up, boundary:** Explain why `[1,3)` and `[3,4)` are compatible but `[1,3]` and `[3,4]` are not.
- **Application, counterexample:** Design a case where shortest duration first loses. It must select a unique shortest interval, not rely on an unspecified tie.
- **Application, proof:** Restate the exchange if every request requires a fixed one-unit cleanup after finish, before the next start. Compare the resulting cutoff with ordinary compatibility.
- **Synthesis, model:** Classify maximizing total points and requiring a fair share across named groups. Identify which property the count proof fails to preserve in each.
- **Challenge, matching:** Design a two-by-two preference example with more than one stable matching. Show how to audit each candidate by checking both potential blocking pairs.

You can now test whether a local policy really buys a guaranteed global result. If an exchange destroys valuable alternatives, do not look for a better slogan. Store the alternative explicitly.

[Back to the contents](../README.md)
