# Quick Testing Guide

## Run Tests

```bash
# All tests (excludes integration by default)
pytest

# Include integration tests (costs money!)
export ANTHROPIC_API_KEY="your-key"
pytest -m integration

# Exclude integration tests explicitly
pytest -m "not integration"

# Specific file
pytest tests/test_github_handler.py

# Specific test
pytest tests/test_github_handler.py::test_extract_lecture_from_comment

# With coverage
pytest --cov=style_checker

# Verbose
pytest -v

# Stop on first failure
pytest -x
```

## View Coverage

```bash
# Terminal report
pytest --cov=style_checker --cov-report=term-missing

# HTML report
pytest --cov=style_checker --cov-report=html
open htmlcov/index.html
```

## Test Status

- **Framework:** pytest 7.4+
- **Coverage Tool:** pytest-cov 4.1+
- **CI Platform:** GitHub Actions
- **Python Versions:** 3.9, 3.10, 3.11, 3.12

## Test Types

### Unit Tests (Fast, Free)
- `test_github_handler.py` - GitHub API interaction, comment parsing
- `test_markdown_parser.py` - LLM response parsing
- `test_parsing.py` - Comment trigger pattern matching (real method)
- `test_fix_applier.py` - Fix application and quality validation
- `test_prompt_loader.py` - Prompt/rules file loading
- `test_reviewer.py` - Rule extraction and evaluation order
- Run automatically with `pytest`

### Integration Tests (Slow, Costs Money)
- `test_llm_integration.py` - Real LLM API calls
- Tests end-to-end with actual providers
- Requires API key (Claude Sonnet 4.5)
- **Cost:** ~$0.05 per test run
- Run manually before releases

## CI Pipeline

Runs on push/PR to `main` via `.github/workflows/ci.yml`:
- **Test** — Unit tests across Python 3.11, 3.12, 3.13
- **Lint** — Syntax errors and undefined names via ruff

## Current Test Coverage

```
Unit Tests:
✅ 59 passed, 0 warnings
📊 43% overall coverage
✅ fix_applier.py: 92%
✅ prompt_loader.py: 86%
✅ github_handler.py: 55%
✅ reviewer.py: 47%
⚠️ main.py: 0% (needs integration test mocking)

⏭️  6 skipped (integration tests, require API keys)
```

## Add New Test

```python
import pytest

@pytest.fixture
def my_data():
    """Setup test data"""
    return {"key": "value"}

def test_my_feature(my_data):
    """Test my feature"""
    result = process(my_data)
    assert result == expected
```

## Useful Commands

```bash
# Run only fast tests
pytest -m "not slow"

# Run tests matching pattern
pytest -k "test_parse"

# Show available fixtures
pytest --fixtures

# Show test collection
pytest --collect-only

# Run with debug output
pytest -s

# Detailed failure info
pytest -vv
```

## CI Badge

Add to README.md:
```markdown
[![CI](https://github.com/QuantEcon/action-style-guide/workflows/CI/badge.svg)](https://github.com/QuantEcon/action-style-guide/actions)
```

## Documentation

- **Full Guide:** [docs/ci-cd-setup.md](ci-cd-setup.md)
- **Test README:** [tests/README.md](../tests/README.md)
- **pytest Docs:** https://docs.pytest.org/
