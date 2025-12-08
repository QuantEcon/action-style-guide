#!/usr/bin/env python3
"""
Build category-specific rule files from style-guide-database.md

This script:
1. Parses style-guide-database.md to extract rules by group
2. Generates individual rule files for each category in rules/ folder
3. Adds appropriate headers for LLM context

Usage:
    python build_rules.py

Output:
    Creates/updates files in tool-style-guide-development/rules/
    These can then be copied to ../../style_checker/rules/ for the action
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class Rule:
    """Represents a single rule from the database"""
    rule_id: str
    rule_type: str  # rule, style, or migrate
    title: str
    group: str
    full_text: str  # Complete markdown for this rule


def parse_database(db_path: Path) -> Dict[str, List[Rule]]:
    """
    Parse style-guide-database.md and group rules by category.
    
    Returns:
        Dictionary mapping group names (e.g., 'WRITING') to list of Rule objects
    """
    with open(db_path, 'r') as f:
        content = f.read()
    
    # Find group sections using GROUP markers
    group_pattern = r'<!-- GROUP:(\w+)-START -->(.+?)<!-- GROUP:\1-END -->'
    groups = {}
    
    for match in re.finditer(group_pattern, content, re.DOTALL):
        group_name = match.group(1)  # e.g., 'WRITING'
        group_content = match.group(2)
        
        # Extract individual rules from this group
        rules = extract_rules_from_group(group_content, group_name)
        if rules:
            groups[group_name] = rules
    
    return groups


def extract_rules_from_group(group_content: str, group_name: str) -> List[Rule]:
    """
    Extract individual rules from a group section.
    
    Each rule starts with ### Rule: qe-group-NNN
    """
    rules = []
    
    # Split by rule headers (### Rule:)
    rule_pattern = r'### Rule: (qe-\w+-\d+)\s*\n\*\*Type:\*\*\s*(\w+)\s*\n\*\*Title:\*\*\s*(.+?)\n((?:.|\n)*?)(?=### Rule:|$)'
    
    for match in re.finditer(rule_pattern, group_content):
        rule_id = match.group(1)
        rule_type = match.group(2)
        title = match.group(3).strip()
        rule_body = match.group(4).strip()
        
        # Reconstruct the full rule markdown
        full_text = f"### Rule: {rule_id}\n"
        full_text += f"**Type:** {rule_type}  \n"
        full_text += f"**Title:** {title}\n\n"
        full_text += rule_body
        
        rules.append(Rule(
            rule_id=rule_id,
            rule_type=rule_type,
            title=title,
            group=group_name,
            full_text=full_text
        ))
    
    return rules


def generate_rule_file_header(category: str) -> str:
    """
    Generate the header for a category-specific rule file.
    
    This matches the format in style_checker/rules/*.md
    """
    category_display = category.title()
    
    header = f"""# {category_display} Style Rules

This document contains detailed {category.lower()} style rules for QuantEcon lectures.

## Purpose

These rules are used by the style checker to identify and fix {category.lower()}-related issues in lecture content.

## Rule Format

Each rule includes:
- **Rule ID**: Unique identifier (e.g., qe-{category.lower()}-001)
- **Type**: Classification (rule/style/migrate)
- **Title**: Brief description
- **Description**: Detailed explanation
- **Check for**: Specific patterns to look for
- **Examples**: Good vs bad examples
- **Implementation notes**: How to detect/fix

---

"""
    return header


def build_rule_files(groups: Dict[str, List[Rule]], output_dir: Path):
    """
    Build individual rule files for each category.
    
    Args:
        groups: Dictionary mapping group names to rules
        output_dir: Directory to write rule files to
    """
    output_dir.mkdir(exist_ok=True)
    
    # Map group names to category filenames
    category_map = {
        'WRITING': 'writing',
        'MATH': 'math',
        'CODE': 'code',
        'JAX': 'jax',
        'FIGURES': 'figures',
        'REFERENCES': 'references',
        'LINKS': 'links',
        'ADMONITIONS': 'admonitions'
    }
    
    for group_name, rules in groups.items():
        if group_name not in category_map:
            print(f"⚠️  Warning: Unknown group '{group_name}', skipping")
            continue
        
        category = category_map[group_name]
        output_file = output_dir / f"{category}-rules.md"
        
        # Generate file content
        content = generate_rule_file_header(category)
        
        # Add all rules for this category
        for i, rule in enumerate(rules):
            if i > 0:
                content += "\n---\n\n"
            content += rule.full_text + "\n"
        
        # Write file
        with open(output_file, 'w') as f:
            f.write(content)
        
        print(f"✓ Created {output_file.name} ({len(rules)} rules)")


def main():
    """Main entry point"""
    script_dir = Path(__file__).parent
    db_path = script_dir / "style-guide-database.md"
    output_dir = script_dir / "rules"
    
    print("="*60)
    print("Building category-specific rule files")
    print("="*60)
    print()
    
    # Check database exists
    if not db_path.exists():
        print(f"❌ Error: {db_path} not found")
        return 1
    
    print(f"📖 Reading: {db_path}")
    
    # Parse database
    groups = parse_database(db_path)
    print(f"✓ Found {len(groups)} categories")
    print()
    
    # Show what we found
    for group_name, rules in sorted(groups.items()):
        print(f"  • {group_name}: {len(rules)} rules")
    print()
    
    # Build rule files
    print(f"📝 Writing to: {output_dir}")
    build_rule_files(groups, output_dir)
    
    print()
    print("="*60)
    print("✅ Done!")
    print("="*60)
    print()
    print("Next steps:")
    print("1. Review generated files in tool-style-guide-development/rules/")
    print("2. Copy to action: cp rules/*.md ../style_checker/rules/")
    print()
    
    return 0


if __name__ == "__main__":
    exit(main())
