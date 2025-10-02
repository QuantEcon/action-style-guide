"""
Style Guide Rule Parser (DEPRECATED)
Loads and parses the style-guide.yaml database

DEPRECATED: This module is deprecated. Use parser_md.py instead for the new 
Markdown-based style guide database (style-guide-database.md).

The YAML format has been replaced with Markdown for better alignment with LLM prompts
and the new category system (rule/style/migrate).
"""

import yaml
import warnings
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path

# Issue deprecation warning when module is imported
warnings.warn(
    "parser.py is deprecated. Use parser_md.py for the new Markdown-based style guide database.",
    DeprecationWarning,
    stacklevel=2
)


@dataclass
class StyleRule:
    """Represents a single style guide rule"""
    rule_id: str
    title: str
    category: str
    type: str
    priority: str
    rule: str
    examples: Optional[Dict[str, Any]] = None
    forbidden: Optional[str] = None
    note: Optional[str] = None
    example: Optional[str] = None
    
    def to_prompt_format(self) -> str:
        """Convert rule to format suitable for LLM prompts"""
        prompt = f"**{self.rule_id}** ({self.title})\n"
        prompt += f"Category: {self.category} | Priority: {self.priority}\n"
        prompt += f"Rule: {self.rule}\n"
        
        if self.examples:
            prompt += f"Examples: {self.examples}\n"
        if self.example:
            prompt += f"Example: {self.example}\n"
        if self.forbidden:
            prompt += f"❌ Forbidden: {self.forbidden}\n"
        if self.note:
            prompt += f"📝 Note: {self.note}\n"
        
        return prompt


@dataclass
class StyleGuideDatabase:
    """Complete style guide database"""
    metadata: Dict[str, Any]
    rules: Dict[str, StyleRule]
    categories: List[str]
    priority_levels: Dict[str, str]
    critical_rules: List[str]
    mandatory_rules: List[str]
    best_practice_rules: List[str]
    preference_rules: List[str]
    
    def get_rules_by_category(self, category: str) -> List[StyleRule]:
        """Get all rules in a specific category"""
        return [rule for rule in self.rules.values() if rule.category == category]
    
    def get_rules_by_priority(self, priority: str) -> List[StyleRule]:
        """Get all rules with specific priority"""
        return [rule for rule in self.rules.values() if rule.priority == priority]
    
    def get_critical_rules(self) -> List[StyleRule]:
        """Get all critical rules"""
        return [self.rules[rule_id] for rule_id in self.critical_rules if rule_id in self.rules]
    
    def get_all_rules(self) -> List[StyleRule]:
        """Get all rules sorted by priority"""
        priority_order = {'critical': 0, 'mandatory': 1, 'best_practice': 2, 'preference': 3}
        return sorted(
            self.rules.values(),
            key=lambda r: (priority_order.get(r.priority, 4), r.rule_id)
        )


def load_style_guide(yaml_path: str) -> StyleGuideDatabase:
    """
    Load and parse the style guide YAML file
    
    Args:
        yaml_path: Path to style-guide.yaml file
        
    Returns:
        StyleGuideDatabase object
    """
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    # Parse rules
    rules = {}
    for rule_id, rule_data in data.get('rules', {}).items():
        rules[rule_id] = StyleRule(
            rule_id=rule_id,
            title=rule_data.get('title', ''),
            category=rule_data.get('category', ''),
            type=rule_data.get('type', ''),
            priority=rule_data.get('priority', ''),
            rule=rule_data.get('rule', ''),
            examples=rule_data.get('examples'),
            forbidden=rule_data.get('forbidden'),
            note=rule_data.get('note'),
            example=rule_data.get('example')
        )
    
    return StyleGuideDatabase(
        metadata=data.get('metadata', {}),
        rules=rules,
        categories=data.get('rule_categories', []),
        priority_levels=data.get('priority_levels', {}),
        critical_rules=data.get('critical_rules', []),
        mandatory_rules=data.get('mandatory_rules', []),
        best_practice_rules=data.get('best_practice_rules', []),
        preference_rules=data.get('preference_rules', [])
    )


def format_rules_for_llm(rules: List[StyleRule], max_rules: int = 15) -> List[str]:
    """
    Format rules into chunks suitable for LLM context windows
    
    Args:
        rules: List of StyleRule objects
        max_rules: Maximum rules per chunk
        
    Returns:
        List of formatted rule strings
    """
    chunks = []
    current_chunk = []
    
    for rule in rules:
        current_chunk.append(rule.to_prompt_format())
        
        if len(current_chunk) >= max_rules:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
    
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks
