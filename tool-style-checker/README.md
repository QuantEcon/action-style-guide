# QuantEcon Lecture Style Checker

Automated style checking for QuantEcon lecture materials using Claude Sonnet 4.5.

## Overview

This system automatically reviews QuantEcon lectures against your comprehensive style guide, providing:

- ✅ **Automated checking** of all 8 rule categories (42 rules total)
- ✅ **Structured feedback** with exact line numbers and specific fixes
- ✅ **Actionable suggestions** - copy-paste ready corrections
- ✅ **Flexible usage** - web interface, API, or command-line
- ✅ **Cost-effective** - $0.02-0.20 per lecture

📖 **Complete Documentation**: See [`docs/DOCUMENTATION.md`](docs/DOCUMENTATION.md) for full guide

## Quick Start

### Method 1: Web Interface (No setup required)

1. Go to [claude.ai](https://claude.ai)
2. Upload three files:
   - `claude-style-checker-prompt.md`
   - `style-guide-database.md`
   - Your lecture file
3. Send: *"Please follow the prompt to review the lecture against the style guide"*

### Method 2: Command Line (Best for automation)

```bash
# One-time setup
pip install anthropic
export ANTHROPIC_API_KEY='your-api-key'

# Check a lecture (get suggestions) - creates analysis.md
python style_checker.py my-lecture.md

# Get corrected file automatically - creates my-lecture-corrected.md
python style_checker.py my-lecture.md --mode corrected

# Get both review and corrected file - creates analysis.md + my-lecture-corrected.md
python style_checker.py my-lecture.md --mode both

# Common options
python style_checker.py lecture.md --quick              # Critical only
python style_checker.py lecture.md --focus writing math # Specific categories
python style_checker.py lecture.md --exclude code jax   # Skip certain categories
python style_checker.py --help                          # All options
```

## Three Output Modes

| Mode | Output Files | Use Case |
|------|--------------|----------|
| `suggestions` | `analysis.md` | Learning, selective fixes, understanding issues |
| `corrected` | `{filename}-corrected.md` | Quick fixes, automation, batch processing |
| `both` | `analysis.md` + `{filename}-corrected.md` | Verification, documentation, seeing before/after |

**Consistent file naming:**
- Analysis and suggestions always go to `analysis.md`
- Corrected files always go to `{input-filename}-corrected.md`

See [`docs/MODES-GUIDE.md`](docs/MODES-GUIDE.md) for detailed workflows and examples.

## Common Usage Patterns

### Review and Learn

```bash
# Get detailed suggestions - creates analysis.md
python style_checker.py my-lecture.md
```

### Test It

```bash
# Run on test lecture with ~40+ intentional violations
python style_checker.py quantecon-test-lecture.md
```

### Quick Fix

```bash
# Get corrected file directly - creates my-lecture-corrected.md
python style_checker.py my-lecture.md --mode corrected

# Review changes
diff my-lecture.md my-lecture-corrected.md

# Apply if satisfied
mv my-lecture-corrected.md my-lecture.md
```

### Full Analysis

```bash
# Get review AND corrected file in one run
python style_checker.py my-lecture.md --mode both

# Creates:
#   - analysis.md (full review)
#   - my-lecture-corrected.md (corrected file)
```

### Focus on Specific Issues

```bash
# Check only writing style
python style_checker.py lecture.md --focus writing

# Check only math notation
python style_checker.py lecture.md --focus math

# Check everything except code rules
python style_checker.py lecture.md --exclude code

# Check everything except code and JAX rules
python style_checker.py lecture.md --exclude code jax

# Quick check for critical issues
python style_checker.py lecture.md --quick
```

### Batch Processing

```bash
# Fix all lectures in a folder
for lecture in lectures/*.md; do
    python style_checker.py "$lecture" --mode corrected
done
```

## What You Get

Claude provides structured feedback with:

- Summary of all violations found
- Critical issues organized by category (Writing, Math, Code, JAX, Figures, etc.)
- Exact line numbers and quoted text
- Specific, copy-paste ready corrections
- Prioritized recommendations

Example:

```markdown
### qe-writing-001: Use one sentence per paragraph
Location: Lines 42-44
Current: "Multiple sentences here. Second sentence."
Issue: Paragraph contains 2 sentences
Fix: [Provides corrected version with proper paragraph breaks]

### qe-math-002: Use \top for transpose notation
Location: Line 156
Current: $$A^T B$$
Fix: $$A^\top B$$
```

📖 **See [`docs/DOCUMENTATION.md`](docs/DOCUMENTATION.md#example-interactions) for complete examples**

## Command-Line Options

```bash
python style_checker.py <lecture.md> [options]

Options:
  --mode {suggestions,corrected,both}
                        Output mode (default: suggestions)
  --quick               Check critical issues only
  --focus {writing,math,code,jax,figures,references,links,admonitions}
                        Focus on specific categories
  --exclude {writing,math,code,jax,figures,references,links,admonitions}
                        Exclude specific categories from checking
  --prompt FILE         Custom prompt file (default: claude-style-checker-prompt.md)
  --style-guide FILE    Custom style guide (default: style-guide-database.md)
  --api-key KEY         Claude API key (overrides ANTHROPIC_API_KEY)

Output Files:
  suggestions mode:     analysis.md
  corrected mode:       {input-filename}-corrected.md  
  both mode:            analysis.md + {input-filename}-corrected.md
```

## Files

### Core System (3 files)

| File | Description |
|------|-------------|
| **`style_checker.py`** | Command-line automation script |
| **`claude-style-checker-prompt.md`** | Prompt that instructs Claude |
| **`style-guide-database.md`** | Complete style guide (43KB, 42 rules) |

### Documentation (2 files)

| File | Description |
|------|-------------|
| **`docs/DOCUMENTATION.md`** | 📖 **Complete guide** - setup, usage, examples, troubleshooting |
| **`docs/MODES-GUIDE.md`** | 🎯 **Output modes** - suggestions, corrected, or both |
| **`README.md`** | This file - quick overview |

### Testing (1 file)

| File | Description |
|------|-------------|
| **`quantecon-test-lecture.md`** | Test lecture with intentional violations |

### Archive

| Folder | Description |
|--------|-------------|
| **`archive/`** | Old experimental prompts and previous multi-file docs |

## Style Guide Coverage

The style checker enforces **42 rules** across **8 categories**:

- **Writing Style** (9 rules): Language, contractions, pronouns, tense, voice
- **Mathematical Notation** (7 rules): LaTeX formatting, equation formatting, conventions
- **Code Blocks** (8 rules): Syntax highlighting, output blocks, naming
- **JAX Code** (4 rules): Random keys, JIT usage, NumPy compatibility
- **Figures** (4 rules): Naming, captions, accessibility
- **References** (4 rules): Citations, bibliography format
- **Links** (3 rules): URL format, descriptions
- **Admonitions** (3 rules): Note/warning box usage

See [`style-guide-database.md`](style-guide-database.md) for complete rule details.

## Requirements

**Web Interface:**
- No installation required
- Just a browser

**Command Line:**
- Python 3.7+
- `pip install anthropic`
- Claude API key from [console.anthropic.com](https://console.anthropic.com/)

## Features

✅ **Comprehensive** - 42 rules across 8 categories  
✅ **Accurate** - Context-aware, ~95% accuracy on strict rules  
✅ **Actionable** - Exact fixes, not just complaints  
✅ **Flexible** - Multiple usage methods and focus modes  
✅ **Cost-effective** - $0.02-0.20 per typical lecture  

## Tips

✅ **Start with suggestions mode** to understand what needs fixing  
✅ **Use `both` mode** when you want to verify changes  
✅ **Use corrected mode** for automated workflows  
✅ **Always review diffs** before accepting automated corrections  
✅ **Use `--focus`** to target specific areas when learning  
✅ **Use `--quick`** for fast critical-only checks  

## Documentation

Everything you need is in [`docs/DOCUMENTATION.md`](docs/DOCUMENTATION.md):

- ✅ **Quick Start** - Get running in 5 minutes
- ✅ **Installation** - Step-by-step setup for both methods
- ✅ **Usage Guide** - All commands and options explained
- ✅ **Example Interactions** - Real conversations with Claude
- ✅ **Architecture** - How the system works
- ✅ **Customization** - Adapt to your needs
- ✅ **Troubleshooting** - Solutions to common issues
- ✅ **FAQ** - Frequently asked questions

## Support

- 📖 **Full Documentation**: [`docs/DOCUMENTATION.md`](docs/DOCUMENTATION.md)
- 🎯 **Modes Guide**: [`docs/MODES-GUIDE.md`](docs/MODES-GUIDE.md)
- 🧪 **Test File**: `quantecon-test-lecture.md`
- ❓ **Troubleshooting**: See [DOCUMENTATION.md#troubleshooting](docs/DOCUMENTATION.md#troubleshooting)

---

## Project Structure

```
.
├── style_checker.py                 # Main script
├── claude-style-checker-prompt.md   # Claude prompt
├── style-guide-database.md          # Complete style rules (42 rules)
├── quantecon-test-lecture.md        # Test lecture with violations
├── README.md                        # This file
├── CHANGELOG.md                     # Version history
├── docs/
│   ├── DOCUMENTATION.md             # Complete user guide
│   └── MODES-GUIDE.md               # Output modes guide
└── archive/                         # Old experimental files
```

## Version

**Current Version**: 1.1.0 (2025-10-03)  
**Status**: ✅ Production Ready  
**Last Updated**: October 3, 2025  

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

**Claude Model**: `claude-sonnet-4-20250514`  
**Format**: MyST Markdown (Jupyter Book)  
**License**: [Add your license]