# LLM Integration Testing Guide

## Overview

The `test_llm_integration.py` file contains **end-to-end integration tests** that make real API calls to LLM providers. These tests verify that the entire style checking pipeline works correctly with actual LLM responses.

## What Do Integration Tests Cover?

### 1. **Real LLM API Calls**
- Tests use actual API key to call Claude Sonnet 4.5
- Verifies that LLM providers return properly formatted responses
- Ensures the Markdown format works in practice (not just in theory)

### 2. **Violation Detection**
- Uses a carefully crafted sample lecture with known violations:
  - Display math using `$$` instead of MyST `{math}` directive
  - Code blocks without language specifiers
  - Exercise/solution format needing admonitions
  - References that could be improved
- Verifies LLM can detect these violations

### 3. **Response Parsing**
- Tests that real LLM responses parse correctly
- Validates the Markdown format elimination of JSON errors
- Ensures all required fields are present in responses

### 4. **Corrected Content**
- Verifies LLM provides corrected content
- Checks that corrections differ from original (when violations found)
- Validates corrected content is complete and usable

## Sample Lecture

The test uses `SAMPLE_LECTURE_WITH_VIOLATIONS` which contains:

```markdown
# Introduction to Dynamic Programming

## Mathematical Notation
$$
V(x) = \max_{y} u(x,y) + \beta V(y)
$$
[VIOLATION: Should use MyST {math} directive]

## Code Example
```
def bellman_operator(v):
    return max(u + beta * v)
```
[VIOLATION: Missing language specifier]

## Exercise 1
**Solution**
[VIOLATION: Should use admonition directive]
```

## Running Integration Tests

### Prerequisites

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API key**:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

### Running Tests

#### Run all integration tests:
```bash
pytest -m integration -v
```

#### Run specific integration test:
```bash
pytest tests/test_llm_integration.py::TestLLMIntegration::test_llm_can_detect_violations -v
```

#### Run with detailed output:
```bash
pytest -m integration -v -s
```

#### Skip integration tests (default):
```bash
pytest -m "not integration"
```

### Expected Output

```
tests/test_llm_integration.py::TestLLMIntegration::test_llm_can_detect_violations 
🤖 Testing with provider: claude
📊 Issues found: 3
📝 Violations: 3

✓ Sample violation detected:
  Rule: qe-format-001
  Severity: mandatory
  Description: Using display math `$$` instead of MyST directive...
PASSED

tests/test_llm_integration.py::TestLLMIntegration::test_llm_provides_corrections 
✓ Corrected content length: 1247 chars
PASSED

tests/test_llm_integration.py::TestLLMIntegration::test_llm_response_is_parseable 
✓ Response successfully parsed with 3 violations
PASSED

tests/test_llm_integration.py::TestLLMIntegration::test_llm_identifies_specific_violations 
✓ Violation categories detected: ['display_math', 'code_language', 'exercise_format']
  Total violations: 3
PASSED

tests/test_llm_integration.py::test_markdown_format_no_json_errors 
✓ Complex lecture processed without JSON errors
  Response length: ~15000 chars
PASSED
```

## Cost Considerations

⚠️ **Integration tests make real API calls and cost money!**

### Approximate Costs per Test Run (as of Jan 2025)

**Anthropic Claude Sonnet 4.5:**
- Input: ~2K tokens × 5 tests = 10K tokens
- Output: ~1K tokens × 5 tests = 5K tokens
- **Cost: ~$0.05 per full test run**

### Cost-Saving Tips

1. **Run selectively:**
   ```bash
   # Run just one test
   pytest tests/test_llm_integration.py::TestLLMIntegration::test_llm_can_detect_violations
   ```

2. **Mock in CI:**
   - Don't run integration tests in CI by default
   - Use `pytest -m "not integration"` in CI
   - Only run integration tests manually before releases

3. **Cache responses:**
   - Consider caching LLM responses for repeated test runs
   - Use `pytest-recording` or similar for HTTP mocking

## Test Structure

### Fixtures

