# Tests

This directory contains all test files for the action-style-guide project using the **pytest** framework.

## Test Files

### `test_github_handler.py`
Tests GitHub API interaction logic:
- Comment parsing for `@qe-style-checker` triggers
- Lecture name and category extraction from comments
- PR body formatting

### `test_markdown_parser.py`
Tests the Markdown response parser used for LLM responses:
- Parsing violations from Markdown format
- Extracting summary and issues count
- Extracting corrected content
- Handling of code blocks and special characters
- Error handling for malformed responses

### `test_parsing.py`
Tests comment parsing using the real `GitHubHandler.extract_lecture_from_comment()` method:
- Basic and backtick syntax
- Category extraction
- Path handling and `.md` extension stripping
- Invalid inputs return None

### `test_fix_applier.py`
Tests the fix application engine:
- Single and multiple fix application
- Missing current_text / suggested_fix handling
- Text-not-found graceful skipping
- First-occurrence-only replacement
- Fix quality validation warnings

### `test_prompt_loader.py`
Tests prompt and rules loading:
- Single and multi-category prompt loading
- All 8 categories loadable
- Invalid category error handling
- Prompt version tracking presence
- Rules file content validation

### `test_reviewer.py`
Tests rule extraction and evaluation order:
- Rule counts per category (49 total)
- Rule type distribution (32 rule, 13 style, 4 migrate)
- RULE_EVALUATION_ORDER consistency with rule files
- Rule field validation and ID format
- No duplicate rule IDs

### `test_llm_integration.py`
**Integration tests** that make real LLM API calls (marked with `@pytest.mark.integration`):
- End-to-end LLM style checking with sample lecture
- Single-rule evaluation with real LLM providers
- Markdown response format validation
- Tests work with Claude Sonnet 4.5

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
pytest tests/test_github_handler.py
pytest tests/test_markdown_parser.py
```

Run specific test function:
```bash
pytest tests/test_github_handler.py::test_extract_lecture_from_comment
```

### Using pytest markers

Exclude integration tests (default behavior):
```bash
pytest -m "not integration"
```

Run ONLY integration tests (requires API keys):
```bash
export ANTHROPIC_API_KEY="your-key-here"
pytest -m integration -v
```

**Warning:** Integration tests make real API calls and will cost money!

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
