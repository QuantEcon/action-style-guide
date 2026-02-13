# Architecture

> Technical documentation for developers working on the QuantEcon Style Guide Checker action.

## Overview

The QuantEcon Style Guide Checker is a GitHub Action that performs AI-powered style guide compliance checking for QuantEcon lecture materials. It uses Claude (Anthropic) to review MyST Markdown lecture files against defined style rules and can automatically create PRs with fixes.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         GitHub Actions Workflow                          │
│  (Triggered by issue comment @qe-style-checker or scheduled)            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              action.yml                                  │
│  - Sets up Python environment                                           │
│  - Installs dependencies                                                │
│  - Invokes style_checker/main.py                                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            main.py                                       │
│  - Entry point and CLI argument parsing                                 │
│  - Orchestrates single or bulk lecture reviews                          │
│  - Coordinates GitHub operations and LLM reviews                        │
└─────────────────────────────────────────────────────────────────────────┘
                    │                               │
                    ▼                               ▼
┌─────────────────────────────┐     ┌─────────────────────────────────────┐
│      github_handler.py       │     │           reviewer.py                │
│  - GitHub API interactions   │     │  - LLM-based style checking         │
│  - PR creation/management    │     │  - Sequential rule processing       │
│  - Comment parsing           │     │  - Response parsing                 │
│  - Branch operations         │     │  - Fix application coordination     │
└─────────────────────────────┘     └─────────────────────────────────────┘
                                                    │
                    ┌───────────────────────────────┼───────────────────┐
                    ▼                               ▼                   ▼
        ┌─────────────────────┐       ┌─────────────────┐    ┌─────────────────┐
        │   prompt_loader.py   │       │  fix_applier.py │    │  Anthropic API  │
        │  - Load prompts      │       │  - Apply fixes  │    │  (Claude)       │
        │  - Load rules        │       │  - Validate     │    └─────────────────┘
        │  - Combine for LLM   │       │    quality      │
        └─────────────────────┘       └─────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   prompts/*.md   │    │   rules/*.md    │
│  (8 categories)  │    │  (8 categories) │
└─────────────────┘    └─────────────────┘
```

## Core Components

### 1. Entry Point (`main.py`)

The main orchestrator that:
- Parses CLI arguments from GitHub Actions
- Initializes `GitHubHandler` and `StyleReviewer`
- Routes to single lecture or bulk review modes
- Manages GitHub outputs for workflow integration

**Key Functions:**
- `review_single_lecture()` - Reviews one lecture, creates PR
- `review_bulk_lectures()` - Reviews all lectures, creates single PR
- `main()` - CLI entry point

### 2. GitHub Handler (`github_handler.py`)

Manages all GitHub API interactions using PyGithub:

**Responsibilities:**
- Parse trigger comments (`@qe-style-checker lecture_name [categories]`)
- Find and read lecture files from repository
- Create branches for changes
- Commit fixes to branches
- Create pull requests with formatted descriptions
- Add detailed comments to PRs (applied fixes, style suggestions)

**Key Methods:**
- `extract_lecture_from_comment()` - Parse trigger syntax
- `find_lecture_file()` - Locate lecture in repository
- `create_branch()`, `commit_changes()` - Git operations
- `create_pull_request()` - PR creation with labels
- `format_pr_body()`, `format_applied_fixes_report()`, `format_style_suggestions_report()` - Report generation

### 3. Style Reviewer (`reviewer.py`)

The LLM coordination layer that implements style checking:

**Architecture Decisions:**

1. **Single-Rule Processing**: Each rule is checked individually via separate LLM calls
   - Guarantees comprehensive coverage (LLM doesn't skip rules)
   - Fixes applied after each rule, so subsequent rules see updated content
   - More API calls but more reliable results

2. **Sequential Category Processing**: Categories processed one at a time
   - Writing → Math → Code → JAX → Figures → References → Links → Admonitions
   - Each category's fixes applied before next category starts
   - Ensures all fixes applied without conflicts

3. **Rule Type Separation**:
   - `rule` type: Mechanical fixes, automatically applied
   - `style` type: Subjective suggestions, collected for human review
   - `migrate` type: Legacy pattern updates (JAX/code), treated as suggestions

**Key Classes:**
- `AnthropicProvider` - Claude API wrapper with extended thinking and streaming fallback
- `StyleReviewer` - Main review orchestrator

**Key Methods:**
- `review_lecture_single_rule()` - Rule-by-rule evaluation
- `review_lecture_smart()` - Full sequential category processing
- `extract_individual_rules()` - Parse rules from markdown files
- `parse_markdown_response()` - Parse LLM output into structured data

### 4. Prompt Loader (`prompt_loader.py`)

Loads and combines category-specific prompts and rules:

**File Structure:**
```
style_checker/
├── prompts/           # Minimal rule-agnostic prompt (~40 lines, identical for all categories)
│   ├── writing-prompt.md
│   ├── math-prompt.md
│   └── ...
│   └── v0.6.1/        # Archived previous prompts
└── rules/             # Rule definitions (~120-235 lines each)
    ├── writing-rules.md
    ├── math-rules.md
    └── ...
```

The prompt is rule-agnostic — all 8 category prompts are identical. Scope and analysis context come from the rule definitions themselves. This prevents signal dilution from category-specific instructions.

**Combination Pattern:**
```
[Category Prompt] + [Style Guide Rules] + [Lecture Content] → LLM
```

### 5. Fix Applier (`fix_applier.py`)

Programmatically applies fixes to content:

**Why Programmatic Fixes?**
- ~50% reduction in output tokens (LLM doesn't generate full corrected content)
- More reliable than LLM-generated corrections
- Validates fix quality before applying

**Key Functions:**
- `apply_fixes()` - Apply fixes to content, returns (corrected, warnings)
- `validate_fix_quality()` - Check for common issues (identical text, missing fields)

## Data Flow

### Single Lecture Review

```
1. Trigger: @qe-style-checker aiyagari writing,math
                    │
2. Parse Comment    ▼
   lecture_name = "aiyagari"
   categories = ["writing", "math"]
                    │
3. Load Content     ▼
   content = github_handler.get_lecture_content("lectures/aiyagari.md")
                    │
4. For each category:
   │
   │  a. For each rule in category (in priority order):
   │     │
   │     │  i.  Create focused prompt (prompt + single rule + content)
   │     │  ii. Send to Claude API
   │     │  iii. Parse response for violations
   │     │  iv.  If rule.type == 'rule': apply_fixes(content, violations)
   │     │  v.   Update content for next rule
   │     │
   │     └── Next rule
   │
   └── Next category
                    │
5. Create PR        ▼
   - Create branch: style-guide/aiyagari-20251208-143022
   - Commit corrected content
   - Create PR with summary
   - Add comment: Applied fixes (collapsible)
   - Add comment: Style suggestions (visible)
```

### Rule Processing Order

Rules are processed in a defined order within each category. For writing:

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

**Rationale:** Mechanical fixes first → Structural → Stylistic → Creative

This ensures:
- Simple fixes don't get confused by complex content
- Later rules see cleaner content
- Subjective rules evaluated last (after objective corrections)

## Rule System

### Rule Structure

Each rule in `rules/*.md` follows this format:

```markdown
### Rule: qe-writing-001
**Type:** rule
**Title:** Use one sentence per paragraph

**Description:**
[Detailed explanation of the rule]

**Check for:**
[Specific patterns to identify]

**Examples:**
[Good and bad examples with explanations]
```

### Rule Types

| Type | Behavior | Application |
|------|----------|-------------|
| `rule` | Mechanical, objective | Automatically applied to content |
| `style` | Subjective, advisory | Collected as suggestions for human review |
| `migrate` | Legacy pattern updates | Suggestions for code modernization (JAX/code only) |

### Categories

| Category | Focus Area | Rules |
|----------|------------|-------|
| `writing` | Prose, paragraphs, clarity | 8 rules |
| `math` | LaTeX notation, equations | 9 rules |
| `code` | Python style, patterns | 6 rules |
| `jax` | JAX-specific patterns | 5 rules |
| `figures` | Matplotlib, captions | 10 rules |
| `references` | Citations | 1 rule |
| `links` | Internal/external links | 2 rules |
| `admonitions` | Notes, warnings | 5 rules |

## LLM Integration

### Model

- **Provider:** Anthropic
- **Model:** Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
- **Extended Thinking:** Enabled with 10,000 token budget
- **Temperature:** 1.0 (required for extended thinking)
- **Max Tokens:** 64,000 output tokens
- **Streaming:** Automatic fallback for large requests (>10 min)

### Why Extended Thinking?

Without extended thinking, the model would commit to writing a violation block before finishing its analysis, then realize the text was actually compliant. This caused ~43% false positive rate. Extended thinking lets the model reason internally before any output, reducing false positives to 0%.

See [testing-extended-thinking.md](testing-extended-thinking.md) for experiment results.

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

```markdown
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
```

## GitHub Integration

### Trigger Syntax

```
@qe-style-checker <lecture_name> [category1,category2,...]
```

**Examples:**
- `@qe-style-checker aiyagari` - All categories
- `@qe-style-checker aiyagari writing,math` - Specific categories
- `@qe-style-checker lectures/aiyagari.md writing` - With path

### PR Structure

Created PRs include:
1. **PR Description:** Summary statistics, changes by category, issues by rule
2. **Comment 1 (Collapsible):** Applied fixes report - all automatic fixes with before/after
3. **Comment 2 (Visible):** Style suggestions - subjective improvements requiring human review

### Labels

PRs are automatically labeled:
- `automated` - Machine-generated
- `style-guide` - Style guide related
- `review` - Ready for review

## Configuration

### Action Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `mode` | Yes | - | `single` or `bulk` |
| `lectures-path` | No | `lectures/` | Path to lectures directory |
| `anthropic-api-key` | Yes | - | Anthropic API key |
| `github-token` | Yes | - | GitHub token for PR operations |
| `comment-body` | No | - | Trigger comment (for single mode) |
| `llm-model` | No | `claude-sonnet-4-5-20250929` | Claude model to use |
| `rule-categories` | No | All | Comma-separated categories |
| `create-pr` | No | `true` | Whether to create PR |
| `pr-branch-prefix` | No | `style-guide` | Branch name prefix |

### Environment Variables

- `ANTHROPIC_API_KEY` - Claude API access
- `GITHUB_TOKEN` - GitHub API access

## Performance Considerations

### Token Optimization

1. **Single-rule prompts:** ~5-12K tokens per call (vs 40K+ for all rules)
2. **No corrected content in response:** ~50% output token reduction
3. **Programmatic fix application:** Reliable and cheap

### Cost Estimation

- Single category: ~$0.01-0.05
- All categories (8): ~$0.08-0.40
- Depends on lecture length and violations found

### API Handling

- Automatic streaming for requests >10 minutes
- Retries on transient failures
- Graceful degradation on partial failures

## Testing

### Test Structure

```
tests/
├── test_fix_applier.py       # Fix application and validation tests
├── test_github_handler.py    # GitHub integration tests
├── test_llm_integration.py   # Real LLM API tests (marked @integration)
├── test_markdown_parser.py   # Response parsing tests
├── test_parsing.py           # Comment parsing tests
├── test_prompt_loader.py     # Prompt loading tests
└── test_reviewer.py          # Rule extraction and ordering tests
```

### Running Tests

```bash
# All tests (excludes integration)
pytest

# Include integration tests (requires API key, costs money)
export ANTHROPIC_API_KEY="your-key"
pytest -m integration

# With coverage
pytest --cov=style_checker --cov-report=html
```

## Development Workflow

### Adding a New Rule

1. Add rule to appropriate `rules/*.md` file
2. Follow the rule template format
3. Update corresponding `prompts/*.md` if needed
4. Test with real lecture files
5. No code changes needed (LLM reads rules directly)

### Adding a New Category

1. Create `prompts/category-prompt.md`
2. Create `rules/category-rules.md`
3. Add category to `VALID_CATEGORIES` in `github_handler.py` and `prompt_loader.py`
4. Add to category list in `review_lecture_smart()`
5. Test end-to-end

### Modifying Rule Evaluation Order

Update `RULE_EVALUATION_ORDER` in `reviewer.py`:

```python
RULE_EVALUATION_ORDER = {
    'writing': [
        'qe-writing-008',  # First
        'qe-writing-001',  # Second
        # ...
    ],
}
```

## Version Management

- Version in `style_checker/__init__.py`
- Prompt versions in comment at top of each prompt file
- CHANGELOG.md follows Keep a Changelog format

## Future Considerations

See [FUTURE-ENHANCEMENTS.md](./FUTURE-ENHANCEMENTS.md) for planned improvements.
