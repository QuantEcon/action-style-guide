"""
LLM-based Style Checker
Supports multiple LLM providers: OpenAI, Anthropic Claude, Google Gemini
Uses Markdown format for LLM responses (more reliable than JSON for long content)
Applies fixes programmatically instead of relying on LLM-generated corrected content
Uses markdown-based prompt templates for simplicity and maintainability
"""

import os
import re
from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING
from abc import ABC, abstractmethod
from .fix_applier import apply_fixes, validate_fix_quality
from .prompt_loader import load_prompt

if TYPE_CHECKING:
    from .parser_md import StyleGuideDatabase, StyleRule


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
    
    ### Violation 1: <rule_id> - <rule_title>
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
    <full corrected content>
    ```
    
    Returns:
        Dictionary with parsed results
    """
    result = {
        'issues_found': 0,
        'violations': [],
        'corrected_content': '',
        'summary': ''
    }
    
    try:
        # Extract summary
        summary_match = re.search(r'##\s+Summary\s*\n(.*?)(?=\n##|\Z)', response, re.DOTALL)
        if summary_match:
            result['summary'] = summary_match.group(1).strip()
        
        # Extract issues count
        issues_match = re.search(r'##\s+Issues Found\s*\n(\d+)', response, re.IGNORECASE)
        if issues_match:
            result['issues_found'] = int(issues_match.group(1))
        
        # Extract violations section
        violations_section = re.search(
            r'##\s+Violations\s*\n(.*?)(?=\n##\s+Corrected Content|\Z)',
            response,
            re.DOTALL | re.IGNORECASE
        )
        
        if violations_section:
            violations_text = violations_section.group(1)
            
            # Parse individual violations
            violation_pattern = re.compile(
                r'###\s+Violation\s+\d+:\s+([a-zA-Z0-9_-]+)\s+-\s+(.+?)\n'
                r'.*?-\s+\*\*Severity:\*\*\s*(.+?)\n'
                r'.*?-\s+\*\*Location:\*\*\s*(.+?)\n'
                r'.*?-\s+\*\*Description:\*\*\s*(.+?)\n'
                r'.*?-\s+\*\*Current text:\*\*\s*\n```(?:.*?\n)?(.*?)```\s*\n'
                r'.*?-\s+\*\*Suggested fix:\*\*\s*\n```(?:.*?\n)?(.*?)```\s*\n'
                r'.*?-\s+\*\*Explanation:\*\*\s*(.+?)(?=\n###|\n##|\Z)',
                re.DOTALL | re.IGNORECASE
            )
            
            for match in violation_pattern.finditer(violations_text):
                violation = {
                    'rule_id': match.group(1).strip(),
                    'rule_title': match.group(2).strip(),
                    'severity': match.group(3).strip(),
                    'location': match.group(4).strip(),
                    'description': match.group(5).strip(),
                    'current_text': match.group(6).strip(),
                    'suggested_fix': match.group(7).strip(),
                    'explanation': match.group(8).strip()
                }
                result['violations'].append(violation)
        
        # Extract corrected content (optional - for backward compatibility)
        # New approach: Apply fixes programmatically, so this field is optional
        corrected_match = re.search(
            r'##\s+Corrected Content\s*\n```(?:markdown)?\s*\n(.*?)(?:\n```\s*(?:$|(?=\n##)))',
            response,
            re.DOTALL | re.IGNORECASE
        )
        if corrected_match:
            result['corrected_content'] = corrected_match.group(1).strip()
        else:
            # Fallback: try to find content after "Corrected Content" header
            # This handles cases where the format might be slightly different
            content_match = re.search(
                r'##\s+Corrected Content\s*\n(.+)',
                response,
                re.DOTALL | re.IGNORECASE
            )
            if content_match:
                # Extract everything after the header
                content_after = content_match.group(1).strip()
                # If it starts with a code fence, extract the content
                code_fence_match = re.match(r'```(?:markdown)?\s*\n(.+)', content_after, re.DOTALL)
                if code_fence_match:
                    # Get content and find the last closing fence
                    full_content = code_fence_match.group(1)
                    # Remove trailing ``` if present
                    if full_content.endswith('```'):
                        full_content = full_content[:-3].rstrip()
                    result['corrected_content'] = full_content
            # If still no corrected content, leave it empty (will be generated from fixes)

        
        # Update issues_found based on actual violations parsed if not set
        if result['issues_found'] == 0 and result['violations']:
            result['issues_found'] = len(result['violations'])
            
    except Exception as e:
        print(f"    ⚠️  Markdown parsing error: {e}")
        print(f"    Response preview: {response[:500]}...")
        result['error'] = f'Markdown parsing failed: {str(e)}'
    
    return result


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def check_style(self, content: str, categories: List[str]) -> Dict[str, Any]:
        """
        Check style and return structured results.
        
        Args:
            content: Lecture content to review
            categories: List of style categories to check (e.g., ["writing", "math"])
        
        Returns:
            Dictionary with parsed review results
        """
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI GPT-4 provider"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    def check_style(self, content: str, categories: List[str]) -> Dict[str, Any]:
        """Check style using OpenAI GPT-4"""
        # Load prompt using category-specific templates
        prompt = load_prompt(categories, content)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        return parse_markdown_response(response.choices[0].message.content)


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider
    
    Token limits by model:
    - claude-sonnet-4-5-20250929: 64000 max output tokens (recommended)
    - claude-sonnet-4-20250514: 64000 max output tokens
    - claude-opus-4-1-20250805: 32000 max output tokens
    - claude-opus-4-20250514: 32000 max output tokens
    - claude-3-7-sonnet-20250219: 64000 max output tokens
    - claude-3-5-haiku-20241022: 8192 max output tokens
    - claude-3-5-sonnet-20241022: 8192 max output tokens (deprecated)
    
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
        """Check style using Anthropic Claude with streaming for long requests"""
        # Load prompt using category-specific templates
        prompt = load_prompt(categories, content)
        
        # Use streaming to avoid 10-minute timeout on long requests
        # See: https://docs.anthropic.com/en/docs/build-with-claude/streaming
        full_response = ""
        stop_reason = None
        
        with self.client.messages.stream(
            model=self.model,
            max_tokens=32000,  # Safe limit for all Claude 4+ models (Sonnet 4.5 supports up to 64K)
            temperature=0.1,
            messages=[
                {"role": "user", "content": prompt}
            ]
        ) as stream:
            for text in stream.text_stream:
                full_response += text
            # Get the final message to check stop reason
            final_message = stream.get_final_message()
            stop_reason = final_message.stop_reason if final_message else None
        
        # Check if response was truncated
        if stop_reason == "max_tokens":
            print(f"    ⚠️  Warning: Response truncated (hit max_tokens limit)")
            print(f"    Consider using specific categories to focus the review")
        
        # Parse the Markdown response
        return parse_markdown_response(full_response)


class GeminiProvider(LLMProvider):
    """Google Gemini provider"""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        self.api_key = api_key
        self.model = model
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                model_name=model,
                generation_config={
                    "temperature": 0.1
                }
            )
        except ImportError:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
    
    def check_style(self, content: str, categories: List[str]) -> Dict[str, Any]:
        """Check style using Google Gemini"""
        # Load prompt using category-specific templates
        prompt = load_prompt(categories, content)
        
        response = self.model.generate_content(prompt)
        return parse_markdown_response(response.text)