- **`style_guide_path`**: Path to style-guide-database.md
- **`sample_rules`**: Loads subset of high-priority rules for faster testing

### Test Class

**`TestLLMIntegration`**:
- Uses `@pytest.mark.integration` marker
- Auto-skips if no API keys found
- Tests work with Claude Sonnet 4.5

### Individual Tests

1. **`test_llm_can_detect_violations`**
   - Primary test: Does LLM find violations?
   - Validates response structure
   - Checks that at least one violation is found

2. **`test_llm_provides_corrections`**
   - Verifies corrected content is provided
   - Checks corrections differ from original

3. **`test_llm_response_is_parseable`**
   - Tests Markdown parsing succeeds
   - Validates all violation fields present
   - No parsing errors

4. **`test_llm_identifies_specific_violations`**
   - Checks for known violation categories
   - Flexible keyword matching across providers
   - Validates meaningful detections

5. **`test_markdown_format_no_json_errors`**
   - Stress test with 3x longer content
   - Verifies no JSON parsing errors
   - Proves Markdown format solves the original problem

## CI/CD Integration

### Don't Run by Default

The CI workflow excludes integration tests:

```yaml
# .github/workflows/ci.yml
- name: Run tests with pytest
  run: |
    pytest tests/ -m "not integration" --cov=style_checker
```

### Optional: Scheduled Integration Tests

You can add a separate workflow for weekly integration tests:

```yaml
name: Weekly Integration Tests

on:
  schedule:
    - cron: '0 0 * * 0'  # Sunday midnight
  workflow_dispatch:

jobs:
  integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run integration tests
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: pytest -m integration -v
```

## Debugging Failed Integration Tests

### Common Issues

1. **"No LLM API key found"**
   ```bash
   # Solution: Set environment variable
   export ANTHROPIC_API_KEY="your-key"
   ```

2. **"401 Unauthorized"**
   - API key is invalid or expired
   - Check key format and permissions

3. **"Rate limit exceeded"**
   - Wait a few seconds between test runs
   - Reduce number of tests
   - Use different provider

4. **"Timeout"**
   - LLM taking too long to respond
   - Try with fewer rules
   - Use faster model

5. **"Parsing errors"**
   - LLM didn't follow Markdown format
   - Check system prompts in reviewer.py
   - May need to adjust regex in parser

### Debug Mode

Run with verbose output to see LLM responses:
```bash
pytest -m integration -v -s --log-cli-level=DEBUG
```

## Adding New Integration Tests

### Template

```python
@pytest.mark.integration
def test_my_integration(sample_rules):
    """Test description"""
    if "ANTHROPIC_API_KEY" not in os.environ:
        pytest.skip("ANTHROPIC_API_KEY not set")
    
    reviewer = StyleReviewer(
        provider="claude",
        api_key=os.environ["ANTHROPIC_API_KEY"]
    )
    
    result = reviewer.review_lecture(
        content=my_test_content,
        rules_text=sample_rules,
        lecture_name="test"
    )
    
    # Your assertions here
    assert result['issues_found'] > 0
```

### Best Practices

1. **Keep tests focused** - One aspect per test
2. **Use small samples** - Reduce token usage and cost
3. **Be flexible** - Different LLMs may phrase things differently
4. **Document expectations** - Comment what violations should be found
5. **Handle failures gracefully** - LLMs can be unpredictable

## Summary

Integration tests provide **high confidence** that the entire system works end-to-end with real LLM providers. They:

✅ Catch bugs that unit tests miss  
✅ Verify real LLM behavior  
✅ Validate the Markdown format solution  
✅ Test error handling with real responses  
✅ Ensure corrections are meaningful  

But they also:

⚠️ Cost money to run  
⚠️ Are slower than unit tests  
⚠️ Can be flaky (LLM variability)  
⚠️ Require API keys  

**Recommendation:** Run integration tests:
- Before major releases
- When changing LLM prompts or parsing logic
- When debugging LLM-related issues
- Weekly/monthly for regression testing

Don't run on every commit - that's what unit tests are for!
