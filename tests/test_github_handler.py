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
    
    # Simulate a real review result with original/final content and fix_log
    original = 'We use $\\alpha$ for the learning rate.\n'
    final = 'We use α for the **learning rate**.\n'
    
    review_result = {
        'original_content': original,
        'corrected_content': final,
        'fix_log': [
            {
                'rule_id': 'qe-math-001',
                'rule_title': 'Unicode for parameters',
                'category': 'math',
                'current_text': 'We use $\\alpha$ for the learning rate.',
                'suggested_fix': 'We use α for the learning rate.',
                'description': 'Use unicode for simple parameters',
                'explanation': 'Unicode improves readability',
                'location': 'Line 10',
            },
            {
                'rule_id': 'qe-writing-005',
                'rule_title': 'Bold for definitions',
                'category': 'writing',
                'current_text': 'We use α for the learning rate.',
                'suggested_fix': 'We use α for the **learning rate**.',
                'description': 'Bold definitions',
                'explanation': 'Key terms should be bolded',
                'location': 'Line 10',
            },
        ],
    }
    
    report = handler.format_applied_fixes_report(review_result, 'test_lecture')
    
    # Should produce a report (content actually changed)
    assert report is not None
    # Should use ~~~ (tilde) fences for markdown blocks
    assert '~~~markdown' in report, "Report should use tilde fences for markdown blocks"
    # Should NOT use ````markdown` (four backticks)
    assert '````markdown' not in report, "Report should not use four-backtick markdown blocks"
    # Should show both rules attributed
    assert 'qe-math-001' in report
    assert 'qe-writing-005' in report
    # Should show original and final text
    assert '$\\alpha$' in report  # Original text
    assert '**learning rate**' in report  # Final text


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
    """Test that ~~~ fences properly handle content with nested ```-backtick code blocks.
    
    The region-based report uses difflib to find changed regions. To verify ~~~
    fencing works with nested backtick blocks, we create a change where the
    backtick-fenced block itself is part of the diff (e.g. the directive type changes).
    """
    handler = create_mock_handler()
    
    # The directive type changes from code-cell to code-cell ipython3,
    # making the backtick fence line part of the diff region
    original_content = """Here is a directive:

```{code-cell} python
def example():
    return 42
```
"""
    
    final_content = """Here is a directive:

```{code-cell} ipython3
def better_example():
    return 42
```
"""
    
    review_result = {
        'original_content': original_content,
        'corrected_content': final_content,
        'fix_log': [{
            'rule_id': 'qe-code-001',
            'rule_title': 'Update code cell',
            'category': 'code',
            'current_text': '```{code-cell} python\ndef example():',
            'suggested_fix': '```{code-cell} ipython3\ndef better_example():',
            'description': 'Updated code cell type and function name',
            'explanation': 'Use ipython3 kernel and better naming',
            'location': 'Line 3',
        }],
    }
    
    report = handler.format_applied_fixes_report(review_result, 'test_lecture')
    
    assert report is not None
    # The outer fence should use tildes, not backticks (to avoid conflicts)
    assert '~~~markdown' in report
    # The nested 3-backtick directive should be preserved inside the ~~~ fence
    assert '```{code-cell}' in report
    # The actual changed content should appear
    assert 'better_example' in report


def test_region_based_report_combines_multi_rule_edits():
    """When multiple rules edit the same line, report should combine them into one entry"""
    handler = create_mock_handler()
    
    original = 'We use $\\alpha$ for the learning rate, but later we call it $\\eta$.\n'
    final = 'We use α for the **learning rate**, but later we call it η.\n'
    
    review_result = {
        'original_content': original,
        'corrected_content': final,
        'fix_log': [
            {
                'rule_id': 'qe-math-001',
                'rule_title': 'Unicode for parameters',
                'category': 'math',
                'current_text': 'We use $\\alpha$ for the learning rate, but later we call it $\\eta$.',
                'suggested_fix': 'We use α for the learning rate, but later we call it η.',
                'description': 'Use unicode for simple parameters',
                'explanation': 'Unicode improves readability',
                'location': 'Line 39',
            },
            {
                'rule_id': 'qe-writing-005',
                'rule_title': 'Bold for definitions',
                'category': 'writing',
                'current_text': 'We use α for the learning rate, but later we call it η.',
                'suggested_fix': 'We use α for the **learning rate**, but later we call it η.',
                'description': 'Bold definitions',
                'explanation': 'Key terms should be bolded',
                'location': 'Line 39',
            },
        ],
    }
    
    report = handler.format_applied_fixes_report(review_result, 'test_lecture')
    
    assert report is not None
    # Should show BOTH rules attributed to the same change
    assert 'qe-math-001' in report
    assert 'qe-writing-005' in report
    # Should show the TRUE original (with $\alpha$) and TRUE final (with α and **bold**)
    assert '$\\alpha$' in report
    assert '**learning rate**' in report
    # Should be ONE combined change, not two separate entries
    assert report.count('### Change') == 1, "Multi-rule edits on same line should be one combined entry"


def test_no_report_when_no_actual_changes():
    """Report should be None when original == final (all fixes were no-ops)"""
    handler = create_mock_handler()
    
    content = 'No changes here.\n'
    review_result = {
        'original_content': content,
        'corrected_content': content,
        'fix_log': [],
    }
    
    report = handler.format_applied_fixes_report(review_result, 'test_lecture')
    assert report is None


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
    
    test_region_based_report_combines_multi_rule_edits()
    print("✅ test_region_based_report_combines_multi_rule_edits")
    
    test_no_report_when_no_actual_changes()
    print("✅ test_no_report_when_no_actual_changes")
    
    print("\n🎉 All tests passed!")
