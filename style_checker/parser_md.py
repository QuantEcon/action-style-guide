"""
Markdown Style Guide Rule Parser
Loads and parses the style-guide-database.md file
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class StyleRule:
    """Represents a single style guide rule from Markdown"""
    rule_id: str
    category: str  # 'rule', 'style', or 'migrate'
    title: str
    description: str
    check_for: List[str]
    examples: str
    implementation_note: Optional[str] = None
    guidance: Optional[str] = None
    exceptions: Optional[str] = None
    reference: Optional[str] = None
    group: Optional[str] = None  # e.g., 'WRITING', 'MATH', 'CODE', etc.
    
    def to_prompt_format(self) -> str:
        """Convert rule to format suitable for LLM prompts"""
        prompt = f"### {self.rule_id}: {self.title}\n"
        prompt += f"**Category:** {self.category}\n\n"
        prompt += f"**Description:**\n{self.description}\n\n"
        
        if self.check_for:
            prompt += "**Check for:**\n"
            for item in self.check_for:
                prompt += f"- {item}\n"
            prompt += "\n"
        
        if self.examples:
            prompt += f"**Examples:**\n{self.examples}\n\n"
        
        if self.implementation_note:
            prompt += f"**Implementation note:** {self.implementation_note}\n\n"
        
        if self.guidance:
            prompt += f"**Guidance:** {self.guidance}\n\n"
        
        if self.exceptions:
            prompt += f"**Exceptions:** {self.exceptions}\n\n"
        
        return prompt
    
    def is_actionable(self) -> bool:
        """Check if this rule should be actioned by LLM (category='rule')"""
        return self.category == 'rule'


@dataclass
class StyleGuideDatabase:
    """Complete style guide database from Markdown"""
    rules: Dict[str, StyleRule]
    groups: Dict[str, List[str]]  # group_name -> list of rule_ids
    metadata: Dict[str, Any]
    
    def get_rules_by_category(self, category: str) -> List[StyleRule]:
        """Get all rules in a specific category"""
        return [rule for rule in self.rules.values() if rule.category == category]
    
    def get_actionable_rules(self) -> List[StyleRule]:
        """Get all rules that should be actioned (category='rule')"""
        return self.get_rules_by_category('rule')
    
    def get_rules_by_group(self, group: str) -> List[StyleRule]:
        """Get all rules in a specific group"""
        rule_ids = self.groups.get(group.upper(), [])
        return [self.rules[rid] for rid in rule_ids if rid in self.rules]
    
    def get_all_groups_with_rules(self, category: Optional[str] = None) -> Dict[str, List[StyleRule]]:
        """
        Get all groups with their rules, optionally filtered by category
        
        Args:
            category: Optional category filter ('rule', 'style', or 'migrate')
            
        Returns:
            Dictionary mapping group names to lists of StyleRule objects
        """
        result = {}
        for group_name, rule_ids in self.groups.items():
            group_rules = [self.rules[rid] for rid in rule_ids if rid in self.rules]
            
            # Apply category filter if specified
            if category:
                group_rules = [r for r in group_rules if r.category == category]
            
            # Only include groups that have rules (after filtering)
            if group_rules:
                result[group_name] = group_rules
        
        return result
    
    def get_all_rules(self) -> List[StyleRule]:
        """Get all rules sorted by rule_id"""
        return sorted(self.rules.values(), key=lambda r: r.rule_id)


def parse_markdown_style_guide(md_path: str) -> StyleGuideDatabase:
    """
    Parse the Markdown style guide database
    
    Args:
        md_path: Path to style-guide-database.md file
        
    Returns:
        StyleGuideDatabase object
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    rules = {}
    groups = {}
    current_group = None
    
    # Extract metadata from top of file
    metadata = {
        'version': extract_version(content),
        'total_rules': 0,
        'groups': []
    }
    
    # Split content into rule sections
    # Rules start with ### Rule: <rule-id>
    rule_pattern = r'### Rule: (qe-[\w-]+)\n\*\*Category:\*\* (rule|style|migrate)'
    
    # Find all group markers (format: <!-- GROUP:NAME-START --> or <!-- GROUP:NAME-END -->)
    group_pattern = r'<!-- GROUP:([\w]+)-(START|END) -->'
    group_matches = list(re.finditer(group_pattern, content))
    
    # Build map of positions to groups (for each position, which group is it in?)
    # Simpler approach: find all GROUP-START markers and their positions
    group_starts = {}  # position -> group_name
    for match in group_matches:
        if match.group(2) == 'START':
            group_starts[match.end()] = match.group(1)
    
    # Parse each rule
    rule_matches = list(re.finditer(rule_pattern, content))
    
    for i, match in enumerate(rule_matches):
        rule_id = match.group(1)
        category = match.group(2)
        
        # Extract rule content
        start_pos = match.start()
        if i + 1 < len(rule_matches):
            end_pos = rule_matches[i + 1].start()
        else:
            # Last rule - find the end by looking for next major section
            next_section = re.search(r'\n## (?!#)', content[start_pos + 100:])
            if next_section:
                end_pos = start_pos + 100 + next_section.start()
            else:
                end_pos = len(content)
        
        rule_content = content[start_pos:end_pos]
        
        # Determine which group this rule belongs to by finding the most recent GROUP-START before it
        rule_group = None
        for group_pos in sorted(group_starts.keys(), reverse=True):
            if group_pos < start_pos:
                rule_group = group_starts[group_pos]
                break
        
        # Parse rule fields
        rule = parse_rule_section(rule_id, category, rule_content, rule_group)
        rules[rule_id] = rule
        
        # Track group membership
        if rule_group:
            if rule_group not in groups:
                groups[rule_group] = []
            groups[rule_group].append(rule_id)
    
    # Update metadata
    metadata['total_rules'] = len(rules)
    metadata['groups'] = list(groups.keys())
    metadata['actionable_rules'] = len([r for r in rules.values() if r.is_actionable()])
    
    return StyleGuideDatabase(
        rules=rules,
        groups=groups,
        metadata=metadata
    )


