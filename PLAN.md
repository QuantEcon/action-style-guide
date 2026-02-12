# Action Style Guide — Development Plan

> Living document tracking bugs, improvements, and new features.
> Work proceeds in phases: fix bugs first, then improve existing code, then add new capabilities.

## Phase 1: Bug Fixes & Dead Code Removal

Critical issues that affect correctness or maintainability.

### 1.1 Fix `review_lecture_smart()` Architecture Bug

**Status: DONE**

**Evidence:** The CHANGELOG documents extensive experimentation proving LLMs cannot reliably check multiple rules simultaneously. Yet the primary code path still does exactly that.

**Fix:**
- [x] Refactor `review_lecture_smart()` to use `review_lecture_single_rule()` for each category
- [x] Remove `_review_category()` and `review_lecture()` (dead/superseded methods)
- [x] Remove `check_style()` from `AnthropicProvider` (no longer needed)
- [x] Ensure single-rule evaluation is the ONLY path for all modes

**Files:** `style_checker/reviewer.py`

### 1.2 Remove Duplicate `format_pr_body()`

**Status: DONE**

- [x] Remove the first (older) implementation
- [x] Verify the second implementation is the one used by `main.py`
- [x] Confirm tests still pass

**Files:** `style_checker/github_handler.py`

### 1.3 Remove Dead Code

**Status: DONE**

- [x] `parser_md.py` — removed (was not imported by any production code)
- [x] `review_lecture()` method in `reviewer.py` — removed
- [x] Removed associated tests: `test_parser_md.py`, `test_semantic_grouping.py`, `test_migration.py`
- [x] Removed `verify_setup.py` (referenced dead parser)
- [x] Removed unused `--github-ref` argument from `main.py`
- [x] Removed unused `load_prompt` import from `reviewer.py`

**Files:** `style_checker/parser_md.py`, `style_checker/reviewer.py`, `style_checker/main.py`, `tests/`

### 1.4 Clean Up `requirements.txt`

**Status: DONE**

- [x] Removed `PyYAML` (not imported by action code)
- [x] Removed `python-dateutil` (not imported by action code)
- [x] Verified action imports still work

**Files:** `requirements.txt`

---

## Phase 2: Documentation Fixes

All docs should be accurate before adding new features.

### 2.1 Version Consistency

**Status: DONE**

- [x] Update README badge from `0.5.0` to match `__init__.py` version
- [x] Fix "50+ rules" claim to "49 rules" in README
- [x] Ensure CHANGELOG, README, and `__init__.py` all reference the same version at release

### 2.2 Fix RULES.md

**Status: DONE**

Complete rebuild from rule files (source of truth). The old version had 15+ type/description mismatches.

- [x] Update rule count (49 actual, doc said 48)
- [x] Update rule type count (32 actual, doc said 31)
- [x] Fix all rule type assignments to match rule files
- [x] Fix all rule titles/descriptions to match rule files
- [x] Add missing `qe-writing-008` entry
- [x] Fix `qe-writing-006` and `qe-writing-007` descriptions (were swapped)

### 2.3 Fix Stale References in Docs

**Status: DONE**

- [x] `CONTRIBUTING.md` — removed `LLMProvider` / `check_style()` references, fixed priority taxonomy
- [x] `testing-quick-reference.md` — replaced `test_basic.py` refs with current test files, updated coverage stats
- [x] `tests/README.md` — rewritten to list current test files, removed `verify_setup.py` reference
- [x] `production-testing.md` — updated `@v0.4` to `@v0.5`
- [x] `ci-cd-setup.md` — added historical note, marked CI pipeline as not yet created

### 2.4 Add Prompt Version Tracking

**Status: DONE**

- [x] Add version comments to all 8 prompt files: `<!-- Prompt Version: 0.5.1 | Last Updated: 2026-02-12 | Single rule per LLM call -->`
- [x] Updated `writing-prompt.md` version from `0.3.23` to `0.5.1`

### 2.5 Define `RULE_EVALUATION_ORDER` for All Categories

**Status: DONE**

- [x] Define evaluation order for all 8 categories in `reviewer.py`
- [x] Follow the principle: mechanical → structural → stylistic → migrate

---

## Phase 3: Test Suite Improvements

The test suite has gaps and some tests don't test the right things.

### 3.1 Fix `test_parsing.py`

**Status: DONE**

- [x] Rewrite to import and test the real `GitHubHandler.extract_lecture_from_comment()` method
- [x] Remove duplicated parsing logic (TestHandler class with copied regex)
- [x] Use pytest class structure with 11 focused test cases
- [x] Fix `PytestReturnNotNoneWarning` (was returning True/False instead of using assertions)

### 3.2 Remove Hardcoded Paths

**Status: DONE** — No hardcoded paths found in `test_llm_integration.py` (may have been cleaned up previously).

### 3.3 Add Missing Test Coverage

**Status: DONE**

- [x] `fix_applier.py` — Added `test_fix_applier.py` (13 tests): `apply_fixes()` and `validate_fix_quality()`
- [x] `prompt_loader.py` — Added `test_prompt_loader.py` (9 tests): single/multi category, all categories, invalid category, version tracking
- [x] `extract_individual_rules()` — Added `test_reviewer.py` (15 tests): rule counts, types, order, field validation
- [ ] `main.py` — No unit tests yet (requires significant mocking of CLI/GitHub/LLM — deferred)

