# QuantEcon Style Guide Checker

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/QuantEcon/action-style-guide/releases)
[![Status](https://img.shields.io/badge/status-development-orange.svg)](https://github.com/QuantEcon/action-style-guide)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> ⚠️ **Development Release**: This is version 0.1.0 - currently in testing phase. Please report any issues or feedback!

A GitHub Action and bot for automated style guide compliance checking of QuantEcon lecture materials.

## Overview

This action automatically reviews MyST Markdown lecture files against the comprehensive [QuantEcon Style Guide](https://manual.quantecon.org), ensuring consistency across all lecture series. It uses AI-powered analysis to check 50+ style rules covering writing, formatting, mathematics, code, JAX patterns, and more.

## Features

- 🤖 **AI-Powered Review**: Intelligent checking using LLM to understand context and suggest improvements
- 📝 **Comprehensive Rule Coverage**: Checks all style guide rules from writing style to technical requirements
- 🎯 **Single Lecture Reviews**: Trigger reviews via issue comments for focused, manageable PRs
- 📅 **Scheduled Bulk Reviews**: Weekly automated reviews of all lectures with individual commits per file
- 🔄 **Updatable Rules**: Style guide rules stored in Markdown format, easy to update and extend
- 📊 **Category System**: Rules organized by category (`rule`, `style`, `migrate`) for targeted reviews
- 🎯 **Actionable Rules**: Automatically applies only `rule` category fixes (clearly actionable improvements)
- 🏷️ **Automated PR Management**: Creates properly labeled PRs with detailed change descriptions

## Usage

### Trigger Single Lecture Review

Comment on any issue in your lecture repository:

```
@quantecon-style-guide aiyagari
```

or

```
@quantecon-style-guide lectures/aiyagari.md
```

This will:
1. Review the specified lecture against all style guide rules
2. Open a PR titled `[aiyagari] Style guide review` 
3. Apply labels: `automated`, `style-guide`, `review`
4. Include detailed explanations of all suggested changes

### Scheduled Bulk Reviews

Configure weekly reviews in your `.github/workflows/style-guide.yml`:

```yaml
name: Weekly Style Guide Review
on:
  schedule:
    - cron: '0 0 * * 0'  # Every Sunday at midnight
  workflow_dispatch:  # Manual trigger

jobs:
  style-review:
    runs-on: ubuntu-latest
    steps:
      - uses: QuantEcon/action-style-guide@v0.2
        with:
          mode: 'bulk'
          lectures-path: 'lectures/'
          style-guide-url: 'https://raw.githubusercontent.com/QuantEcon/action-style-guide/main/style-guide-database.md'
          llm-provider: 'claude'
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Installation

### 1. Add Workflow to Your Lecture Repository

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
    if: contains(github.event.comment.body, '@quantecon-style-guide') || contains(github.event.issue.body, '@quantecon-style-guide')
    runs-on: ubuntu-latest
    steps:
      - uses: QuantEcon/action-style-guide@v0.2
        with:
          mode: 'single'
          lectures-path: 'lectures/'
          style-guide-url: 'https://raw.githubusercontent.com/QuantEcon/action-style-guide/main/style-guide-database.md'
          llm-provider: 'claude'  # Default: best results
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
          comment-body: ${{ github.event.comment.body || github.event.issue.body }}
```

### 2. Configure Secrets

Add to your repository settings → Secrets and variables → Actions:

- `ANTHROPIC_API_KEY`: Your Anthropic API key for Claude (recommended)
- Or `OPENAI_API_KEY`: Your OpenAI API key for GPT-4
- Or `GOOGLE_API_KEY`: Your Google API key for Gemini
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
| `style-guide-url` | URL or path to style-guide-database.md | No | Built-in rules |
| `openai-api-key` | OpenAI API key for GPT-4 | No | - |
| `anthropic-api-key` | Anthropic API key for Claude | No | - |
| `google-api-key` | Google API key for Gemini | No | - |
| `github-token` | GitHub token for PR creation | Yes | - |
| `comment-body` | Issue comment body (for single mode) | No | - |
| `llm-provider` | LLM provider: `openai`, `claude`, `gemini` | No | `claude` |
| `llm-model` | Specific model name | No | Provider default |
| `rule-categories` | Comma-separated categories to check | No | All categories |
| `create-pr` | Whether to create PR with fixes | No | `true` |

### LLM Model Options

The action supports three LLM providers with different models and capabilities:

#### Claude (Anthropic) - Recommended ⭐
- **Default Model**: `claude-sonnet-4-5-20250929` (64,000 max output tokens) - **Latest & Best!**
  - Best model for complex agents and coding
  - Highest intelligence across most tasks
  - 8x more output capacity than previous Sonnet 3.5
- **Alternative Models**:
  - `claude-sonnet-4-20250514` (64,000 max output tokens)
  - `claude-opus-4-1-20250805` (32,000 max output tokens) - Exceptional for specialized tasks
  - `claude-opus-4-20250514` (32,000 max output tokens)
  - `claude-3-7-sonnet-20250219` (64,000 max output tokens with beta header)
  - `claude-3-5-haiku-20241022` (8,192 max output tokens) - Fastest
- **Best For**: Comprehensive style reviews, nuanced language analysis, long lectures
- **Note**: Claude Sonnet 4.5 is the most capable model with 64K output tokens

#### OpenAI (GPT-4)
- **Default Model**: `gpt-4` (8,192 max output tokens)
- **Alternative Models**:
  - `gpt-4-turbo` (4,096 max output tokens)
  - `gpt-4o` (16,384 max output tokens)
- **Best For**: Structured JSON responses, code analysis

#### Google (Gemini)
- **Default Model**: `gemini-1.5-pro` (8,192 max output tokens)
- **Alternative Models**:
  - `gemini-1.5-flash` (8,192 max output tokens, faster)
- **Best For**: Cost-effective reviews, multi-modal content

**Important**: The action now uses semantic grouping to intelligently organize rules by topic (Writing, Math, Code, etc.), which naturally handles token limits by processing related rules together. The default configuration works well for all models.

If you need to focus on specific areas, use the `rule-categories` parameter to check only certain rule categories.

## Rule Categories

The style guide uses a three-tier category system:

### Category: `rule` (Actionable) ✅
Rules that are clearly actionable and will be automatically applied by the action:
- **Writing**: One sentence per paragraph, capitalization, bold/italic usage
- **Mathematics**: Transpose notation (`\top`), matrix brackets, sequence notation
- **Code**: Unicode Greek letters, package installation placement, `quantecon.Timer()` usage
- **Figures**: Caption formatting, figure naming, axis labels, line width
- **References**: Citation style (`{cite}` vs `{cite:t}`), cross-references
- **Links**: Internal vs cross-series linking syntax
- **Admonitions**: Exercise/solution syntax, nested directive tick counts

**These rules are automatically checked and fixed by the action.**

### Category: `style` (Advisory) 💡
Guidelines that may require human judgment or context:
- Writing clarity and conciseness
- Logical flow and narrative structure  
- Figure placement and visualization choices
- Mathematical notation simplicity
- Code readability patterns

**These rules are tracked but not automatically actioned. Future versions will add comment-based suggestions.**

### Category: `migrate` (Code Transformation) 🔄
Legacy code patterns suitable for automated transformation tools:
- `tic/toc` → `quantecon.Timer()` migration
- `%timeit` → `quantecon.timeit()` migration
- NumPy → JAX functional patterns
- In-place operations → JAX immutable updates

**These rules are for specialized migration tools and are not actioned by the main checker.**

## Style Guide Database

The complete style guide is maintained in `style-guide-database.md` with:
- **48 rules** organized into **8 groups**
- **31 actionable rules** (category=`rule`)
- **13 advisory guidelines** (category=`style`)
- **4 migration patterns** (category=`migrate`)

Each rule includes:
- Unique rule code (e.g., `qe-writing-001`, `qe-math-004`)
- Category classification
- Detailed description and rationale
- Examples showing correct/incorrect usage
- Implementation notes for automated checking

For the complete database, see: [style-guide-database.md](style-guide-database.md)

## Example Review Output

When a lecture is reviewed, the action will:

1. **Analyze the file** against all applicable rules
2. **Generate specific suggestions** with rule references
3. **Create a PR** with changes organized by category
4. **Include detailed commit messages** explaining each fix

Example PR description:

```markdown
## Style Guide Review: aiyagari.md

This PR addresses style guide compliance issues found in the Aiyagari model lecture.

### Changes Summary

#### Writing Rules (5 issues)
- Split multi-sentence paragraphs per qe-writing-002
- Fixed capitalization in section headings per qe-title-002

#### Mathematics Rules (3 issues)
- Changed A' to A⊤ for transpose notation per qe-math-001
- Converted matrices to square brackets per qe-math-003

#### Code Rules (2 issues)
- Added Unicode Greek letters per qe-code-004
- Replaced manual timing with qe.Timer() per qe-code-006

### Rule References

Each change references the specific style guide rule:
- qe-writing-002: One-sentence paragraphs only
- qe-title-002: Capitalize only first word in headings
- qe-math-001: Use \top for transpose
...
```

## Updating Style Guide Rules

To update the style guide rules:

1. Edit `style-guide-database.md` in this repository
2. Commit and push changes
3. All future reviews will use the updated rules automatically

## Development

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run single lecture check
python -m style_checker.cli --mode single --lecture lectures/aiyagari.md

# Run bulk check
python -m style_checker.cli --mode bulk --lectures-dir lectures/
```

### Project Structure

```
```
action-style-guide/
├── action.yml                 # GitHub Action definition
├── style-guide-database.md   # Style guide rules database
├── style_checker/            # Main package
│   ├── __init__.py
│   ├── parser_md.py         # Markdown rule parser
│   ├── reviewer.py          # LLM-based review logic
```
│   ├── github_handler.py    # PR/issue management
│   ├── prompts.py           # LLM prompt templates
│   └── cli.py               # CLI interface
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
