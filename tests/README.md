# Tests

[![CI](https://github.com/QuantEcon/action-style-guide/workflows/CI/badge.svg)](https://github.com/QuantEcon/action-style-guide/actions)

This directory contains all test files for the action-style-guide project using the **pytest** framework.

## Test Files

### `test_basic.py`
Tests core functionality of the style guide checker:
- Style guide YAML loading
- Rule formatting for LLM
- Rule querying and filtering by category and priority
- Rule uniqueness and required fields validation
- GitHub comment parsing (if credentials available)

### `test_markdown_parser.py`
Tests the Markdown response parser used for LLM responses:
- Parsing violations from Markdown format
- Extracting summary and issues count
- Extracting corrected content
- Handling of code blocks and special characters
- Error handling for malformed responses

### `test_llm_integration.py`
**Integration tests** that make real LLM API calls (marked with `@pytest.mark.integration`):
- End-to-end LLM style checking with sample lecture
- Violation detection with real LLM providers
- Corrected content generation
- Markdown response format validation
- Tests work with Claude, GPT-4, or Gemini

**Note:** These tests are skipped by default (require API keys and cost money to run).

## Running Tests

### Using pytest (Recommended)

Run all tests:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

Run with coverage report:
```bash
pytest --cov=style_checker --cov-report=term-missing
```

Run specific test file:
```bash
pytest tests/test_basic.py
pytest tests/test_markdown_parser.py
```

Run specific test function:
```bash
pytest tests/test_basic.py::test_load_style_guide
```

### Using pytest markers

Run only fast tests (excluding slow integration tests):
```bash
pytest -m "not slow"
```

Exclude integration tests (default behavior):
```bash
pytest -m "not integration"
```

Run ONLY integration tests (requires API keys):
```bash
# Set API key first
export ANTHROPIC_API_KEY="your-key-here"
# or: export OPENAI_API_KEY="your-key-here"
# or: export GOOGLE_API_KEY="your-key-here"

# Run integration tests
pytest -m integration -v
```

**⚠️ Warning:** Integration tests make real API calls and will cost money!

### Legacy Method

Tests can also be run directly (backwards compatible):
```bash
python tests/test_basic.py
python tests/test_markdown_parser.py
```

## Continuous Integration

Tests run automatically on GitHub Actions for:
- Every push to `main` and `develop` branches
- Every pull request
- Python versions: 3.9, 3.10, 3.11, 3.12

The CI workflow also includes:
- **Linting**: Code quality checks with flake8
- **Formatting**: Black and isort checks
- **Coverage**: Code coverage reporting to Codecov

See `.github/workflows/ci.yml` for full CI configuration.

## Setup Verification

For initial setup verification (checking environment, dependencies, API keys), run:
```bash
python verify_setup.py
```

This is located in the root directory as it's a setup/diagnostic tool rather than a unit test.

## Test Requirements

Install test dependencies:
```bash
pip install -r requirements.txt
```

This includes:
- `pytest>=7.4.0` - Test framework
- `pytest-cov>=4.1.0` - Coverage plugin
- All project dependencies

## Test Configuration

Test behavior is configured in `pyproject.toml`:
- Test discovery patterns
- Coverage settings
- Output formatting
- Test markers

## Coverage Reports

After running tests with coverage, view the HTML report:
```bash
pytest --cov=style_checker --cov-report=html
open htmlcov/index.html  # macOS
```

## Writing New Tests

When adding new tests:
1. Create test file with `test_*.py` naming pattern
2. Use `test_*` function names
3. Use pytest fixtures for setup/teardown
4. Use pytest assertions (`assert`)
5. Add docstrings explaining what's tested
6. Use appropriate markers if needed

Example:
```python
import pytest

@pytest.fixture
def my_fixture():
    """Provide test data"""
    return {"key": "value"}

def test_my_feature(my_fixture):
    """Test description"""
    result = process(my_fixture)
    assert result == expected
```
