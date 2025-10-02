"""
Tests for the Markdown style guide database parser
Tests parsing of the new style-guide-database.md format
"""

import sys
import os
from pathlib import Path
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from style_checker.parser_md import load_style_guide, StyleRule


@pytest.fixture
def style_guide_path():
    """Fixture to provide the style guide path"""
    # Look for the style guide in the attachments directory or root
    possible_paths = [
        Path(__file__).parent.parent / "style-guide-database.md",
        Path("/Users/mmcky/work/quantecon/QuantEcon.manual/manual/style-guide-database.md")
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    pytest.skip("Style guide database not found")


@pytest.fixture
def style_guide_db(style_guide_path):
    """Fixture to provide loaded style guide database"""
    return load_style_guide(str(style_guide_path))


def test_load_markdown_style_guide(style_guide_path):
    """Test loading the style guide Markdown"""
    assert style_guide_path.exists(), f"Style guide not found at {style_guide_path}"
    
    db = load_style_guide(str(style_guide_path))
    
    # Verify database is loaded
    assert db is not None
    assert len(db.rules) > 0, "No rules loaded"
    assert len(db.groups) > 0, "No groups found"
    
    # Check metadata
    assert 'total_rules' in db.metadata
    assert db.metadata['total_rules'] > 0
    
    print(f"✓ Loaded {len(db.rules)} rules")
    print(f"✓ Groups: {', '.join(db.groups.keys())}")
    print(f"✓ Total rules in metadata: {db.metadata['total_rules']}")
    print(f"✓ Actionable rules: {db.metadata.get('actionable_rules', 0)}")


def test_category_filtering(style_guide_db):
    """Test filtering by category (rule, style, migrate)"""
    # Get actionable rules (category='rule')
    actionable = style_guide_db.get_actionable_rules()
    assert len(actionable) > 0, "No actionable rules found"
    
    # Verify all are category='rule'
    for rule in actionable:
        assert rule.category == 'rule', f"Rule {rule.rule_id} has wrong category: {rule.category}"
        assert rule.is_actionable(), f"Rule {rule.rule_id} should be actionable"
    
    # Get style rules
    style_rules = style_guide_db.get_rules_by_category('style')
    
    # Get migrate rules
    migrate_rules = style_guide_db.get_rules_by_category('migrate')
    
    # Verify total
    total = len(actionable) + len(style_rules) + len(migrate_rules)
    assert total == len(style_guide_db.rules), "Category counts don't match total"
    
    print(f"✓ Actionable rules (rule): {len(actionable)}")
    print(f"✓ Advisory rules (style): {len(style_rules)}")
    print(f"✓ Migration rules (migrate): {len(migrate_rules)}")
    print(f"✓ Total: {total}")


def test_group_extraction(style_guide_db):
    """Test group membership extraction"""
    # Check expected groups
    expected_groups = ['WRITING', 'MATH', 'CODE', 'JAX', 'FIGURES', 'REFERENCES', 'LINKS', 'ADMONITIONS']
    
    for group in expected_groups:
        assert group in style_guide_db.groups, f"Group {group} not found"
        rules = style_guide_db.get_rules_by_group(group)
        assert len(rules) > 0, f"No rules in group {group}"
    
    print(f"✓ All expected groups found")
    for group in expected_groups:
        rules = style_guide_db.get_rules_by_group(group)
        print(f"  - {group}: {len(rules)} rules")


def test_rule_structure(style_guide_db):
    """Test that rules have correct structure"""
    all_rules = style_guide_db.get_all_rules()
    assert len(all_rules) > 0, "No rules to test"
    
    # Check first few rules
    for rule in all_rules[:5]:
        assert hasattr(rule, 'rule_id'), "Rule missing rule_id"
        assert hasattr(rule, 'category'), "Rule missing category"
        assert hasattr(rule, 'title'), "Rule missing title"
        assert hasattr(rule, 'description'), "Rule missing description"
        assert hasattr(rule, 'check_for'), "Rule missing check_for"
        assert hasattr(rule, 'examples'), "Rule missing examples"
        assert hasattr(rule, 'group'), "Rule missing group"
        
        # Verify category is valid
        assert rule.category in ['rule', 'style', 'migrate'], f"Invalid category: {rule.category}"
        
        # Verify rule_id format
        assert rule.rule_id.startswith('qe-'), f"Invalid rule_id format: {rule.rule_id}"
        
        print(f"✓ Rule {rule.rule_id}: {rule.title} ({rule.category})")


def test_rule_formatting(style_guide_db):
    """Test rule formatting for LLM prompts"""
    # Get actionable rules only
    actionable_rules = style_guide_db.get_actionable_rules()
    assert len(actionable_rules) > 0, "No actionable rules to format"
    
    # Test that each rule can be formatted for prompts
    for rule in actionable_rules[:5]:  # Test first 5 rules
        formatted = rule.to_prompt_format()
        
        assert len(formatted) > 0, "Formatted rule should not be empty"
        assert isinstance(formatted, str), "Formatted rule should be a string"
        
        # Verify formatted text contains key information
        assert rule.rule_id in formatted, "Should contain rule ID"
        assert rule.title in formatted, "Should contain title"
        assert "**Category:**" in formatted, "Should contain category"
        assert rule.category in formatted, "Should contain category value"
    
    print(f"✓ Successfully formatted {len(actionable_rules)} actionable rules")
    print(f"✓ Sample rule format length: {len(actionable_rules[0].to_prompt_format())} characters")


def test_specific_rule_codes(style_guide_db):
    """Test that specific expected rules exist"""
    expected_rules = [
        'qe-writing-001',  # One sentence per paragraph
        'qe-math-001',     # UTF-8 unicode for parameters
        'qe-code-001',     # PEP8
        'qe-fig-003',      # No matplotlib titles
        'qe-ref-001',      # Citation style
    ]
    
    for rule_id in expected_rules:
        assert rule_id in style_guide_db.rules, f"Expected rule {rule_id} not found"
        rule = style_guide_db.rules[rule_id]
        print(f"✓ Found {rule_id}: {rule.title}")


def test_rule_counts_match_documentation(style_guide_db):
    """Test that rule counts match documentation claims"""
    # According to the "Using This Database" section:
    # - 48 rules total
    # - 31 actionable (category='rule')
    # - 13 advisory (category='style')
    # - 4 migration (category='migrate')
    
    total_rules = len(style_guide_db.rules)
    actionable = len(style_guide_db.get_actionable_rules())
    style_rules = len(style_guide_db.get_rules_by_category('style'))
    migrate_rules = len(style_guide_db.get_rules_by_category('migrate'))
    
    print(f"Total rules: {total_rules} (expected ~48)")
    print(f"Actionable: {actionable} (expected ~31)")
    print(f"Style: {style_rules} (expected ~13)")
    print(f"Migrate: {migrate_rules} (expected ~4)")
    
    # Allow some variance in case rules were added/removed
    assert 40 <= total_rules <= 60, f"Total rules ({total_rules}) outside expected range"
    assert 25 <= actionable <= 40, f"Actionable rules ({actionable}) outside expected range"
    assert actionable + style_rules + migrate_rules == total_rules


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
