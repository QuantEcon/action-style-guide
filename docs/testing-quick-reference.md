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
pytest tests/test_basic.py

# Specific test
pytest tests/test_basic.py::test_load_style_guide

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
- `test_basic.py` - Style guide parsing
- `test_markdown_parser.py` - Response parsing
- Run automatically on every commit

### Integration Tests (Slow, Costs Money)
- `test_llm_integration.py` - Real LLM API calls
- Tests end-to-end with actual providers
- Requires API key (Claude Sonnet 4.5)
- **Cost:** ~$0.05 per test run
- Run manually before releases

## CI Pipeline

**Runs on:**
- Every push to `main` / `develop`
- Every pull request
- Manual trigger

**Jobs:**
1. **Test** - Run all tests across Python versions
2. **Lint** - Check code quality (non-blocking)
3. **Integration** - Run setup verification

## Current Test Coverage

```
Unit Tests:
✅ 23 passed
📊 39% overall coverage
✅ parser_md.py: 98%
✅ __init__.py: 100%
⚠️ reviewer.py: 44%
⚠️ fix_applier.py: 69%
⚠️ github_handler.py: 12%
⚠️ main.py: 7%

Integration Tests:
⏭️  5 skipped (require API keys)
✅ 1 passed (sample validation)
```

Run integration tests to increase coverage.

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
