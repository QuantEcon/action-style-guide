# Architecture Review — Style Checking for QuantEcon Lectures

> **Question asked:** Is `action-style-guide` the best approach for applying style-guide checks to
> QuantEcon lecture projects? Is there a better architecture that gives (a) high-value automatic
> updates and (b) recommendations authors can easily accept, reject or change — possibly via the CLI?
>
> **Date:** 2026-11-26 · **Scope:** `style_checker/`, `action.yml`, rules, prompts, tests, docs, the
> planning docs (`PLAN.md`, `IMPROVEMENTS.md`, `TECHNICAL-REVIEW.md`), plus an empirical prototype of
> deterministic checks run over the 161 lectures in `QuantEcon/lecture-python.myst` and the seeded test
> lecture in `QuantEcon/test-action-style-guide`.
> **Status at review time:** 87/87 unit tests pass (`uv run pytest`); no live API calls were made for this review.

---

## TL;DR

**No — not in its current shape.** The project has proven something valuable: Claude, given one
focused rule at a time and room to think, makes good *judgment* calls on lecture style. But it uses
that one tool for every job. All 49 rules — including ones a regex or the Python `ast` module can
check exactly — go through a sequential chain of 49 full-lecture LLM calls, and edits are applied by
searching for text the model quoted back. That shape works against both of your goals:

- **(a) Automatic updates** should be *deterministic*: free, instant, reproducible and runnable on
  every commit. Today none are — each one costs a model call, varies from run to run
  (temperature 1), and can land in the wrong place.
- **(b) Suggestions** need a *stable record* (what, where, why) that people can act on later, one at
  a time. Today they are a single long Markdown comment. Their anchors go stale as later rules edit
  the file, bulk mode throws them away, and no decision is recorded.

**Recommendation: evolve to a layered hybrid.** Keep the rules, the CLI name and the LLM prompt
learnings; change the engine shape:

```
                ┌───────────────────── MyST document model (parsed once) ─────────────────────┐
  lecture.md ──►│ regions with line ranges: front matter · headings · prose · lists · math ·  │
                │ code cells (+ Python AST) · directives (exercise/solution nesting) · links   │
                └───────────────┬───────────────────────────────────────┬─────────────────────┘
                                │                                       │
                   Tier 1: deterministic rules               Tier 2: LLM judgment rules
                   (regex / AST, ~20 rules)                  (~25 rules, one shared snapshot)
                   free · ms · reproducible                  structured output · line-anchored
                   autofix where safe                        cached prefix · parallel / Batch API
                                │                                       │
                                └──────────────┬────────────────────────┘
                                               ▼
                       Findings file (JSON; stable IDs, line range, original,
                       replacement, rationale, rule, tier, source, status)
                                               │
          ┌────────────────────┬───────────────┼─────────────────────┬────────────────────────┐
          ▼                    ▼               ▼                     ▼                        ▼
   qestyle fix          pre-commit hook   qestyle review      GitHub PR check          Scheduled audit
   (apply autofix       (Tier 1 fixes     (interactive:       (changed files: Tier 1   (autofix PR per
    tier)                at commit)        accept / reject /   annotations + Tier 2     lecture; Tier 2
                                           edit, git-add-p     suggestion blocks on     findings as an
                                           style)              changed lines)           artifact → review)
```

The two things that matter most:

1. **A deterministic tier (Tier 1)** built on a MyST parser. This gives you the "high-value automatic
   updates": heading case, `pmatrix`→`bmatrix`, `align`→`aligned` (fixes PDF builds), `prf:`
   prefixes, `hide-output` tags, `lw=2`, cross-series `{doc}` links, whitespace and more. These cost
   nothing, run in milliseconds, behave identically every time, and can run in pre-commit and on
   every PR. §5 gives measured hit rates and precision on the real corpus.
2. **A findings file with an interactive `qestyle review`** (plus GitHub suggestion blocks for PR
   diffs). This is the accept / reject / edit experience. Finding *what to suggest* (expensive, done
   by the LLM, possibly overnight in CI) is separated from *deciding* (cheap, done by a person,
   whenever suits them).

Before any of that, three **urgent fixes** (§3.1) are needed whatever the architecture. One is
verified: **a fresh `pip install` of the CLI is broken today.**

---

## 1. What the project does today

| Piece | Behaviour |
|---|---|
| Rules | 49 rules in 8 `rules/*-rules.md` files, each typed `rule` (auto-apply), `style` (suggest) or `migrate` (suggest). |
| Engine (`reviewer.py`) | For each category, for each rule (in a hard-coded order): build a prompt = shared `prompt.md` + **one rule** + **the whole lecture**; call `claude-sonnet-4-5-20250929` with extended thinking (`budget_tokens=10000`, `temperature=1`, `max_tokens=64000`); regex-parse the Markdown reply; if the rule is `rule`-type, **apply its fixes immediately** so the next rule sees the edited text. |
| Fix application (`fix_applier.py`) | `content.find(current_text)` — first occurrence of the text the model quoted; descending-position slice replacement; skip if not found verbatim. |
| CLI (`qestyle`) | Runs the engine locally, writes fixes straight into the file (with a dirty-tree prompt), writes a Markdown report next to the lecture. |
| Action (`action.py`) | `@qe-style-checker lecture [cats]` comment → one PR with all applied fixes in one commit, a collapsed "applied fixes" comment and an open "style suggestions" comment. `bulk` mode → one PR across all lectures. |

---

## 2. What is good and worth keeping

- **The rules as Markdown specs.** They're human-readable, versionable and already function as the
  style guide. Keep them as the *specification*, and as the LLM prompt for judgment rules.
- **One rule per prompt + thinking.** `docs/developer/extended-thinking.md` documents a real lesson:
  focused prompts and thinking before answering sharply cut "report then retract" false positives. Keep
  the focus. Change only *how* each call is anchored, parsed and merged (§4.4).
- **Programmatic fix application rather than asking the model to re-emit the file.** Right idea;
  it needs a better anchor (§3.2).
- **The `rule` / `style` split.** It's the right instinct (auto-apply vs. human judgment). It just
  needs a second axis (§4.2).
- **The engineering hygiene already done:** env-var input passing in `action.yml`, collision-safe
  branch names, default-branch detection, `uv` lockfile, CI on 3.11–3.13, the region-based
  applied-fixes report, and the honest planning documents. `IMPROVEMENTS.md` already names most of
  the root causes; this review mostly argues for a different *order* and a different *shape* of fix.
- **The seeded test lecture with an annotated catalogue** (`test-action-style-guide`). That is the
  seed of a proper evaluation set (§4.6).

---

## 3. Findings

### 3.1 Urgent — fix regardless of architecture

