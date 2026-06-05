---
title: CLI Tutorial
---

# Tutorial: Reviewing a lecture with `qestyle`

This is a hands-on walkthrough of the local CLI. In about 10 minutes you'll
run a real review on a QuantEcon lecture, read the report, apply fixes, and
inspect the changes with `git diff`.

We use the [`test-action-style-guide`](https://github.com/QuantEcon/test-action-style-guide)
repository as our material. Its `markov_chains_jax.md` is a realistic QuantEcon
lecture (adapted from the intro Markov chains lecture) seeded with **42
catalogued style violations** across all 8 categories. Because every violation
is documented, you can *measure* what `qestyle` catches — which makes it ideal
for a demo.

```{tip}
This page doubles as a **live-demo script**. The exact command sequence is
collected at the end under [Demo cheat-sheet](#demo-cheat-sheet) for copy-paste
during a screen-share.
```

```{note}
**Short on time, or no API key handy?** A pre-baked run of this exact tutorial —
the console output, the applied-changes diff, and a precision/recall analysis — is
on the companion page [Sample CLI output](cli-tutorial-output.md). That run found
86 issues and reached **rule-level recall of 27 of the 30 rules seeded in the test
catalog (90%)**. Walk through that page instead of running live.
```

## Before you start

You need `qestyle` installed and an Anthropic API key exported. If you haven't
done this, see the [CLI reference → Installation](cli.md#installation):

```bash
uv tool install git+https://github.com/QuantEcon/action-style-guide.git
export ANTHROPIC_API_KEY='your-key-here'

qestyle --version          # qestyle 0.7.2
```

```{note}
Each category is one Claude call with extended thinking (temperature `1.0`), so
output is **not deterministic** — the exact violations and counts shift slightly
run to run. The numbers in this tutorial are illustrative.
```

## 1. Get the demo lecture

Clone the test repository and move into it:

```bash
git clone https://github.com/QuantEcon/test-action-style-guide.git
cd test-action-style-guide

ls lectures/
# markov_chains_jax.md             ← realistic lecture, 42 seeded violations
# markov_chains_jax.annotated.md   ← the violation catalog (line-by-line)
# test-lecture-violations.md       ← smaller violation set
# test-lecture-clean.md            ← should pass all checks
```

The companion [`markov_chains_jax.annotated.md`](https://github.com/QuantEcon/test-action-style-guide/blob/main/lectures/markov_chains_jax.annotated.md)
lists every intentional violation with its rule ID and line number. Keep it open
in a second pane during the demo so you can point at "it found W6, M1, C3…".

## 2. Preview without touching the file (`--dry-run`)

Always start with `--dry-run`. It runs the full review and writes a report, but
**never modifies the lecture**. Let's check the `writing` category first:

```bash
qestyle lectures/markov_chains_jax.md --dry-run -c writing
```

The console output looks like:

```text
📋 qestyle v0.7.2
   Lecture:    markov_chains_jax.md
   Categories: writing
   Mode:       dry-run (report only, no changes)

✅ Review complete — 9 issue(s) found
   🔧 6 fix(es) available (run without --dry-run to apply)
   📝 3 style suggestion(s) for human review
   📄 Report: …/lectures/qestyle(writing)-markov_chains_jax.md
```

Two numbers matter here:

- **fixes available** — *rule-type* violations (mechanical, unambiguous). These
  get applied automatically when you drop `--dry-run`.
- **style suggestions** — *style-type* items that need human judgment. These are
  **never** auto-applied; they only ever appear in the report.

## 3. Read the report

Open the report written next to the lecture:

```bash
# macOS `open`; on Linux use `xdg-open`, or just open it in your editor
open lectures/'qestyle(writing)-markov_chains_jax.md'
```

It has a fixed structure — **style suggestions first** (they need your
attention), then the rule violations:

````markdown
# Style Guide Report: markov_chains_jax.md

- **Date:** 2026-06-05 14:32
- **Version:** qestyle v0.7.2
- **Issues found:** 9
- **Mode:** dry-run (no changes applied)

## 📝 Style Suggestions (3)

> **Action required:** These suggestions require human review and judgment.

### 1. qe-writing-002 — Prefer clear, concise sentences
**Location:** Overview
**Description:** Opening sentence is wordy and could be tighter.
...

---

## 🔧 Rule Violations (6)

> **Fixable:** These violations can be auto-fixed (run without `--dry-run`).

### 1. qe-writing-004 — Avoid unnecessary capitalization
**Location:** "The Transition Matrix is"
**Current text:**

```
The Transition Matrix is
```

**Suggested fix:**

```
The transition matrix is
```

**Explanation:** "Transition Matrix" is a common noun mid-sentence...
````

This split — *mechanical fixes* vs *human-judgment suggestions* — is the core
idea to land in the demo. The CLI only ever automates the unambiguous half.

## 4. Apply the fixes and inspect the diff

Now run the same command **without** `--dry-run`. This is the money shot for a
live demo:

```bash
qestyle lectures/markov_chains_jax.md -c writing
```

```text
📋 qestyle v0.7.2
   Lecture:    markov_chains_jax.md
   Categories: writing
   Mode:       fix (rule violations will be applied)

✅ Review complete — 9 issue(s) found
   🔧 Applied 6 fix(es) to markov_chains_jax.md
      Restore original: git checkout markov_chains_jax.md
   📝 3 style suggestion(s) for human review
   📄 Report: …/lectures/qestyle(writing)-markov_chains_jax.md
```

Because the lecture lives in a git repo, the changes are reviewable with a plain
`git diff`:

```bash
git diff lectures/markov_chains_jax.md
```

```diff
-The Transition Matrix is
+The transition matrix is
```

Every applied change is mechanical and visible in the diff — nothing is hidden,
and nothing requiring judgment was touched.

```{important}
If the lecture has **uncommitted changes**, `qestyle` warns you and asks to
confirm before modifying it — commit or stash first so the diff stays clean.
Start every demo from a clean working tree.
```

## 5. Undo

Roll the file back to its committed state at any time:

```bash
git checkout -- lectures/markov_chains_jax.md
```

## 6. Try other categories

Each category targets a different rule family. A couple of nice ones to show:

```bash
qestyle lectures/markov_chains_jax.md --dry-run -c math
```

```diff
# qe-math-003 — use bmatrix, not pmatrix
-P = \begin{pmatrix}
+P = \begin{bmatrix}
 1 - \alpha & \alpha \\
 \beta      & 1 - \beta
-\end{pmatrix}
+\end{bmatrix}
```

```bash
qestyle lectures/markov_chains_jax.md --dry-run -c code
```

```diff
# qe-code-004 — prefer qe.Timer() over manual time.time()
-start_time = time.time()
-result = power_iteration(P)
-elapsed = time.time() - start_time
+with qe.Timer():
+    result = power_iteration(P)
```

You can pass several at once: `-c math,code,writing`.

## 7. Run the full review

With no `-c` flag, `qestyle` runs **every** category in sequence. This is the
most thorough pass — and the slowest, since it's one Claude call per category:

```bash
qestyle lectures/markov_chains_jax.md
# Report: lectures/qestyle(all)-markov_chains_jax.md
```

## 8. Measure recall against the catalog (the punchline)

This is what makes the test repo special. After a run, compare the report's rule
IDs against [`markov_chains_jax.annotated.md`](https://github.com/QuantEcon/test-action-style-guide/blob/main/lectures/markov_chains_jax.annotated.md):

- **True positive** — a catalogued violation that `qestyle` flagged
- **False negative** — catalogued but missed
- **False positive** — flagged but not a real issue (the catalog includes
  deliberate *control* cases, e.g. a correct `{cite:t}` citation, to catch these)

For one rule you can even check recall deterministically. The repo ships a
ground-truth finder for the "one sentence per paragraph" rule:

```bash
python scripts/find_multisentence.py lectures/markov_chains_jax.md
```

This parses the file structurally and lists every multi-sentence paragraph —
the exact set `qe-writing-001` should catch. It's the closest thing to an
objective score, and it's the bridge to the project's larger claim: **most style
violations are mechanical, and a checker catches them reliably.**

(demo-cheat-sheet)=
## Demo cheat-sheet

The full sequence, ready to paste during a screen-share. Start from a clean
working tree.

```bash
# Setup (once)
uv tool install git+https://github.com/QuantEcon/action-style-guide.git
export ANTHROPIC_API_KEY='your-key-here'
git clone https://github.com/QuantEcon/test-action-style-guide.git
cd test-action-style-guide

# 1. Preview — no changes to the file
qestyle lectures/markov_chains_jax.md --dry-run -c writing

# 2. Show the report (style suggestions vs auto-fixes)
open lectures/'qestyle(writing)-markov_chains_jax.md'   # macOS; use xdg-open / your editor elsewhere

# 3. Apply fixes for real
qestyle lectures/markov_chains_jax.md -c writing

# 4. The money shot — every change is a reviewable diff
git diff lectures/markov_chains_jax.md

# 5. Undo
git checkout -- lectures/markov_chains_jax.md

# (optional) other categories / full run
qestyle lectures/markov_chains_jax.md --dry-run -c math
qestyle lectures/markov_chains_jax.md            # all categories

# Reset everything between takes
git checkout -- lectures/
```

## Where to next

- [CLI reference](cli.md) — every flag, option, and exit behavior
- [Rules reference](rules-reference.md) — all 49 rules by category and type
- [Configuration](configuration.md) — model, temperature, rule selection
