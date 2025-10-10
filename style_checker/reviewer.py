"""
LLM-based Style Checker using Claude Sonnet 4.5
Uses Markdown format for LLM responses (more reliable than JSON for long content)
Applies fixes programmatically instead of relying on LLM-generated corrected content
Uses markdown-based prompt templates for simplicity and maintainability
"""

import os
import re
from typing import List, Dict, Any, Optional, Tuple
from .fix_applier import apply_fixes, validate_fix_quality
from .prompt_loader import load_prompt


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
        
        # Extract corrected content (handle nested code blocks)
        corrected_match = re.search(r'## Corrected Content\s*\n```(?:markdown)?\s*\n(.+)', response, re.DOTALL)
        if corrected_match:
            # Extract everything after the opening ``` and before the final ```
            content_after_header = corrected_match.group(1)
            # Remove the final closing ``` (it will be the last one before end or next ##)
            content_after_header = re.sub(r'\n```\s*$', '', content_after_header)
            result['corrected_content'] = content_after_header.strip()
        
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
        """Check style using Anthropic Claude"""
        # Load prompt using category-specific templates
        prompt = load_prompt(categories, content)
        
        # Make API call
        response = self.client.messages.create(
            model=self.model,
            max_tokens=64000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extract text from response
        full_response = response.content[0].text
        
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
