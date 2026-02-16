---
title: Roadmap
---

# Roadmap

Development plan, version targets, and future enhancements.

## Current Status

The project is in **active development**. Breaking changes are acceptable — the focus is on getting things right, not backward compatibility.

## Completed Phases

### Phase 1: Bug Fixes & Dead Code Removal ✅

- Refactored `review_lecture_smart()` to use single-rule evaluation
- Removed dead code (`parser_md.py`, duplicate methods, unused imports)
- Cleaned up `requirements.txt` (removed unused packages)

### Phase 2: Documentation Fixes ✅

- Version consistency across README, CHANGELOG, `__init__.py`
- Rebuilt RULES.md from source (fixed 15+ mismatches)
- Fixed stale references across all docs
- Added prompt version tracking

### Phase 3: Test Suite Improvements ✅

- Fixed `test_parsing.py` to test real methods
- Added tests for `fix_applier.py`, `prompt_loader.py`, `reviewer.py`
- Set up CI pipeline (GitHub Actions, ruff linting, Python 3.11/3.12/3.13)

## In Progress

### Phase 4: Reliability Improvements

Focus: reduce LLM hallucinations, improve fix accuracy, move mechanical rules to deterministic checking.

| Item | Description | Status |
|------|-------------|--------|
| 4.1 Structural Guardrails | Reject destructive fixes (heading/directive deletion) | Planned |
| 4.2 Line-Number Anchoring | Replace free-text quoting with line-number targeting | Planned |
| 4.3 Deterministic Checkers | ~13 mechanical rules via regex (zero hallucination risk) | Planned |
| 4.4 Rule Clarity | Improve 12 rule descriptions to reduce misinterpretation | Planned |
| 4.5 Scope Reduction | Reduce noise from overly subjective rules | Planned |
| 4.6 Prompt Consolidation | Merge 8 identical prompt files into single `prompt.md` | Planned |
| 4.7 Extended Thinking | Claude reasons internally → 0% false positives | **Done** (v0.7.0) |

### Phase 5: Style Suggestion UX

Focus: make it easy for authors to review and accept/reject suggestions.

| Item | Description | Status |
|------|-------------|--------|
| 5.1 Better Formatting | Line numbers, side-by-side tables, cap displayed suggestions | Planned |
| 5.2 GitHub Suggestion Blocks | One-click "Commit suggestion" via PR review comments | Planned |
| 5.3 Token/Cost Tracking | Parse API usage, aggregate by rule/category, report in PR | Planned |

### Phase 6: New Capabilities

| Item | Description | Status |
|------|-------------|--------|
| 6.1 PR Review Mode | Auto-trigger on PR, review only changed files | Planned |
| 6.2 Checkbox + `/apply-style` | Author selects suggestions, comments to apply | Planned |
| 6.3 Batch Processing | Resume capability, progress reporting, partial failure handling | Planned |
| 6.4 Rule Confidence Scoring | Track suggestion acceptance rates to guide refinement | Planned |
| 6.5 Interactive CLI | `qestyle --interactive` — step through suggestions like `git add -p` | Planned |

## Version Plan

| Version | Scope | Status |
|---------|-------|--------|
| 0.6.0 | Bug fixes, docs, rule clarity (Phases 1–2) | Done |
| 0.6.1 | Anti-false-positive prompt instruction | Done |
| 0.7.0 | Extended thinking, minimal prompt, `qestyle` CLI, tests | Done |
| 0.7.1 | Fix circular import (`github.py` → `action.py`) | Done |
| 0.7.2 | Fix temperature default (must be 1 for extended thinking) | Done |
| 0.8.0 | Structural guardrails + rule clarity (4.1, 4.4) | Not started |
| 0.9.0 | Line numbers + deterministic checkers + prompt consolidation | Not started |
| 0.10.0 | Suggestion UX + suggestion blocks (5.1, 5.2) | Not started |
| 0.11.0 | Token tracking + PR mode (5.3, 6.1) | Not started |
| 1.0.0 | Stable release after production validation | Not started |

## Future Enhancements

### Large-Context Batch Evaluation

The current architecture makes 49 separate LLM calls per full review (one per rule). With next-generation models (1M+ context), batch evaluation may become reliable — potentially reducing 49 calls to 1–8.

Three progressive strategies to test:

1. **Category-level batching** (8 calls) — all rules for one category in a single call
2. **Two-pass detect-then-fix** (2+ calls) — detect all violations in one call, fix individually
3. **Full single-call batch** (1 call) — maximum speed, maximum risk

### Multi-Model Support

Different rules have different complexity requirements. Simple mechanical checks could use cheaper/faster models, while complex stylistic judgments benefit from more capable models.

### Interactive CLI Mode

`qestyle --interactive` — guided editing experience where authors step through suggestions one at a time, similar to `git add -p`.

## Phase Dependencies

```
Phase 1 (Bugs) → Phase 2 (Docs) → Phase 3 (Tests) → Phase 4 (Reliability) → Phase 5 (UX) → Phase 6 (Features)
```

- Phase 4.3 (deterministic checkers) enables 4.2 (line numbers)
- Phase 3.5 (CI) should land before Phase 4+
- Phase 5 depends on Phase 4 reliability improvements being proven
- Phase 6 depends on Phase 5 patterns being proven
