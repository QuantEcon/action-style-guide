---
title: Getting Started
---

# Getting Started

This guide walks you through setting up the QuantEcon Style Guide Checker for your lecture repository.

## Prerequisites

- A GitHub repository containing MyST Markdown lecture files
- An [Anthropic API key](https://console.anthropic.com/) for Claude Sonnet 4.5

## Setup

### 1. Create the Workflow File

Create `.github/workflows/style-guide-comment.yml` in your lecture repository:

```yaml
name: Style Guide Comment Trigger
on:
  issues:
    types: [opened, edited]
  issue_comment:
    types: [created]

jobs:
  check-trigger:
    if: contains(github.event.comment.body, '@qe-style-checker')
    runs-on: ubuntu-latest
    steps:
      - uses: QuantEcon/action-style-guide@v0.7
        with:
          mode: 'single'
          lectures-path: 'lectures/'
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
          comment-body: ${{ github.event.comment.body || github.event.issue.body }}
```

### 2. Configure Secrets

In your repository, go to **Settings → Secrets and variables → Actions** and add:

- `ANTHROPIC_API_KEY` — Your Anthropic API key for Claude Sonnet 4.5
- `GITHUB_TOKEN` — Automatically provided by GitHub Actions (no setup needed)

### 3. Configure Labels

Ensure these labels exist in your repository:

- `automated`
- `style-guide`
- `review`

The action adds these labels to PRs it creates.

## Triggering a Review

Comment on any issue in your lecture repository:

```
@qe-style-checker lecture_name
```

With specific categories:

```
@qe-style-checker lecture_name writing,math
```

### Available Categories

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

If no categories are specified, all categories are checked sequentially.

## What Happens Next

1. The action reviews the lecture against the specified rules
2. **Rule-type** violations (mechanical, objective) are fixed automatically
3. **Style-type** suggestions (subjective, advisory) are reported for human review
4. A PR is created with all fixes and a detailed summary
5. Style suggestions are posted as a PR comment

## Scheduled Reviews

You can also set up weekly automated reviews. Create `.github/workflows/style-guide-weekly.yml`:

```yaml
name: Weekly Style Guide Review
on:
  schedule:
    - cron: '0 0 * * 0'  # Every Sunday at midnight UTC

jobs:
  bulk-review:
    runs-on: ubuntu-latest
    steps:
      - uses: QuantEcon/action-style-guide@v0.7
        with:
          mode: 'bulk'
          lectures-path: 'lectures/'
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Next Steps

- [Configuration](configuration.md) — All action inputs and options
- [Rules Reference](rules-reference.md) — Complete list of all 49 style rules
- [CLI Guide](cli.md) — Run the checker locally with `qestyle`
- [GitHub App Setup](github-app-setup.md) — Better rate limits and security for production
