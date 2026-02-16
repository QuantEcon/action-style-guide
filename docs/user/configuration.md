---
title: Configuration
---

# Configuration

All configuration options for the GitHub Action and local CLI.

## Action Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `mode` | Review mode: `single` or `bulk` | Yes | — |
| `lectures-path` | Path to lectures directory | No | `lectures/` |
| `anthropic-api-key` | Anthropic API key for Claude Sonnet 4.5 | Yes | — |
| `github-token` | GitHub token for PR creation | Yes | — |
| `comment-body` | Issue comment body (for single mode) | No | — |
| `llm-model` | Specific Claude model to use | No | `claude-sonnet-4-5-20250929` |
| `rule-categories` | Comma-separated categories to check | No | All categories |
| `create-pr` | Whether to create PR with fixes | No | `true` |
| `temperature` | LLM temperature | No | `1` |

## LLM Model

The action uses **Claude Sonnet 4.5** (`claude-sonnet-4-5-20250929`) with **extended thinking**:

- Extended thinking lets the model reason internally before responding, eliminating false positives (0% FP rate)
- Requires `temperature=1.0` (Anthropic constraint for extended thinking)
- Thinking budget: 10,000 tokens
- Minimal rule-agnostic prompt (~40 lines) + detailed rules (120–235 lines) per category

## Rule Types

The style guide uses a three-tier type system:

### `rule` — Actionable ✅

Clearly actionable rules that are **automatically applied**. These are mechanical, objective checks (32 rules):

- Writing: One sentence per paragraph, capitalization, bold/italic usage
- Mathematics: Transpose notation (`\top`), matrix brackets, sequence notation
- Code: Unicode Greek letters, package installation placement
- Figures: Caption formatting, figure naming, axis labels, line width
- References: Citation style, cross-references
- Links: Internal vs cross-series linking syntax
- Admonitions: Exercise/solution syntax, nested directive tick counts

### `style` — Advisory 💡

Subjective guidelines that **require human judgment** (13 rules):

- Writing clarity and conciseness
- Logical flow between sections
- Visual element opportunities
- Figure size decisions

### `migrate` — Code Modernization 🔄

Legacy patterns that should be updated (4 rules, JAX and code categories only):

- `tic/toc` → `quantecon.Timer()` context manager
- `%timeit` → `quantecon.timeit()` function
- NumPy in-place operations → JAX functional updates
- Implicit random state → explicit JAX PRNG key management

**`rule` types are automatically applied. `style` and `migrate` types are reported as suggestions.**

## Sequential Category Processing

The action processes categories one at a time, feeding the updated document from each category into the next:

1. **Category 1** (e.g., Writing): Reviews original document → finds violations → applies fixes → **updated document**
2. **Category 2** (e.g., Math): Reviews **updated document** → finds violations → applies fixes → **updated document**
3. Continue for all requested categories...

This ensures:
- All fixes are applied without conflicts
- Later categories see changes made by earlier categories
- More coherent and complete final output

**Trade-off**: Sequential processing is slower than parallel (8 sequential API calls vs 8 parallel), but produces more reliable results.

## Review Modes

### Single Mode

Reviews a single lecture file. Triggered by issue comments:

```
@qe-style-checker lecture_name
@qe-style-checker lecture_name writing,math
```

### Bulk Mode

Reviews all lectures in the `lectures-path` directory. Typically used with scheduled workflows:

```yaml
- uses: QuantEcon/action-style-guide@v0.7
  with:
    mode: 'bulk'
    lectures-path: 'lectures/'
```

## PR Creation

When `create-pr` is `true` (default), the action:

1. Creates a new branch: `style-guide/{lecture}-{timestamp}`
2. Commits all applied fixes with detailed messages
3. Opens a PR with:
   - Summary of all changes by category
   - Style suggestions as a PR comment
   - Labels: `automated`, `style-guide`, `review`
