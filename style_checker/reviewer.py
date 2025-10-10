"""
LLM-based Style Checker using Claude Sonnet 4.5
Uses Markdown format for LLM responses (more reliable than JSON for long content)
Applies fixes programmatically instead of relying on LLM-generated corrected content
Uses markdown-based prompt templates for simplicity and maintainability
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from .fix_applier import apply_fixes, validate_fix_quality
from .prompt_loader import load_prompt


# Rule evaluation order - defines the sequence for checking rules
# This order is optimized for best results: mechanical → structural → stylistic → creative
RULE_EVALUATION_ORDER = {
    'writing': [
        'qe-writing-008',  # Whitespace formatting (mechanical)
        'qe-writing-001',  # Paragraph structure (structural)
        'qe-writing-004',  # Capitalization (mechanical)
        'qe-writing-006',  # Title capitalization (mechanical)
        'qe-writing-005',  # Bold/italic formatting (mechanical)
        'qe-writing-002',  # Clarity and conciseness (stylistic)
        'qe-writing-003',  # Logical flow (creative)
        'qe-writing-007',  # Visual elements (creative)
    ],
    # Other categories can be added here with their optimal order
    # 'math': ['qe-math-001', 'qe-math-002', ...],
}


def extract_individual_rules(category: str) -> List[Dict[str, str]]:
    """
    Extract individual rules from a category rules file.
    
    Returns rules in the optimal evaluation order defined by RULE_EVALUATION_ORDER.
    If no order is specified for a category, returns rules in file order.
    
    Args:
        category: Category name (e.g., 'writing', 'math')
        
    Returns:
        List of dicts with 'rule_id', 'title', and 'content' for each rule, 
        sorted by evaluation priority
    """
    rules_dir = Path(__file__).parent / "rules"
    rules_file = rules_dir / f"{category}-rules.md"
    
    if not rules_file.exists():
        return []
    
    with open(rules_file, 'r') as f:
        content = f.read()
    
    # Extract individual rules using regex
    # Pattern matches: ### Rule: qe-writing-001 ... until next ### Rule: or end
    rule_pattern = r'### Rule: (qe-[a-z]+-\d+)\s*\n\*\*Category:\*\* (rule|style)\s*\n\*\*Title:\*\* ([^\n]+)\s*\n(.+?)(?=\n### Rule: |$)'
    
    # First, extract all rules into a dict keyed by rule_id
    rules_dict = {}
    for match in re.finditer(rule_pattern, content, re.DOTALL):
        rule_id = match.group(1)
        rule_category = match.group(2).strip()  # 'rule' or 'style'
        title = match.group(3).strip()
        rule_content = match.group(4).strip()
        
        # Reconstruct the full rule markdown
        full_rule = f"### Rule: {rule_id}\n**Category:** {rule_category}\n**Title:** {title}\n\n{rule_content}"
        
        rules_dict[rule_id] = {
            'rule_id': rule_id,
            'rule_category': rule_category,  # NEW: Store rule category
            'title': title,
            'content': full_rule
        }
    
    # If we have a defined evaluation order for this category, use it
    if category in RULE_EVALUATION_ORDER:
        ordered_rules = []
        for rule_id in RULE_EVALUATION_ORDER[category]:
            if rule_id in rules_dict:
                ordered_rules.append(rules_dict[rule_id])
        
        # Add any rules not in the priority list (shouldn't happen, but defensive)
        for rule_id, rule_data in rules_dict.items():
            if rule_id not in RULE_EVALUATION_ORDER[category]:
                ordered_rules.append(rule_data)
        
        return ordered_rules
    else:
        # No defined order, return in file order
        return list(rules_dict.values())


def create_single_rule_prompt(category: str, rule: Dict[str, str], lecture_content: str) -> str:
    """
    Create a focused prompt for checking a single rule.
    
    Args:
        category: Category name (e.g., 'writing')
        rule: Dict with 'rule_id', 'title', and 'content'
        lecture_content: The lecture to check
        
    Returns:
        Complete prompt focused on one specific rule
    """
    # Load the base prompt (without rules)
    prompts_dir = Path(__file__).parent / "prompts"
    prompt_file = prompts_dir / f"{category}-prompt.md"
    
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    
    with open(prompt_file, 'r') as f:
        base_prompt = f.read()
    
    # Create focused prompt with single rule
    focused_prompt = f"""{base_prompt}

