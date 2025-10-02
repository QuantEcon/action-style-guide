"""
Integration tests for LLM-based style checking
These tests make real API calls to LLM providers - run with pytest -m integration
"""

import sys
import os
from pathlib import Path
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from style_checker.parser_md import load_style_guide, format_rules_for_llm
from style_checker.reviewer import StyleReviewer


# Sample lecture content with deliberate style violations
SAMPLE_LECTURE_WITH_VIOLATIONS = """
---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Introduction to Dynamic Programming

This lecture introduces dynamic programming using the Bellman equation.

## Mathematical Notation

Let's look at the value function using display math:

$$
V(x) = \\max_{y} u(x,y) + \\beta V(y)
$$

## Code Example

Here's some code without a language specifier:

```
def bellman_operator(v):
    return max(u + beta * v)
```

And here's some code with improper formatting:

```python
x=[1,2,3]
for i in range(len(x)):
    print(x[i])
```

## References

See Smith (2020) for more details.

## Exercise 1

Solve the Bellman equation.

**Solution**

The solution is V(x) = 42.
"""


@pytest.fixture
def style_guide_path():
    """Fixture to provide the style guide path"""
    return Path(__file__).parent.parent / "style-guide-database.md"


@pytest.fixture
def sample_rules(style_guide_path):
    """Load a subset of critical rules for testing"""
    db = load_style_guide(str(style_guide_path))
    
    # Get high-priority rules for testing
    critical = db.get_critical_rules()
    mandatory = db.get_rules_by_priority('mandatory')
    all_rules = critical + mandatory
    
    # Format for LLM (limit to first chunk for faster testing)
    chunks = format_rules_for_llm(all_rules[:10], max_rules=10)
    return chunks[0] if chunks else ""


@pytest.mark.integration
@pytest.mark.skipif(
    "ANTHROPIC_API_KEY" not in os.environ and 
    "OPENAI_API_KEY" not in os.environ and
    "GOOGLE_API_KEY" not in os.environ,
    reason="No LLM API key found - set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY"
)
class TestLLMIntegration:
    """Integration tests that make real LLM API calls"""
    
    def get_available_provider(self):
        """Determine which LLM provider to use based on available API keys"""
        if os.environ.get("ANTHROPIC_API_KEY"):
            return "claude", os.environ["ANTHROPIC_API_KEY"]
        elif os.environ.get("OPENAI_API_KEY"):
            return "openai", os.environ["OPENAI_API_KEY"]
        elif os.environ.get("GOOGLE_API_KEY"):
            return "gemini", os.environ["GOOGLE_API_KEY"]
        else:
            pytest.skip("No LLM API key available")
    
    def test_llm_can_detect_violations(self, sample_rules):
        """Test that LLM can detect style violations in sample lecture"""
        provider_name, api_key = self.get_available_provider()
        
        print(f"\n🤖 Testing with provider: {provider_name}")
        
        # Create reviewer
        reviewer = StyleReviewer(provider=provider_name, api_key=api_key)
        
        # Review the sample lecture
        result = reviewer.review_lecture(
            content=SAMPLE_LECTURE_WITH_VIOLATIONS,
            rules_text=sample_rules,
            lecture_name="test_lecture"
        )
        
        # Verify response structure
        assert 'issues_found' in result, "Response missing 'issues_found'"
        assert 'violations' in result, "Response missing 'violations'"
        assert 'corrected_content' in result, "Response missing 'corrected_content'"
        
        print(f"📊 Issues found: {result['issues_found']}")
        print(f"📝 Violations: {len(result['violations'])}")
        
        # We expect the LLM to find at least some violations
        # The sample has: display math $$, missing code language, etc.
        assert result['issues_found'] > 0, "LLM should detect at least one violation"
        
        # Check violation structure
        if result['violations']:
            v = result['violations'][0]
            assert 'rule_id' in v, "Violation missing rule_id"
            assert 'severity' in v, "Violation missing severity"
            assert 'description' in v, "Violation missing description"
            
            print(f"\n✓ Sample violation detected:")
            print(f"  Rule: {v.get('rule_id', 'unknown')}")
            print(f"  Severity: {v.get('severity', 'unknown')}")
            print(f"  Description: {v.get('description', 'unknown')[:80]}...")
    
    def test_llm_provides_corrections(self, sample_rules):
        """Test that LLM provides corrected content"""
        provider_name, api_key = self.get_available_provider()
        
        reviewer = StyleReviewer(provider=provider_name, api_key=api_key)
        
        result = reviewer.review_lecture(
            content=SAMPLE_LECTURE_WITH_VIOLATIONS,
            rules_text=sample_rules,
            lecture_name="test_lecture"
        )
        
        # Verify corrected content is provided
        assert result.get('corrected_content'), "LLM should provide corrected content"
        assert len(result['corrected_content']) > 0, "Corrected content should not be empty"
        
        # Corrected content should be different from original
        # (unless there were truly no violations, which is unlikely with our sample)
        if result['issues_found'] > 0:
            assert result['corrected_content'] != SAMPLE_LECTURE_WITH_VIOLATIONS, \
                "Corrected content should differ from original when violations found"
        
        print(f"\n✓ Corrected content length: {len(result['corrected_content'])} chars")
    
    def test_llm_response_is_parseable(self, sample_rules):
        """Test that LLM response follows expected Markdown format"""
        provider_name, api_key = self.get_available_provider()
        
        reviewer = StyleReviewer(provider=provider_name, api_key=api_key)
        
        result = reviewer.review_lecture(
            content=SAMPLE_LECTURE_WITH_VIOLATIONS,
            rules_text=sample_rules,
            lecture_name="test_lecture"
        )
        
        # Should not have parsing errors
        assert 'error' not in result or result.get('issues_found', 0) > 0, \
            f"Parsing error: {result.get('error', 'unknown')}"
        
        # Verify all violations have required fields
        for i, violation in enumerate(result.get('violations', [])):
            assert 'rule_id' in violation, f"Violation {i} missing rule_id"
            assert 'severity' in violation, f"Violation {i} missing severity"
            assert 'description' in violation, f"Violation {i} missing description"
        
        print(f"\n✓ Response successfully parsed with {len(result.get('violations', []))} violations")
    
    def test_llm_identifies_specific_violations(self, sample_rules):
        """Test that LLM identifies known violations in sample"""
        provider_name, api_key = self.get_available_provider()
        
        reviewer = StyleReviewer(provider=provider_name, api_key=api_key)
        
        result = reviewer.review_lecture(
            content=SAMPLE_LECTURE_WITH_VIOLATIONS,
            rules_text=sample_rules,
            lecture_name="test_lecture"
        )
        
        violations_text = str(result.get('violations', [])).lower()
        
        # Check if LLM detected common violations
        # Note: These checks are flexible since different LLMs may phrase things differently
        expected_issues = {
            'display_math': ['$$', 'display math', 'math directive', 'latex'],
            'code_language': ['language', 'specifier', 'python', 'code block'],
            'exercise_format': ['exercise', 'solution', 'admonition', 'directive'],
        }
        
        found_categories = []
        for category, keywords in expected_issues.items():
            if any(keyword in violations_text for keyword in keywords):
                found_categories.append(category)
        
        print(f"\n✓ Violation categories detected: {found_categories}")
        print(f"  Total violations: {result['issues_found']}")
        
        # We expect at least one category to be detected
        assert len(found_categories) > 0, \
            "LLM should detect at least one category of known violations"


