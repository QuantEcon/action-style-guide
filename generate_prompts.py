#!/usr/bin/env python3
"""
DEPRECATED: This script is no longer used.

We now use hand-written focused prompts from tool-style-checker instead of
auto-generating them from style-guide-database.md.

The focused approach:
- Concise instruction prompts in style_checker/prompts/
- Detailed rules in style_checker/rules/
- Much smaller and more effective

If you need to update prompts or rules, edit the files directly in:
- style_checker/prompts/ (instruction templates)
- style_checker/rules/ (detailed rule specifications)

These files are maintained manually for better quality and smaller size.
"""

import sys

if __name__ == "__main__":
    print("=" * 70)
    print("DEPRECATED SCRIPT")
    print("=" * 70)
    print()
    print("This script is no longer used.")
    print()
    print("We now use hand-written focused prompts copied from tool-style-checker.")
    print()
    print("To update prompts or rules:")
    print("  - Edit files in style_checker/prompts/ (instruction templates)")
    print("  - Edit files in style_checker/rules/ (detailed rules)")
    print()
    print("=" * 70)
    sys.exit(1)
