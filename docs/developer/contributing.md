---
title: Contributing
---

# Contributing

Guidelines for contributing to the QuantEcon Style Guide Checker.

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- GitHub account

### Local Development

```bash
# Clone and install
git clone https://github.com/QuantEcon/action-style-guide.git
cd action-style-guide
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Set up API keys
export ANTHROPIC_API_KEY="your-key"
export GITHUB_TOKEN="your-token"
```

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to all functions/classes
- Keep functions focused and small
- Comment complex logic (explain "why", not "what")

### Guiding Principles

1. **Simplicity above all** — write the simplest code that works
2. **Direct over abstract** — don't abstract until you have 3+ use cases
3. **Readable over concise** — explicit is better than implicit
4. **Less code = less bugs** — every line is a liability

```python
# Good: Simple, clear, explicit
def apply_fix(content: str, violation: dict) -> str:
    """Apply a single fix to content."""
    old_text = violation['current_text']
    new_text = violation['suggested_fix']
    return content.replace(old_text, new_text, 1)

# Avoid: Clever, requires mental parsing
def apply_fix(c, v):
    return c.replace(v['ct'], v['sf'], 1) if 'ct' in v and 'sf' in v else c
```

## Adding New Rules

Rules are in `style_checker/rules/` and are read directly by the LLM — **no code changes needed**.

1. Edit the appropriate rules file (e.g., `style_checker/rules/writing-rules.md`)
2. Follow the existing format:

   ```markdown
   ### Rule: qe-writing-001
   **Type:** rule
   **Title:** Use one sentence per paragraph

   **Description:**
   [Detailed explanation]

   **Check for:**
   [Specific patterns to identify]

   **Examples:**
   [Good and bad examples]
   ```

3. Update corresponding prompt file in `style_checker/prompts/` if needed
4. Test with real lecture files

### Adding a New Category

1. Create `prompts/category-prompt.md`
2. Create `rules/category-rules.md`
3. Add category to `VALID_CATEGORIES` in `github_handler.py` and `prompt_loader.py`
4. Add to category list in `review_lecture_smart()`
5. Test end-to-end

## Pull Request Process

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/your-feature-name`
3. **Make changes** — write clean, documented code
4. **Run tests**: `pytest tests/ -v`
5. **Commit with clear messages** using conventional commits
6. **Push and create PR** with clear description

### Commit Message Format

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

## Version Management

```python
# In __init__.py — bump for every release
__version__ = "0.7.2"
```

### Release Process

1. Make changes
2. **Run full test suite**: `pytest tests/ -v`
3. Update `__version__` in `style_checker/__init__.py`
4. Update prompt versions if prompts were modified
5. Update `CHANGELOG.md`
6. Commit: `Release vX.Y.Z - Description`
7. Create GitHub release: `gh release create vX.Y.Z`
8. Update floating tag: `git tag -f v0.7 && git push origin v0.7 --force`

## Debugging LLM Issues

1. Check the prompt — is it clear and explicit?
2. Add more examples to rules
3. Strengthen language (e.g., "do NOT" instead of "don't")
4. Add "Important:" or "Critical:" sections
5. Test with isolated examples first

## Reporting Issues

Include:

1. Description of the problem
2. Steps to reproduce
3. Expected vs actual behavior
4. Environment details (OS, Python version)
5. Relevant logs or error messages
