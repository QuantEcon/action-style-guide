#!/usr/bin/env python3
"""
Test the Markdown response parser
Uses pytest framework for better test organization
"""

import sys
import os
from pathlib import Path
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from style_checker.reviewer import parse_markdown_response


@pytest.fixture
def sample_markdown_response():
    """Fixture providing a sample Markdown response from LLM"""
    return """# Review Results

## Summary
Fixed 2 issues: corrected LaTeX delimiter and improved code formatting.

## Issues Found
2

## Violations

### Violation 1: qe-format-001 - LaTeX Delimiters
- **Severity:** mandatory
- **Location:** Line 45
- **Description:** Using display math `$$` instead of MyST directive
- **Current text:**
```
$$
E[X] = \sum_{i=1}^n x_i p_i
$$
```
- **Suggested fix:**
```
```{math}
E[X] = \sum_{i=1}^n x_i p_i
```
```
- **Explanation:** MyST Markdown requires math directives instead of raw LaTeX delimiters

### Violation 2: qe-code-002 - Code Block Language
- **Severity:** best_practice
- **Location:** Line 78
- **Description:** Missing language specifier for code block
- **Current text:**
```
```
def compute(x):
    return x * 2
```
```
- **Suggested fix:**
```
```python
def compute(x):
    return x * 2
```
```
- **Explanation:** Code blocks should specify the language for syntax highlighting

## Corrected Content

```markdown
# Sample Lecture

This is a sample lecture with corrected content.

```{math}
E[X] = \sum_{i=1}^n x_i p_i
```

And some code:

```python
def compute(x):
    return x * 2
```

End of lecture.
```
"""


def test_parse_issues_count(sample_markdown_response):
    """Test parsing the issues count from Markdown"""
    result = parse_markdown_response(sample_markdown_response)
    
    assert 'issues_found' in result
    assert result['issues_found'] == 2


def test_parse_violations(sample_markdown_response):
    """Test parsing violations from Markdown"""
    result = parse_markdown_response(sample_markdown_response)
    
    assert 'violations' in result
    assert len(result['violations']) == 2
    
    # Check first violation
    v1 = result['violations'][0]
    assert v1['rule_id'] == 'qe-format-001'
    assert v1['rule_title'] == 'LaTeX Delimiters'
    assert v1['severity'] == 'mandatory'
    assert v1['location'] == 'Line 45'
    assert 'display math' in v1['description']
    
    # Check second violation
    v2 = result['violations'][1]
    assert v2['rule_id'] == 'qe-code-002'
    assert v2['rule_title'] == 'Code Block Language'
    assert v2['severity'] == 'best_practice'


def test_parse_summary(sample_markdown_response):
    """Test parsing the summary from Markdown"""
    result = parse_markdown_response(sample_markdown_response)
    
    assert 'summary' in result
    assert 'Fixed 2 issues' in result['summary']


def test_parse_corrected_content(sample_markdown_response):
    """Test that corrected_content field exists (even if empty)
    
    Note: We no longer request corrected content from the LLM.
    Instead, we apply fixes programmatically using fix_applier.py.
    This test verifies the parser handles the field correctly.
    """
    result = parse_markdown_response(sample_markdown_response)
    
    # Corrected content field should exist in result
    assert 'corrected_content' in result
    # But may be empty since we don't parse it from LLM responses anymore
    # (it's generated programmatically by apply_fixes() instead)


def test_parse_empty_response():
    """Test parsing an empty or minimal response"""
    empty_response = """# Review Results

## Summary
No issues found.

## Issues Found
0

## Violations

## Corrected Content

```markdown
Original content unchanged.
```
"""
    
    result = parse_markdown_response(empty_response)
    
    assert result['issues_found'] == 0
    assert len(result['violations']) == 0
    assert 'No issues found' in result['summary']


def test_parse_malformed_response():
    """Test parsing a malformed response returns error gracefully"""
    malformed = "This is not a properly formatted response"
    
    result = parse_markdown_response(malformed)
    
    # Should not crash, should return default structure
    assert 'issues_found' in result
    assert 'violations' in result
    assert 'corrected_content' in result
    assert 'summary' in result


def test_violation_fields_present(sample_markdown_response):
    """Test that all required violation fields are parsed"""
    result = parse_markdown_response(sample_markdown_response)
    
    required_fields = [
        'rule_id', 'rule_title', 'severity', 'location',
        'description', 'explanation'  # current_text and suggested_fix may be complex
    ]
    
    for violation in result['violations']:
        for field in required_fields:
            assert field in violation, f"Missing field: {field}"
            assert violation[field], f"Empty field: {field} in violation {violation.get('rule_id', 'unknown')}"
        
        # Check that current_text and suggested_fix exist (may be empty for complex cases)
        assert 'current_text' in violation
        assert 'suggested_fix' in violation


if __name__ == '__main__':
    # Allow running directly for backwards compatibility
    pytest.main([__file__, '-v'])
