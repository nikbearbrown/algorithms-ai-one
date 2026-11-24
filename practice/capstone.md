# Unaided capstone — What should the exchange deploy?

*Submit a decision with a witness, a test that could contradict it, and a stated limit.*

All data below are fictional and for this activity only. Set aside automated assistance until you have a complete first attempt. A short script is allowed; a paper solution with explicit algorithm steps is equally acceptable. Do not use real patrons, schedule commitments or service data.

## Packet

The inventory team sees shelf marks, in input order: `30, 8, 46, 15, 41, 17, 80, 19, 70`. It needs the closest two distinct positions' values, ties resolved as in Chapter 1.

The transport team can travel these directed links; each weight is a nonnegative number of minutes:

| From | To | Minutes |
| --- | --- | ---: |
| depot | ramp | 3 |
| depot | hall | 9 |
| ramp | bridge | 2 |
| bridge | hall | 1 |
| hall | annex | 2 |
| ramp | annex | 11 |

The room team has the following half-open time requests and separately assigned point values. A single room can take non-overlapping requests.

| ID | Start | Finish | Points |
| --- | ---: | ---: | ---: |
| K | 0 | 8 | 13 |
| L | 1 | 3 | 4 |
| M | 2 | 5 | 10 |
| N | 3 | 5 | 4 |
| P | 5 | 8 | 5 |

Outside the room bookings, the planning team has a graph of arbitrary pair conflicts between project requests, not derived from those times. Conflict edges are `KL, LM, NP`; the threshold is at least three independent projects.

## Deliverables

1. Submit the closest-gap answer and explain why the tie choice is correct. Count the specified baseline evaluations and final scan evaluations separately, not the sort time.
2. State which route is said to be “best” under hops versus summed minutes; give a verifiable path for each and justify your frontier choice.
3. Recommend a maximum-count room schedule and then a maximum-point schedule under their separate objectives. Show a recurrence row that actually changes which choice survives, a deterministic tie rule, and witness IDs.
4. Transform the independent-project threshold into a vertex-cover budget. Give a yes-certificate or a reason this tiny instance is no. Label why an algorithm timeout would not be equivalent to your answer.
5. Compare tree frontiers at the same size for two contrasting shapes. Record graph shape, visited/error checks, counted operations, measured units and machine/software environment if timed. Explain a limit not resolved by the comparison.
6. Supply one changed assumption that invalidates a proof above. State whether you would change the method, narrow the promise, or request new evidence.

## Review, then transfer

Score each of the following from 0 to 2: exact input/output contract and tie semantics; traceable witness checked against the original model; proof with named assumptions; independently motivated failing test; reproducible evidence of cost with a correctly bounded conclusion. A correct number without a verifiable witness earns at most 1 in that dimension. A claim that a timeout proves impossibility or that a minimum-vertex-cover ratio transfers directly to independent sets needs revision regardless of score.

After submitting, redo the routing recommendation for a different graph that includes an unreachable target and a nonnegative zero edge somewhere reachable. Then revise the scheduling memo for an explicit one-unit cleanup gap. If you choose an optional assistant critique, give it only your synthetic changed case, your proposed answer and your test; ask for one counterexample, not a replacement solution. Check it by hand or your own oracle. Record any disagreement and what observable result resolved it. An assistant's confidence is not a source of truth for a path or a proof.

[Back to the contents](../README.md)
