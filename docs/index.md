---
title: QuantEcon Style Guide Checker
---

# QuantEcon Style Guide Checker

A GitHub Action and local CLI for automated style guide compliance checking of [QuantEcon](https://quantecon.org) lecture materials using AI-powered analysis.

## What It Does

The style checker reviews MyST Markdown lecture files against the [QuantEcon Style Guide](https://manual.quantecon.org), ensuring consistency across all lecture series. It uses Claude Sonnet 4.5 with extended thinking to check **49 style rules** covering writing, mathematics, code, JAX patterns, figures, and more.

### Key Features

- **AI-Powered Review** — Uses Claude Sonnet 4.5 with extended thinking for zero false positives
- **49 Style Rules** — Covering 8 categories: writing, math, code, JAX, figures, references, links, admonitions
- **Automated Fixes** — Applies rule-type fixes programmatically for reliable results
- **Local CLI** — `qestyle` command runs the same engine locally
- **GitHub Integration** — Creates labeled PRs with detailed explanations

### How It Works

1. **Trigger** a review via issue comment (`@qe-style-checker lecture_name`) or scheduled workflow
2. The action checks each rule individually using Claude with extended thinking
3. **Rule-type** violations are fixed automatically; **style-type** suggestions are reported for human review
4. A **PR is created** with all fixes and a detailed summary

## Quick Start

::::{tab-set}

:::{tab-item} GitHub Action
Comment on any issue in your lecture repository:

```
@qe-style-checker lecture_name
```

With specific categories:

```
@qe-style-checker lecture_name writing,math
```

See [Getting Started](user/getting-started.md) for full setup instructions.
:::

:::{tab-item} Local CLI
Install and run locally:

```bash
pip install git+https://github.com/QuantEcon/action-style-guide.git
export ANTHROPIC_API_KEY='your-key-here'
qestyle lecture.md --categories writing
```

See [CLI Guide](user/cli.md) for full usage documentation.
:::

::::

## Documentation

::::{grid} 1 2 2 2

:::{card} User Guide
:link: user/getting-started.md

Setup instructions, configuration options, rule reference, and CLI usage for lecture authors and repository admins.
:::

:::{card} Developer Guide
:link: developer/architecture.md

Architecture, contributing guidelines, testing, and roadmap for contributors.
:::

::::
