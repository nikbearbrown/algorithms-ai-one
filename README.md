# Algorithms (AI Plus One)

**Compact first draft.** Six chapters with original worked examples, paper exercises, an independent capstone and optional offline checks. This is not a finished textbook, an expert-reviewed edition or a replacement for any existing course or book.

An algorithm makes three promises: what problem it solves, why its answer is correct, and how much work it needs. This book opens each promise up and shows you how to test what is inside. It is for readers who can write a small program and follow a proof by contradiction or induction. Read the main path without a specific language; the optional labs use Python 3.10 or newer and no external packages or model calls.

## Learning outcomes

After working through this draft, readers should be able to:

- State an algorithm’s contract, justify correctness, and count its work.
- Choose between graph search, greedy methods, and dynamic programming based on problem assumptions.
- Explain a hardness claim and benchmark implementation behavior separately from theoretical bounds.

## Chapters

1. [Write the contract and count the work](chapters/01-contract.md)
2. [Represent reachability and cost](chapters/02-reachability.md)
3. [Earn the greedy choice](chapters/03-greedy.md)
4. [Combine solutions across subproblems](chapters/04-subproblems.md)
5. [Explain why a choice is hard](chapters/05-hardness.md)
6. [Benchmark what the proof does not predict](chapters/06-benchmark.md)
7. [Unaided capstone: what should the exchange deploy?](practice/capstone.md)

The proof track asks you to justify an invariant, a recurrence or a reduction. The implementation track asks you to inspect actual outputs and design a check that can fail. Do the independent work before any optional assistant critique. Do not upload coursework, private data or source material. Deliberately wrong suggestions in the book are teaching examples, not outputs of a measured AI system.

From this directory:

```sh
python3 -B -m lab.check_examples
python3 -B -m unittest discover -s tests -v
python3 -B -m lab.benchmark --n 4095 --repeats 7
```

The benchmarks use bounded synthetic trees and run locally. Frontier items are not bytes; allocation peaks measured by Python are not process resident memory. All fixtures, prose and implementations here are original or standard mathematical ideas restated in original examples. Technical references are linked where used. More exercises, deeper treatments of alternative algorithms and classroom review remain future work.