class StyleReviewer:
    """Main style reviewer coordinating LLM-based checking"""
    
    def __init__(self, provider: str = "claude", api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize reviewer with specified LLM provider
        
        Args:
            provider: 'openai', 'claude', or 'gemini'
            api_key: API key (or will use environment variable)
            model: Specific model to use
        """
        self.provider_name = provider.lower()
        
        # Get API key from parameter or environment
        if not api_key:
            if provider == 'openai':
                api_key = os.environ.get('OPENAI_API_KEY')
            elif provider == 'claude':
                api_key = os.environ.get('ANTHROPIC_API_KEY')
            elif provider == 'gemini':
                api_key = os.environ.get('GOOGLE_API_KEY')
        
        if not api_key:
            raise ValueError(f"No API key provided for {provider}")
        
        # Initialize provider
        if provider == 'openai':
            self.provider = OpenAIProvider(api_key, model or "gpt-4")
        elif provider == 'claude':
            # Use provider's default if no model specified (Sonnet 4.5)
            self.provider = AnthropicProvider(api_key, model) if model else AnthropicProvider(api_key)
        elif provider == 'gemini':
            self.provider = GeminiProvider(api_key, model or "gemini-1.5-pro")
        else:
            raise ValueError(f"Unknown provider: {provider}. Use 'openai', 'claude', or 'gemini'")
    
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
        style_guide: 'StyleGuideDatabase',
        lecture_name: str
    ) -> Dict[str, Any]:
        """
        Smart review strategy using semantic category grouping.
        
        Groups rules by their semantic categories (WRITING, MATH, CODE, etc.)
        and processes them in parallel for better performance and quality.
        
        Benefits:
        - Related rules checked together (better context for LLM)
        - Parallel processing (3-4x faster than sequential)
        - Reasonable cost (~8 API calls vs 31 single-rule calls)
        - Natural alignment with style guide structure
        - Better quality results from semantic coherence
        
        Args:
            content: Full lecture content
            style_guide: Parsed style guide database with rules
            lecture_name: Name of the lecture file
            
        Returns:
            Dictionary with all violations found across all groups
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        print(f"\n🤖 Starting AI-powered review using semantic grouping...")
        print(f"📊 Lecture: {lecture_name}")
        
        # Get all groups with their actionable rules (category='rule' only)
        groups = style_guide.get_all_groups_with_rules(category='rule')
        
        if not groups:
            print("  ⚠️  No actionable rules found!")
            return {
                'issues_found': 0,
                'violations': [],
                'corrected_content': content,
                'summary': 'No actionable rules to check',
                'provider': self.provider_name,
                'lecture_name': lecture_name
            }
        
        total_rules = sum(len(rules) for rules in groups.values())
        print(f"📋 Total actionable rules: {total_rules}")
        
        print(f"\n📦 Processing {len(groups)} semantic groups in parallel:")
        for group_name, rules in sorted(groups.items()):
            print(f"   • {group_name}: {len(rules)} rules")
        
        # Process groups in parallel
        all_violations = []
        max_workers = min(4, len(groups))  # Max 4 parallel calls to avoid rate limits
        
        print(f"\n🚀 Running {max_workers} parallel reviews...")
        print()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all group reviews
            futures = {
                executor.submit(
                    self._review_group,
                    content,
                    group_name,
                    rules,
                    lecture_name
                ): group_name
                for group_name, rules in groups.items()
            }
            
            # Collect results as they complete
            for future in as_completed(futures):
                group_name = futures[future]
                try:
                    result = future.result()
                    violations_count = len(result.get('violations', []))
                    
                    if violations_count > 0:
                        print(f"  ✓ {group_name}: {violations_count} issues found")
                    else:
                        print(f"  ✓ {group_name}: No issues found")
                    
                    all_violations.extend(result.get('violations', []))
                    
                except Exception as e:
                    print(f"  ❌ {group_name} failed: {e}")
        
        print(f"\n📊 Total issues found across all groups: {len(all_violations)}")
        
        # Apply ALL fixes programmatically to the original content
        corrected_content = content
        fix_warnings = []
        
        if all_violations:
            print(f"  🔧 Applying {len(all_violations)} fixes programmatically...")
            
            # Validate fix quality
            validation_warnings = validate_fix_quality(all_violations)
            if validation_warnings:
                print(f"  ⚠️  Fix quality warnings:")
                for warning in validation_warnings[:5]:  # Show first 5
                    print(f"      - {warning}")
            
            # Apply fixes
            corrected_content, fix_warnings = apply_fixes(content, all_violations)
            
            if corrected_content == content and all_violations:
                print(f"  ⚠️  Could not apply any fixes - keeping original content")
        else:
            print(f"  ✨ No issues found - lecture follows all style guide rules!")
        
        return {
            'issues_found': len(all_violations),
            'violations': all_violations,
            'corrected_content': corrected_content,
            'fix_warnings': fix_warnings,
            'summary': f"Found {len(all_violations)} issues across {len(groups)} semantic groups",
            'provider': self.provider_name,
            'lecture_name': lecture_name,
            'groups_checked': list(groups.keys())
        }
    
    def _review_group(
        self,
        content: str,
        group_name: str,
        rules: List['StyleRule'],
        lecture_name: str
    ) -> Dict[str, Any]:
        """
        Review lecture content against a single semantic group of rules.
        
        Now uses markdown-based category prompts instead of programmatic formatting.
        
        Args:
            content: Full lecture content
            group_name: Name of the semantic group (e.g., 'WRITING', 'MATH')
            rules: List of StyleRule objects in this group (not used - kept for compatibility)
            lecture_name: Name of the lecture file
            
        Returns:
            Dictionary with violations found for this group
        """
        # Convert group name to category (e.g., "WRITING" -> "writing")
        category = group_name.lower()
        
        # Review using category-specific prompt
        try:
            result = self.provider.check_style(content, [category])
            result['group'] = group_name
            return result
        except Exception as e:
            return {
                'error': str(e),
                'violations': [],
                'group': group_name
            }
