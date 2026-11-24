# Chapter 1 — Write the contract and count the work

*The faster answer is no improvement if it solves somebody else's problem.*

Suppose a library is digitizing shelf labels. Its inventory has the offsets of scan marks on a strip, in millimeters, and needs to identify two positions whose marks are closest. Somebody suggests comparing each mark with the next one. At a glance that sounds fast. In which order? In the order the sensor happened to return them, “next” is a fact about the file, not a fact about the shelf. The word you want is *adjacent in numerical order*.

By the end of this chapter, write a contract that settles ties and invalid input, derive counts in a named cost model, and distinguish a proof from a measurement. Basic loops and comparisons are enough to begin.

## The answer comes before the loop

The input contains at least two integers. Choose two distinct positions, not necessarily two different values. Return the smallest absolute difference and its two endpoint values in ascending order. Among pairs with the same difference, choose the lexicographically smaller endpoint pair: compare lower values first, then upper values if needed. The lab rejects input with fewer than two positions. It assumes integer values; it is not a general file parser. It returns values rather than original indices. If a reader needs original row identities, this contract is insufficient and the representation must retain them.

This looks like bookkeeping until you get `[7, 2, 7, 2]`. The minimum is zero. Which pair? There are two eligible value pairs, `(2, 2)` and `(7, 7)`; our order makes the answer `(0, 2, 2)`. A helper that discards duplicates silently solves a different task. A helper that returns only the minimum gap throws away a checkable witness. A helper that returns the same position twice manufactures a zero gap on every input. No number of favorable microbenchmarks fixes any of those errors.

The baseline enumerates every unordered pair of positions. Before the first iteration there is no best pair. After processing any nonempty prefix of pairs, the saved triple is the smallest triple among exactly those pairs. Replacing it only when the new triple is smaller preserves that invariant. At termination the processed prefix is the whole set, so the saved triple is an answer. The loop must advance through finite pairs; the invariant alone would not guarantee termination. Think of the invariant as explaining what the state means, not as a spell that makes the program right.

## Where did the other pairs go?

Sort the values as $x_1$ through $x_n$, from smallest to largest. For any $i<j$, their difference telescopes:

$$x_j-x_i=\sum_{t=i}^{j-1}(x_{t+1}-x_t).$$

Every term is nonnegative. In particular the first adjacent term is no larger than the whole sum. If a nonadjacent pair had the global minimum difference, that adjacent pair could not be strictly better by definition, so the differences must tie. The adjacent pair starts at the same lower value and has an upper value no greater, so it also cannot lose our endpoint tie-break. This gives a defensible sorted scan even with duplicates. If the problem asked for the lexicographically smallest *original positions* with the same gap, this value-based reasoning would not settle the requested tie.

On the fictional desk fixture `[42,19,67,26,85,29,54,70]` the sorted list is `[19,26,29,42,54,67,70,85]`. The gaps in order are `7,3,13,12,13,3,15`. Two gaps tie; choose `26,29`, not `67,70`. Looking at adjacent entries in the original unsorted list sees neither of these pairs. That is a test with an explanation, not just another input in a spreadsheet.

| Number of positions | Baseline pair evaluations | Sorted scan gap evaluations |
| ---: | ---: | ---: |
| 8 | 28 | 7 |
| 16 | 120 | 15 |

The baseline count is $n(n-1)/2$: every position can be paired with $n-1$ others and each unordered pair was counted twice. The final scan has $n-1$ evaluations. Neither column includes the work to read the data or sort. Sorting is the bill the shortcut sends later. With a comparison sort whose worst-case time is $O(n\log n)$, sorting plus a linear scan is $O(n\log n)$ under unit-cost integer arithmetic and comparison. With input already sorted and trusted, the scan alone is linear. If you must validate that promise, an adjacent-order check can also be linear. If integers grow with the input, their bit operations are not automatically constant time. Name that assumption rather than pretending a 1000-digit subtraction costs what a small register subtraction costs.

## Why the representation is part of the design

An array keeps an ordered collection and gives direct indexing. A heap does not keep a fully sorted listing; it cheaply exposes the next highest-priority item under a specified order. In an array-backed binary min heap with zero-based indexing, position $i$ has candidate children at $2i+1$ and $2i+2$ if those indices exist. The order promises that a parent is no greater than either child. Following ancestor comparisons shows the root is no greater than any descendant. Push repair travels up at most the height, and pop repair travels down at most the height. The shape is complete, so that height grows logarithmically with the number of entries. [Python's heap documentation](https://docs.python.org/3/library/heapq.html) shows which operations its interface actually supplies.

A heap on the shelf offsets would not magically contain the pairwise differences. A heap over *all pairs* would first generate quadratically many items. Storing a list in a fancy type does not make an expensive state representation cheap. A heap becomes useful when the state to order is already meaningful, such as the tentative route costs in the next chapter. The closest-gap lab makes separate sorted data and a slice for its demonstration. It does not claim that this particular implementation is an in-place algorithm.

A comparison count answers “how many comparisons in this model?” Wall time answers “what happened on this run?” The proof also answers neither “does this particular code have a defect?” nor “is input scan order trustworthy?” Add tests that can disprove those claims separately. A constant difference between Python calls may outweigh the growth curve at small sizes. Conversely two measurements cannot tell you the asymptotic class for all sizes. [MIT's course notes on algorithms and computation](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-notes/) provide a reference frame for input size and cost models.

## Exercises

- **Warm-up, contract:** For `[4, 10, 4, 8]`, state the required triple. Write a distinct spec if a client needs original position IDs.
- **Warm-up, counting:** Derive the baseline and scan counts for 32 positions without timing anything.
- **Application, falsification:** Give a four-position input that defeats an unsorted neighbor scan. Name the answer the shortcut misses.
- **Application, proof:** Replace the distance objective with the greatest absolute difference. Decide whether adjacent pairs remain enough and justify the answer.
- **Synthesis, design:** A batch system can validate that all its data are sorted; an update service interleaves arbitrary inserts and queries. Propose a measurement and a data-structure question, not a blanket performance prediction.
- **Challenge, model:** Suppose offsets arrive as strings with arbitrary digit length. Describe two places the original analysis used a hidden unit-cost assumption.

You should now be able to make an algorithm answerable: name the object returned, prove where the candidates come from, and point at the omitted work. The next chapter makes a related change that matters even more: two routes with the same endpoints can be ranked by different notions of distance.

[Back to the contents](../README.md)
