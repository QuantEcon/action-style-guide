#!/usr/bin/env python3
"""
Test GitHub handler PR comment formatting
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from style_checker.github_handler import GitHubHandler


class MockGitHub:
    """Mock GitHub API for testing"""
    def get_repo(self, name):
        return None


def create_mock_handler():
    """Create a GitHubHandler instance without real GitHub API"""
    handler = GitHubHandler.__new__(GitHubHandler)
    handler.github = MockGitHub()
    handler.repo = None
    handler.repository = "test/repo"
    return handler


def test_format_detailed_report_uses_four_backticks():
    """Test that format_detailed_report uses 4 backticks for markdown blocks"""
    handler = create_mock_handler()
    
    review_result = {
        'violations': [{
            'rule_id': 'qe-writing-001',
            'rule_title': 'Test Rule',
            'location': 'Line 10',
            'severity': 'error',
            'description': 'Test description',
            'current_text': '```python\ncode\n```',
            'suggested_fix': '```python\nfixed_code\n```',
            'explanation': 'Fixed the issue'
        }],
        'issues_found': 1,
        'summary': 'Test summary'
    }
    
    report = handler.format_detailed_report(review_result, 'test_lecture')
    
    # Should use 4 backticks for markdown blocks
    assert '````markdown' in report, "Report should use 4 backticks for markdown blocks"
    # Should NOT use 3 backticks for markdown blocks
    four_tick_count = report.count('````markdown')
    three_tick_count = report.count('```markdown') - four_tick_count
    assert three_tick_count == 0, f"Found {three_tick_count} three-backtick markdown blocks"
    assert four_tick_count > 0, "Should have at least one four-backtick markdown block"


def test_format_applied_fixes_report_uses_four_backticks():
    """Test that format_applied_fixes_report uses 4 backticks for markdown blocks"""
    handler = create_mock_handler()
    
    review_result = {
        'rule_violations': [{
            'rule_id': 'qe-writing-001',
            'rule_title': 'Test Rule',
            'location': 'Line 10',
            'description': 'Test description',
            'current_text': '```{code-cell} python\ncode\n```',
            'suggested_fix': '```{code-cell} python\nfixed_code\n```',
            'explanation': 'Fixed the issue'
        }]
    }
    
    report = handler.format_applied_fixes_report(review_result, 'test_lecture')
    
    # Should use 4 backticks for markdown blocks
    assert '````markdown' in report, "Report should use 4 backticks for markdown blocks"
    # Verify no 3-backtick markdown blocks
    four_tick_count = report.count('````markdown')
    three_tick_count = report.count('```markdown') - four_tick_count
    assert three_tick_count == 0, f"Found {three_tick_count} three-backtick markdown blocks"
    assert four_tick_count == 2, "Should have 2 four-backtick markdown blocks (current + fix)"


def test_format_style_suggestions_report_uses_four_backticks():
    """Test that format_style_suggestions_report uses 4 backticks for markdown blocks"""
    handler = create_mock_handler()
    
    review_result = {
        'style_violations': [{
            'rule_id': 'qe-writing-007',
            'rule_title': 'Visual Elements',
            'location': 'Line 20',
            'severity': 'suggestion',
            'description': 'Consider adding visual element',
            'current_text': '```{note}\nSome note\n```',
            'suggested_fix': '```{note}\nImproved note\n```',
            'explanation': 'Better formatting'
        }]
    }
    
    report = handler.format_style_suggestions_report(review_result, 'test_lecture')
    
    # Should use 4 backticks for markdown blocks
    assert '````markdown' in report, "Report should use 4 backticks for markdown blocks"
    # Verify no 3-backtick markdown blocks
    four_tick_count = report.count('````markdown')
    three_tick_count = report.count('```markdown') - four_tick_count
    assert three_tick_count == 0, f"Found {three_tick_count} three-backtick markdown blocks"
    assert four_tick_count == 2, "Should have 2 four-backtick markdown blocks (current + fix)"


def test_four_backticks_handles_nested_code_blocks():
    """Test that 4 backticks properly handle content with nested 3-backtick code blocks"""
    handler = create_mock_handler()
    
    # Content with nested 3-backtick code blocks (common in MyST Markdown directives)
    nested_content = """Here is a directive:

```{code-cell} python
def example():
    return 42
```

And another:

```{note}
This is a note
```
"""
    
    review_result = {
        'rule_violations': [{
            'rule_id': 'qe-writing-001',
            'rule_title': 'Test Rule',
            'location': 'Line 10',
            'current_text': nested_content,
            'suggested_fix': nested_content.replace('example', 'better_example'),
            'explanation': 'Improved naming'
        }]
    }
    
    report = handler.format_applied_fixes_report(review_result, 'test_lecture')
    
    # The nested 3-backtick blocks should be preserved inside the 4-backtick fence
    assert '````markdown' in report
    assert '```{code-cell} python' in report
    assert '```{note}' in report
    # The outer fence should use 4 backticks
    assert report.count('````markdown') == 2  # Opening for current_text and suggested_fix


if __name__ == '__main__':
    print("Testing GitHub handler PR comment formatting...\n")
    
    test_format_detailed_report_uses_four_backticks()
    print("✅ test_format_detailed_report_uses_four_backticks")
    
    test_format_applied_fixes_report_uses_four_backticks()
    print("✅ test_format_applied_fixes_report_uses_four_backticks")
    
    test_format_style_suggestions_report_uses_four_backticks()
    print("✅ test_format_style_suggestions_report_uses_four_backticks")
    
    test_four_backticks_handles_nested_code_blocks()
    print("✅ test_four_backticks_handles_nested_code_blocks")
    
    print("\n🎉 All tests passed!")