def extract_version(content: str) -> str:
    """Extract version from metadata"""
    match = re.search(r'## Version:\s*(.+)', content)
    return match.group(1).strip() if match else 'unknown'


def parse_rule_section(rule_id: str, category: str, content: str, group: Optional[str]) -> StyleRule:
    """Parse a single rule section from Markdown"""
    
    # Extract title (first line after rule_id line)
    title_match = re.search(r'### Rule: qe-[\w-]+\n\*\*Category:\*\*.+?\n\*\*Title:\*\* (.+)', content)
    title = title_match.group(1).strip() if title_match else ''
    
    # Extract description
    desc_match = re.search(r'\*\*Description:\*\*\s*\n(.+?)(?=\n\*\*|\n###|\n##|$)', content, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else ''
    
    # Extract "Check for" items
    check_for = []
    check_match = re.search(r'\*\*Check for:\*\*\s*\n((?:- .+\n?)+)', content)
    if check_match:
        check_items = check_match.group(1).strip().split('\n')
        check_for = [item.strip('- ').strip() for item in check_items if item.strip()]
    
    # Extract examples section (everything between **Examples:** and next ** or ###)
    examples_match = re.search(r'\*\*Examples:\*\*\s*\n(.+?)(?=\n\*\*(?!Example)|\n###|\n##|<!-- GROUP)', content, re.DOTALL)
    examples = examples_match.group(1).strip() if examples_match else ''
    
    # Extract implementation note
    impl_match = re.search(r'\*\*Implementation note:\*\*\s*\n(.+?)(?=\n\*\*|\n###|\n##|$)', content, re.DOTALL)
    implementation_note = impl_match.group(1).strip() if impl_match else None
    
    # Extract guidance
    guidance_match = re.search(r'\*\*Guidance:\*\*\s*\n(.+?)(?=\n\*\*|\n###|\n##|$)', content, re.DOTALL)
    guidance = guidance_match.group(1).strip() if guidance_match else None
    
    # Extract exceptions
    exceptions_match = re.search(r'\*\*Exceptions:\*\*\s*\n(.+?)(?=\n\*\*|\n###|\n##|$)', content, re.DOTALL)
    exceptions = exceptions_match.group(1).strip() if exceptions_match else None
    
    # Extract reference
    ref_match = re.search(r'\*\*Reference.*?:\*\*\s*\n(.+?)(?=\n\*\*|\n###|\n##|$)', content, re.DOTALL)
    reference = ref_match.group(1).strip() if ref_match else None
    
    return StyleRule(
        rule_id=rule_id,
        category=category,
        title=title,
        description=description,
        check_for=check_for,
        examples=examples,
        implementation_note=implementation_note,
        guidance=guidance,
        exceptions=exceptions,
        reference=reference,
        group=group
    )


def load_style_guide(md_path: str) -> StyleGuideDatabase:
    """
    Load and parse the style guide Markdown file
    
    Args:
        md_path: Path to style-guide-database.md file
        
    Returns:
        StyleGuideDatabase object
    """
    return parse_markdown_style_guide(md_path)
