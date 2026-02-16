---
title: Architecture
---

# Architecture

Technical documentation for developers working on the QuantEcon Style Guide Checker.

## System Overview

```
┌─────────────────────────────────────────────────────┐
│                GitHub Actions Workflow                │
│  (Triggered by issue comment or schedule)            │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                      action.yml                      │
│  Sets up Python, installs deps, invokes action.py    │
└──────────────────────────┬──────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌──────────────────────┐   ┌──────────────────────────┐
│   github_handler.py   │   │       reviewer.py         │
│ GitHub API, PR ops    │   │ LLM coordination,         │
│ Comment parsing       │   │ Sequential rule processing │
│ Branch/commit         │   │ Response parsing           │
└──────────────────────┘   └────────────┬─────────────┘
                                        │
                    ┌───────────────────┼──────────────┐
                    ▼                   ▼              ▼
          ┌──────────────┐   ┌──────────────┐  ┌─────────────┐
          │prompt_loader  │   │ fix_applier   │  │Anthropic API│
          │Load prompts   │   │Apply fixes    │  │(Claude)     │
          │Load rules     │   │Validate       │  └─────────────┘
          └──────┬───────┘   └──────────────┘
          ┌──────┴───────┐
          ▼              ▼
    ┌──────────┐  ┌──────────┐
    │prompts/  │  │ rules/   │
    │(8 files) │  │(8 files) │
    └──────────┘  └──────────┘
```

## Two Entry Points, One Engine

- **`action.py`**: GitHub Action entry point. Reads files via GitHub API, creates PRs with fixes.
- **`cli.py`** (`qestyle` command): Local CLI for authors. Reads files from disk, writes report to file.
- Both use the **same `StyleReviewer`**, prompts, rules, and `fix_applier` — results are identical.

## Core Components

### Entry Point (`action.py`)

The main orchestrator:
- Parses CLI arguments from GitHub Actions
- Initializes `GitHubHandler` and `StyleReviewer`
- Routes to single lecture or bulk review modes
- Manages GitHub outputs for workflow integration

### GitHub Handler (`github_handler.py`)

Manages all GitHub API interactions using PyGithub:

- Parse trigger comments (`@qe-style-checker lecture_name [categories]`)
- Find and read lecture files from repository
- Create branches, commit fixes
- Create pull requests with formatted descriptions
- Add detailed comments to PRs (applied fixes, style suggestions)

### Style Reviewer (`reviewer.py`)

The LLM coordination layer. Key architectural decisions:

1. **Single-Rule Processing**: Each rule checked individually via separate LLM calls. Guarantees comprehensive coverage — LLM doesn't skip rules. Fixes applied after each rule, so subsequent rules see updated content.

2. **Sequential Category Processing**: Categories processed one at a time (Writing → Math → Code → JAX → Figures → References → Links → Admonitions). Each category's fixes applied before next category starts.

3. **Rule Type Separation**:
   - `rule`: Mechanical fixes, automatically applied
   - `style`: Subjective suggestions, collected for human review
   - `migrate`: Legacy pattern updates, treated as suggestions

Key classes:
- `AnthropicProvider` — Claude API wrapper with extended thinking and streaming fallback
- `StyleReviewer` — Main review orchestrator

### Prompt Loader (`prompt_loader.py`)

Loads and combines category-specific prompts and rules:

```
[Category Prompt]  +  [Style Guide Rules]  +  [Lecture Content]  →  LLM
```

The prompt is rule-agnostic — all 8 category prompts are identical. Scope and analysis context come from the rule definitions themselves. This prevents signal dilution from category-specific instructions.

### Fix Applier (`fix_applier.py`)

Programmatically applies fixes to content:

- ~50% reduction in output tokens (LLM doesn't generate full corrected content)
- More reliable than LLM-generated corrections
- Validates fix quality before applying (identical text detection, missing fields)

## Data Flow — Single Lecture Review

```
1. Trigger: @qe-style-checker aiyagari writing,math
                    │
2. Parse Comment    ▼
   lecture = "aiyagari", categories = ["writing", "math"]
                    │
3. Load Content     ▼
   content = github_handler.get_lecture_content("lectures/aiyagari.md")
                    │
4. For each category:
   │  For each rule in category (in priority order):
   │     i.   Create focused prompt (prompt + single rule + content)
   │     ii.  Send to Claude API (extended thinking)
   │     iii. Parse response for violations
   │     iv.  If rule.type == 'rule': apply_fixes(content, violations)
   │     v.   Update content for next rule
   │
5. Create PR         ▼
   - Branch: style-guide/aiyagari-20251208-143022
   - Commit corrected content
   - PR with summary + comments
```

## Rule Processing Order

Rules are processed in a defined order within each category. The principle: **mechanical → structural → stylistic → creative**.

```python
RULE_EVALUATION_ORDER = {
    'writing': [
        'qe-writing-008',  # Whitespace formatting (mechanical)
        'qe-writing-001',  # Paragraph structure (structural)
        'qe-writing-004',  # Capitalization (mechanical)
        'qe-writing-006',  # Title capitalization (mechanical)
        'qe-writing-005',  # Bold/italic formatting (mechanical)
        'qe-writing-002',  # Clarity and conciseness (stylistic)
        'qe-writing-003',  # Logical flow (creative)
        'qe-writing-007',  # Visual elements (creative)
    ],
}
```

This ensures simple fixes don't get confused by complex content, later rules see cleaner content, and subjective rules are evaluated last.

## LLM Integration

### Model Configuration

| Setting | Value |
|---------|-------|
| Provider | Anthropic |
| Model | Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`) |
| Extended Thinking | Enabled, 10,000 token budget |
| Temperature | 1.0 (required for extended thinking) |
| Max Tokens | 64,000 output tokens |
| Streaming | Automatic fallback for large requests |

### Extended Thinking

Without extended thinking, the model commits tokens before finishing analysis — it reports a violation, then realizes the text is compliant, producing ~43% false positive rate. Extended thinking lets the model reason internally before any output, reducing false positives to **0%**.

See [Extended Thinking Results](extended-thinking.md) for experiment data.

### Prompt Structure

```
[Minimal prompt]          ← ~40 lines, rule-agnostic
- Identity: "You are a style checker..."
- Task: "Find violations, verify, report confirmed only"
- Response format template

[Style Guide Rule]        ← One rule at a time
- Rule definition with scope, criteria, examples

[Lecture Content]          ← Full lecture markdown
```

### Response Format

LLM responses use structured markdown:

````markdown
# Review Results

## Summary
[Brief finding summary]

## Issues Found
[NUMBER]

## Violations

### Violation 1: qe-writing-001 - Rule Title
**Severity:** error
**Location:** Line X / Section "Name"
**Description:** [Why this violates the rule]
**Current text:**
~~~markdown
[Exact problematic text]
~~~
**Suggested fix:**
~~~markdown
[Corrected text]
~~~
**Explanation:** [Reasoning]
````

## Cost Estimation

| Scope | Estimated Cost |
|-------|---------------|
| Single category | $0.01–0.05 |
| All 8 categories | $0.08–0.40 |

Depends on lecture length and violations found.

## Repository Structure

```
action-style-guide/
├── action.yml                 # GitHub Action definition
├── style_checker/             # Main package
│   ├── __init__.py            # Version (__version__)
│   ├── cli.py                 # Local CLI entry point (qestyle)
│   ├── action.py              # GitHub Action entry point
│   ├── reviewer.py            # LLM review engine (shared)
│   ├── fix_applier.py         # Apply fixes to files (shared)
│   ├── github_handler.py      # GitHub API (action only)
│   ├── prompt_loader.py       # Load prompts + rules (shared)
│   ├── prompts/               # Minimal rule-agnostic prompts
│   └── rules/                 # Category-specific rule definitions
├── tests/                     # Test suite
├── docs/                      # Documentation (this site)
└── examples/                  # Example workflows
```
