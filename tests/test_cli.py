"""
Tests for the qestyle CLI (style_checker/cli.py)

Tests cover:
- Report formatting (format_report)
- Default report path generation
- Argument validation (categories, file existence)
- CLI entry point error handling

Does NOT test LLM integration — that's covered by test_reviewer.py and test_llm_integration.py.
"""

import subprocess
import os
import tempfile
from pathlib import Path

from style_checker.cli import format_report, default_report_path, check_git_dirty, ALL_CATEGORIES
from style_checker import __version__


# ---------------------------------------------------------------------------
# format_report tests
# ---------------------------------------------------------------------------

class TestFormatReport:
    """Tests for the format_report() function."""

    def _make_result(self, rule_violations=None, style_violations=None, warnings=None, issues_found=0):
        """Helper to build a result dict matching StyleReviewer output."""
        return {
            'issues_found': issues_found,
            'rule_violations': rule_violations or [],
            'style_violations': style_violations or [],
            'warnings': warnings or [],
            'corrected_content': '',
        }

    def test_no_issues(self):
        result = self._make_result()
        report = format_report(result, 'lecture.md', dry_run=False)
        assert 'No issues found' in report
        assert 'Issues found:** 0' in report

    def test_rule_violations_dry_run(self):
        """In dry-run mode, rule violations appear as 'Rule Violations'."""
        violations = [{
            'rule_id': 'qe-writing-001',
            'rule_title': 'One sentence per paragraph',
            'location': 'Line 42',
            'description': 'Paragraph has multiple sentences',
            'current_text': 'First sentence. Second sentence.',
            'suggested_fix': 'First sentence.\n\nSecond sentence.',
            'explanation': 'Split into separate paragraphs',
        }]
        result = self._make_result(rule_violations=violations, issues_found=1)
        report = format_report(result, 'lecture.md', dry_run=True)

        assert 'Rule Violations' in report
        assert 'without `--dry-run`' in report
        assert 'qe-writing-001' in report
        assert 'Line 42' in report
        assert 'First sentence. Second sentence.' in report
        assert 'Suggested fix' in report

    def test_rule_violations_fix_mode(self):
        """In default (fix) mode, rule violations appear as 'Applied Fixes'."""
        violations = [{
            'rule_id': 'qe-math-001',
            'rule_title': 'UTF-8 unicode',
            'location': 'Line 10',
            'description': 'Use unicode',
            'current_text': '$\\alpha$',
            'suggested_fix': 'α',
            'explanation': 'Replace with unicode',
        }]
        result = self._make_result(rule_violations=violations, issues_found=1)
        report = format_report(result, 'lecture.md', dry_run=False)

        assert 'Applied Fixes' in report
        assert 'automatically fixed' in report
        assert 'Applied fix' in report

    def test_style_suggestions(self):
        suggestions = [{
            'rule_id': 'qe-writing-002',
            'rule_title': 'Clarity',
            'location': 'Line 50',
            'description': 'Could be clearer',
            'current_text': 'Some text',
            'suggested_fix': 'Clearer text',
            'explanation': 'Improves readability',
        }]
        result = self._make_result(style_violations=suggestions, issues_found=1)
        report = format_report(result, 'my-lecture.md', dry_run=False)

        assert 'Style Suggestions' in report
        assert 'human review' in report
        assert 'qe-writing-002' in report

    def test_suggestions_appear_before_fixes(self):
        """Style suggestions should appear BEFORE applied fixes in the report."""
        rule_v = [{'rule_id': 'qe-math-001', 'rule_title': 'Unicode'}]
        style_v = [{'rule_id': 'qe-writing-002', 'rule_title': 'Clarity'}]
        result = self._make_result(
            rule_violations=rule_v,
            style_violations=style_v,
            issues_found=2,
        )
        report = format_report(result, 'test.md', dry_run=False)

        suggestions_pos = report.index('Style Suggestions')
        fixes_pos = report.index('Applied Fixes')
        assert suggestions_pos < fixes_pos, "Suggestions should appear before Applied Fixes"

    def test_warnings_included(self):
        result = self._make_result(warnings=['Fix quality warning: text too short'])
        report = format_report(result, 'lecture.md', dry_run=False)

        assert 'Warnings (1)' in report
        assert 'Fix quality warning' in report

    def test_mixed_results(self):
        rule_v = [{'rule_id': 'qe-math-001', 'rule_title': 'Unicode'}]
        style_v = [{'rule_id': 'qe-writing-002', 'rule_title': 'Clarity'}]
        result = self._make_result(
            rule_violations=rule_v,
            style_violations=style_v,
            warnings=['Some warning'],
            issues_found=2,
        )
        report = format_report(result, 'test.md', dry_run=False)

        assert 'Applied Fixes' in report
        assert 'Style Suggestions' in report
        assert 'Warnings (1)' in report

    def test_report_header(self):
        result = self._make_result()
        report = format_report(result, 'path/to/my-lecture.md', dry_run=False)

        assert 'my-lecture.md' in report
        assert f'v{__version__}' in report

    def test_report_includes_mode(self):
        """Report should indicate whether fixes were applied or dry-run."""
        result = self._make_result()
        report_fix = format_report(result, 'lecture.md', dry_run=False)
        report_dry = format_report(result, 'lecture.md', dry_run=True)

        assert 'fix' in report_fix.lower()
        assert 'dry-run' in report_dry

    def test_missing_optional_fields(self):
        """Violations with missing optional fields should not crash."""
        violations = [{'rule_id': 'qe-code-001', 'rule_title': 'PEP8'}]
        result = self._make_result(rule_violations=violations, issues_found=1)
        report = format_report(result, 'lecture.md', dry_run=False)

        assert 'qe-code-001' in report


