#!/usr/bin/env python3
"""
Initialize and verify the actions-style-guide repository setup
"""

import sys
import yaml
from pathlib import Path


def check_file_exists(path: str, description: str) -> bool:
    """Check if a file exists"""
    if Path(path).exists():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description} missing: {path}")
        return False


def validate_yaml(path: str) -> bool:
    """Validate YAML file"""
    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        print(f"✓ Valid YAML: {path}")
        return True
    except Exception as e:
        print(f"✗ Invalid YAML in {path}: {e}")
        return False


def count_rules(style_guide_path: str) -> int:
    """Count rules in Markdown style guide"""
    try:
        with open(style_guide_path, 'r') as f:
            content = f.read()
        # Count lines that start with "### Rule: qe-" (rule headers)
        import re
        rules = re.findall(r'^### (?:Rule|Style|Migration Pattern): qe-\w+-\d+', content, re.MULTILINE)
        return len(rules)
    except:
        return 0


def main():
    """Main verification"""
    print("=" * 60)
    print("QuantEcon Style Guide Checker - Setup Verification")
    print("=" * 60)
    print()
    
    checks_passed = 0
    total_checks = 0
    
    # Check core files
    print("📁 Checking Core Files...")
    files_to_check = [
        ("action.yml", "GitHub Action definition"),
        ("tool-style-guide-development/style-guide-database.md", "Style guide rules database"),
        ("requirements.txt", "Python dependencies"),
        ("README.md", "Main documentation"),
        ("LICENSE", "License file"),
    ]
    
    for path, desc in files_to_check:
        total_checks += 1
        if check_file_exists(path, desc):
            checks_passed += 1
    print()
    
    # Check Python package
    print("🐍 Checking Python Package...")
    python_files = [
        ("style_checker/__init__.py", "Package init"),
        ("style_checker/parser_md.py", "Markdown rule parser"),
        ("style_checker/reviewer.py", "LLM reviewer"),
        ("style_checker/github_handler.py", "GitHub handler"),
        ("style_checker/main.py", "Main orchestrator"),
    ]
    
    for path, desc in python_files:
        total_checks += 1
        if check_file_exists(path, desc):
            checks_passed += 1
    print()
    
    # Check documentation
    print("📚 Checking Documentation...")
    doc_files = [
        ("CONTRIBUTING.md", "Contributing guide"),
        ("CHANGELOG.md", "Changelog"),
        ("docs/quickstart.md", "Quick start guide"),
        ("docs/github-app-setup.md", "GitHub App setup"),
    ]
    
    for path, desc in doc_files:
        total_checks += 1
        if check_file_exists(path, desc):
            checks_passed += 1
    print()
    
    # Check examples
    print("📋 Checking Examples...")
    example_files = [
        ("examples/style-guide-comment.yml", "Comment trigger workflow"),
        ("examples/style-guide-weekly.yml", "Weekly review workflow"),
    ]
    
    for path, desc in example_files:
        total_checks += 1
        if check_file_exists(path, desc):
            checks_passed += 1
    print()
    
    # Validate YAML files
    print("🔍 Validating YAML Files...")
    yaml_files = [
        "action.yml",
        "examples/style-guide-comment.yml",
        "examples/style-guide-weekly.yml",
    ]
    
    for yaml_file in yaml_files:
        total_checks += 1
        if Path(yaml_file).exists() and validate_yaml(yaml_file):
            checks_passed += 1
    print()
    
    # Count rules from development database
    print("📊 Style Guide Statistics...")
    db_path = "tool-style-guide-development/style-guide-database.md"
    rule_count = count_rules(db_path)
    if rule_count > 0:
        print(f"✓ Found {rule_count} style guide rules in {db_path}")
        checks_passed += 1
    else:
        print(f"✗ No rules found in {db_path}")
    total_checks += 1
    print()
    
    # Final summary
    print("=" * 60)
    print(f"Results: {checks_passed}/{total_checks} checks passed")
    print("=" * 60)
    
    if checks_passed == total_checks:
        print("\n✅ All checks passed! Repository is ready.")
        print("\n📝 Next Steps:")
        print("1. Review docs/quickstart.md for setup instructions")
        print("2. Add API key secrets to your GitHub repository")
        print("3. Copy example workflows to lecture repositories")
        print("4. Test with: @quantecon-style-guide <lecture-name>")
        return 0
    else:
        print(f"\n⚠️  {total_checks - checks_passed} checks failed.")
        print("Please review the errors above and fix any issues.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
