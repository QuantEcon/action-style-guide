---
title: Sample CLI output
---

# Sample CLI output

Real captured output from running `qestyle` on the test lecture
[`markov_chains_jax.md`](https://github.com/QuantEcon/test-action-style-guide/blob/main/lectures/markov_chains_jax.md)
— a realistic QuantEcon lecture seeded with **42 catalogued style violations**. Use
this page to show what a run produces **without a live API call** (the companion to
the [CLI Tutorial](cli-tutorial.md)).

- **Version:** qestyle v0.7.2 · **Date:** 2026-06-05 · **Categories:** all 8

```{note}
Output is **not deterministic** (temperature 1.0 + extended thinking) — a fresh run
will differ slightly. This is one representative snapshot.
```

## The run

```bash
qestyle lectures/markov_chains_jax.md
```

```text
✅ Review complete — 86 issue(s) found
   🔧 Applied 47 fix(es) to markov_chains_jax.md
      Restore original: git checkout markov_chains_jax.md
   📝 38 style suggestion(s) for human review
   📄 Report: …/lectures/qestyle(all)-markov_chains_jax.md
```

| Metric | Count |
|--------|-------|
| Total issues reported | **86** |
| Applied fixes (auto, rule-type) | **47** |
| Style suggestions (human review) | **38** |
| Warnings (apply/empty issues) | **3** |

## What changed

A `git diff` of the applied fixes — every change is mechanical and reviewable:

```diff
-Markov chains are one of the most useful classes of stochastic processes in economics and finance. They provide a framework for modeling systems that transition between states over time, where the future state depends only on the current state.
+Markov chains are one of the most useful classes of stochastic processes in economics and finance.
+
+They provide a framework for modeling systems that transition between states over time, where the future state depends only on the current state.

 ```{code-cell} ipython3
+---
+tags: [hide-output]
+---
 !pip install quantecon

-## Definitions and Setup
+## Definitions and setup

-### Stochastic Matrices
+### Stochastic matrices

-In other words, knowing the Current State is enough to determine probabilities for future states.
+In other words, knowing the current state is enough to determine probabilities for future states.

-The Transition Matrix is
+The transition matrix is
```

These map to real rules: one-sentence-per-paragraph (`qe-writing-001`), the
`hide-output` tag on `pip install` (`qe-code-003`), and heading/word
de-capitalization (`qe-writing-006`, `qe-writing-004`).

## Precision / recall vs the catalog

Every seeded violation is documented in
[`markov_chains_jax.annotated.md`](https://github.com/QuantEcon/test-action-style-guide/blob/main/lectures/markov_chains_jax.annotated.md),
so recall is measurable.

**Rule-level recall: 27 of the 30 rules seeded in the catalog (90%)** — i.e. the run
flagged at least one violation for 27 of the 30 distinct ground-truth rules (up from
26/30 at v0.7.0). Note this is the *seeded catalog* denominator, not the full ~50-rule
registry.

### 3 rules missed

| Rule | Violation | Note |
|------|-----------|------|
| `qe-writing-008` | double space before "and" | possibly normalised by an earlier writing fix |
| `qe-fig-008` | line width not set to `lw=2` | **persistent miss** (also missed at v0.7.0) |
| `qe-link-001` | bare URL / generic "here" link text | **persistent miss** — `qe-link-002` fixes may transform the URLs first |

`qe-fig-008` and `qe-link-001` are missed across both versions — the two rules most
worth a prompt-engineering pass.

### Beyond the seeded set

Seven additional rules fired (e.g. `qe-writing-003`, `qe-math-009`, `qe-jax-003`) —
**either genuine extra finds or false positives; they need a human spot-check.** Two
are already flagged low-quality by the run's own warnings (`qe-writing-007`:
suggestion identical to source; `qe-fig-002`: missing fix).

```{tip}
Rule-level recall (which rules fired) is measured here. **Instance-level precision is
not** — scoring it means reading each of the 86 entries against the catalog, which is
exactly the validation the annotated ground-truth file enables, and a good live
exercise.
```

## Reproduce

```bash
# in the test-action-style-guide repo, with qestyle installed + ANTHROPIC_API_KEY set
qestyle lectures/markov_chains_jax.md          # all categories, applies fixes
git diff lectures/markov_chains_jax.md         # inspect the applied changes
git checkout -- lectures/markov_chains_jax.md   # reset
```
