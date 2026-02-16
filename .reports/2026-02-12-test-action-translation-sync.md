# Test Action Translation Sync Report

**Date:** 2026-02-12
**Test Repository:** QuantEcon/test-action-style-guide
**Test Lecture:** `lectures/test-lecture-violations.md`
**Comparison:** [PR #13](https://github.com/QuantEcon/test-action-style-guide/pull/13) (main/v0.5.1) vs [PR #11](https://github.com/QuantEcon/test-action-style-guide/pull/11) (cleanup branch)

---

## Purpose

Compare the output quality of the current `main` branch (v0.5.1) against the `cleanup/dead-code-docs-tests` branch to evaluate whether the cleanup branch improvements should be merged.

**Key differences between branches:**

| Feature | main (PR #13) | cleanup (PR #11) |
|---------|--------------|------------------|
| Temperature | 1.0 (Anthropic default) | 0.0 (explicit) |
| qe-code-003 rule | Vague — triggers on Anaconda packages | Clarified — excludes numpy, matplotlib, etc. |
| Report format | Per-violation (one entry per fix) | Region-based (grouped by changed text region) |
| No-op handling | Included in report | Skipped automatically |

---

## Summary

| Metric | PR #13 (main) | PR #11 (cleanup) |
|--------|--------------|------------------|
| Total issues found | 49 | 56 |
| Applied fixes | 21 | 8 regions |
| Suggestions for review | 28 | 24 |
| Diff size | +33 / -14 | +34 / -11 |
| Applied fixes report size | 17,918 chars | 7,409 chars |
| Suggestions report size | 24,861 chars | 22,010 chars |
| Hallucinations | **1 (destructive)** | **0** |
| No-op fix entries | 4 | 0 |

---

## Critical Finding: qe-code-003 Hallucination

**PR #13 (main) contains a destructive hallucination** from the qe-code-003 rule ("Package installation at lecture top").

The LLM incorrectly triggered qe-code-003 because it saw numpy/matplotlib imports and thought they needed installation cells. The replacement-based fix model grabbed a section header as anchor text and overwrote it:

**Original text (destroyed):**
```markdown
## Math Violations
```

**Replaced with:**
```markdown
In addition to what's in Anaconda, this lecture will need the following libraries:
```

This is a **data-corrupting bug** — it deletes a section header and replaces it with unrelated text.

**PR #11 (cleanup) has zero qe-code-003 mentions** because the rule was clarified to explicitly state that numpy, matplotlib, scipy, pandas, and sympy are Anaconda-included and do NOT need installation cells.

---

## Applied Fixes Comparison

### PR #13 (main) — 21 fixes

**Code (4 fixes):**
- 3× qe-code-002: All no-ops ("no violations found" / identical before/after text)
- 1× qe-code-003: **Hallucination** — replaced `## Math Violations` header

**Math (2 fixes):**
- 1× qe-math-001: Correct — converted `$\alpha$` → `α`, `$\eta$` → `η`, `$x$` → `x`, `$y$` → `y`
- 1× qe-math-002: No-op ("N/A - No violations found")

**Writing (15 fixes):**
- 9× qe-writing-001 (sentence splitting): 7 correct, 2 no-ops (already separated)
- 6× qe-writing-005 (bold/italic): 2 correct (bold "learning rate", "output"), 4 questionable (italicized informal words and link text)

### PR #11 (cleanup) — 8 regions from 4 rules

| Region | Rules Applied | Description | Correct? |
|--------|--------------|-------------|----------|
| Change 1 (Line 37) | qe-math-001, qe-writing-001 | Split sentence + `$m$` → `m` | ✅ |
| Change 2 (Line 41) | qe-math-001, qe-writing-005 | `$\alpha$` → `α` + bold "learning rate" | ✅ |
| Change 3 (Line 49) | qe-code-002 | Added `python` language specifier | ✅ |
| Change 4 (Line 78) | qe-writing-001 | Split 4 sentences (contractions section) | ✅ |
| Change 5 (Line 83) | qe-writing-001 | Split 4 sentences (passive voice section) | ✅ |
| Change 6 (Line 93) | qe-writing-001, qe-writing-005 | Split sentences + italic `*should*` | ✅ |
| Change 7 (Line 106) | qe-writing-001 | Split 2 sentences (figure reference) | ✅ |
| Change 8 (Line 146) | qe-writing-001 | Split 4 sentences (references section) | ✅ |

### Fix-by-Fix Differences

| Fix | PR #13 (main) | PR #11 (cleanup) | Assessment |
|-----|--------------|------------------|------------|
| qe-code-003 install cell | **Hallucination** — destroyed header | Not triggered | Cleanup wins |
| qe-code-002 language specifier | Not applied | ` ``` ` → ` ```python ` | Cleanup wins — caught real fix |
| qe-code-002 no-ops | 3 entries ("no violations") | 0 entries | Cleanup wins — no noise |
| qe-math-002 no-op | 1 entry ("N/A") | 0 entries | Cleanup wins — no noise |
| qe-math-001 unicode | Correct | Correct | Same |
| qe-writing-001 sentence splits | 7 correct + 2 no-ops | 7 correct + 1 extra (references) | Cleanup wins — more thorough |
| qe-writing-005 bold defs | Bold "learning rate", "output" | Bold "learning rate" | Similar |
| qe-writing-005 informal italics | `*pretty*`, `*really*`, `*kinda*` | Not applied | Main questionable — italicizing slang |
| qe-writing-005 link italic | `learn *more*` | Not applied | Main questionable — spurious |
| qe-writing-005 admonition italic | `*CRITICAL:*`, `*exactly*` | Not applied | Main questionable — altering admonition |
| References splitting | Not applied | Applied (4 sentences) | Cleanup wins |

---

## Suggestions Comparison

| Rule | PR #13 (main) | PR #11 (cleanup) | Notes |
|------|--------------|------------------|-------|
| qe-code-001 (PEP8) | 6 | 3 | Main has 3 extra (likely temp=1 noise) |
| qe-math-009 | 2 | 0 | Main only — borderline flagging |
| qe-writing-002 (contractions) | 8 | 8 | Same |
| qe-writing-003 (passive voice) | 4 | 5 | Cleanup found 1 more |
| qe-writing-007 (second person) | 8 | 8 | Same |
| **Total** | **28** | **24** | Main has +4 (mostly noise) |

The extra suggestions in main (qe-math-009, additional qe-code-001) are likely attributable to temperature=1.0 producing more "creative" and less deterministic responses.

---

## Report Format Comparison

### PR #13 (main) — Per-Violation Format

- Each fix listed individually as numbered entries under category headers
- No-ops included (entries where original = fix or "no violations found")
- When multiple rules affect the same text, each gets its own entry
- **17,918 chars** for 21 entries

### PR #11 (cleanup) — Region-Based Format

- Fixes grouped by changed text region using `difflib.SequenceMatcher`
- No-ops automatically filtered (skipped when `current_text == suggested_fix`)
- Multiple rules on overlapping text shown together with combined before/after
- **7,409 chars** for 8 entries — **59% smaller**

The region-based format is significantly easier to review because:
1. You see the actual before/after for each changed region
2. Multi-rule overlaps are visible (e.g., Change 2 shows qe-math-001 + qe-writing-005 together)
3. No wasted entries for non-changes

---

## Actual Diff Comparison

Both PRs make similar correct changes. The key differences in the actual file modifications:

**Changes only in PR #13 (main):**
- `## Math Violations` → `In addition to what's in Anaconda, this lecture will need...` (**hallucination**)
- `pretty cool` → `*pretty* cool` / `really well` → `*really* well` (questionable italics)
- `kinda important` → `*kinda* important` (questionable)
- `learn more` → `learn *more*` (spurious)
- `CRITICAL:` → `*CRITICAL:*` / `exactly` → `*exactly*` (questionable admonition modification)

**Changes only in PR #11 (cleanup):**
- ` ``` ` → ` ```python ` (correct language specifier fix)
- References section: 4 sentences properly split (missed by main)
- Bare URLs / Poor Link Text sections: proper sentence splitting with blank lines

**Changes in both (matching):**
- `$\alpha$` → `α`, `$\eta$` → `η`, `$x$` → `x`, `$y$` → `y`
- `learning rate` → `**learning rate**`
- All major sentence splits (contractions, passive voice, second person, figure reference)
- Display math sentence split

---

## Conclusions

### Cleanup branch is strictly better for applied fixes quality

1. **Eliminates the hallucination bug** — the most important improvement
2. **Catches a real fix main missed** — the `python` language specifier
3. **Filters out no-ops** — 4 fewer wasted entries
4. **More thorough** — caught references section sentence splitting
5. **More readable report** — 59% smaller, region-based grouping
6. **More deterministic** — temperature=0 gives consistent results across runs

### Main branch's extras are mostly noise

The additional qe-writing-005 italics in main (informal words, link text, admonitions) are questionable and would likely not pass human review:
- Italicizing slang (`*kinda*`, `*pretty*`) doesn't make it more formal
- Modifying link text (`learn *more*`) is a formatting error
- Altering admonition content (`*CRITICAL:*`) changes the message tone

### Recommendation

Merge the cleanup branch. The improvements are clear and measurable:
- **Safety:** No hallucinations vs destructive header replacement
- **Accuracy:** Caught more real issues, zero false fixes
- **UX:** Report is 59% smaller and more informative
- **Consistency:** Deterministic output with temperature=0
