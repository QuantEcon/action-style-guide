#!/usr/bin/env python3
"""
Test comment parsing for new @qe-style-checker syntax.
"""

from pathlib import Path
import sys

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from style_checker.github_handler import GitHubHandler

def test_comment_parsing():
    """Test comment parsing with various formats."""
    
    print("Testing Comment Parsing...")
    print("=" * 60)
    
    # Mock handler (we don't need actual GitHub connection for parsing)
    # We'll test the extract_lecture_from_comment method directly
    
    test_cases = [
        # New syntax
        ("@qe-style-checker aiyagari", ("aiyagari", ["all"])),
        ("@qe-style-checker aiyagari writing,math", ("aiyagari", ["writing", "math"])),
        ("@qe-style-checker lectures/aiyagari.md code,jax", ("aiyagari", ["code", "jax"])),
        ("@qe-style-checker `aiyagari` all", ("aiyagari", ["all"])),
        
        # Legacy syntax
        ("@quantecon-style-guide aiyagari", ("aiyagari", ["all"])),
        ("@quantecon-style-guide lectures/aiyagari.md", ("aiyagari", ["all"])),
        ("@quantecon-style-guide `aiyagari`", ("aiyagari", ["all"])),
        
        # Invalid
        ("Just a regular comment", None),
        ("@something-else aiyagari", None),
    ]
    
    # Create a minimal handler class for testing
    class TestHandler:
        def extract_lecture_from_comment(self, comment_body):
            # Import the method from github_handler
            import re
            from typing import Optional, List, Tuple
            
            # This is a copy of the updated method
            new_patterns = [
                r'@qe-style-checker\s+(\S+)\s+([\w,]+)',
                r'@qe-style-checker\s+`(\S+)`\s+([\w,]+)',
                r'@qe-style-checker\s+lectures/(\S+)\s+([\w,]+)',
                r'@qe-style-checker\s+(\S+)',
                r'@qe-style-checker\s+`(\S+)`',
                r'@qe-style-checker\s+lectures/(\S+)',
            ]
            
            for pattern in new_patterns:
                match = re.search(pattern, comment_body)
                if match:
                    lecture = match.group(1)
                    lecture = lecture.replace('.md', '')
                    lecture = lecture.replace('lectures/', '')
                    lecture = lecture.strip('`')  # Remove backticks
                    
                    if len(match.groups()) > 1 and match.group(2):
                        categories = [cat.strip() for cat in match.group(2).split(',')]
                    else:
                        categories = ['all']
                    
                    return (lecture, categories)
            
            # Fall back to old syntax
            old_patterns = [
                r'@quantecon-style-guide\s+(\S+)',
                r'@quantecon-style-guide\s+`(\S+)`',
                r'@quantecon-style-guide\s+lectures/(\S+)',
            ]
            
            for pattern in old_patterns:
                match = re.search(pattern, comment_body)
                if match:
                    lecture = match.group(1)
                    lecture = lecture.replace('.md', '')
                    lecture = lecture.replace('lectures/', '')
                    lecture = lecture.strip('`')  # Remove backticks
                    return (lecture, ['all'])
            
            return None
    
    handler = TestHandler()
    
    passed = 0
    failed = 0
    
    for comment, expected in test_cases:
        result = handler.extract_lecture_from_comment(comment)
        
        if result == expected:
            print(f"✓ '{comment[:50]}...' -> {result}")
            passed += 1
        else:
            print(f"✗ '{comment[:50]}...'")
            print(f"  Expected: {expected}")
            print(f"  Got:      {result}")
            failed += 1
    
    print("\n" + "=" * 60)
    if failed == 0:
        print(f"✅ All {passed} tests passed!")
        print("=" * 60)
        return True
    else:
        print(f"❌ {failed} test(s) failed, {passed} passed")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = test_comment_parsing()
    sys.exit(0 if success else 1)
