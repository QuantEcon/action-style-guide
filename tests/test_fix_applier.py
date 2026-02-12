"""
Tests for fix_applier.py — apply_fixes() and validate_fix_quality()
"""

from style_checker.fix_applier import apply_fixes, validate_fix_quality


class TestApplyFixes:
    """Test apply_fixes() function"""

    def test_single_fix_applied(self):
        """A single valid fix should be applied"""
        content = "This is the old text in a document."
        violations = [{
            'rule_id': 'qe-writing-001',
            'current_text': 'old text',
            'suggested_fix': 'new text',
            'location': 'paragraph 1',
        }]
        result, warnings, applied = apply_fixes(content, violations)
        assert result == "This is the new text in a document."
        assert len(warnings) == 0
        assert len(applied) == 1
        assert applied[0]['rule_id'] == 'qe-writing-001'

    def test_multiple_fixes_applied(self):
        """Multiple non-overlapping fixes should all be applied"""
        content = "Alpha is first. Beta is second."
        violations = [
            {
                'rule_id': 'qe-test-001',
                'current_text': 'Alpha',
                'suggested_fix': 'α',
                'location': 'line 1',
            },
            {
                'rule_id': 'qe-test-002',
                'current_text': 'Beta',
                'suggested_fix': 'β',
                'location': 'line 1',
            },
        ]
        result, warnings, applied = apply_fixes(content, violations)
        assert 'α' in result
        assert 'β' in result
        assert len(warnings) == 0
        assert len(applied) == 2

    def test_missing_current_text_skipped(self):
        """Violations without current_text should be skipped with warning"""
        content = "Unchanged content."
        violations = [{
            'rule_id': 'qe-test-001',
            'current_text': '',
            'suggested_fix': 'something',
        }]
        result, warnings, applied = apply_fixes(content, violations)
        assert result == content
        assert len(warnings) == 1
        assert 'No current_text' in warnings[0]
        assert len(applied) == 0

    def test_missing_suggested_fix_skipped(self):
        """Violations without suggested_fix should be skipped with warning"""
        content = "Some old text here."
        violations = [{
            'rule_id': 'qe-test-001',
            'current_text': 'old text',
            'suggested_fix': '',
        }]
        result, warnings, applied = apply_fixes(content, violations)
        assert result == content
        assert len(warnings) == 1
        assert 'No suggested_fix' in warnings[0]
        assert len(applied) == 0

    def test_text_not_found_skipped(self):
        """Violations where current_text isn't in content should be skipped"""
        content = "This content has nothing to match."
        violations = [{
            'rule_id': 'qe-test-001',
            'current_text': 'nonexistent text',
            'suggested_fix': 'replacement',
            'location': 'unknown',
        }]
        result, warnings, applied = apply_fixes(content, violations)
        assert result == content
        assert len(warnings) == 1
        assert 'Could not find' in warnings[0]
        assert len(applied) == 0

    def test_empty_violations_list(self):
        """Empty violations list should return content unchanged"""
        content = "Unchanged."
        result, warnings, applied = apply_fixes(content, [])
        assert result == content
        assert len(warnings) == 0
        assert len(applied) == 0

    def test_fix_replaces_only_first_occurrence(self):
        """Fix should apply to only the first occurrence"""
        content = "word word word"
        violations = [{
            'rule_id': 'qe-test-001',
            'current_text': 'word',
            'suggested_fix': 'WORD',
            'location': 'line 1',
        }]
        result, warnings, applied = apply_fixes(content, violations)
        # Only first 'word' replaced
        assert result == "WORD word word"
        assert len(applied) == 1

    def test_identical_text_skipped(self):
        """Violations where current_text == suggested_fix should be skipped (no-op)"""
        content = "We use α for the learning rate."
        violations = [{
            'rule_id': 'qe-code-002',
            'current_text': 'We use α for the learning rate.',
            'suggested_fix': 'We use α for the learning rate.',
            'location': 'line 29',
        }]
        result, warnings, applied = apply_fixes(content, violations)
        assert result == content  # Content unchanged
        assert len(applied) == 0  # Not counted as applied
        assert any('identical' in w.lower() or 'no change' in w.lower() for w in warnings)

    def test_identical_text_mixed_with_real_fixes(self):
        """Real fixes should apply while identical-text no-ops are skipped"""
        content = "Alpha is first. Same text stays."
        violations = [
            {
                'rule_id': 'qe-test-001',
                'current_text': 'Alpha',
                'suggested_fix': 'α',
                'location': 'line 1',
            },
            {
                'rule_id': 'qe-test-002',
                'current_text': 'Same text stays.',
                'suggested_fix': 'Same text stays.',
                'location': 'line 1',
            },
        ]
        result, warnings, applied = apply_fixes(content, violations)
        assert 'α is first' in result
        assert 'Same text stays.' in result
        assert len(applied) == 1
        assert applied[0]['rule_id'] == 'qe-test-001'


class TestValidateFixQuality:
    """Test validate_fix_quality() function"""

    def test_valid_violation_no_warnings(self):
        """A complete, valid violation should produce no warnings"""
        violations = [{
            'rule_id': 'qe-test-001',
            'current_text': 'This is old text with enough length.',
            'suggested_fix': 'This is new text with enough length.',
        }]
        warnings = validate_fix_quality(violations)
        assert len(warnings) == 0

    def test_missing_current_text_warning(self):
        """Missing current_text should produce warning"""
        violations = [{
            'rule_id': 'qe-test-001',
            'current_text': '',
            'suggested_fix': 'something',
        }]
        warnings = validate_fix_quality(violations)
        assert any('Missing current_text' in w for w in warnings)

    def test_missing_suggested_fix_warning(self):
        """Missing suggested_fix should produce warning"""
        violations = [{
            'rule_id': 'qe-test-001',
            'current_text': 'some text here',
            'suggested_fix': '',
        }]
        warnings = validate_fix_quality(violations)
        assert any('Missing suggested_fix' in w for w in warnings)

    def test_identical_text_warning(self):
        """Identical current_text and suggested_fix should warn"""
        violations = [{
            'rule_id': 'qe-test-001',
            'current_text': 'same text',
            'suggested_fix': 'same text',
        }]
        warnings = validate_fix_quality(violations)
        assert any('identical' in w for w in warnings)

    def test_short_current_text_warning(self):
        """Very short current_text should warn about ambiguous matches"""
        violations = [{
            'rule_id': 'qe-test-001',
            'current_text': 'hi',
            'suggested_fix': 'hello',
        }]
        warnings = validate_fix_quality(violations)
        assert any('very short' in w for w in warnings)

    def test_commentary_in_fix_warning(self):
        """Suggested fix containing commentary should warn"""
        violations = [{
            'rule_id': 'qe-test-001',
            'current_text': 'original code here',
            'suggested_fix': 'fixed code # NOTE: changed this',
        }]
        warnings = validate_fix_quality(violations)
        assert any('commentary' in w for w in warnings)