# ---------------------------------------------------------------------------
# default_report_path tests
# ---------------------------------------------------------------------------

class TestDefaultReportPath:
    """Tests for the default_report_path() function."""

    def test_basic_all(self):
        path = default_report_path(Path('/tmp/lecture.md'))
        assert path == Path('/tmp/qestyle(all)-lecture.md')

    def test_single_category(self):
        path = default_report_path(Path('/tmp/lecture.md'), 'writing')
        assert path == Path('/tmp/qestyle(writing)-lecture.md')

    def test_nested_path(self):
        path = default_report_path(Path('/home/user/lectures/my-lecture.md'), 'math')
        assert path == Path('/home/user/lectures/qestyle(math)-my-lecture.md')

    def test_preserves_parent_dir(self):
        path = default_report_path(Path('lectures/intro.md'))
        assert path.parent == Path('lectures')
        assert path.name == 'qestyle(all)-intro.md'


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# check_git_dirty tests
# ---------------------------------------------------------------------------

class TestCheckGitDirty:
    """Tests for the check_git_dirty() function."""

    def test_clean_file_returns_false(self):
        """A committed file with no changes should return False."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Set up a git repo with a clean file
            subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
            f = Path(tmpdir) / "lecture.md"
            f.write_text("# Clean")
            subprocess.run(["git", "add", "."], cwd=tmpdir, capture_output=True)
            subprocess.run(["git", "commit", "-m", "init"], cwd=tmpdir, capture_output=True)
            assert check_git_dirty(f) is False

    def test_modified_file_returns_true(self):
        """A modified but uncommitted file should return True."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True)
            f = Path(tmpdir) / "lecture.md"
            f.write_text("# Original")
            subprocess.run(["git", "add", "."], cwd=tmpdir, capture_output=True)
            subprocess.run(["git", "commit", "-m", "init"], cwd=tmpdir, capture_output=True)
            # Modify the file
            f.write_text("# Modified")
            assert check_git_dirty(f) is True

    def test_untracked_file_returns_true(self):
        """An untracked file should return True (has status output)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True)
            f = Path(tmpdir) / "new-lecture.md"
            f.write_text("# New")
            assert check_git_dirty(f) is True

    def test_not_a_git_repo_returns_false(self):
        """A file outside a git repo should return False (skip check)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            f = Path(tmpdir) / "lecture.md"
            f.write_text("# Test")
            assert check_git_dirty(f) is False


# ---------------------------------------------------------------------------
# Category validation tests
# ---------------------------------------------------------------------------

class TestCategories:
    """Tests for category validation."""

    def test_all_categories_present(self):
        """ALL_CATEGORIES should match the 8 standard categories."""
        expected = {'writing', 'math', 'code', 'jax', 'figures', 'references', 'links', 'admonitions'}
        assert set(ALL_CATEGORIES) == expected

    def test_all_categories_count(self):
        assert len(ALL_CATEGORIES) == 8


# ---------------------------------------------------------------------------
# CLI invocation tests (subprocess)
# ---------------------------------------------------------------------------

class TestCLIInvocation:
    """Tests for the qestyle command-line interface."""

    def test_version_flag(self):
        result = subprocess.run(
            ['qestyle', '--version'],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert __version__ in result.stdout

    def test_help_flag(self):
        result = subprocess.run(
            ['qestyle', '--help'],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert 'categories' in result.stdout
        assert '--dry-run' in result.stdout

    def test_missing_file_exits_with_error(self):
        result = subprocess.run(
            ['qestyle', 'nonexistent-file.md'],
            capture_output=True, text=True,
            env={**__import__('os').environ, 'ANTHROPIC_API_KEY': 'fake-key'}
        )
        assert result.returncode != 0
        assert 'not found' in result.stderr.lower() or 'not found' in result.stdout.lower()

    def test_invalid_category_exits_with_error(self):
        # Create a temp file so the file-not-found check passes
        tmp = Path('/tmp/qestyle-test-lecture.md')
        tmp.write_text('# Test\n\nHello world.')
        try:
            result = subprocess.run(
                ['qestyle', str(tmp), '--categories', 'invalid_cat'],
                capture_output=True, text=True,
                env={**__import__('os').environ, 'ANTHROPIC_API_KEY': 'fake-key'}
            )
            assert result.returncode != 0
            assert 'invalid' in result.stderr.lower()
        finally:
            tmp.unlink(missing_ok=True)

    def test_missing_api_key_exits_with_error(self):
        tmp = Path('/tmp/qestyle-test-lecture.md')
        tmp.write_text('# Test\n\nHello world.')
        # Remove ANTHROPIC_API_KEY from env
        import os
        env = {k: v for k, v in os.environ.items() if k != 'ANTHROPIC_API_KEY'}
        try:
            result = subprocess.run(
                ['qestyle', str(tmp), '--categories', 'writing'],
                capture_output=True, text=True,
                env=env
            )
            assert result.returncode != 0
            assert 'ANTHROPIC_API_KEY' in result.stderr
        finally:
            tmp.unlink(missing_ok=True)