## Style Rule to Check

**IMPORTANT**: Check ONLY for violations of this specific rule. Do not check other rules.

{rule['content']}

## Lecture to Review

{lecture_content}
"""
    
    return focused_prompt

def parse_markdown_response(response: str) -> Dict[str, Any]:
    """
    Parse structured Markdown response from LLM into dict format.
    
    Expected format:
    # Review Results
    
    ## Summary
    <summary text>
    
    ## Issues Found
    <number>
    
    ## Violations
    
    ###Violation 1: <rule_id> - <rule_title>
    - **Severity:** <severity>
    - **Location:** <location>
    - **Description:** <description>
    - **Current text:**
    ```
    <current_text>
    ```
    - **Suggested fix:**
    ```
    <suggested_fix>
    ```
    - **Explanation:** <explanation>
    
    [... more violations ...]
    
    ## Corrected Content
    
    ```markdown
    <corrected_content>
    ```
    
    Returns:
        Dictionary with parsed review results
    """
    result = {
        'issues_found': 0,
        'violations': [],
        'corrected_content': '',
        'summary': ''
    }
    
    try:
        # Extract summary
        summary_match = re.search(r'## Summary\s*\n(.+?)(?=\n##|\Z)', response, re.DOTALL)
        if summary_match:
            result['summary'] = summary_match.group(1).strip()
        
        # Extract issues count
        issues_match = re.search(r'## Issues Found\s*\n(\d+)', response)
        if issues_match:
            result['issues_found'] = int(issues_match.group(1))
        
        # Extract violations
        violations_section = re.search(r'## Violations\s*\n(.+?)(?=\n## Corrected Content|\Z)', response, re.DOTALL)
        if violations_section:
            violations_text = violations_section.group(1)
            
            # Parse individual violations
            violation_pattern = r'### Violation \d+: ([^\n]+)\n(.+?)(?=\n### Violation|\Z)'
            for match in re.finditer(violation_pattern, violations_text, re.DOTALL):
                header = match.group(1)
                body = match.group(2)
                
                # Parse rule_id and title from header
                header_parts = header.split(' - ', 1)
                rule_id = header_parts[0].strip()
                rule_title = header_parts[1].strip() if len(header_parts) > 1 else ''
                
                violation = {
                    'rule_id': rule_id,
                    'rule_title': rule_title
                }
                
                # Extract fields from violation body
                severity_match = re.search(r'\*\*Severity:\*\*\s*(.+)', body)
                if severity_match:
                    violation['severity'] = severity_match.group(1).strip()
                
                location_match = re.search(r'\*\*Location:\*\*\s*(.+)', body)
                if location_match:
                    violation['location'] = location_match.group(1).strip()
                
                desc_match = re.search(r'\*\*Description:\*\*\s*(.+?)(?=\n\*\*|\Z)', body, re.DOTALL)
                if desc_match:
                    violation['description'] = desc_match.group(1).strip()
                
                # Extract current text (in code block)
                current_match = re.search(r'\*\*Current text:\*\*\s*\n```[^\n]*\n(.+?)\n```', body, re.DOTALL)
                if current_match:
                    violation['current_text'] = current_match.group(1).strip()
                
                # Extract suggested fix (in code block)
                fix_match = re.search(r'\*\*Suggested fix:\*\*\s*\n```[^\n]*\n(.+?)\n```', body, re.DOTALL)
                if fix_match:
                    violation['suggested_fix'] = fix_match.group(1).strip()
                
                # Extract explanation
                expl_match = re.search(r'\*\*Explanation:\*\*\s*(.+?)(?=\n\*\*|\n###|\Z)', body, re.DOTALL)
                if expl_match:
                    violation['explanation'] = expl_match.group(1).strip()
                
                result['violations'].append(violation)
        
        # Note: Corrected content is not extracted from LLM response anymore
        # Fixes are applied programmatically using apply_fixes() function
        # This reduces output tokens by ~50% and matches tool-style-checker approach
        
    except Exception as e:
        result['error'] = f'Markdown parsing failed: {str(e)}'
    
    return result


class AnthropicProvider:
    """Anthropic Claude provider
    
    Uses Claude Sonnet 4.5 (claude-sonnet-4-5-20250929) by default.
    Supports up to 64,000 output tokens.
    
    For latest models and limits, see: https://docs.anthropic.com/en/docs/about-claude/models
    """
    
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        self.api_key = api_key
        self.model = model
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
    
    def check_style(self, content: str, categories: List[str]) -> Dict[str, Any]:
        """Check style using Anthropic Claude with automatic streaming for large requests"""
        # Load prompt using category-specific templates
        prompt = load_prompt(categories, content)
        
        # Try non-streaming first, fall back to streaming if required
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=64000,
                messages=[{"role": "user", "content": prompt}]
            )
            full_response = response.content[0].text
        except Exception as e:
            # If we get the streaming error, use streaming
            if "Streaming is required" in str(e) or "10 minutes" in str(e):
                print(f"    ℹ️  Using streaming for large request...")
                full_response = ""
                with self.client.messages.stream(
                    model=self.model,
                    max_tokens=64000,
                    messages=[{"role": "user", "content": prompt}]
                ) as stream:
                    for text in stream.text_stream:
                        full_response += text
            else:
                # Re-raise if it's a different error
                raise
        
        # Parse the Markdown response
        return parse_markdown_response(full_response)
    
    def check_single_rule(self, prompt: str) -> Dict[str, Any]:
        """Check a single rule using provided prompt"""
        # Try non-streaming first, fall back to streaming if required
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=64000,
                messages=[{"role": "user", "content": prompt}]
            )
            full_response = response.content[0].text
        except Exception as e:
            # If we get the streaming error, use streaming
            if "Streaming is required" in str(e) or "10 minutes" in str(e):
                full_response = ""
                with self.client.messages.stream(
                    model=self.model,
                    max_tokens=64000,
                    messages=[{"role": "user", "content": prompt}]
                ) as stream:
                    for text in stream.text_stream:
                        full_response += text
            else:
                # Re-raise if it's a different error
                raise
        
        # Parse the Markdown response
        return parse_markdown_response(full_response)


class StyleReviewer:
    """Main style reviewer using Claude Sonnet 4.5"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize reviewer with Claude Sonnet 4.5
        
        Args:
            api_key: Anthropic API key (or will use ANTHROPIC_API_KEY environment variable)
            model: Specific Claude model to use (default: claude-sonnet-4-5-20250929)
        """
        self.provider_name = 'claude'
        
        # Get API key from parameter or environment
        if not api_key:
            api_key = os.environ.get('ANTHROPIC_API_KEY')
        
        if not api_key:
            raise ValueError("No API key provided. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter")
        
        # Initialize Claude provider
        self.provider = AnthropicProvider(api_key, model) if model else AnthropicProvider(api_key)
    
    def review_lecture_single_rule(
        self,
        content: str,
        categories: List[str],
        lecture_name: str
    ) -> Dict[str, Any]:
        """
        Review a lecture by checking each rule individually.
        
        This approach guarantees comprehensive coverage by evaluating one rule at a time.
        Applies fixes after each rule, so subsequent rules check the updated content.
        More expensive (multiple LLM calls) but ensures no rules are skipped.
        
        Args:
            content: Full lecture content
            categories: List of category names to check (e.g., ["writing", "math"])
            lecture_name: Name of the lecture
            
        Returns:
            Dictionary with combined review results from all rules
        """
        all_violations = []
        rule_violations = []  # NEW: Track rule category violations (auto-apply)
        style_violations = []  # NEW: Track style category violations (suggestions only)
        all_warnings = []
        current_content = content  # Track the evolving content as fixes are applied
        
        for category in categories:
            print(f"  📋 Checking {category} rules individually...")
            rules = extract_individual_rules(category)
            
            if not rules:
                print(f"    ⚠️  No rules found for category: {category}")
                continue
            
            print(f"    ℹ️  Found {len(rules)} rules to check")
            
            for i, rule in enumerate(rules, 1):
                rule_id = rule['rule_id']
                rule_category = rule.get('rule_category', 'rule')  # NEW: Get rule category, default to 'rule'
                print(f"    ⏳ Checking {rule_id}: {rule['title']} ({i}/{len(rules)}) [category: {rule_category}]")
                
                try:
                    # Create focused prompt for this specific rule using CURRENT content
                    prompt = create_single_rule_prompt(category, rule, current_content)
                    
                    # Check this single rule
                    result = self.provider.check_single_rule(prompt)
                    
                    # Process violations from this rule
                    if result.get('violations'):
                        violations_count = len(result['violations'])
                        print(f"      ✓ Found {violations_count} violation(s)")
                        
                        # Validate fix quality
                        validation_warnings = validate_fix_quality(result['violations'])
                        if validation_warnings:
                            print(f"      ⚠️  Fix quality warnings: {len(validation_warnings)}")
                            all_warnings.extend(validation_warnings)
                        
                        # NEW: Separate by category - only auto-apply fixes for 'rule' category
                        if rule_category == 'rule':
                            # Apply fixes immediately to current content
                            corrected_content, apply_warnings = apply_fixes(current_content, result['violations'])
                            
                            if apply_warnings:
                                all_warnings.extend(apply_warnings)
                            
                            # Update current content for next rule
                            if corrected_content != current_content:
                                current_content = corrected_content
                                print(f"      ✓ Applied {violations_count} fix(es) automatically - content updated for next rule")
                            else:
                                print(f"      ⚠️  Could not apply fixes - content unchanged")
                            
                            # Store rule violations for applied fixes report
                            rule_violations.extend(result['violations'])
                        else:
                            # Style category - collect suggestions but don't auto-apply
                            print(f"      ℹ️  Style suggestions collected (not auto-applied) - requires human review")
                            style_violations.extend(result['violations'])
                        
                        # Store all violations for comprehensive reporting
                        all_violations.extend(result['violations'])
                    else:
                        print(f"      ✓ No violations")
                        
                except Exception as e:
                    warning = f"Error checking {rule_id}: {str(e)}"
                    print(f"      ⚠️  {warning}")
                    all_warnings.append(warning)
        
        # Combine all results
        combined_result = {
            'issues_found': len(all_violations),
            'violations': all_violations,
            'rule_violations': rule_violations,  # NEW: Automatic fixes applied
            'style_violations': style_violations,  # NEW: Suggestions for human review
            'provider': self.provider_name,
            'lecture_name': lecture_name,
            'warnings': all_warnings,
            'corrected_content': current_content  # Final content after all rule fixes
        }
        
        return combined_result
    
    def review_lecture(
        self,
        content: str,
        categories: List[str],
        lecture_name: str
    ) -> Dict[str, Any]:
        """
        Review a lecture against specified style categories.
        
        Args:
            content: Full lecture content
            categories: List of category names to check (e.g., ["writing", "math"] or ["all"])
            lecture_name: Name of the lecture
            
        Returns:
            Dictionary with review results and corrected content
        """
        try:
            result = self.provider.check_style(content, categories)
            result['provider'] = self.provider_name
            result['lecture_name'] = lecture_name
            
            # Apply fixes programmatically if we have violations
            if result.get('violations'):
                print(f"  🔧 Applying {len(result['violations'])} fixes programmatically...")
                
                # Validate fix quality
                validation_warnings = validate_fix_quality(result['violations'])
                if validation_warnings:
                    print(f"  ⚠️  Fix quality warnings:")
                    for warning in validation_warnings[:5]:  # Show first 5
                        print(f"      - {warning}")
                
                # Apply fixes
                corrected_content, apply_warnings = apply_fixes(content, result['violations'])
                result['corrected_content'] = corrected_content
                result['fix_warnings'] = apply_warnings
                
                # If we couldn't apply any fixes, keep original content
                if corrected_content == content and result['violations']:
                    print(f"  ⚠️  Could not apply any fixes - keeping original content")
                    result['corrected_content'] = content
            else:
                # No violations, keep original content
                result['corrected_content'] = content
            
            return result
        except Exception as e:
            return {
                'error': str(e),
                'issues_found': 0,
                'violations': [],
                'corrected_content': content,  # Return original on error
                'provider': self.provider_name,
                'lecture_name': lecture_name
            }
    
    def review_lecture_smart(
        self,
        content: str,
        lecture_name: str
    ) -> Dict[str, Any]:
        """
        Smart review strategy using sequential category processing.
        
        Processes categories one at a time, feeding the updated document from
        one category into the next. This matches the tool-style-checker approach
        and ensures all fixes are applied without conflicts.
        
        Benefits:
        - All fixes applied without conflicts
        - Later categories see changes from earlier categories
        - More coherent final output
        - No skipped fixes due to overlapping changes
        
        Trade-off:
        - Slower than parallel processing (sequential API calls)
        - But more reliable and complete results
        
        Args:
            content: Full lecture content
            lecture_name: Name of the lecture file
            
        Returns:
            Dictionary with all violations found across all categories
        """
        print(f"\n🤖 Starting AI-powered review using sequential category processing...")
        print(f"📊 Lecture: {lecture_name}")
        
        # Define all categories to check (matches files in style_checker/rules/)
        categories = [
            'writing',
            'math',
            'code',
            'jax',
            'figures',
            'references',
            'links',
            'admonitions'
        ]
        
        print(f"\n📦 Processing {len(categories)} categories sequentially:")
        for category in categories:
            print(f"   • {category}")
        
        # Process categories sequentially, updating content after each
        all_violations = []
        current_content = content
        
        print(f"\n🔄 Processing categories one at a time...\n")
        
        for i, category in enumerate(categories, 1):
            print(f"  [{i}/{len(categories)}] Processing {category}...")
            
            try:
                result = self._review_category(
                    current_content,
                    category,
                    lecture_name
                )
                
                violations_count = len(result.get('violations', []))
                
                if violations_count > 0:
                    print(f"       ✓ Found {violations_count} issues")
                    
                    # Apply fixes from this category to current content
                    print(f"       🔧 Applying {violations_count} fixes...")
                    
                    # Validate fix quality
                    validation_warnings = validate_fix_quality(result.get('violations', []))
                    if validation_warnings:
                        print(f"       ⚠️  Fix quality warnings:")
                        for warning in validation_warnings[:3]:  # Show first 3
                            print(f"           - {warning}")
                    
                    # Apply fixes to current content
                    updated_content, fix_warnings = apply_fixes(
                        current_content, 
                        result.get('violations', [])
                    )
                    
                    if updated_content != current_content:
                        current_content = updated_content
                        print(f"       ✓ Updated document with {category} fixes")
                    else:
                        print(f"       ⚠️  No changes applied (possible conflicts)")
                    
                    # Track all violations for reporting
                    all_violations.extend(result.get('violations', []))
                else:
                    print(f"       ✓ No issues found")
                
            except Exception as e:
                print(f"       ❌ Failed: {e}")
        
        print(f"\n📊 Total issues found across all categories: {len(all_violations)}")
        
        if all_violations:
            print(f"  ✅ All fixes have been applied sequentially")
        else:
            print(f"  ✨ No issues found - lecture follows all style guide rules!")
        
        return {
            'issues_found': len(all_violations),
            'violations': all_violations,
            'corrected_content': current_content,
            'summary': f"Found {len(all_violations)} issues across {len(categories)} categories (processed sequentially)",
            'provider': self.provider_name,
            'lecture_name': lecture_name,
            'categories_checked': categories
        }
    
    def _review_category(
        self,
        content: str,
        category: str,
        lecture_name: str
    ) -> Dict[str, Any]:
        """
        Review lecture content against a single category of rules.
        
        Uses markdown-based category prompts from style_checker/rules/
        
        Args:
            content: Full lecture content
            category: Name of the category (e.g., 'writing', 'math')
            lecture_name: Name of the lecture file
            
        Returns:
            Dictionary with violations found for this category
        """
        try:
            result = self.provider.check_style(content, [category])
            result['category'] = category
            return result
        except Exception as e:
            return {
                'error': str(e),
                'violations': [],
                'category': category
            }
