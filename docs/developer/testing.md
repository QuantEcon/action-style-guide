---
title: Testing
---

# Testing

Comprehensive testing guide covering unit tests, integration tests, and production testing.

## Quick Start

```bash
# All tests (excludes integration by default)
pytest

# Verbose with coverage
pytest -v --cov=style_checker

# Stop on first failure
pytest -x
```

## Test Structure

```
tests/
├── test_fix_applier.py       # Fix application and quality validation
├── test_github_handler.py    # GitHub API interaction, comment parsing
├── test_markdown_parser.py   # LLM response parsing
├── test_parsing.py           # Comment trigger pattern matching
├── test_prompt_loader.py     # Prompt/rules file loading
├── test_reviewer.py          # Rule extraction and evaluation order
├── test_llm_integration.py   # Real LLM API calls (@integration)
└── test_cli.py               # CLI argument parsing
```

### Unit Tests (Fast, Free)

Run automatically with `pytest`:

| File | Focus |
|------|-------|
| `test_fix_applier.py` | Fix application and quality validation |
| `test_github_handler.py` | GitHub API interaction, comment parsing |
| `test_markdown_parser.py` | LLM response parsing |
| `test_parsing.py` | Comment trigger pattern matching (real method) |
| `test_prompt_loader.py` | Prompt/rules file loading |
| `test_reviewer.py` | Rule extraction and evaluation order |
| `test_cli.py` | CLI argument parsing |

### Integration Tests (Slow, Costs Money)

Require an Anthropic API key (~$0.05 per run):

```bash
export ANTHROPIC_API_KEY="your-key"
pytest -m integration
```

These tests make real Claude Sonnet 4.5 API calls and verify end-to-end functionality.

## Coverage

```bash
# Terminal report
pytest --cov=style_checker --cov-report=term-missing

# HTML report
pytest --cov=style_checker --cov-report=html
open htmlcov/index.html
```

Current coverage:

| File | Coverage |
|------|----------|
| `fix_applier.py` | 92% |
| `prompt_loader.py` | 86% |
| `github_handler.py` | 55% |
| `reviewer.py` | 47% |
| `action.py` | 0% (needs integration mocking) |

## CI Pipeline

Runs on push/PR to `main` via `.github/workflows/ci.yml`:

- **Test** — Unit tests across Python 3.11, 3.12, 3.13
- **Lint** — Syntax errors and undefined names via ruff

## Production Testing

### Test Repository

[test-action-style-guide](https://github.com/QuantEcon/test-action-style-guide) is a dedicated test repository with intentional violations. Safe environment for testing new features.

```bash
# Clone if needed
git clone https://github.com/QuantEcon/test-action-style-guide.git

# Test CLI on a test lecture
qestyle test-action-style-guide/lectures/quantecon-test-lecture.md --categories writing

# Dry-run (no changes)
qestyle test-action-style-guide/lectures/quantecon-test-lecture.md --dry-run

# Reset test files after testing
cd test-action-style-guide && git checkout -- . && cd ..
```

### Real-World Testing

[lecture-python-advanced.myst](https://github.com/QuantEcon/lecture-python-advanced.myst) is enabled for real-world testing:

- [Testing issue #261](https://github.com/QuantEcon/lecture-python-advanced.myst/issues/261)
- Comment `@qe-style-checker lecture_name` to test on actual lectures

### Verification Checklist

Before releasing, verify:

1. `pytest tests/ -v` — all unit tests pass
2. `qestyle` runs on a real lecture without errors
3. GitHub Action triggers and creates PR correctly
4. Applied fixes are legitimate corrections
5. Style suggestions are reasonable recommendations
6. No false positives in output

## Writing Tests

```python
import pytest

@pytest.fixture
def sample_content():
    """Setup test data."""
    return "# My Lecture\n\nSome content here.\n"

def test_my_feature(sample_content):
    """Test description."""
    result = process(sample_content)
    assert result == expected_output
```

### Marking Integration Tests

```python
@pytest.mark.integration
def test_real_api_call():
    """Requires ANTHROPIC_API_KEY."""
    ...
```

## Useful Commands

```bash
# Run specific file
pytest tests/test_fix_applier.py

# Run specific test
pytest tests/test_github_handler.py::test_extract_lecture_from_comment

# Exclude integration tests
pytest -m "not integration"

# Include integration tests
pytest -m integration

# Run with coverage, stop on first failure
pytest -x --cov=style_checker
```
