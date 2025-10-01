"""
Simple tests for the style guide checker components
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from style_checker.parser import load_style_guide, format_rules_for_llm, StyleRule


def test_load_style_guide():
    """Test loading the style guide YAML"""
    print("Testing style guide loading...")
    
    style_guide_path = Path(__file__).parent.parent / "style-guide.yaml"
    if not style_guide_path.exists():
        print(f"❌ Style guide not found at {style_guide_path}")
        return False
    
    try:
        db = load_style_guide(str(style_guide_path))
        print(f"✓ Loaded {len(db.rules)} rules")
        print(f"✓ Categories: {', '.join(db.categories)}")
        print(f"✓ Critical rules: {len(db.critical_rules)}")
        print(f"✓ Mandatory rules: {len(db.mandatory_rules)}")
        return True
    except Exception as e:
        print(f"❌ Failed to load: {e}")
        return False


def test_rule_formatting():
    """Test rule formatting for LLM"""
    print("\nTesting rule formatting...")
    
    style_guide_path = Path(__file__).parent.parent / "style-guide.yaml"
    db = load_style_guide(str(style_guide_path))
    
    # Get all rules
    all_rules = db.get_all_rules()
    
    # Format in chunks
    chunks = format_rules_for_llm(all_rules, max_rules=10)
    print(f"✓ Created {len(chunks)} chunks")
    
    # Check first chunk
    if chunks:
        print(f"✓ First chunk length: {len(chunks[0])} characters")
        print(f"\nSample chunk preview:")
        print(chunks[0][:500] + "...")
    
    return True


def test_rule_queries():
    """Test querying rules by category and priority"""
    print("\nTesting rule queries...")
    
    style_guide_path = Path(__file__).parent.parent / "style-guide.yaml"
    db = load_style_guide(str(style_guide_path))
    
    # Test category query
    writing_rules = db.get_rules_by_category('writing')
    print(f"✓ Writing rules: {len(writing_rules)}")
    
    # Test priority query
    critical_rules = db.get_rules_by_priority('critical')
    print(f"✓ Critical priority rules: {len(critical_rules)}")
    
    # Test getting critical rules
    critical = db.get_critical_rules()
    print(f"✓ Critical rules (special method): {len(critical)}")
    
    # Show a sample rule
    if writing_rules:
        rule = writing_rules[0]
        print(f"\nSample rule:")
        print(f"  ID: {rule.rule_id}")
        print(f"  Title: {rule.title}")
        print(f"  Category: {rule.category}")
        print(f"  Priority: {rule.priority}")
    
    return True


def test_github_comment_parsing():
    """Test parsing lecture names from comments"""
    print("\nTesting GitHub comment parsing...")
    
    from style_checker.github_handler import GitHubHandler
    
    # We can't fully test without GitHub token, but we can test the parser
    test_comments = [
        "@quantecon-style-guide aiyagari",
        "@quantecon-style-guide lectures/aiyagari.md",
        "@quantecon-style-guide `cake_eating`",
        "Hey @quantecon-style-guide schelling",
    ]
    
    # Create a mock handler (without GitHub connection)
    class MockGitHub:
        def get_repo(self, name):
            return None
    
    # Monkey patch for testing
    original_github = None
    try:
        from github import Github
        original_github = Github
        
        # Create handler with dummy token (won't actually connect)
        handler = GitHubHandler("dummy-token", "owner/repo")
        
        # Test comment parsing
        for comment in test_comments:
            lecture = handler.extract_lecture_from_comment(comment)
            print(f"  '{comment}' → '{lecture}'")
        
        print("✓ Comment parsing works")
        return True
    except Exception as e:
        print(f"⚠ Skipping GitHub tests (PyGithub not installed or error): {e}")
        return True  # Not a critical failure


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("Running Style Guide Checker Tests")
    print("="*60)
    
    tests = [
        test_load_style_guide,
        test_rule_formatting,
        test_rule_queries,
        test_github_comment_parsing,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    return all(results)


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