**U1. The documented CLI install is broken today (verified).**
`pyproject.toml` says only `anthropic>=0.18.0`. `pip install git+https://github.com/QuantEcon/action-style-guide.git`
(the README's Quick Start) now resolves `anthropic` 2.14.0. That SDK targets API version
`2026-10-21`, which removed `temperature`, so `Messages.create()` no longer accepts the argument. I
installed 2.14.0 in an isolated environment and ran the project's own `StyleReviewer` against a mock
transport. The first rule aborts with
`TypeError: Messages.create() got an unexpected keyword argument 'temperature'`. The GitHub Action
and CI are shielded because `uv sync --frozen` uses the lockfile, which pins 0.104.1. That is also
why CI is green.
*Fix now:* either cap `anthropic<1` in `pyproject.toml`, or (better) migrate the call: drop
`temperature`, move to a current model with adaptive thinking + `effort`, and stream with
`get_final_message()`. Add a CI job that resolves the *latest* allowed dependencies so this class of
break shows up in CI.

**U2. Any current model silently produces "0 issues" (code path verified; server response per API docs).**
`--model` / `llm-model` can be set to any model, but the request always sends
`thinking={"type":"enabled","budget_tokens":10000}`. Every current model (Sonnet 5.5, Opus 5.5,
Haiku 5.5, and all 4.7+ models) rejects `budget_tokens` with HTTP 400. `review_lecture_single_rule`
catches `anthropic.APIError` per rule — `BadRequestError` is a subclass — logs a warning and moves
on. Result: all 49 rules "pass" and the run reports success. In practice you cannot move off Sonnet
4.5 without code changes, and a misconfiguration looks like a clean lecture.
*Fix:* treat non-retryable 4xx errors (400/401/403/404) as fatal. Treat only transient errors as
per-rule warnings (the SDK already retries 429/5xx). Set a non-zero exit code when any rule was
skipped.

**U3. Skipped rules are invisible in the GitHub PR (verified by reading).**
`warnings` — which include per-rule API failures — are never rendered by `format_pr_body`,
`format_applied_fixes_report` or `format_style_suggestions_report`. A reviewer has no way to know
that a PR titled "Style guide review" actually skipped, say, 12 of 49 rules. *Fix:* add a "Coverage:
N/49 rules ran" line and list the skipped rules.

### 3.2 Structural problems with the current shape

**S1. No deterministic tier — every rule pays the LLM tax.**
`IMPROVEMENTS.md` §1.3 and `PLAN.md` §4.3 already call for "~13–20 deterministic rules". None are
implemented, and the version plan puts them behind guardrails and rule-clarity work. The cost is not
only money. LLM-only checks are *non-reproducible* (temperature 1: the CLI tutorial notes "a fresh run
will differ"). They *miss mechanical things*: the tutorial records `qe-fig-008` (`lw=2`) and
`qe-link-001` as "persistent misses" — both trivial for a parser. And they can't run where authors
would get the most value: pre-commit and every PR. §5 has the measured numbers.

**S2. Edits are anchored on quoted text, first occurrence (verified with a mock).**
`apply_fixes` uses `content.find(current_text)`. I confirmed two failure modes with a fake provider:
- *Wrong location:* with `current_text="Transition Matrix"` and the phrase appearing in a code comment
  before the prose sentence, the **code comment is edited and the prose is left unchanged**.
- *Duplicates dropped:* two genuine identical violations (e.g. the same heading text twice) → only
  the first is fixed; the second becomes a "position no longer matches" warning.

The `## Math Violations` header overwrite in `.reports/2026-02-12-…` is the same class of bug. The
planned line-number anchoring (`PLAN.md` §4.2) is the right fix. It works best combined with
*verification*: the model returns a line range **and** the original text, and the engine checks they
agree before applying.

**S3. Sequential apply-and-recheck compounds errors and makes suggestions stale (verified with a mock).**
Applying rule N's edits before rule N+1 runs means:
- a bad early fix becomes ground truth for every later rule (`TECHNICAL-REVIEW.md` §4.3);
- the 49 calls cannot run in parallel, and **prompt caching can't work**: the lecture comes *after*
  the rule in the prompt, and the lecture changes between calls anyway;
- **style suggestions are anchored to text that may no longer exist.** I ran a `qe-writing-002`
  suggestion on a sentence, then a later `qe-math-001` fix rewrote `$\alpha$` → `α` in the same
  sentence. The suggestion's `current_text` was **no longer present in the final file** the PR
  contains, so it can't be applied mechanically — by a bot or by a GitHub suggestion block.

Running every LLM rule against **one shared snapshot** and resolving overlaps at merge time removes
all three problems (§4.4).

**S4. The `rule`/`style`/`migrate` type conflates two different questions.**
"Can we *detect* this reliably?" and "Is the *fix* safe to apply unreviewed?" are separate axes.
Several `rule`-typed (auto-applied) rules need judgment to *fix*:
- `qe-writing-005` — what counts as a "definition"? The Feb report shows auto-applied italics on slang
  and on link text.
- `qe-writing-004` — which words are proper nouns?
- `qe-math-001` — the Feb report shows `$x$` → `x`, which degrades typesetting.
- `qe-math-002` — `^T` is often a power or horizon, not a transpose.
- `qe-code-002` — renaming `alpha` breaks code when it's a library keyword argument.

These should be *detected* automatically but *proposed*, not applied.

**S5. Regex-parsed Markdown replies.** `parse_markdown_response` depends on the model reproducing a
template exactly (headings, bold labels, fence styles). Structured outputs (`output_config.format`
with a JSON schema, or `client.messages.parse()`) now guarantee schema-valid replies. That removes
the parser and the `"no change needed"` / identical-text special cases.

**S6. Quality claims rest on thin evidence, and there's no regression harness.**
The README says "**zero false positives**". That comes from one rule (`qe-writing-001`) on one
lecture (`extended-thinking.md`) plus one production run of the writing rules. The CLI tutorial
measures *rule-level recall* (27/30 seeded rules fired) but explicitly not instance-level precision,
and it reports 7 extra rules firing that "need a human spot-check". At temperature 1 every run
differs. Without a scored evaluation set, prompt, rule and model changes can't be judged — and the
model *must* change soon (U1/U2).

**S7. Cost and wall-clock don't scale to bulk mode (estimate — measure with token logging).**
See §6 for the arithmetic. The architecture doc's "$0.08–0.40 per lecture for all 8 categories" looks
roughly an order of magnitude low for 49 thinking calls over a full lecture. Sequential calls make a
full review take tens of minutes, so the weekly `bulk` example over a 100–160-lecture repository
would far exceed GitHub's 6-hour job limit. `bulk` mode also **discards style suggestions** entirely
(`review_bulk_lectures` posts only counts), after paying for them. Token/cost tracking (`PLAN.md`
§5.3) should land early so these numbers are measured, not estimated.

**S8. The accept / reject / change experience is the weakest part.**
- *Auto-fixes:* one PR, one commit with every rule's changes. Reverting one bad fix means editing by
  hand.
- *Suggestions:* a long comment (22–25k characters in the Feb test report). There is no one-click
  accept, no reject, no record of decisions, and anchors may be stale (S3).
- *CLI:* writes fixes directly into the file and suggestions to a report. The author copies by hand.

There is no way to learn which rules authors actually accept, which is the data you need to promote
or retire rules (`PLAN.md` §6.4).

**S9. Some rule text is wrong, and the rules are the prompt.**
Errors in examples teach the model the wrong thing:
- `qe-writing-004` marks "The **bellman** equation" as correct, but Bellman is a proper noun.
- `qe-writing-008`'s "correct" example is a Title-Case `##` heading, which contradicts `qe-writing-006`.
- `qe-writing-001` says lists "can be **proceeded** by" (should be *preceded*).
- `qe-fig-009` (80–100% width) and `qe-fig-001` (don't set size) pull in opposite directions without
  saying how they interact.

§5 adds the issues the prototype surfaced.

### 3.3 Smaller issues

- **Possible empty PRs:** `issues_found` counts suggestions and unapplied fixes. A run that only has
  suggestions still creates a branch and "commits" unchanged content, then opens a PR. *Likely, not
  verified against the live API.*
- **Doc drift:**
  - The examples pin `QuantEcon/action-style-guide@v0.8`, which doesn't exist (`__version__` is
    0.7.2; the roadmap says 0.8 is "not started").
  - `cli-tutorial.md` §7 says "one Claude call per category" — it is one per **rule**.
  - The cost table (§6).
- **Hard-coded `RULE_EVALUATION_ORDER`** duplicates the rule files. A new rule needs edits in two
  places (a test guards this, but metadata belongs with the rule).
- **Non-streaming-then-fallback:** with `max_tokens=64000` the SDK refuses non-streaming requests, so
  every call raises and retries as a stream. Just stream.
- **Only the last text block is kept** (`full_response = block.text` in a loop) — fine today; fragile
  with tools or citations.

---

## 4. Recommended architecture

### 4.1 Principles

1. **Deterministic first, LLM for judgment.** If a parser can decide it, don't pay a model to guess.
2. **Separate detection from decision.** Detectors produce *findings*. Fixers, people and bots act on
   findings. Detection can run overnight in CI; decisions happen whenever the author is ready.
3. **Two axes per rule:** `detector ∈ {deterministic, llm}` × `action ∈ {autofix, suggest, advise}`.
4. **Every edit is anchored and validated** against the parsed document (line range + original text +
   allowed region types). Nothing is applied by blind substring search.
5. **Measure, then promote.** An evaluation set and acceptance telemetry decide when a rule moves from
   `suggest` to `autofix` — or gets retired.

### 4.2 Rule metadata (single source of truth)

Put the metadata in each rule's front matter and drop `RULE_EVALUATION_ORDER` and the regex that
parses `**Type:**`:

```markdown
---
id: qe-math-006
category: math
title: Use aligned (not align) inside $$
detector: deterministic        # deterministic | llm
action: autofix                # autofix | suggest | advise
scope: [math_block]            # regions an edit may touch
builder: pdf
since: 0.9.0
---
(description + examples — still the human spec, and the LLM prompt when detector: llm)
```

### 4.3 Tier 1 — deterministic engine

- **Parser:** `markdown-it-py` + `mdit-py-plugins` (the tokenizer `myst-parser` itself uses). It gives
  tokens with `map` line ranges for front matter, headings, paragraphs, lists, fences/`code-cell`,
  `$$`/`$` math and directives (with nesting, so "inside an exercise" is a tree query). Code cells go
  through Python's `ast`. This also provides the *region map* Tier 2 needs for scope guards.
- **Rules** are small Python functions `check(doc) -> list[Finding]`, with an optional `fix`. Unit
  tests are fixture pairs (`before.md` / `after.md`), so precision is tested, not hoped for.
- **Reuse proven tools where they fit:** `qe-code-001` (PEP 8) is a linter's job. Run `ruff` on
  extracted code cells rather than asking an LLM.
- **Runs everywhere:** `qestyle check`/`fix` locally, a `pre-commit` hook, and a PR check. Exit codes
  and `--format json|github|sarif` make it CI-native.

### 4.4 Tier 2 — LLM engine, redesigned

- **One snapshot.** After Tier 1 fixes, every LLM rule reviews the *same* text. No sequential
  mutation. Calls can run concurrently (CLI) or through the Message Batches API (scheduled audits,
  50% cheaper).
- **Cache the lecture, not the rule.** Order the prompt as frozen instructions + line-numbered lecture
  (cache breakpoint), *then* the rule. The lecture is paid for once per review; each further rule
  costs roughly its own text plus output (§6).
- **Structured output.** A JSON schema for findings:
  `{line_start, line_end, original, replacement?, rationale, confidence}`.
- **Verified anchors.** Accept a finding only if `original` matches the lecture at
  `line_start..line_end` (exactly, or by whitespace-normalised match within that span). Reject
  otherwise and count the rejection as a quality metric.
- **Scope guard.** Reject any edit whose range touches regions the rule's `scope` doesn't allow
  (writing rules can't edit code or math; math rules only edit math). This one check would have
  stopped the header overwrite and the admonition and link-text italics.
- **Merge.** Overlapping edits from different rules are demoted to `suggest` and grouped for the
  author, never applied blindly.
- **Model config in one place.** Use a current model (Sonnet 5.5 is cheaper per token than Sonnet 4.5
  and newer) with adaptive thinking and an explicit `effort`, and no sampling parameters. Choose by
  evaluation score, not by habit. Per-rule model/effort overrides make sense later. Once the eval
  exists, also test **grouping several rules per call** — a big cost lever whose quality impact is
  currently unknown.

### 4.5 Findings file and front-ends — the accept / reject / change experience

**Findings file** (`.qestyle/<lecture>.findings.json`, or a CI artifact): stable finding IDs (a hash
of rule + normalised original + context), line range, original, replacement, rationale, rule + rule
version, tier, source (`deterministic` or model + effort), and **status**
(`open | accepted | rejected | edited`). Optionally export SARIF for editor and code-scanning tools.
Before applying, findings are re-anchored by content hash, so a file edited since detection still
works or the finding is reported as stale.

**CLI (the primary authoring surface):**

```text
qestyle check  lecture.md            # Tier 1 only, ~instant, exit 1 on findings (CI/pre-commit)
qestyle fix    lecture.md            # apply Tier-1 autofixes (like `ruff --fix`)
qestyle suggest lecture.md           # Tier 2 → findings file (costs money; shows estimate first)
qestyle review lecture.md            # step through open findings one at a time:
                                     #   [a]ccept  [r]eject  [e]dit ($EDITOR, suggestion pre-filled)
                                     #   [s]kip  [A]ccept all for this rule  [q]uit
qestyle apply  lecture.md --rule qe-writing-001   # bulk-accept by rule/ID
```

`review` shows the rule, the rationale and a coloured diff in context. It applies decisions
atomically and records them. That's the `git add -p` experience `PLAN.md` §6.5 already sketches, now
backed by durable findings. **Zero-build interim option:** `qestyle suggest --to-worktree` writes all
suggestions into the file *unstaged*. Authors then use VS Code's Source Control diff ("Stage/Revert
Selected Ranges", or edit in place) to accept, reject or change each hunk, with the report giving the
rationale per line.

**GitHub:**
1. **PR mode (new, highest value):** on PRs touching `lectures/*.md`, run Tier 1 on changed files.
   Post annotations, and either push autofixes as a bot commit or offer them as suggestion blocks.
   Run Tier 2 only on *changed paragraphs* and post **review comments with ```` ```suggestion ````
   blocks**. That gives native one-click "Commit suggestion" (accept), "Resolve" (reject), and edit
   before committing (change). This works precisely because the lines are in the diff — the
   constraint `PLAN.md` §5.2 worries about disappears when you check what authors are changing.
2. **Scheduled audit:** per lecture (or per category), open a **small autofix PR with only Tier 1
   fixes** — mergeable at a glance, like pre-commit.ci or Dependabot. Run Tier 2 with the Batch API
   and publish findings as an artifact, plus a short tracking issue that says
   `qestyle review --from <artifact>`. No more 25k-character comments.
3. **Comment trigger** (`@qe-style-checker`) stays, routed to whichever of the above fits.

**Optional complement — a Claude Code skill.** Because the rules are Markdown, packaging them as a
Claude Code skill is cheap. Authors who already use Claude Code then get "review this lecture against
the QuantEcon style guide" with per-edit approve / reject / redirect built in. It's a good
interactive layer for Tier 2 but not a substitute for Tier 1: it isn't reproducible, and its cost is
harder to control in bulk.

### 4.6 Evaluation and feedback

- **`qestyle eval`:** run against a golden set — the seeded `markov_chains_jax.md` + its annotated
  catalogue, plus a few real lectures with human-labelled findings. Report **per-rule precision and
  recall**, anchor-rejection rate and cost. Run it on every rule, prompt or model change (a few
  dollars per run). Deterministic rules get the same treatment through fixture tests.
- **Promotion gate:** a rule moves `suggest → autofix` only with eval precision ≥ ~0.97 *and* a high
  acceptance rate in `review` / PR suggestions. Rules with persistently low acceptance (likely
  `qe-writing-003`, `qe-writing-007`, `qe-fig-002`) become `advise`-only or are retired.

### 4.7 Alternatives considered

| Option | Verdict |
|---|---|
| **A. Finish the existing PLAN as written** (guardrails → rule clarity → line numbers → deterministic → suggestion UX) | The right ingredients in a costly order. Guardrails and prompt tuning patch symptoms of LLM-only, sequential, substring-anchored design. Deterministic checks and a shared snapshot remove whole classes of bug and should come first. |
| **B. Off-the-shelf linters only** (Vale for prose, `ruff` via code cells, `mdformat-myst`) | Useful *components* (`ruff` for `qe-code-001`; Vale's heading-case check is a good reference). But none understands MyST math, directives and exercise nesting together, and none can make judgment calls. Adopt piecemeal inside Tier 1, not as the architecture. |
| **C. Agent-only** (Claude Code skill / Claude GitHub action) | Great interactive UX, less custom plumbing. Weak on reproducibility, cost control and bulk audits; still can't do cheap per-commit checks. Best as an optional front-end over the same rules (§4.5). |
| **D. One LLM call per lecture with all rules** | Cheapest, but the repo's own experiments show focus matters. Revisit *only* with the eval harness, starting with per-category grouping. |
| **E. Layered hybrid (recommended)** | Deterministic where possible, LLM where necessary, a findings file in the middle, several thin front-ends. Gives you both (a) and (b), and makes quality measurable. |

---

## 5. Evidence — deterministic checks on real lectures

<!-- EMPIRICAL-RESULTS -->

---

## 6. Cost model

<!-- COST-MODEL -->

---

## 7. Migration plan (incremental — no big-bang rewrite)

| Step | Scope | Maps to existing plan | Outcome |
|---|---|---|---|
| **0. Hotfixes** (days) | U1–U3: pin or migrate the SDK call (drop `temperature`, adaptive thinking, current model), fail fast on 4xx, show coverage and skipped rules in the PR and the CLI exit code; log `usage` tokens per call; fix doc drift (`@v0.8`, cost table, "per category"). | 5.3 (token tracking) | The CLI installs again; failures are visible; real cost data starts flowing. |
| **1. Tier 1 MVP** (1–2 wks) | Parser + `Finding` model + ~10 highest-yield deterministic rules from §5 with fixture tests; `qestyle check` / `fix`; pre-commit hook; take those rules out of the LLM set. | 4.3, 4.1 (guardrails come for free from the region map) | High-value automatic updates on every commit, at $0. |
| **2. Tier 2 v2** (2–3 wks) | Rule front-matter metadata; snapshot + merge; structured output; verified line anchors; scope guard; cached prefix; `qestyle eval` on the golden set; choose model/effort by score. | 4.2, 4.4, 4.6, roadmap "multi-model" | Measurable, cheaper, safer LLM findings. |
| **3. Decision UX** (2 wks) | Findings file; `qestyle review` / `apply`; GitHub PR mode with suggestion blocks on changed lines; scheduled audit = Tier 1 autofix PRs + Tier 2 artifact via the Batch API. | 5.1, 5.2, 6.1, 6.2, 6.5 | Accept / reject / change in one keystroke or one click; decisions recorded. |
| **4. Feedback loop** (ongoing) | Acceptance telemetry → promote or demote rules; optional Claude Code skill packaging. | 6.4 | Rules improve from evidence. |

Steps 1 and 2 are independent and could proceed in parallel. Step 3 depends on the findings model
from step 1.

---

*Prepared as an advisory review; no production code was changed. Verification artefacts
(mock-provider probes, SDK 2.14 reproduction, deterministic-check prototype) were run in a scratch
environment.*
