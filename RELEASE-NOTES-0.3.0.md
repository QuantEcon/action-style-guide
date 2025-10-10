# Release Notes - Version 0.3.0

**Release Date:** October 10, 2025  
**Status:** Major Release - Breaking Changes

---

## 🚀 Overview

Version 0.3.0 is a major release featuring a complete architecture redesign with **focused prompts** for better quality and lower costs. This release simplifies the action to use only **Claude Sonnet 4.5** and introduces **sequential category processing** for more reliable results.

**⚠️ Breaking Changes:** This release is not backward compatible with 0.2.x. See migration guide below.

---

## ✨ Highlights

### 1. Focused Prompts Architecture 🎯

Replaced the large auto-generated database with hand-crafted focused prompts:

- **Prompts**: 8 concise instruction files (~85 lines each)
- **Rules**: 8 detailed specification files (~120-235 lines each)
- **Result**: 48% reduction in prompt size (3,610 → 1,901 lines)
- **Benefit**: Better quality, lower costs, easier maintenance

### 2. Sequential Category Processing 🔄

Categories are now processed one at a time, feeding updated content between each:

- ✅ All fixes applied without conflicts
- ✅ Later categories see changes from earlier categories
- ✅ More coherent final output
- ✅ Matches proven `tool-style-checker` approach

**Trade-off**: Slower than parallel processing, but more reliable results.

### 3. Claude Sonnet 4.5 Exclusive 🤖

Simplified to use only the best LLM for style checking:

- **Model**: `claude-sonnet-4-5-20250929` (default)
- **Input Limit**: 200,000 tokens
- **Output Limit**: 64,000 tokens
- **Removed**: OpenAI and Google Gemini support

### 4. Rule Development Workflow 🛠️

New `tool-style-guide-development/` folder for managing style guide rules:

- Single source of truth: `style-guide-database.md`
- Build script: `build_rules.py` generates category files
- Separates development from action runtime
- Enables independent updates to style guide content

### 5. Simplified Architecture ⚡

- Removed runtime database parsing
- Simplified API (removed unnecessary streaming)
- Faster startup and clearer code flow
- Direct file loading from `style_checker/rules/`

---

## 🔧 What's Changed

### Added

- **Focused Prompts**: 8 category-specific prompts in `style_checker/prompts/`
- **Detailed Rules**: 8 rule files in `style_checker/rules/`
- **Sequential Processing**: `review_lecture_smart()` method
- **Rule Development Tools**: `tool-style-guide-development/` folder
- **Category Validation**: Validates category names from comments
- **Smart Prompt Loading**: `PromptLoader` class

### Changed

- **Simplified Configuration**: Removed unnecessary inputs
- **Claude Only**: Now requires `anthropic-api-key` (was optional)
- **Non-Streaming API**: Simplified from streaming to standard API calls
- **Updated Trigger**: Use `@qe-style-checker` instead of `@quantecon-style-guide`
- **All Tests**: Consolidated in `tests/` directory

### Removed

- ❌ Legacy trigger `@quantecon-style-guide`
- ❌ `style-guide-url` input parameter
- ❌ `all` category keyword
- ❌ OpenAI and Gemini support
- ❌ `llm-provider`, `openai-api-key`, `google-api-key` inputs
- ❌ Deprecated `generate_prompts.py`
- ❌ Outdated migration documentation

---

## 📊 Performance & Costs

### Token Usage

With a typical lecture (~11 KB):

- **Single category**: ~5,000 tokens (2.5% of input limit)
- **All 8 categories**: ~12,000 tokens per category
- **Total for all categories**: ~96,000 tokens

### Cost Estimates

Based on Claude Sonnet 4.5 pricing ($3/M input, $15/M output):

- **Single lecture (all categories)**: ~$0.60
- **Single category**: ~$0.10
- **Bulk review (100 lectures)**: ~$60

**Savings**: 33% reduction in input tokens vs old architecture

---

## 🔄 Migration Guide

### From 0.2.x to 0.3.0

**1. Update Workflow File**

```yaml
# Before (0.2.x)
- uses: QuantEcon/action-style-guide@v0.2
  with:
    llm-provider: 'anthropic'
    openai-api-key: ${{ secrets.OPENAI_API_KEY }}
    anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
    style-guide-url: 'https://...'

# After (0.3.0)
- uses: QuantEcon/action-style-guide@v0.3
  with:
    anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
    # That's it! Much simpler.
```

**2. Update Trigger Comment**

```markdown
<!-- Before (0.2.x) -->
@quantecon-style-guide lecture_name

<!-- After (0.3.0) -->
@qe-style-checker lecture_name
@qe-style-checker lecture_name writing,math
```

**3. Remove Category "all"**

```markdown
<!-- Before (0.2.x) -->
@quantecon-style-guide lecture_name all

<!-- After (0.3.0) -->
@qe-style-checker lecture_name
<!-- Omit categories to check all -->
```

**4. Update API Keys**

- Remove `OPENAI_API_KEY` secret (no longer used)
- Remove `GOOGLE_API_KEY` secret (no longer used)
- Keep `ANTHROPIC_API_KEY` (now required)

---

## 📚 Available Categories

Check specific categories for faster, cheaper reviews:

- `writing` - Writing style and formatting
- `math` - Mathematics notation and LaTeX
- `code` - Python code style
- `jax` - JAX-specific patterns
- `figures` - Figure formatting and captions
- `references` - Citations and bibliography
- `links` - Hyperlinks and cross-references
- `admonitions` - Note/warning/tip blocks

**Examples:**

```bash
# All categories (default)
@qe-style-checker aiyagari

# Specific categories
@qe-style-checker aiyagari writing,math
@qe-style-checker numerical_methods jax
```

---

## 🧪 Testing

All tests passing:

```
===== 18 passed, 7 deselected, 2 warnings =====
Coverage: 34%
```

Integration tests require API keys and are marked as optional.

---

## 📖 Documentation

Updated documentation:

- ✅ README.md - Complete rewrite for v0.3.0
- ✅ CHANGELOG.md - Comprehensive release notes
- ✅ CONTRIBUTING.md - Updated guidelines
- ✅ ARCHITECTURE-REVIEW.md - Deep technical review
- ✅ Examples updated to use `@v0.3`

---

## 🙏 Acknowledgments

This release was inspired by the proven architecture in `tool-style-checker` and extensive testing with Claude Sonnet 4.5.

---

## 📦 Installation

### Quick Start

```yaml
name: Style Guide Comment Trigger
on:
  issue_comment:
    types: [created]

jobs:
  check-trigger:
    if: contains(github.event.comment.body, '@qe-style-checker')
    runs-on: ubuntu-latest
    steps:
      - uses: QuantEcon/action-style-guide@v0.3
        with:
          mode: 'single'
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
          comment-body: ${{ github.event.comment.body }}
```

See [README.md](README.md) for complete documentation.

---

## 🐛 Known Issues

None at this time.

---

## 🚀 What's Next (v0.3.1+)

Potential enhancements for future versions:

- Progress percentage display for bulk reviews
- Success rate tracking in fix applier
- Additional example workflows
- Enhanced cost tracking and reporting

---

## 📞 Support

- 📚 [Documentation](README.md)
- 🐛 [Report Issues](https://github.com/QuantEcon/action-style-guide/issues)
- 💬 [Discussions](https://github.com/QuantEcon/action-style-guide/discussions)

---

**Full Changelog**: https://github.com/QuantEcon/action-style-guide/blob/main/CHANGELOG.md
