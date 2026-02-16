---
title: Local CLI
---

# Local CLI: `qestyle`

The `qestyle` command runs the **exact same** review engine locally — same prompts, rules, and fix logic as the GitHub Action.

## Installation

Install directly from GitHub:

```bash
# Latest release
pip install git+https://github.com/QuantEcon/action-style-guide.git

# Specific version
pip install git+https://github.com/QuantEcon/action-style-guide.git@v0.7

# Development (editable install from local clone)
git clone https://github.com/QuantEcon/action-style-guide.git
cd action-style-guide
pip install -e .
```

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY='your-key-here'
```

## Usage

```bash
# Review all categories — applies fixes, writes report
qestyle lecture.md

# Check specific categories only
qestyle lecture.md --categories writing
qestyle lecture.md --categories math,code

# Report only, don't modify the file
qestyle lecture.md --dry-run

# Write report to a custom path
qestyle lecture.md -o custom-report.md

# Use a specific model or temperature
qestyle lecture.md --model claude-sonnet-4-5-20250929 --temperature 1.0

# Check version
qestyle --version
```

## Output

By default, `qestyle` **applies rule-type fixes** directly to the lecture file and writes a Markdown report to `qestyle({category})-{lecture}.md` alongside the original file.

Since lectures live in Git repos, you can review changes with `git diff` and restore with `git checkout`.

### Uncommitted changes warning

If the lecture file has **uncommitted changes**, `qestyle` will warn you and ask to confirm before proceeding — giving you a chance to commit or stash first.

### Report contents

The report contains:

- **Style suggestions** — advisory items requiring human judgment (listed first)
- **Applied fixes** — record of what was automatically changed (at the end)
- **Warnings** — any processing issues

### Dry-run mode

Use `--dry-run` to skip applying fixes and just write the report. Useful to preview what would change.

## Categories

| Category | Focus |
|----------|-------|
| `writing` | Writing style and formatting |
| `math` | Mathematics notation and LaTeX |
| `code` | Python code style |
| `jax` | JAX-specific patterns |
| `figures` | Figure formatting and captions |
| `references` | Citations and bibliography |
| `links` | Hyperlinks and cross-references |
| `admonitions` | Note/warning/tip blocks |

If no categories specified, all categories are checked sequentially.

## Examples

### Check a single category

```bash
qestyle lectures/aiyagari.md --categories writing
```

### Preview changes without applying

```bash
qestyle lectures/aiyagari.md --dry-run --categories math
```

### Review all categories and inspect

```bash
qestyle lectures/aiyagari.md
git diff lectures/aiyagari.md
```

### Undo all changes

```bash
git checkout -- lectures/aiyagari.md
```
