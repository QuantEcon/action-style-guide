#!/usr/bin/env python3
"""
Quick test to verify the prompt-based architecture works correctly.
"""

from pathlib import Path
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from style_checker.prompt_loader import PromptLoader

def test_prompt_loader():
    """Test that prompt loader can load category-specific prompts."""
    
    print("Testing Prompt Loader...")
    print("=" * 60)
    
    loader = PromptLoader()
    
    # Test 1: Load single category
    print("\n1. Testing single category (math)...")
    test_content = "This is a test lecture with $\\alpha$ parameter."
    prompt = loader.load_prompt(["math"], test_content)
    
    assert "Math" in prompt, "Prompt should contain 'Math'"
    assert test_content in prompt, "Prompt should contain lecture content"
    print("   ✓ Single category works")
    
    # Test 2: Load multiple categories
    print("\n2. Testing multiple categories (writing, code)...")
    prompt = loader.load_prompt(["writing", "code"], test_content)
    
    assert "Writing" in prompt or "writing" in prompt.lower(), "Prompt should mention writing"
    assert "Code" in prompt or "code" in prompt.lower(), "Prompt should mention code"
    assert test_content in prompt, "Prompt should contain lecture content"
    print("   ✓ Multiple categories work")
    
    # Test 3: Load all categories
    print("\n3. Testing 'all' category...")
    prompt = loader.load_prompt(["all"], test_content)
    
    assert "Complete Style Guide" in prompt or "All Categories" in prompt, "Prompt should indicate comprehensive review"
    assert test_content in prompt, "Prompt should contain lecture content"
    print("   ✓ 'all' category works")
    
    # Test 4: Invalid category
    print("\n4. Testing invalid category...")
    try:
        loader.load_prompt(["invalid_category"], test_content)
        print("   ✗ Should have raised ValueError")
        return False
    except ValueError as e:
        print(f"   ✓ Correctly raised ValueError: {e}")
    
    # Test 5: Verify all valid categories exist
    print("\n5. Verifying all category files exist...")
    for category in PromptLoader.VALID_CATEGORIES:
        if category == "all":
            continue  # 'all' is special
        try:
            prompt = loader.load_prompt([category], "test")
            print(f"   ✓ {category}.md exists and loads")
        except FileNotFoundError:
            print(f"   ✗ {category}.md missing!")
            return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_prompt_loader()
    sys.exit(0 if success else 1)
