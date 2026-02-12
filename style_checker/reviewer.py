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
    'math': [
        'qe-math-001',  # UTF-8 unicode for parameters (mechanical)
        'qe-math-002',  # Transpose notation (mechanical)
        'qe-math-003',  # Square brackets for matrices (mechanical)
        'qe-math-004',  # No bold face for matrices/vectors (mechanical)
        'qe-math-005',  # Curly brackets for sequences (mechanical)
        'qe-math-007',  # Automatic equation numbering (mechanical)
        'qe-math-006',  # Aligned environment for PDF (structural)
        'qe-math-008',  # Explain special notation (structural)
        'qe-math-009',  # Simplicity in notation (stylistic)
    ],
    'code': [
        'qe-code-002',  # Unicode Greek letters in code (mechanical)
        'qe-code-003',  # Package installation at top (structural)
        'qe-code-006',  # Binary package installation notes (structural)
        'qe-code-001',  # PEP8 / math notation (stylistic)
        'qe-code-004',  # quantecon Timer (migrate)
        'qe-code-005',  # quantecon timeit (migrate)
    ],
    'jax': [
        'qe-jax-002',  # NamedTuple for parameters (structural)
        'qe-jax-001',  # Functional programming patterns (stylistic)
        'qe-jax-003',  # generate_path for sequences (stylistic)
        'qe-jax-005',  # jax.lax for control flow (stylistic)
        'qe-jax-007',  # Consistent function naming (stylistic)
        'qe-jax-004',  # Functional update patterns (migrate)
        'qe-jax-006',  # Explicit PRNG key management (migrate)
    ],
    'figures': [
        'qe-fig-003',  # No matplotlib embedded titles (mechanical)
        'qe-fig-004',  # Caption formatting (mechanical)
        'qe-fig-005',  # Descriptive figure names (mechanical)
        'qe-fig-006',  # Lowercase axis labels (mechanical)
        'qe-fig-007',  # Keep figure box and spines (mechanical)
        'qe-fig-008',  # lw=2 for line charts (mechanical)
        'qe-fig-010',  # Plotly latex directive (structural)
        'qe-fig-011',  # Image directive when nested (structural)
        'qe-fig-009',  # Figure sizing (structural)
        'qe-fig-001',  # Figure size only when necessary (stylistic)
        'qe-fig-002',  # Prefer code-generated figures (stylistic)
    ],
    'references': [
        'qe-ref-001',  # Correct citation style (mechanical)
    ],
    'links': [
        'qe-link-002',  # Doc links for cross-series (mechanical)
        'qe-link-001',  # Markdown links for same series (stylistic)
    ],
    'admonitions': [
        'qe-admon-001',  # Gated syntax for exercises (structural)
        'qe-admon-003',  # Tick count for nested directives (mechanical)
        'qe-admon-004',  # prf prefix for proofs (mechanical)
        'qe-admon-005',  # Link solutions to exercises (structural)
        'qe-admon-002',  # Dropdown class for solutions (stylistic)
    ],
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
    rule_pattern = r'### Rule: (qe-[a-z]+-\d+)\s*\n\*\*Type:\*\* (rule|style|migrate)\s*\n\*\*Title:\*\* ([^\n]+)\s*\n(.+?)(?=\n### Rule: |$)'
    
    # First, extract all rules into a dict keyed by rule_id
    rules_dict = {}
    for match in re.finditer(rule_pattern, content, re.DOTALL):
        rule_id = match.group(1)
        rule_type = match.group(2).strip()  # 'rule' (auto-fix), 'style' (suggestion), or 'migrate' (modernize)
        title = match.group(3).strip()
        rule_content = match.group(4).strip()
        
        # Reconstruct the full rule markdown
        full_rule = f"### Rule: {rule_id}\n**Type:** {rule_type}\n**Title:** {title}\n\n{rule_content}"
        
        rules_dict[rule_id] = {
            'rule_id': rule_id,
            'rule_type': rule_type,  # 'rule' = auto-fix, 'style' = suggestion
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
        
        # Short-circuit: if Issues Found is 0, skip violation parsing entirely.
        # This prevents the LLM's "no change needed" commentary from being
        # treated as a suggested fix and replacing actual content.
        if result['issues_found'] == 0:
            return result
        
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
                
                # Extract current text (in code block - supports both ``` and ~~~ fences)
                current_match = re.search(r'\*\*Current text:\*\*\s*\n(?:```|~~~)[^\n]*\n(.+?)\n(?:```|~~~)', body, re.DOTALL)
                if current_match:
                    violation['current_text'] = current_match.group(1).strip()
                
                # Extract suggested fix (in code block - supports both ``` and ~~~ fences)
                fix_match = re.search(r'\*\*Suggested fix:\*\*\s*\n(?:```|~~~)[^\n]*\n(.+?)\n(?:```|~~~)', body, re.DOTALL)
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
    
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929", temperature: float = 0.0):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
    
    def check_single_rule(self, prompt: str) -> Dict[str, Any]:
        """Check a single rule using provided prompt"""
        # Try non-streaming first, fall back to streaming if required
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=64000,
                temperature=self.temperature,
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
                    temperature=self.temperature,
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
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, temperature: float = 0.0):
        """
        Initialize reviewer with Claude Sonnet 4.5
        
        Args:
            api_key: Anthropic API key (or will use ANTHROPIC_API_KEY environment variable)
            model: Specific Claude model to use (default: claude-sonnet-4-5-20250929)
            temperature: LLM temperature (0=deterministic, 1=creative, default: 0)
        """
        self.provider_name = 'claude'
        
        # Get API key from parameter or environment
        if not api_key:
            api_key = os.environ.get('ANTHROPIC_API_KEY')
        
        if not api_key:
            raise ValueError("No API key provided. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter")
        
        # Initialize Claude provider
        self.provider = AnthropicProvider(api_key, model, temperature=temperature) if model else AnthropicProvider(api_key, temperature=temperature)
    
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
        original_content = content  # Snapshot before any rules run
        fix_log = []  # Track each applied fix with rule attribution
        
        for category in categories:
            print(f"  📋 Checking {category} rules individually...")
            rules = extract_individual_rules(category)
            
            if not rules:
                print(f"    ⚠️  No rules found for category: {category}")
                continue
            
            print(f"    ℹ️  Found {len(rules)} rules to check")
            
            for i, rule in enumerate(rules, 1):
                rule_id = rule['rule_id']
                rule_type = rule.get('rule_type', 'rule')  # 'rule' = auto-fix, 'style' = suggestion
                print(f"    ⏳ Checking {rule_id}: {rule['title']} ({i}/{len(rules)}) [type: {rule_type}]")
                
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
                        
                        # Separate by type - only auto-apply fixes for 'rule' type
                        if rule_type == 'rule':
                            # Apply fixes immediately to current content
                            corrected_content, apply_warnings, applied = apply_fixes(current_content, result['violations'])
                            
                            if apply_warnings:
                                all_warnings.extend(apply_warnings)
                            
                            # Update current content for next rule
                            if corrected_content != current_content:
                                current_content = corrected_content
                                print(f"      ✓ Applied {len(applied)} fix(es) automatically - content updated for next rule")
                                
                                # Log each actually-applied fix for region-based reporting
                                for v in applied:
                                    fix_log.append({
                                        'rule_id': v.get('rule_id', 'unknown'),
                                        'rule_title': v.get('rule_title', ''),
                                        'category': category,
                                        'current_text': v.get('current_text', '').strip(),
                                        'suggested_fix': v.get('suggested_fix', '').strip(),
                                        'description': v.get('description', ''),
                                        'explanation': v.get('explanation', ''),
                                        'location': v.get('location', ''),
                                    })
                            else:
                                print(f"      ⚠️  Could not apply fixes - content unchanged")
                            
                            # Store only actually-applied violations for reporting
                            rule_violations.extend(applied)
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
            'rule_violations': rule_violations,  # Automatic fixes actually applied
            'style_violations': style_violations,  # Suggestions for human review
            'provider': self.provider_name,
            'lecture_name': lecture_name,
            'warnings': all_warnings,
            'corrected_content': current_content,  # Final content after all rule fixes
            'original_content': original_content,  # Snapshot before any fixes
            'fix_log': fix_log,  # Per-fix log with rule attribution
        }
        
        return combined_result
    
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
        # Define all categories to check (matches files in style_checker/rules/)
        all_categories = [
            'writing',
            'math',
            'code',
            'jax',
            'figures',
            'references',
            'links',
            'admonitions'
        ]
        
        print(f"\n🤖 Starting AI-powered review using single-rule evaluation...")
        print(f"📊 Lecture: {lecture_name}")
        print(f"\n📦 Processing {len(all_categories)} categories:")
        for category in all_categories:
            print(f"   • {category}")
        
        # Delegate to review_lecture_single_rule which handles:
        # - Single-rule-per-LLM-call evaluation
        # - Sequential fix application between rules
        # - Rule vs style type separation
        return self.review_lecture_single_rule(content, all_categories, lecture_name)
