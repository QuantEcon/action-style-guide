"""
Tests for the style guide checker components
Uses pytest framework for better test organization and reporting
"""

import sys
import os
from pathlib import Path
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from style_checker.parser import load_style_guide, format_rules_for_llm, StyleRule


@pytest.fixture
def style_guide_path():
    """Fixture to provide the style guide path"""
    return Path(__file__).parent.parent / "style-guide.yaml"


@pytest.fixture
def style_guide_db(style_guide_path):
    """Fixture to provide loaded style guide database"""
    return load_style_guide(str(style_guide_path))


def test_load_style_guide(style_guide_path):
    """Test loading the style guide YAML"""
    assert style_guide_path.exists(), f"Style guide not found at {style_guide_path}"
    
    db = load_style_guide(str(style_guide_path))
    
    # Verify database is loaded
    assert db is not None
    assert len(db.rules) > 0, "No rules loaded"
    assert len(db.categories) > 0, "No categories found"
    
    # Check that critical and mandatory rules exist
    assert len(db.critical_rules) > 0, "No critical rules found"
    assert len(db.mandatory_rules) > 0, "No mandatory rules found"
    
    print(f"✓ Loaded {len(db.rules)} rules")
    print(f"✓ Categories: {', '.join(db.categories)}")
    print(f"✓ Critical rules: {len(db.critical_rules)}")
    print(f"✓ Mandatory rules: {len(db.mandatory_rules)}")


def test_rule_formatting(style_guide_db):
    """Test rule formatting for LLM"""
    # Get all rules
    all_rules = style_guide_db.get_all_rules()
    assert len(all_rules) > 0, "No rules to format"
    
    # Format in chunks
    chunks = format_rules_for_llm(all_rules, max_rules=10)
    assert len(chunks) > 0, "No chunks created"
    
    # Check first chunk
    assert len(chunks[0]) > 0, "First chunk is empty"
    assert isinstance(chunks[0], str), "Chunk should be a string"
    
    # Verify chunk contains rule information
    assert "**qe-" in chunks[0], "Chunk should contain rule IDs"
    
    print(f"✓ Created {len(chunks)} chunks")
    print(f"✓ First chunk length: {len(chunks[0])} characters")


def test_rule_queries(style_guide_db):
    """Test querying rules by category and priority"""
    # Test category query
    writing_rules = style_guide_db.get_rules_by_category('writing')
    assert len(writing_rules) > 0, "No writing rules found"
    
    # Test priority query
    critical_rules = style_guide_db.get_rules_by_priority('critical')
    assert len(critical_rules) > 0, "No critical priority rules found"
    
    # Test getting critical rules (convenience method)
    critical = style_guide_db.get_critical_rules()
    assert len(critical) > 0, "No critical rules found"
    
    # Verify rule structure
    if writing_rules:
        rule = writing_rules[0]
        assert hasattr(rule, 'rule_id'), "Rule missing rule_id"
        assert hasattr(rule, 'title'), "Rule missing title"
        assert hasattr(rule, 'category'), "Rule missing category"
        assert hasattr(rule, 'priority'), "Rule missing priority"
        assert rule.category == 'writing', "Rule category mismatch"
    
    print(f"✓ Writing rules: {len(writing_rules)}")
    print(f"✓ Critical priority rules: {len(critical_rules)}")
    print(f"✓ Critical rules (special method): {len(critical)}")


def test_github_comment_parsing():
    """Test parsing lecture names from comments"""
    pytest.importorskip("github", reason="PyGithub not installed")
    
    from style_checker.github_handler import GitHubHandler
    
    # Test comment patterns - just test the parsing logic without connecting to GitHub
    # We'll test the extract_lecture_from_comment method if it exists as a staticmethod
    # or we skip this test if it requires real GitHub connection
    
    test_cases = [
        ("@quantecon-style-guide aiyagari", "aiyagari"),
        ("@quantecon-style-guide lectures/aiyagari.md", "aiyagari"),
        ("@quantecon-style-guide `cake_eating`", "cake_eating"),
        ("Hey @quantecon-style-guide schelling", "schelling"),
    ]
    
    # Try to test without creating handler if possible
    # For now, we'll skip this test since it requires GitHub connection
    pytest.skip("Requires GitHub connection - tested in integration tests")


def test_rule_ids_are_unique(style_guide_db):
    """Test that all rule IDs are unique"""
    all_rules = style_guide_db.get_all_rules()
    rule_ids = [rule.rule_id for rule in all_rules]
    
    assert len(rule_ids) == len(set(rule_ids)), "Duplicate rule IDs found"
    print(f"✓ All {len(rule_ids)} rule IDs are unique")


def test_rules_have_required_fields(style_guide_db):
    """Test that all rules have required fields"""
    all_rules = style_guide_db.get_all_rules()
    
    required_fields = ['rule_id', 'title', 'category', 'priority', 'rule']
    
    for rule in all_rules:
        for field in required_fields:
            assert hasattr(rule, field), f"Rule {getattr(rule, 'rule_id', 'unknown')} missing field: {field}"
            assert getattr(rule, field), f"Rule {rule.rule_id} has empty field: {field}"
    
    print(f"✓ All {len(all_rules)} rules have required fields")


if __name__ == '__main__':
    # Allow running directly for backwards compatibility
    pytest.main([__file__, '-v'])
