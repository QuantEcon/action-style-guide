# QuantEcon Style Guide Checker

[![Version](https://img.shields.io/badge/version-0.5.1-blue.svg)](https://github.com/QuantEcon/action-style-guide/releases)
[![Status](https://img.shields.io/badge/status-active-green.svg)](https://github.com/QuantEcon/action-style-guide)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> 🚀 **Version 0.5.1**: Production testing infrastructure, PR labels, @qe-style-checker syntax

A GitHub Action for automated style guide compliance checking of QuantEcon lecture materials using AI-powered analysis.

## Overview

This action automatically reviews MyST Markdown lecture files against the [QuantEcon Style Guide](https://manual.quantecon.org), ensuring consistency across all lecture series. It uses category-specific focused prompts to check 49 style rules covering writing, mathematics, code, JAX patterns, figures, and more.

## Features

- 🤖 **AI-Powered Review**: Uses Claude Sonnet 4.5 for intelligent, nuanced style analysis
- 🏷️ **Category-Based Reviews**: Target specific areas (writing, math, code, jax, figures, references, links, admonitions)
- 📝 **Focused Prompts**: Hand-crafted prompts + detailed rules = better quality, lower cost
- 🎯 **Flexible Targeting**: Check all categories or focus on specific ones
- 📅 **Scheduled Reviews**: Weekly automated reviews or on-demand via comments
- 🔄 **Automated Fixes**: Applies fixes programmatically for reliable results
- 🏷️ **PR Management**: Creates labeled PRs with detailed explanations

## Quick Start

### Trigger a Review

Comment on any issue in your lecture repository:

```
@qe-style-checker lecture_name
```

With specific categories:

```
@qe-style-checker lecture_name writing,math
```

**Available Categories:**
- `writing` - Writing style and formatting
- `math` - Mathematics notation and LaTeX
- `code` - Python code style
- `jax` - JAX-specific patterns
- `figures` - Figure formatting and captions
- `references` - Citations and bibliography
- `links` - Hyperlinks and cross-references  
- `admonitions` - Note/warning/tip blocks

If no categories specified, checks all categories sequentially (one at a time, feeding updated content between categories).

## Installation

### 1. Add Workflow to Your Lecture Repository

### 1. Create Workflow File

Create `.github/workflows/style-guide-comment.yml`:

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
      - uses: QuantEcon/action-style-guide@v0.5
        with:
          mode: 'single'
          lectures-path: 'lectures/'
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
          comment-body: ${{ github.event.comment.body || github.event.issue.body }}
```

### 2. Configure Secrets

Add to your repository settings → Secrets and variables → Actions:

- `ANTHROPIC_API_KEY`: Your Anthropic API key for Claude Sonnet 4.5
- `GITHUB_TOKEN`: Automatically provided (or use PAT for extended permissions)

### 3. Configure Labels

Ensure these labels exist in your repository:
- `automated`
- `style-guide`
- `review`

## Configuration Options

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `mode` | Review mode: `single` or `bulk` | Yes | - |
| `lectures-path` | Path to lectures directory | No | `lectures/` |
| `anthropic-api-key` | Anthropic API key for Claude Sonnet 4.5 | Yes | - |
| `github-token` | GitHub token for PR creation | Yes | - |
| `comment-body` | Issue comment body (for single mode) | No | - |
| `llm-model` | Specific Claude model to use | No | `claude-sonnet-4-5-20250929` |
| `rule-categories` | Comma-separated categories to check | No | All categories |
| `create-pr` | Whether to create PR with fixes | No | `true` |

### LLM Model

The action uses **Claude Sonnet 4.5** (`claude-sonnet-4-5-20250929`) by default, which provides:
- Excellent comprehension for nuanced style rules
- Strong markdown and code understanding
- Reliable structured output for suggestions and fixes

The focused prompts architecture (85-line instructions + 120-235 line rules) ensures efficient token usage while maintaining comprehensive analysis.

## Rule Types

The style guide uses a three-tier type system:

### Type: `rule` (Actionable) ✅
Rules that are clearly actionable and will be automatically applied by the action:
- **Writing**: One sentence per paragraph, capitalization, bold/italic usage
- **Mathematics**: Transpose notation (`\top`), matrix brackets, sequence notation
- **Code**: Unicode Greek letters, package installation placement
- **Figures**: Caption formatting, figure naming, axis labels, line width
- **References**: Citation style (`{cite}` vs `{cite:t}`), cross-references
- **Links**: Internal vs cross-series linking syntax
- **Admonitions**: Exercise/solution syntax, nested directive tick counts

### Type: `style` (Advisory) 💡
Subjective guidelines that require human judgment:
- Writing clarity and conciseness
- Logical flow between sections
- Visual element opportunities
- Figure size decisions

### Type: `migrate` (Code Modernization) 🔄
Legacy patterns that should be updated (JAX and code categories only):
- `tic/toc` → `quantecon.Timer()` context manager
- `%timeit` → `quantecon.timeit()` function
- NumPy in-place operations → JAX functional updates
- Implicit random state → explicit JAX PRNG key management

**`rule` types are automatically applied. `style` and `migrate` types are reported as suggestions.**

## Architecture

The action uses a **focused prompts architecture** with **sequential category processing**:

1. **Prompts** (`style_checker/prompts/*.md`): Concise instructions (~85 lines each) for LLM analysis
2. **Rules** (`style_checker/rules/*.md`): Detailed specifications (~120-235 lines each) with examples
3. **Categories**: 8 focused areas (writing, math, code, jax, figures, references, links, admonitions)
4. **Sequential Processing**: Processes categories one at a time, feeding the updated document from each category into the next

Each category combines its prompt (how to check) with its rules (what to check) for targeted, efficient analysis.

### How Sequential Processing Works

The action processes categories in order, ensuring all fixes are applied without conflicts:

1. **Category 1 (e.g., Writing)**: Reviews original document → finds violations → applies fixes → **updated document**
2. **Category 2 (e.g., Math)**: Reviews **updated document** → finds violations → applies fixes → **updated document**
3. **Category 3 (e.g., Code)**: Reviews **updated document** → finds violations → applies fixes → **updated document**
4. Continue for all 8 categories...

This approach matches `tool-style-checker` and ensures:
- ✅ All fixes are applied without conflicts
- ✅ Later categories see changes made by earlier categories
- ✅ More coherent and complete final output
- ✅ No skipped fixes due to overlapping changes

**Trade-off**: Sequential processing is slower than parallel (8 sequential API calls vs 8 parallel), but produces more reliable results.

## Example Review Output

When a lecture is reviewed, the action will:

1. **Analyze the file** against all applicable categories
2. **Generate specific suggestions** with detailed explanations
3. **Create a PR** with changes organized by category
4. **Include detailed commit messages** explaining each fix

Example PR description:

```markdown
## Style Guide Review: aiyagari.md

This PR addresses style guide compliance issues found in the Aiyagari model lecture.

### Changes Summary

#### Writing
- Split multi-sentence paragraphs
- Fixed capitalization in section headings

#### Mathematics
- Changed A' to A⊤ for transpose notation
- Converted matrices to square brackets

#### Code
- Added Unicode Greek letters
- Replaced manual timing with qe.Timer()

See commits for detailed explanations of each change.
```

## Development

### Local CLI Tool

For local testing without GitHub infrastructure, use the standalone CLI in `tool-style-checker/`:

```bash
cd tool-style-checker

# Install requirements
pip install anthropic
export ANTHROPIC_API_KEY='your-api-key'

# Check a lecture against specific categories
python style_checker.py lecture.md --focus writing
python style_checker.py lecture.md --focus writing,math,code

# Output files created:
# - lecture-suggestions.md (detailed review)
# - lecture-corrected.md (corrected version)
```

The CLI uses the **same prompts and rules** as the GitHub Action (loaded from `style_checker/prompts/` and `style_checker/rules/`), ensuring local testing matches production behavior.

See [tool-style-checker/README.md](tool-style-checker/README.md) for full documentation.

### Testing

#### Unit Tests

Run the test suite locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_github_handler.py -v
```

See [docs/testing-quick-reference.md](docs/testing-quick-reference.md) for more testing options.

#### GitHub Integration Testing

**Test Repository**: [test-action-style-guide](https://github.com/QuantEcon/test-action-style-guide)
- Dedicated test repository with intentional violations
- Safe environment for testing new features
- Automated regression tests

**Real-World Testing**: [lecture-python-advanced.myst](https://github.com/QuantEcon/lecture-python-advanced.myst)
- Enabled for real-world testing and validation
- [Testing issue #261](https://github.com/QuantEcon/lecture-python-advanced.myst/issues/261)
- Comment `@qe-style-checker lecture_name` to test on actual lectures

See [docs/production-testing.md](docs/production-testing.md) for complete testing guide.

### Project Structure

```
action-style-guide/
├── action.yml                 # GitHub Action definition
├── style_checker/            # Main package
│   ├── main.py              # Entry point
│   ├── parser_md.py         # Comment parsing
│   ├── reviewer.py          # LLM review logic
│   ├── github_handler.py    # PR/issue management
│   ├── fix_applier.py       # Apply fixes to files
│   ├── prompt_loader.py     # Load prompts + rules
│   ├── prompts/             # Category-specific prompts
│   └── rules/               # Category-specific rules
├── tests/                    # Test suite
├── examples/                 # Example workflows
└── docs/                     # Documentation
```

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- 📚 [QuantEcon Manual](https://manual.quantecon.org)
- 🐛 [Report Issues](https://github.com/QuantEcon/action-style-guide/issues)
- 💬 [Discussions](https://github.com/QuantEcon/action-style-guide/discussions)
