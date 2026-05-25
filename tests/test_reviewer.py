"""
Tests for reviewer.py — extract_individual_rules() and RULE_EVALUATION_ORDER
"""

from pathlib import Path

import style_checker
from style_checker.categories import VALID_CATEGORIES
from style_checker.reviewer import (
    extract_individual_rules,
    RULE_EVALUATION_ORDER,
)


PROMPTS_DIR = Path(style_checker.__file__).parent / "prompts"


# Expected rule counts per category (from rule files)
EXPECTED_RULE_COUNTS = {
    'writing': 8,
    'math': 9,
    'code': 6,
    'jax': 7,
    'figures': 11,
    'references': 1,
    'links': 2,
    'admonitions': 5,
}


class TestExtractIndividualRules:
    """Test rule extraction from markdown files"""

    def test_all_categories_extract(self):
        """Every category should extract at least one rule"""
        for category in VALID_CATEGORIES:
            rules = extract_individual_rules(category)
            assert len(rules) > 0, f"No rules extracted for '{category}'"

    def test_rule_counts_match(self):
        """Each category should have the expected number of rules"""
        for category, expected_count in EXPECTED_RULE_COUNTS.items():
            rules = extract_individual_rules(category)
            assert len(rules) == expected_count, \
                f"'{category}': expected {expected_count} rules, got {len(rules)}"

    def test_total_rule_count(self):
        """Total rules across all categories should be 49"""
        total = sum(
            len(extract_individual_rules(cat))
            for cat in VALID_CATEGORIES
        )
        assert total == 49

    def test_rule_has_required_fields(self):
        """Each rule dict should have rule_id, rule_type, title, content"""
        rules = extract_individual_rules('writing')
        for rule in rules:
            assert 'rule_id' in rule, f"Missing rule_id: {rule}"
            assert 'rule_type' in rule, f"Missing rule_type: {rule}"
            assert 'title' in rule, f"Missing title: {rule}"
            assert 'content' in rule, f"Missing content: {rule}"

    def test_rule_type_values(self):
        """Rule types should only be 'rule', 'style', or 'migrate'"""
        for category in VALID_CATEGORIES:
            rules = extract_individual_rules(category)
            for rule in rules:
                assert rule['rule_type'] in ('rule', 'style', 'migrate'), \
                    f"{rule['rule_id']} has invalid type: {rule['rule_type']}"

    def test_rule_id_format(self):
        """Rule IDs should follow qe-category-NNN pattern"""
        for category in VALID_CATEGORIES:
            rules = extract_individual_rules(category)
            for rule in rules:
                assert rule['rule_id'].startswith('qe-'), \
                    f"Rule ID doesn't start with 'qe-': {rule['rule_id']}"

    def test_no_duplicate_rule_ids(self):
        """No duplicate rule IDs across all categories"""
        all_ids = []
        for category in VALID_CATEGORIES:
            rules = extract_individual_rules(category)
            all_ids.extend(r['rule_id'] for r in rules)
        assert len(all_ids) == len(set(all_ids)), \
            f"Duplicate rule IDs found: {[x for x in all_ids if all_ids.count(x) > 1]}"

    def test_nonexistent_category_returns_empty(self):
        """A nonexistent category should return empty list"""
        assert extract_individual_rules('nonexistent') == []


class TestRuleEvaluationOrder:
    """Test RULE_EVALUATION_ORDER configuration"""

    def test_rule_evaluation_order_keys_match_valid_categories(self):
        """RULE_EVALUATION_ORDER must have exactly the same keys as VALID_CATEGORIES,
        in the same order. Catches drift between the two when either is edited."""
        assert tuple(RULE_EVALUATION_ORDER.keys()) == tuple(VALID_CATEGORIES), (
            "RULE_EVALUATION_ORDER keys diverged from VALID_CATEGORIES.\n"
            f"  RULE_EVALUATION_ORDER: {tuple(RULE_EVALUATION_ORDER.keys())}\n"
            f"  VALID_CATEGORIES:      {tuple(VALID_CATEGORIES)}"
        )

    def test_all_categories_have_order(self):
        """Every valid category should have an evaluation order defined"""
        for category in VALID_CATEGORIES:
            assert category in RULE_EVALUATION_ORDER, \
                f"'{category}' missing from RULE_EVALUATION_ORDER"

    def test_order_matches_extracted_rules(self):
        """Evaluation order should include exactly the rules in the rule files"""
        for category in VALID_CATEGORIES:
            rules = extract_individual_rules(category)
            extracted_ids = [r['rule_id'] for r in rules]
            ordered_ids = RULE_EVALUATION_ORDER[category]
            assert set(extracted_ids) == set(ordered_ids), \
                f"'{category}': order has {set(ordered_ids) - set(extracted_ids)} extra, " \
                f"missing {set(extracted_ids) - set(ordered_ids)}"

    def test_evaluation_order_is_respected(self):
        """extract_individual_rules should return rules in RULE_EVALUATION_ORDER"""
        for category in VALID_CATEGORIES:
            rules = extract_individual_rules(category)
            ids = [r['rule_id'] for r in rules]
            expected = RULE_EVALUATION_ORDER[category]
            assert ids == expected, \
                f"'{category}': rules not in evaluation order.\n" \
                f"  Expected: {expected}\n" \
                f"  Got:      {ids}"

    def test_no_extra_ids_in_order(self):
        """RULE_EVALUATION_ORDER should not reference nonexistent rules"""
        for category, order in RULE_EVALUATION_ORDER.items():
            rules = extract_individual_rules(category)
            existing_ids = {r['rule_id'] for r in rules}
            for rule_id in order:
                assert rule_id in existing_ids, \
                    f"'{category}': '{rule_id}' in order but not in rule file"


class TestPromptFile:
    """Test the single shared prompt file used by create_single_rule_prompt.

    Replaces coverage from the deleted test_prompt_loader.py — but for a
    single consolidated prompt instead of one file per category.
    """

    def test_prompt_file_exists(self):
        """create_single_rule_prompt() raises FileNotFoundError at runtime if
        the prompt file is missing — assert at test time so we catch packaging
        regressions before they hit production."""
        prompt_file = PROMPTS_DIR / "prompt.md"
        assert prompt_file.exists(), \
            f"Shared prompt file missing: {prompt_file}"

    def test_prompt_file_has_version_header(self):
        """The prompt should carry a `<!-- Prompt Version: X.Y.Z ... -->` comment
        so logs can record which prompt produced a given review."""
        content = (PROMPTS_DIR / "prompt.md").read_text()
        assert "Prompt Version:" in content, \
            "prompt.md missing the 'Prompt Version: ...' header comment"


class TestRuleTypeCounts:
    """Test that rule type distribution matches expectations"""

    def test_rule_type_count(self):
        """Should have 32 'rule' type rules"""
        count = sum(
            1 for cat in VALID_CATEGORIES
            for r in extract_individual_rules(cat)
            if r['rule_type'] == 'rule'
        )
        assert count == 32

    def test_style_type_count(self):
        """Should have 13 'style' type rules"""
        count = sum(
            1 for cat in VALID_CATEGORIES
            for r in extract_individual_rules(cat)
            if r['rule_type'] == 'style'
        )
        assert count == 13

    def test_migrate_type_count(self):
        """Should have 4 'migrate' type rules"""
        count = sum(
            1 for cat in VALID_CATEGORIES
            for r in extract_individual_rules(cat)
            if r['rule_type'] == 'migrate'
        )
        assert count == 4
