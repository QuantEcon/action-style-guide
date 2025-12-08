# QuantEcon Lecture Style Checker (Development Tool)

> ⚠️ **NOTE:** This is a standalone development tool for **local testing** of the style checker.
> It is **NOT part of the GitHub Action** itself - use the main GitHub Action for production.

Focused style checking for QuantEcon lecture materials using Claude Sonnet 4.5.

## Purpose

This tool is for **local development and testing**:
- Testing lectures locally before submitting to CI
- Quick iteration without GitHub infrastructure  
- Validating prompt/rule changes work correctly

## Shared Resources

This tool **uses the same prompts and rules** as the main GitHub Action:
- Prompts loaded from: `../style_checker/prompts/`
- Rules loaded from: `../style_checker/rules/`

This ensures local testing uses identical rules to production.

## Overview

This tool provides **automated, category-focused** style checking for QuantEcon lectures. Each check focuses on specific categories (writing, math, code, etc.) with specialized prompts and relevant rules only.

**Benefits:**
- ✅ **Focused reviews** - Check one or multiple categories at a time
- ✅ **Token efficient** - 80% reduction vs checking all 42 rules at once
- ✅ **Always get both** - Suggestions AND corrected file in every run
- ✅ **Fast** - Targeted analysis completes quickly
- ✅ **Cost-effective** - $0.01-0.05 per focused check

## Quick Start

### Installation

```bash
pip install anthropic
export ANTHROPIC_API_KEY='your-api-key'
```

### Basic Usage

```bash
# Single category - creates 2 files
python style_checker.py my-lecture.md --focus writing
# → Creates: my-lecture-suggestions.md + my-lecture-corrected.md

# Multiple categories - sequential processing
python style_checker.py my-lecture.md --focus writing,math,code
# → Creates: my-lecture-suggestions.md + my-lecture-corrected.md
```

## Output Files (Always Created)

Every run creates **two files**:

1. **`{lecture-name}-suggestions.md`** - Detailed review with:
   - All violations found
   - Exact line numbers
   - Current vs. suggested text
   - Explanations and fixes

2. **`{lecture-name}-corrected.md`** - Fully corrected version:
   - All violations fixed
   - Ready to use
   - Preserves all content and structure

## Sequential Multi-Category Processing

When you specify multiple categories (comma-separated), the tool processes them **sequentially**:

1. Category 1 processes original lecture → produces corrected version + analysis
2. Category 2 processes Category 1's corrected output → produces corrected version + analysis
3. Category 3 processes Category 2's corrected output → produces final corrected version + analysis
4. All analyses combined in `{lecture-name}-suggestions.md`
5. Final corrected version saved in `{lecture-name}-corrected.md`

### Examples

```bash
# Single category
python style_checker.py lecture.md --focus writing
# → Creates: lecture-suggestions.md + lecture-corrected.md

# Sequential corrections: writing → math → code
python style_checker.py lecture.md --focus writing,math,code
# → Creates: lecture-suggestions.md (3 category reviews)
# → Creates: lecture-corrected.md (3 sequential corrections)
```

## Available Categories

| Category | Rules | Focus Area |
|----------|-------|------------|
| `writing` | 11 | Writing style, grammar, clarity |
| `math` | 7 | Mathematical notation and LaTeX |
| `code` | 10 | Code blocks, syntax, structure |
| `jax` | 3 | JAX library conventions |
| `figures` | 8 | Plots, diagrams, visualizations |
| `references` | 2 | Bibliography and citations |
| `links` | 1 | Hyperlinks and URLs |
| `admonitions` | 2 | Note/warning boxes |

## Common Workflows

### Single Category Review

```bash
# Check writing only
python style_checker.py lecture.md --focus writing
# → lecture-suggestions.md + lecture-corrected.md

# Check math notation only
python style_checker.py lecture.md --focus math
# → lecture-suggestions.md + lecture-corrected.md
```

### Multi-Category Comprehensive Review

```bash
# Check writing, then math, then code (sequential)
python style_checker.py lecture.md --focus writing,math,code
# → lecture-suggestions.md (all 3 reviews)
# → lecture-corrected.md (writing fixes → math fixes → code fixes)

# Full review across all categories
python style_checker.py lecture.md --focus writing,math,code,figures,references
# → Comprehensive review with sequential corrections
```

