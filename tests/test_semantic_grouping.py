"""
Test script for semantic grouping implementation
Tests that the new review_lecture_smart() method works correctly
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from style_checker.parser_md import load_style_guide


def test_group_extraction():
    """Test that groups are correctly extracted from the database"""
    print("=" * 60)
    print("Testing Group Extraction")
    print("=" * 60)
    
    # Load style guide
    style_guide_path = Path(__file__).parent.parent / "style-guide-database.md"
    if not style_guide_path.exists():
        print(f"❌ Style guide not found: {style_guide_path}")
        return False
    
    print(f"✓ Loading style guide from: {style_guide_path}")
    style_guide = load_style_guide(str(style_guide_path))
    
    # Check basic stats
    print(f"\n📊 Style Guide Statistics:")
    print(f"   Total rules: {len(style_guide.rules)}")
    print(f"   Total groups: {len(style_guide.groups)}")
    print(f"   Actionable rules: {len(style_guide.get_actionable_rules())}")
    
    # Test get_all_groups_with_rules
    print(f"\n📦 Testing get_all_groups_with_rules():")
    all_groups = style_guide.get_all_groups_with_rules()
    print(f"   Total groups: {len(all_groups)}")
    for group_name, rules in sorted(all_groups.items()):
        print(f"   • {group_name}: {len(rules)} rules")
    
    # Test with category filter
    print(f"\n📦 Testing get_all_groups_with_rules(category='rule'):")
    actionable_groups = style_guide.get_all_groups_with_rules(category='rule')
    print(f"   Actionable groups: {len(actionable_groups)}")
    total_actionable = 0
    for group_name, rules in sorted(actionable_groups.items()):
        print(f"   • {group_name}: {len(rules)} actionable rules")
        total_actionable += len(rules)
    
    print(f"\n   Total actionable rules across groups: {total_actionable}")
    
    # Verify counts match
    expected_actionable = len(style_guide.get_actionable_rules())
    if total_actionable == expected_actionable:
        print(f"   ✓ Count matches expected: {expected_actionable}")
    else:
        print(f"   ❌ Count mismatch! Expected {expected_actionable}, got {total_actionable}")
        return False
    
    return True


def test_reviewer_integration():
    """Test that StyleReviewer has the new method"""
    print("\n" + "=" * 60)
    print("Testing StyleReviewer Integration")
    print("=" * 60)
    
    from style_checker.reviewer import StyleReviewer
    
    # Check that the method exists
    if hasattr(StyleReviewer, 'review_lecture_smart'):
        print("✓ StyleReviewer.review_lecture_smart() method exists")
    else:
        print("❌ StyleReviewer.review_lecture_smart() method NOT found")
        return False
    
    # Check helper methods
    helper_methods = ['_review_group', '_format_rules_for_prompt', '_estimate_tokens']
    for method in helper_methods:
        if hasattr(StyleReviewer, method):
            print(f"✓ StyleReviewer.{method}() method exists")
        else:
            print(f"❌ StyleReviewer.{method}() method NOT found")
            return False
    
    return True


def test_imports():
    """Test that all necessary imports work"""
    print("\n" + "=" * 60)
    print("Testing Imports")
    print("=" * 60)
    
    try:
        from style_checker.parser_md import StyleGuideDatabase, StyleRule, load_style_guide
        print("✓ parser_md imports successful")
    except ImportError as e:
        print(f"❌ parser_md import failed: {e}")
        return False
    
    try:
        from style_checker.reviewer import StyleReviewer
        print("✓ reviewer imports successful")
    except ImportError as e:
        print(f"❌ reviewer import failed: {e}")
        return False
    
    try:
        from style_checker.main import review_single_lecture, review_bulk_lectures
        print("✓ main imports successful")
    except ImportError as e:
        print(f"❌ main import failed: {e}")
        return False
    
    return True


if __name__ == '__main__':
    print("🧪 Testing Semantic Grouping Implementation\n")
    
    tests = [
        ("Imports", test_imports),
        ("Group Extraction", test_group_extraction),
        ("Reviewer Integration", test_reviewer_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' raised exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Semantic grouping implementation is ready.")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
        sys.exit(1)
