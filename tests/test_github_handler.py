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


def test_format_detailed_report_uses_tilde_fences():
    """Test that format_detailed_report uses ~~~ fences for markdown blocks"""
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
    
    # Should use ~~~ (tilde) fences for markdown blocks
    assert '~~~markdown' in report, "Report should use tilde fences for markdown blocks"
    # Should NOT use ` ````markdown` (four backticks)
    assert '````markdown' not in report, "Report should not use four-backtick markdown blocks"
    # Count tilde fences
    tilde_fence_count = report.count('~~~markdown')
    assert tilde_fence_count > 0, "Should have at least one tilde-fenced markdown block"


def test_format_applied_fixes_report_uses_tilde_fences():
    """Test that format_applied_fixes_report uses ~~~ fences for markdown blocks"""
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
    
    # Should use ~~~ (tilde) fences for markdown blocks
    assert '~~~markdown' in report, "Report should use tilde fences for markdown blocks"
    # Should NOT use four backticks
    assert '````markdown' not in report, "Report should not use four-backtick markdown blocks"
    # Should have 2 tilde fences (current + fix)
    tilde_fence_count = report.count('~~~markdown')
    assert tilde_fence_count == 2, "Should have 2 tilde-fenced markdown blocks (current + fix)"


def test_format_style_suggestions_report_uses_tilde_fences():
    """Test that format_style_suggestions_report uses ~~~ fences for markdown blocks"""
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
    
    # Should use ~~~ (tilde) fences for markdown blocks
    assert '~~~markdown' in report, "Report should use tilde fences for markdown blocks"
    # Should NOT use four backticks
    assert '````markdown' not in report, "Report should not use four-backtick markdown blocks"
    # Should have 2 tilde fences (current + fix)
    tilde_fence_count = report.count('~~~markdown')
    assert tilde_fence_count == 2, "Should have 2 tilde-fenced markdown blocks (current + fix)"


def test_tilde_fences_handle_nested_code_blocks():
    """Test that ~~~ fences properly handle content with nested ```-backtick code blocks"""
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
    
    # The nested 3-backtick blocks should be preserved inside the ~~~ fence
    assert '~~~markdown' in report
    assert '```{code-cell} python' in report
    assert '```{note}' in report
    # The outer fence should use tildes
    assert report.count('~~~markdown') == 2  # Opening for current_text and suggested_fix


if __name__ == '__main__':
    print("Testing GitHub handler PR comment formatting...\n")
    
    test_format_detailed_report_uses_tilde_fences()
    print("✅ test_format_detailed_report_uses_tilde_fences")
    
    test_format_applied_fixes_report_uses_tilde_fences()
    print("✅ test_format_applied_fixes_report_uses_tilde_fences")
    
    test_format_style_suggestions_report_uses_tilde_fences()
    print("✅ test_format_style_suggestions_report_uses_tilde_fences")
    
    test_tilde_fences_handle_nested_code_blocks()
    print("✅ test_tilde_fences_handle_nested_code_blocks")
    
    print("\n🎉 All tests passed!")