### Test the Tool

```bash
# Run on test lecture with intentional violations
python style_checker.py quantecon-test-lecture.md --focus writing
# → Creates quantecon-test-lecture-suggestions.md + quantecon-test-lecture-corrected.md
```

## Command Reference

```bash
# Required
python style_checker.py <lecture_file> --focus <category>[,<category>,...]

# Options
--api-key <key>    # Override ANTHROPIC_API_KEY env var

# Examples
python style_checker.py lecture.md --focus writing
python style_checker.py lecture.md --focus writing,math,code

# Help
python style_checker.py --help
```

**Category Order Matters:** Categories process sequentially, each using the previous category's corrected output as input.

## File Structure

```
tool-style-checker/
├── style_checker.py              # Main script (single file, ~300 lines)
├── quantecon-test-lecture.md     # Test file with intentional violations
├── README.md                     # This file
├── CHANGELOG.md                  # Version history
├── prompts/                      # Category-specific prompts (8 files)
│   ├── writing-prompt.md
│   ├── math-prompt.md
│   ├── code-prompt.md
│   ├── jax-prompt.md
│   ├── figures-prompt.md
│   ├── references-prompt.md
│   ├── links-prompt.md
│   └── admonitions-prompt.md
└── rules/                        # Category-specific rules (8 files)
    ├── writing-rules.md          (11 rules)
    ├── math-rules.md             (7 rules)
    ├── code-rules.md             (10 rules)
    ├── jax-rules.md              (3 rules)
    ├── figures-rules.md          (8 rules)
    ├── references-rules.md       (2 rules)
    ├── links-rules.md            (1 rule)
    └── admonitions-rules.md      (2 rules)
```

**Total: 19 files** - Simple and focused!

## Why Focused Categories?

**Single category checks:**
- Small, targeted prompt (low token cost)  
- Specialized instructions per category
- Clear, actionable feedback
- Faster and more accurate
- **Always get both suggestions AND corrected file**

**Multi-category sequential processing:**
- Combine multiple focused checks in one command
- Each category uses optimized prompt and rules
- Progressive corrections build on each other
- Comprehensive review with category-specific analysis
- **One command, complete results**

**vs Traditional all-at-once approach:**
- Large prompt with all 42 rules (high token cost)
- Mixed feedback across unrelated areas
- Harder to focus on specific improvements
- Less accurate due to prompt complexity
- **Must choose between suggestions OR corrections**

## Output Files

Every run creates exactly **two files**:

### {lecture-name}-suggestions.md
Detailed review with:
- Rule violations with line numbers
- Current vs suggested text
- Explanations and context
- Priority ranking
- All categories combined (if multiple)

### {lecture-name}-corrected.md
Fully corrected version of your lecture:
- All violations fixed
- Sequential corrections applied (if multiple categories)
- Ready to review and use
- Preserves all technical content

## Cost Estimate

**Per single category check** (typical lecture):
- **Short lecture** (~2000 words): $0.01-0.02
- **Medium lecture** (~5000 words): $0.02-0.04  
- **Long lecture** (~10000 words): $0.04-0.05

**Multi-category sequential processing** (3 categories):
- Each category is a separate LLM call
- Total cost = (single category cost) × (number of categories)
- Example: 3 categories on medium lecture = $0.06-0.12

Compare to checking all 42 rules at once: $0.08-0.20 per check (and less accurate!)

## Requirements

- Python 3.7+
- `anthropic` package
- Claude API key
- Internet connection

## Getting Claude API Access

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Create account and get API key
3. Set environment variable:
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

## Tips

1. **Always get both outputs** - Review suggestions before using corrected file
2. **Start with writing** - Foundation for all other improvements  
3. **Check diffs** - `diff my-lecture.md my-lecture-corrected.md` to see what changed
4. **Multi-category for comprehensive** - `--focus writing,math,code` for full review
5. **Category order matters** - Suggested: writing → math → code → figures → others
6. **Test on examples first** - Use `quantecon-test-lecture.md` to see how it works

## Troubleshooting

**Error: ANTHROPIC_API_KEY not set**
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

**Error: File not found**
- Check file path is correct
- Use relative or absolute paths

**Error: Category not found**  
- Check category name spelling
- Use one of: writing, math, code, jax, figures, references, links, admonitions

## License

QuantEcon Project
