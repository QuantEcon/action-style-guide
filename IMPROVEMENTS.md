# Improvements — Reliability & Architecture Review

> Deep review of the action-style-guide architecture with focus on reducing LLM hallucinations,
> improving fix reliability, and identifying rules that can be made more deterministic.
>
> Date: 2026-02-12

---

## Table of Contents

1. [Root Cause Analysis](#1-root-cause-analysis)
2. [Architecture Improvements](#2-architecture-improvements)
3. [Rule-by-Rule Review](#3-rule-by-rule-review)

---

## 1. Root Cause Analysis

### 1.1 Free-text quoting is the #1 hallucination vector

The fix pipeline relies on the LLM perfectly quoting `current_text` from the document. LLMs are not copy-paste machines — they paraphrase, truncate, and occasionally fabricate text. From the [test report](docs/reports/report-test-action-translation-sync-2026-02-12.md), the qe-code-003 hallucination happened because the LLM fabricated a `current_text` that matched a section header (`## Math Violations`), and `str.replace()` blindly replaced it with an install cell introduction.

### 1.2 `str.replace()` is position-unaware

In `fix_applier.py`, `corrected.replace(current_text, suggested_fix, 1)` matches the *first* occurrence. If the LLM meant a different occurrence, or hallucinated the text entirely, the wrong content gets replaced. There is no line-number anchoring to verify intent.

### 1.3 Mechanical rules don't need an LLM

Many rules are pure pattern-matching (e.g., `^T` → `^\top`, `pmatrix` → `bmatrix`, multiple spaces → single space). Sending these to an LLM adds cost, latency, and hallucination risk for zero benefit. Approximately 15–20 of the 49 rules could be implemented as regex or AST-based checks.

### 1.4 49 independent LLM calls = 49 chances to hallucinate

Each API call is an independent opportunity for a bad result. The one-rule-per-call approach maximizes coverage but also maximizes hallucination surface area.

### 1.5 Subjective rules produce noisy results

Rules like qe-writing-002 (clarity), qe-writing-003 (logical flow), qe-writing-007 (visual elements) are inherently judgment calls. The test report shows these produce questionable suggestions (italicizing slang, modifying admonitions). Even as "suggestions," they add noise that reduces trust.

### 1.6 No structural guardrails on fixes

Nothing currently prevents a fix from:
- Replacing a heading with body text
- Deleting a MyST directive
- Breaking markdown structure
- Changing content meaning substantially

---

## 2. Architecture Improvements

### Tier 1: High-Impact, Low-Effort

#### A. Line-number anchoring

Prepend line numbers (e.g., `L001: # Title`) to the lecture content before sending to the LLM. Ask the LLM to reference line ranges instead of quoting text. Then use the *actual* content at those lines as the anchor, not the LLM's quote.

```
Current flow:  LLM quotes text → str.replace() → hope it matches
Better flow:   LLM says "lines 45-48" → extract real text at L45-48 → apply fix
```

This eliminates the core hallucination vector — the LLM no longer needs to perfectly reproduce text.

**Implementation:**
- Add `add_line_numbers(content: str) -> str` utility
- Update prompts to instruct the LLM to use `L045-L048` format
- Update `parse_markdown_response()` to extract line ranges
- Update `fix_applier.py` to use line-based targeting instead of `str.replace()`

#### B. Structural guardrails in `fix_applier.py`

Before applying any fix, validate:
- `current_text` is not a heading (`#`), directive (`` ``` ``), or frontmatter
- The fix doesn't change more than N lines (e.g., 10)
- Edit distance between `current_text` and `suggested_fix` is reasonable (reject replacements where they're completely different content)
- The fix doesn't break markdown structure (matched fences, etc.)

This would have caught the qe-code-003 hallucination — replacing a `## Math Violations` header with an install cell intro is structurally nonsensical.

#### C. Deterministic checkers for mechanical rules

Move pure pattern-matching rules out of the LLM entirely. See section 3 for which rules qualify.

**Candidates (high confidence):**
- qe-math-002: `^T` → `^\top` (regex in math blocks)
- qe-math-003: `pmatrix` → `bmatrix` (regex)
- qe-math-004: `\mathbf` removal (regex)
- qe-math-006: `align` → `aligned` inside `$$` (regex)
- qe-math-007: `\tag` detection (regex)
- qe-writing-008: Multiple spaces → single space (regex)
- qe-fig-003: `set_title()` / `suptitle()` detection (regex in code blocks)

### Tier 2: Medium-Impact, Medium-Effort

#### D. Two-phase detect-then-fix

Split the LLM's job:
1. **Detection**: "List the line ranges that violate this rule. Output ONLY line ranges and a brief reason."
2. **Fixing**: Extract the actual text at that location, then apply a deterministic fix or ask a focused follow-up.

Phase 1 is much simpler for the LLM (just identify locations, not generate fixes), reducing hallucination risk.

#### E. Use Anthropic tool use / structured output

Define a tool schema instead of asking for markdown that gets regex-parsed:

```json
{
  "violations": [{
    "line_start": 45,
    "line_end": 48,
    "description": "...",
    "suggested_fix": "..."
  }]
}
```

This eliminates parsing failures and format drift. Anthropic's tool use forces structured output.

#### F. Confidence-gated application

Ask the LLM to include a confidence field (high/medium/low). Only auto-apply `high` confidence fixes. Route `medium` to suggestions. Discard `low`.

### Tier 3: Architectural Improvements

#### G. Group compatible mechanical rules

Instead of 1 rule per call, group 3–5 mechanical rules from the same category that don't interact. For example, all math-notation rules can be checked simultaneously — they operate on different patterns and won't conflict. This reduces API calls from ~49 to ~15–20 while maintaining coverage.

#### H. Post-fix validation pass

After applying all fixes, validate:
- The resulting markdown still has valid structure
- Run deterministic checkers on the result — did we introduce new violations?
- Compare section headings before/after — were any destroyed?

#### I. Reduce subjective rule scope

Consider whether qe-writing-002, qe-writing-003, and qe-writing-007 should run in auto-fix mode at all. They could be:
- Moved to a separate "advisory" mode that only generates reports (no PRs)
- Triggered only when explicitly requested
- Given much stricter thresholds for what counts as a violation

### Recommended Implementation Order

1. **Line-number anchoring** (A) — biggest bang for the buck
2. **Structural guardrails** (B) — safety net, prevents destructive fixes
3. **Deterministic checkers** (C) — removes LLM from 40% of rules
4. **Structured output** (E) — cleaner data flow
5. **Two-phase detect/fix** (D) — further reduces hallucination for remaining LLM rules
6. **Rule grouping** (G) — cost/latency optimization

Items 1–3 could be implemented in a single release and would dramatically improve reliability.

---

## 3. Rule-by-Rule Review

Detailed assessment of each of the 49 rules across all 8 categories. For each rule we evaluate:
- **Clarity**: Is the rule unambiguous enough for an LLM to follow reliably?
- **Reliability**: How consistently does the LLM apply it correctly?
- **Deterministic potential**: Could this be a regex/programmatic check instead?
- **Recommendations**: Specific improvements

### Legend

| Rating | Meaning |
|--------|---------|
| ✅ Clear | Rule is well-defined, LLM applies it reliably |
| ⚠️ Needs work | Rule is ambiguous or LLM struggles — improvements needed |
| 🔄 Deterministic | Can be moved to regex/programmatic checking |
| 🤖 LLM-only | Requires LLM judgment, cannot be automated |

---

### 3.1 Writing Rules (8 rules)

#### qe-writing-001: One sentence per paragraph
- **Type:** rule | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - Sentence boundary detection is hard — abbreviations (e.g., "i.e.", "Dr."), inline math with periods, and URLs all create false boundaries
  - The rule says "punctuation should be examined to determine a sentence" but doesn't define how to handle edge cases
  - LLM sometimes splits inside list contexts, directive content, or YAML frontmatter
- **Recommendations:**
  1. Add explicit exclusion list: "Do NOT split inside: code blocks, math blocks, YAML frontmatter, directive arguments, list items, table cells"
  2. Add edge-case examples: sentences ending with `e.g.,` or `i.e.,` are not separate sentences; inline math like `$x = 0.$` may have a period that is part of math, not a sentence end
  3. Consider: Could partially automate detection (count periods outside code/math blocks per paragraph) but fix still needs LLM judgment for how to split

#### qe-writing-002: Keep writing clear, concise, and valuable
- **Type:** style | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - Very subjective — "clarity" and "value" are in the eye of the reader
  - The 30–40 word guideline is too vague for the LLM; it sometimes flags perfectly clear 35-word sentences
  - Produces noisy suggestions that reduce trust in the tool
- **Recommendations:**
  1. Raise the word count threshold to 50+ words, or remove the numeric guideline entirely
  2. Add explicit instructions: "Only flag sentences where specific words can be removed without losing meaning. Always show which words to delete."
  3. Add negative examples: "Do NOT flag technical sentences that need every word for precision"
  4. Consider making this advisory-only (never auto-fix, only in the style suggestions report)

#### qe-writing-003: Maintain logical flow
- **Type:** style | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - Extremely subjective — "logical flow" requires understanding the full lecture context
  - LLM suggestions here are often unhelpful ("add a transition sentence") without providing the actual transition
  - Low signal-to-noise ratio in practice
- **Recommendations:**
  1. Narrow the scope: "Only flag cases where a section introduces a concept that hasn't been mentioned or defined previously in the lecture"
  2. Make the check more concrete: "Flag sections that reference variables, functions, or theorems that haven't been introduced yet"
  3. Consider removing from automated checking entirely — this is better as a human editorial review

#### qe-writing-004: Avoid unnecessary capitalization
- **Type:** rule | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only (partially deterministic)
- **Current issues:**
  - The example shows "Bellman Equation" → "bellman equation", but "Bellman" is arguably a proper noun (named after Richard Bellman)
  - No clear list of what counts as a proper noun in economics/math context
  - LLM may decapitalize proper nouns or leave common nouns capitalized inconsistently
- **Recommendations:**
  1. Add an explicit proper noun exception list: "These ARE proper nouns and should stay capitalized: Bellman, Euler, Lagrange, Markov, Nash, Pareto, Bayesian, Gaussian, Hamiltonian, Jacobian, Kalman, Lyapunov, Monte Carlo, Walrasian, Ramsey, Solow"
  2. Clarify: "These are NOT proper nouns: dynamic programming, optimal control, equilibrium, steady state, value function, policy function"
  3. Add: "When in doubt, do not change capitalization — err on the side of not flagging"
  4. Partially deterministic: Could build a word list and flag mid-sentence capitalized words not in the proper noun list, but the fix still needs LLM judgment

#### qe-writing-005: Use bold for definitions, italic for emphasis
- **Type:** rule | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - The test report shows the LLM italicizing slang words (`*kinda*`, `*pretty*`), link text (`learn *more*`), and admonition keywords (`*CRITICAL:*`)
  - "Definition" vs "emphasis" is a judgment call the LLM often gets wrong
  - No guidance on what NOT to format
- **Recommendations:**
  1. Add explicit exclusions: "Do NOT add italic/bold to: words inside links, words inside admonitions/directives, code spans, informal/colloquial words, single common words like 'the', 'more', 'very'"
  2. Narrow the definition of "definition": "A definition is when a technical term is being formally introduced for the first time, typically in the pattern 'A **term** is ...'"
  3. Add: "Do NOT italicize words just because they are emphasized in speech. Only italicize when the emphasis changes the meaning of the sentence."
  4. Add negative examples showing what NOT to do

#### qe-writing-006: Capitalize lecture titles properly
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:** Mostly works well. Clear rule with good examples.
- **Recommendations:**
  1. Detection could be partially automated: identify `## ` headings with Title Case words
  2. Fix still benefits from LLM judgment (which words are proper nouns)
  3. Add: "Articles (a, an, the), conjunctions (and, but, or), and prepositions (in, on, at, for, to, with) should be lowercase in both title case AND sentence case unless they start the heading"

#### qe-writing-007: Use visual elements to enhance understanding
- **Type:** style | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - Extremely vague — "consider opportunities to visualize concepts" is not actionable
  - LLM can't actually create diagrams or figures, so suggestions are always incomplete
  - Very low value in automated checking; better as a human editorial checklist item
- **Recommendations:**
  1. Consider removing from automated checking entirely
  2. If kept, narrow drastically: "Only flag sections that describe a process with 3+ steps and no accompanying figure or diagram"
  3. The reference example URL adds no value to the LLM prompt — remove it

#### qe-writing-008: Remove excessive whitespace
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic
- **Current issues:** The rule is clear but sending to an LLM is wasteful — this is pure regex.
- **Recommendations:**
  1. **Move to deterministic checker**: `re.sub(r'(?<![`$])  +(?![`$])', ' ', text)` with proper code/math block exclusion
  2. No LLM needed at all — zero hallucination risk
  3. Implement as a pre-processing step before any LLM calls

---

### 3.2 Math Rules (9 rules)

#### qe-math-001: UTF-8 unicode for simple parameter mentions
- **Type:** rule | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - The "consistency" exception is hard to apply: "if your text contains mathematical expressions using those parameters, it's acceptable to use inline math"
  - LLM sometimes converts `$x$` → `x` which is technically correct per the rule but often inappropriate (single-letter math variables look odd without math formatting)
  - No clear list of which Greek letters commonly appear as unicode in economics text
- **Recommendations:**
  1. Restrict scope to a concrete list: "Convert ONLY these isolated parameter mentions: `$\alpha$` → α, `$\beta$` → β, `$\gamma$` → γ, `$\delta$` → δ, `$\epsilon$` → ε, `$\lambda$` → λ, `$\mu$` → μ, `$\sigma$` → σ, `$\theta$` → θ, `$\rho$` → ρ, `$\pi$` → π"
  2. Add: "Do NOT convert single Latin letters like `$x$`, `$y$`, `$n$`, `$t$` to plain text — these need math formatting for readability"
  3. Add: "Do NOT convert when the parameter appears in a math expression anywhere in the same paragraph"
  4. Detection is partially deterministic: find `$\alpha$` patterns where no other math expression uses `\alpha` in the same paragraph

#### qe-math-002: Use \top for transpose
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic
- **Current issues:** None significant — clear mechanical rule.
- **Recommendations:**
  1. **Move to deterministic checker**: regex `\^T\b` and `\^\{T\}` inside math blocks → replace with `^\top`
  2. Be careful with `^{\prime}` — only replace if it's used for transpose, not for derivatives. Add: "Only replace `^{\prime}` when clearly used for matrix/vector transpose, not for derivatives like `f'(x)`"

#### qe-math-003: Square brackets for matrices
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic
- **Current issues:** None — clean mechanical rule.
- **Recommendations:**
  1. **Move to deterministic checker**: regex `\\begin\{pmatrix\}` → `\\begin{bmatrix}` (and matching `\end`)
  2. Add exception: "Do NOT change `vmatrix` when used for actual determinant notation (`|A|` or `det(A)`)"

#### qe-math-004: No bold face for matrices/vectors
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic
- **Current issues:** None — clean mechanical rule.
- **Recommendations:**
  1. **Move to deterministic checker**: regex `\\mathbf\{([^}]+)\}` → `\1` inside math blocks
  2. Also handle `\\boldsymbol\{([^}]+)\}` and `\\bm\{([^}]+)\}`
  3. Add exception: "Do NOT remove `\mathbb` (blackboard bold) — this is different from `\mathbf` and is used for sets like ℝ, ℤ, ℕ"

#### qe-math-005: Curly brackets for sequences
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:** Rule is clear but detection is tricky — need to distinguish sequences from index notation.
- **Recommendations:**
  1. Detection is partially deterministic: find `\[ x_t \]_{t=0}` patterns
  2. Fix is mechanical: `[` → `\{`, `]` → `\}`
  3. Add clarification: "This applies ONLY to sequence notation with subscript ranges like `_{t=0}^{\infty}`, not to general bracket usage"

#### qe-math-006: Aligned environment for PDF
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic
- **Current issues:** None — clean mechanical rule.
- **Recommendations:**
  1. **Move to deterministic checker**: regex `\\begin\{align\}` (not `aligned`) inside `$$` blocks → `\\begin{aligned}`
  2. Must check the environment is inside `$$...$$` delimiters to avoid false matches
  3. Also needs to match `\end{align}` → `\end{aligned}`

#### qe-math-007: No manual \tag
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:** Detection is clear but the fix (converting to MyST label syntax) requires understanding the equation context.
- **Recommendations:**
  1. **Detection is deterministic**: regex `\\tag\{` inside math blocks
  2. Fix requires LLM judgment for choosing appropriate label names
  3. Consider: Flag-only for deterministic detection, use LLM only for fix generation

#### qe-math-008: Explain special notation
- **Type:** rule | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - Very narrow scope (only `\mathbb{1}`) but written as a general rule
  - "Explain" is vague — how much explanation is enough?
  - LLM may flag `\mathbb{1}` that IS already explained earlier in the document
- **Recommendations:**
  1. Clarify: "If `\mathbb{1}` appears in the lecture AND there is no preceding sentence explaining what it represents, flag it"
  2. Add: "The explanation must appear BEFORE the first use, not after"
  3. Consider broadening or removing: This is extremely specific for a single symbol. Either broaden to all special notation or make it part of a general "define before use" guideline

#### qe-math-009: Choose simplicity in notation
- **Type:** style | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - "Simpler" is subjective — in math, `\mathcal{P}` may be standard notation for probability measures and `P` would be incorrect
  - LLM doesn't know the author's notational conventions or the field's standards
  - Test report shows this producing borderline flags
- **Recommendations:**
  1. Narrow dramatically: "Only flag when bolded/calligraphic/fraktur notation is used for a quantity that has no established convention requiring that style"
  2. Add: "Do NOT flag `\mathcal`, `\mathbb`, or `\mathfrak` when used for standard mathematical objects (e.g., `\mathcal{F}` for filtrations, `\mathbb{R}` for reals, `\mathcal{L}` for Lagrangian)"
  3. Consider making advisory-only or removing — the risk of incorrect suggestions is high

---

### 3.3 Code Rules (6 rules)

#### qe-code-001: PEP8 unless mathematical notation
- **Type:** style | **Clarity:** ✅ Clear | **Potential:** 🤖 LLM-only
- **Current issues:** Mostly fine — the "unless closer to mathematical notation" exception is appropriate.
- **Recommendations:**
  1. Add: "Capital letters for matrices (A, B, X) and lowercase for vectors/scalars (x, y, z) are always acceptable regardless of PEP8"
  2. Add: "Do NOT flag single-letter variable names that correspond to mathematical notation in the lecture"

#### qe-code-002: Unicode Greek letters in code
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:**
  - The test report showed 3 no-op violations — the LLM reported "no violations found" but the parser treated it as a violation
  - Need to ensure the parser correctly handles the no-violation case
- **Recommendations:**
  1. Detection is partially deterministic: scan code blocks for `alpha`, `beta`, `gamma`, `delta`, `epsilon`, `sigma`, `theta`, `lambda`, `mu`, `rho`, `pi` as variable names
  2. Must avoid false matches: `alpha` in `alpha_channel`, `lambda` (Python keyword), or inside strings/comments
  3. Add: "Do NOT rename `lambda` — it is a Python reserved keyword. Use `λ` only for parameters, not for Python lambda expressions"
  4. Add: "Only convert when the word is used as a standalone variable name or parameter, not as part of a longer name like `alpha_hat` or `n_samples`"

#### qe-code-003: Package installation at lecture top
- **Type:** rule | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only (partially deterministic)
- **Current issues:**
  - **This is the hallucination-causing rule from the test report.** The LLM incorrectly triggered on standard Anaconda packages and generated a destructive fix.
  - The "Important" clarification about Anaconda packages was added after the hallucination was discovered
  - Even with the clarification, the rule requires the LLM to know what's in Anaconda
- **Recommendations:**
  1. Add an explicit Anaconda package list: "The following packages are included in Anaconda and do NOT need installation cells: numpy, scipy, pandas, matplotlib, seaborn, statsmodels, sympy, networkx, scikit-learn, requests, beautifulsoup4, h5py, pillow, sqlalchemy, bokeh, numba, cython, dask, xlrd, openpyxl, lxml"
  2. Detection is partially deterministic: parse import statements from code cells, compare against Anaconda list, check if `!pip install` exists near the top
  3. Consider: make detection-only deterministic (flag missing installs) and let LLM handle the fix (generating the install cell text) — or better yet, use a template for the fix
  4. Add structural guardrail: "The fix for this rule should ONLY add new content (an install cell). It should NEVER modify or replace existing content."

#### qe-code-004: Use quantecon Timer
- **Type:** migrate | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:** None significant.
- **Recommendations:**
  1. Detection is partially deterministic: scan for `time.time()` patterns and `tic()`/`toc()` calls in code blocks
  2. Fix requires LLM judgment for restructuring timing code
  3. Consider: Flag-only mode for detection, with a template-based suggestion

#### qe-code-005: Use quantecon timeit
- **Type:** migrate | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:** None significant.
- **Recommendations:**
  1. Detection is deterministic: scan for `%timeit`, `%%timeit` magic commands
  2. Fix requires LLM judgment for restructuring benchmark code

#### qe-code-006: Binary packages need install notes
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🤖 LLM-only
- **Current issues:** Narrow scope rule — only applies to `graphviz` and similar. Works fine.
- **Recommendations:**
  1. Add more examples of binary packages: `graphviz`, `ffmpeg`, `latex`
  2. The admonition template is specific enough that a deterministic fix could be used once the package is identified

---

### 3.4 JAX Rules (7 rules)

#### qe-jax-001: Functional programming patterns
- **Type:** style | **Clarity:** ✅ Clear | **Potential:** 🤖 LLM-only
- **Current issues:** Subjective but well-scoped to JAX context. Good examples.
- **Recommendations:** None — this rule is appropriate for LLM review.

#### qe-jax-002: NamedTuple for parameters
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🤖 LLM-only
- **Current issues:** Good rule with clear before/after examples.
- **Recommendations:**
  1. Add: "Only flag classes that are purely data containers (no complex methods). Classes with significant logic should remain classes."
  2. Detection is partially deterministic: find `class` definitions with only `__init__` that sets attributes

#### qe-jax-003: generate_path for sequences
- **Type:** style | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - The "standard pattern" shown is fairly specific — lectures may have valid alternative scan patterns
  - Not all iterative generation needs this exact pattern
- **Recommendations:**
  1. Clarify: "This pattern is a recommendation, not a requirement. Only flag when a lecture has imperative Python loops that could clearly benefit from `jax.lax.scan`"
  2. Add: "If the lecture already uses `jax.lax.scan` with a different structure, that is acceptable"

#### qe-jax-004: Functional update patterns
- **Type:** migrate | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:** None — clear mechanical pattern.
- **Recommendations:**
  1. Detection is partially deterministic: scan JAX code blocks for `arr[i] = x` patterns
  2. Fix is mechanical: `arr[i] = x` → `arr = arr.at[i].set(x)`

#### qe-jax-005: jax.lax for control flow
- **Type:** style | **Clarity:** ✅ Clear | **Potential:** 🤖 LLM-only
- **Current issues:** Good rule with clear guidance on when to use each `jax.lax` function.
- **Recommendations:** None — appropriate for LLM review.

#### qe-jax-006: Explicit PRNG key management
- **Type:** migrate | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:** None — clear mechanical pattern.
- **Recommendations:**
  1. Detection is deterministic: scan for `np.random.seed()`, `np.random.normal()`, etc. in JAX-context lectures
  2. Fix requires LLM judgment for restructuring random code

#### qe-jax-007: Consistent function naming
- **Type:** style | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - "Use descriptive names following the pattern `[quantity]_update`" is prescriptive about naming convention
  - "Include time step parameter even if unused" may introduce lint warnings
- **Recommendations:**
  1. Soften: "Prefer descriptive names. The `_update` suffix is recommended but not required."
  2. Reconsider the "include time step even if unused" guidance — unused parameters are a code smell

---

### 3.5 Figure Rules (11 rules)

#### qe-fig-001: Don't set figure size unless necessary
- **Type:** style | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:** None — clear guidance.
- **Recommendations:**
  1. Detection is deterministic: scan code blocks for `figsize=`
  2. Fix requires LLM judgment (is the figsize justified?)

#### qe-fig-002: Prefer code-generated figures
- **Type:** style | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - Very difficult for an LLM to know if a static image could be generated by code
  - Low reliability, high noise
- **Recommendations:**
  1. Narrow: "Flag only when an `{image}` directive points to a `.png` or `.jpg` file that appears to be a simple chart or graph"
  2. Consider removing — this is better as a human editorial guideline

#### qe-fig-003: No matplotlib embedded titles
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic
- **Current issues:** None — clear mechanical rule.
- **Recommendations:**
  1. **Move to deterministic checker**: regex `ax\.set_title\(` and `fig\.suptitle\(` inside code blocks
  2. Must respect the exception: skip if inside exercise/solution directives. This requires parsing directive nesting, which may need LLM or a lightweight MyST parser.

#### qe-fig-004: Caption formatting
- **Type:** rule | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - "5-6 words maximum" is very strict and may conflict with meaningful captions
  - "Lowercase except first letter" is clear but the word limit is arbitrary
- **Recommendations:**
  1. Relax word count: "Keep captions concise, ideally under 10 words" or remove the limit entirely
  2. Focus on the formatting rules (lowercase, no period at end) rather than length

#### qe-fig-005: Descriptive figure names
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:** None — clear naming convention.
- **Recommendations:**
  1. Detection is partially deterministic: scan for `{figure}` directives and check `:name:` field exists and follows `fig-*` pattern
  2. Fix requires LLM judgment for choosing descriptive names

#### qe-fig-006: Lowercase axis labels
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:** None — clear mechanical rule.
- **Recommendations:**
  1. Detection is partially deterministic: scan for `set_xlabel("Capital")`
  2. Add: "Proper nouns and acronyms (GDP, CPI, USA) should remain capitalized"

#### qe-fig-007: Keep figure box and spines
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic
- **Current issues:** None — clear mechanical rule.
- **Recommendations:**
  1. **Move to deterministic checker**: regex `spines\[.*\]\.set_visible\(False\)` in code blocks
  2. Fix is simple: remove the spine-hiding lines

#### qe-fig-008: lw=2 for line charts
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:**
  - "Missing `lw` parameter" requires understanding if a `plot()` call is a line chart
  - Adding `lw=2` to every `plot()` call could be noisy
- **Recommendations:**
  1. Detection: search for `ax.plot(` and `plt.plot(` without `lw=` or `linewidth=` parameter
  2. Consider: Flag-only rather than auto-fix — adding `lw=2` to scatter-style plots would be wrong
  3. Add: "Only applies to line-style plots (ax.plot), not to scatter, bar, hist, or other plot types"

#### qe-fig-009: Figure sizing 80-100%
- **Type:** rule | **Clarity:** ⚠️ Needs work | **Potential:** 🔄 Deterministic (detection)
- **Current issues:**
  - How is "80-100% of text width" measured? In MyST, this is the `:width:` field
  - Many figures don't have an explicit width parameter
- **Recommendations:**
  1. Clarify: "If a `:width:` parameter is set in a figure directive, it should be between 80% and 100%"
  2. Add: "If no `:width:` is set, the default is acceptable — do NOT add `:width:`"

#### qe-fig-010: Plotly latex directive
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:** None — clear pattern match.
- **Recommendations:**
  1. Detection is deterministic: scan for `plotly` imports or `fig.show()` patterns, then check for `{only} latex` directive
  2. Fix could be template-based

#### qe-fig-011: Image directive when nested
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🤖 LLM-only
- **Current issues:** Requires understanding directive nesting, which is hard to do programmatically.
- **Recommendations:**
  1. A lightweight MyST parser could detect this deterministically, but current implementation via LLM is acceptable
  2. Clarify: "Inside `exercise`, `solution`, `admonition`, or any nested directive, use `{image}` instead of `{figure}`"

---

### 3.6 Reference Rules (1 rule)

#### qe-ref-001: Correct citation style
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🤖 LLM-only
- **Current issues:**
  - Very well-documented rule with extensive examples
  - The examples clearly show the distinction between `{cite}` and `{cite:t}`
  - LLM may struggle with context-dependent citation style (is the author name "part of the sentence"?)
- **Recommendations:**
  1. Add a simple heuristic: "If the citation appears at the end of a sentence before a period, use `{cite}`. If the citation appears as a noun phrase (subject or object of the sentence), use `{cite:t}`"
  2. Detection is partially deterministic: find `{cite}` and `{cite:t}` usage, then use LLM to assess context
  3. Rule is well-written — no major changes needed

---

### 3.7 Link Rules (2 rules)

#### qe-link-001: Markdown links for same series
- **Type:** style | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:** None significant.
- **Recommendations:**
  1. Detection is partially deterministic: find `[text](https://xxx.quantecon.org/...)` links that match the current series
  2. Requires knowing which series the lecture belongs to — would need configuration

#### qe-link-002: Doc links for cross-series
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:** Clear rule with good intersphinx prefix list.
- **Recommendations:**
  1. Detection is deterministic: find `[text](https://xxx.quantecon.org/...)` links where `xxx` doesn't match the current series
  2. Fix is template-based: convert URL to `{doc}\`prefix:filename\``
  3. Would need to know which series the current lecture belongs to

---

### 3.8 Admonition Rules (5 rules)

#### qe-admon-001: Gated syntax for exercises with code
- **Type:** rule | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - No examples provided in the rule — this is the only `rule`-type rule with no examples
  - "Gated syntax" (`exercise-start`/`exercise-end`) is specific MyST terminology that the LLM may not know well
- **Recommendations:**
  1. Add examples showing the gated syntax pattern:
     ````
     ```{exercise-start}
     :label: my-exercise
     ```
     Exercise text...
     ```{code-cell} ipython3
     code here
     ```
     ```{exercise-end}
     ```
     ````
  2. Also show the non-gated (incorrect) version for contrast
  3. Clarify: "This is required because MyST Markdown cannot nest code-cell directives inside standard directive fences"

#### qe-admon-002: Dropdown class for solutions
- **Type:** style | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic (detection)
- **Current issues:** None — clear pattern.
- **Recommendations:**
  1. Detection is deterministic: find `solution-start` directives without `:class: dropdown`
  2. Fix is mechanical: add `:class: dropdown`

#### qe-admon-003: Tick count for nested directives
- **Type:** rule | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - No examples provided
  - "Ensure the outer directive uses more ticks than nested directives" is clear in principle but hard to verify automatically
- **Recommendations:**
  1. Add examples showing correct tick count nesting:
     `````
     ````{admonition} Example
     ```python
     code here
     ```
     ````
     `````
  2. Detection is partially deterministic: parse fence-tick counts and check nesting
  3. This is a tricky parse problem — the LLM approach is reasonable but examples would help

#### qe-admon-004: prf prefix for proofs
- **Type:** rule | **Clarity:** ✅ Clear | **Potential:** 🔄 Deterministic
- **Current issues:** None — clear mechanical rule with an explicit list of directives.
- **Recommendations:**
  1. **Move to deterministic checker**: scan for `{theorem}`, `{lemma}`, `{proof}`, etc. without `prf:` prefix
  2. Fix is mechanical: add `prf:` prefix

#### qe-admon-005: Link solutions to exercises
- **Type:** rule | **Clarity:** ⚠️ Needs work | **Potential:** 🤖 LLM-only
- **Current issues:**
  - No examples showing the correct linking pattern
  - "Must include the label of the corresponding exercise" — how? via a directive argument?
- **Recommendations:**
  1. Add examples:
     ````
     ```{solution-start} my-exercise
     :label: my-solution
     ```
     ````
  2. Show that the first argument to `solution-start` should be the exercise label
  3. Detection is partially deterministic: find `solution-start` directives and check if they reference an existing exercise label

---

## Summary: Rules by recommended approach

### Move to deterministic checking (13 rules)
These rules can be checked with regex/pattern matching rather than LLM calls:

| Rule | Detection | Fix |
|------|-----------|-----|
| qe-writing-008 | Regex: `  +` outside code/math | Regex replace |
| qe-math-002 | Regex: `\^T`, `\^\{T\}` in math | Regex replace |
| qe-math-003 | Regex: `pmatrix` | Regex replace |
| qe-math-004 | Regex: `\mathbf`, `\boldsymbol`, `\bm` | Regex replace |
| qe-math-006 | Regex: `\begin{align}` inside `$$` | Regex replace |
| qe-math-007 | Regex: `\tag{` in math | Flag only |
| qe-fig-003 | Regex: `set_title()`, `suptitle()` | Flag only |
| qe-fig-007 | Regex: `spines[...].set_visible(False)` | Remove lines |
| qe-admon-004 | Regex: `{theorem}` without `prf:` | Add prefix |
| qe-code-004 | Regex: `time.time()`, `tic()`/`toc()` | Flag only |
| qe-code-005 | Regex: `%timeit`, `%%timeit` | Flag only |
| qe-jax-004 | Regex: `arr[i] = x` in JAX code | Flag only |
| qe-jax-006 | Regex: `np.random.seed()` in JAX code | Flag only |

### Keep with LLM but improve clarity (12 rules)
These rules need LLM judgment but their descriptions should be clarified:

| Rule | Key improvement |
|------|----------------|
| qe-writing-001 | Add exclusion list (code blocks, math, lists, frontmatter) |
| qe-writing-002 | Raise word threshold, add "show which words to remove" |
| qe-writing-004 | Add proper noun exception list for economics/math |
| qe-writing-005 | Add exclusions (links, admonitions, slang); narrow "definition" |
| qe-math-001 | Restrict to Greek letters only, don't convert `$x$` → `x` |
| qe-math-008 | Clarify scope (first use, define before use) |
| qe-math-009 | Narrow to avoid flagging standard notation |
| qe-code-003 | Explicit Anaconda package list, structural fix guardrail |
| qe-fig-004 | Relax word count, focus on formatting |
| qe-admon-001 | Add examples showing gated syntax |
| qe-admon-003 | Add examples showing tick count nesting |
| qe-admon-005 | Add examples showing solution-exercise linking |

### Consider removing from automated checking (3 rules)
These rules are too subjective for reliable automated review:

| Rule | Reason |
|------|--------|
| qe-writing-003 | "Logical flow" requires deep content understanding |
| qe-writing-007 | "Use visual elements" — LLM can't create figures |
| qe-fig-002 | "Prefer code-generated" — LLM can't know if code could generate the image |

### Already working well (21 rules)
These rules are clear, well-structured, and produce reliable results as-is:

qe-writing-006, qe-code-001, qe-code-002, qe-code-006, qe-jax-001, qe-jax-002, qe-jax-003, qe-jax-005, qe-jax-007, qe-fig-001, qe-fig-005, qe-fig-006, qe-fig-008, qe-fig-009, qe-fig-010, qe-fig-011, qe-ref-001, qe-link-001, qe-link-002, qe-admon-002, qe-math-005