@pytest.mark.integration
def test_markdown_format_no_json_errors(sample_rules):
    """Test that Markdown format eliminates JSON parsing errors"""
    if "ANTHROPIC_API_KEY" not in os.environ:
        pytest.skip("ANTHROPIC_API_KEY not set")
    
    reviewer = StyleReviewer(provider="claude", api_key=os.environ["ANTHROPIC_API_KEY"])
    
    # Use a longer, more complex lecture to stress-test the parser
    complex_lecture = SAMPLE_LECTURE_WITH_VIOLATIONS * 3  # Triple the content
    
    result = reviewer.review_lecture(
        content=complex_lecture,
        rules_text=sample_rules,
        lecture_name="test_complex_lecture"
    )
    
    # The key test: should NOT have JSON parsing errors
    if 'error' in result:
        error_msg = result['error'].lower()
        assert 'json parsing' not in error_msg, \
            f"Should not have JSON parsing errors with Markdown format: {result['error']}"
        assert 'unterminated string' not in error_msg, \
            f"Should not have unterminated string errors: {result['error']}"
    
    # Should successfully parse the response
    assert 'violations' in result, "Response should have violations field"
    print(f"\n✓ Complex lecture processed without JSON errors")
    print(f"  Response length: ~{len(str(result))} chars")


# Utility test that doesn't require API key
def test_sample_lecture_has_violations():
    """Verify our sample lecture actually contains violations"""
    # Check for known violations
    assert '$$' in SAMPLE_LECTURE_WITH_VIOLATIONS, \
        "Sample should contain display math violation"
    assert '```\ndef' in SAMPLE_LECTURE_WITH_VIOLATIONS, \
        "Sample should contain code without language specifier"
    assert 'Smith (2020)' in SAMPLE_LECTURE_WITH_VIOLATIONS, \
        "Sample should contain reference format that could be improved"
    assert '**Solution**' in SAMPLE_LECTURE_WITH_VIOLATIONS, \
        "Sample should contain exercise/solution that needs admonition"
    
    print("\n✓ Sample lecture contains expected violations")


if __name__ == '__main__':
    # Run integration tests
    pytest.main([__file__, '-v', '-m', 'integration'])
