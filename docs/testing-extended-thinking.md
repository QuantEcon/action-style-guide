# Extended Thinking: Testing & Findings

> Testing results from the v0.7.0 extended thinking integration (2026-02-13).

## Problem: False Positives from Autoregressive Generation

Prior to v0.7.0, the style checker had a persistent false positive problem where the model would report violations that didn't exist — the "suggested fix" was identical to the "current text." This happened at rates of 40-60% depending on the rule.

### Root Cause

The root cause is inherent to how autoregressive language models generate text:

1. The model starts writing a violation block (commits tokens)
2. Mid-way through, it realizes the text is actually compliant
3. But it can't "undo" the tokens already written
4. So it either retracts inline or emits identical current/suggested text

No amount of prompt engineering can fix this — the model must commit tokens sequentially and can't look ahead.

## Solution: Extended Thinking

Extended thinking (Anthropic's feature for Claude Sonnet 4.5) lets the model reason internally in a "thinking" phase before producing any output tokens. This means:

- The model analyzes the entire document silently
- Verifies every candidate violation before committing any output
- Only includes confirmed violations in the response
- Result: **0% false positive rate**

### Configuration

```python
# In AnthropicProvider
thinking = {
    "type": "enabled",
    "budget_tokens": 10000,  # Max tokens for internal reasoning
}
temperature = 1.0  # Required by Anthropic for extended thinking
```

## Experiment Results

All experiments used rule `qe-writing-001` (one sentence per paragraph) against the test lecture `markov_chains_jax.md` (42 embedded violations across 8 categories).

### Prompt Iteration Results

| # | Approach | Violations Found | False Positives | FP Rate |
|---|----------|-----------------|-----------------|---------|
| 1 | Baseline (verbose prompt, no thinking) | 21 | 9 | 43% |
| 2 | Minimal prompt, no thinking | 27 | 13 | 48% |
| 3 | Minimal prompt + "verify first" | 16 | 10 | 63% |
| 4 | Minimal prompt + "analyze then report" | 20 | 8 | 40% |
| 5 | **Minimal prompt + extended thinking** | **6** | **0** | **0%** |

### Ground Truth Validation

A deterministic Python script (`find_multisentence.py`) was written to find all multi-sentence paragraph blocks in the test lecture. It identified 5-6 genuine violations. The extended thinking result (6 violations, all genuine) aligned correctly with ground truth.

The baseline's 21 "violations" included:
- 9 outright false positives (identical text)
- Several debatable items (compound sentences, list items)
- Only ~6 genuine violations

### Full Production Validation

After deploying to production (`qestyle lectures/markov_chains_jax.md -c writing`), the extended thinking approach was validated across all 8 writing rules:

| Metric | Result |
|--------|--------|
| Total issues found | 40 |
| Applied fixes (rule-type) | 25 |
| Style suggestions (advisory) | 15 |
| False positives | **0** |
| Warnings | 2 (minor parser issues) |

All 25 applied fixes were legitimate corrections. All 15 style suggestions were reasonable recommendations.

## Prompt Design Learnings

### What Hurt (v0.6.1 approach)

1. **Category-specific instructions** — 8 verbose prompts (~120 lines each) with ~60% boilerplate diluted the actual task signal
2. **"Decision process" instructions** (e.g., "for each paragraph, decide if...") triggered exhaustive classify-everything behavior, generating more false positives
3. **Scope instructions** in the prompt (e.g., "skip code blocks") conflicted across categories — scope is rule-specific, not prompt-level

### What Worked (v0.7.0 approach)

1. **Minimal rule-agnostic prompt** (~40 lines) — identity line + task + format template
2. **Rules carry their own context** — each rule defines its scope, unit of analysis, and violation criteria
3. **Extended thinking** — model reasons internally before any output
4. **"Verify before reporting" in prompt** — combined with extended thinking, this ensures only confirmed violations are output

### The Winning Prompt

```markdown
You are a style checker for QuantEcon lecture files written in MyST Markdown.

## Task

Find all violations of the provided rule in the lecture document.

First, silently analyze the entire document and identify candidate violations.
Then, verify each candidate — confirm the current text actually violates the rule
and the fix changes the text.
Only include confirmed violations in your response. Report 0 if none exist.

## Response Format
[template...]
```

This is 40 lines vs the previous 120-line category-specific prompts, and it produces better results.

## Testing Tools

### `test_rule_prompt.py`

Standalone script for prompt iteration. Located in [test-action-style-guide/scripts/](https://github.com/QuantEcon/test-action-style-guide).

```bash
# Test a single rule against a lecture
python scripts/test_rule_prompt.py lectures/markov_chains_jax.md

# Edit PROMPT and RULE in the script to iterate
# Results saved to scripts/last_response.md
```

Features:
- Configurable prompt, rule, model, temperature
- Extended thinking toggle (`USE_EXTENDED_THINKING`)
- Counts violations and false positives (identical text)
- Saves raw response for comparison

### `find_multisentence.py`

Deterministic ground truth finder for `qe-writing-001` violations.

```bash
python scripts/find_multisentence.py lectures/markov_chains_jax.md
```

Parses the file structurally (skips code blocks, directives, frontmatter) and reports all paragraph blocks containing multiple sentences.

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| `thinking_budget=10000` | Enough for careful analysis, not excessive cost |
| `temperature=1.0` | Required by Anthropic for extended thinking |
| 8 identical prompt files (for now) | Validated on writing; consolidate to single file after testing all categories |
| Archive v0.6.1 prompts | Reference for regression testing and comparison |