### 3.4 Fix Test Warnings

**Status: DONE**

- [x] `test_parsing.py` rewritten to use assertions (warning fixed)
- [x] `test_migration.py` was deleted in Phase 1 (tested removed parser)

### 3.5 Add CI Pipeline

**Status: DONE**

- [x] Updated `.github/workflows/ci.yml` — runs unit tests on push/PR to main
- [x] Ruff for linting (replaced flake8/black/isort)
- [x] Python 3.11, 3.12, 3.13 matrix
- [x] Removed stale `verify_setup.py` reference and integration job

---

## Phase 4: Improve Style Suggestion UX

The core goal: make it easy for authors to review and accept/reject style suggestions.

### 4.1 Better Formatting (Quick Win)

Improve `format_style_suggestions_report()` output:

- [ ] Add line number references for each suggestion
- [ ] Use side-by-side table format for current vs. suggested text
- [ ] Cap displayed suggestions (e.g., top 10) to prevent suggestion fatigue
- [ ] Improve language: "suggestion" not "violation" throughout

### 4.2 PR Reviews with GitHub Suggestion Blocks

**The big UX win.** Post style suggestions as PR review comments with `suggestion` blocks. Authors get a one-click "Commit suggestion" button.

**How it works:**
1. PR is created with rule fixes applied (as today)
2. For each style suggestion, post a PR review comment on the relevant line:
   ````
   **qe-writing-002** — Simplify for clarity

   ```suggestion
   This algorithm was first developed by Bellman in 1957.
   ```
   ````
3. Author clicks "Commit suggestion" to accept, or ignores it

**Constraint:** Suggestion blocks only work on lines in the PR diff. For lines not in the diff, fall back to the formatted comment approach from 4.1.

**Implementation:**
- [ ] Add line-number tracking to violation data (LLM already provides `location`)
- [ ] Parse line numbers from violation location field
- [ ] Build `find_line_in_diff()` utility to check if a line is in the PR diff
- [ ] Use PyGithub `pull.create_review(comments=[...])` to post suggestion blocks
- [ ] Fall back to comment-based format for suggestions not in diff
- [ ] Test with real lectures

### 4.3 Token/Cost Tracking

- [ ] Parse `usage` field from Anthropic API responses
- [ ] Aggregate tokens by rule, category, and lecture
- [ ] Add usage summary to PR comment
- [ ] Expose as action output for workflow access

---

## Phase 5: New Capabilities

Longer-term features, after the foundation is solid.

### 5.1 Incremental PR Review Mode

Trigger style checking automatically when a PR is opened against the lecture repo.

- [ ] New `--mode pr` option
- [ ] Parse PR diff to identify changed `.md` files
- [ ] Review only changed files
- [ ] Post results as PR review comments (integrates with 4.2)
- [ ] Tag rules with `scope: line` vs `scope: document` metadata

### 5.2 Checkbox + `/apply-style` Command

For style suggestions not in the diff (can't use suggestion blocks):

- [ ] Post structured checkbox list in PR comment
- [ ] Author checks desired items, comments `/apply-style`
- [ ] Action triggers, parses checked items, applies as new commit

### 5.3 Batch Processing Improvements

- [ ] Resume capability for bulk reviews (track progress in state file)
- [ ] Progress reporting: `[15/47] Reviewing: intro_to_python.md`
- [ ] Estimated time remaining
- [ ] Partial failure handling with retry

### 5.4 Rule Confidence Scoring

- [ ] Track suggestion acceptance rates (manual initially)
- [ ] Use data to promote reliable style → rule
- [ ] Use data to identify rules needing prompt improvements

### 5.5 Local CLI Tool Enhancement

Improve `tool-style-checker/` for pre-submission author workflow:

- [ ] Structured terminal output with file:line references
- [ ] Machine-readable output format (JSON) for editor integration
- [ ] Share prompts/rules with main action (already partially done)
- [ ] Interactive mode: review suggestions one at a time

---

## Phase Order & Dependencies

```
Phase 1 (Bugs)  ──→  Phase 2 (Docs)  ──→  Phase 3 (Tests)  ──→  Phase 4 (UX)  ──→  Phase 5 (Features)
     │                     │                     │
     │                     │                     └── 3.5 CI blocks nothing but should
     │                     │                          land before Phase 4+
     │                     └── Can run parallel with Phase 1
     │
     └── 1.1 (architecture fix) is prerequisite for everything else
```

- **1.1** must be done first — it fixes the core evaluation path
- **1.2, 1.3, 1.4** are independent and quick
- **Phase 2** can start in parallel with Phase 1 (different files)
- **Phase 3** depends on Phase 1 (dead code removal changes what tests exist)
- **Phase 4** depends on Phases 1-3 being stable
- **Phase 5** depends on Phase 4 patterns being proven

---

## Version Plan

| Version | Includes | Status |
|---------|----------|--------|
| 0.6.0 | Phase 1 + Phase 2 (bugs & docs) | Not started |
| 0.7.0 | Phase 3 (test improvements, CI) | Not started |
| 0.8.0 | Phase 4.1-4.2 (suggestion blocks) | Not started |
| 0.9.0 | Phase 4.3 + Phase 5.1 (tracking, PR mode) | Not started |
| 1.0.0 | Stable release after production validation | Not started |
