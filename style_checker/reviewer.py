"""
LLM-based Style Checker
Supports multiple LLM providers: OpenAI, Anthropic Claude, Google Gemini
Uses Markdown format for LLM responses (more reliable than JSON for long content)
Applies fixes programmatically instead of relying on LLM-generated corrected content
"""

import os
import re
from typing import List, Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod
from .fix_applier import apply_fixes, validate_fix_quality


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
    def check_style(self, content: str, rules: str, lecture_name: str) -> Dict[str, Any]:
        """Check style and return structured results"""
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
    
    def check_style(self, content: str, rules: str, lecture_name: str) -> Dict[str, Any]:
        """Check style using OpenAI GPT-4"""
        prompt = self._build_prompt(content, rules, lecture_name)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        return parse_markdown_response(response.choices[0].message.content)
    
    def _get_system_prompt(self) -> str:
        return """You are an expert QuantEcon style guide reviewer. Your task is to:

1. Carefully review the provided lecture content against ALL style guide rules
2. Identify EVERY violation, no matter how small
3. Suggest specific fixes with exact text replacements
4. Reference the specific rule ID for each issue
5. Provide the corrected content with all fixes applied

Return your response in this EXACT Markdown format:

# Review Results

## Summary
<Brief summary of issues found by category>

## Issues Found
<number>

## Violations

### Violation 1: <rule_id> - <rule_title>
- **Severity:** <critical|mandatory|best_practice|preference>
- **Location:** <Line X or section name>
- **Description:** <What's wrong>
- **Current text:**
```
<EXACT text that violates rule - must match content precisely>
```
- **Suggested fix:**
```
<EXACT replacement text>
```
- **Explanation:** <Why this change is needed>

[Repeat for each violation...]

CRITICAL INSTRUCTIONS:
- For "Current text": Copy the EXACT text from the lecture that needs to be changed
- For "Suggested fix": Provide the EXACT replacement text only (no explanations, no notes)
- Do NOT include any commentary or notes in the suggested fixes
- Be precise with quotes, spacing, and formatting
- Each violation should be independently fixable

Do NOT include a "Corrected Content" section - fixes will be applied programmatically."""
    
    def _build_prompt(self, content: str, rules: str, lecture_name: str) -> str:
        return f"""Review the following QuantEcon lecture for style guide compliance.

**Lecture Name:** {lecture_name}

**Style Guide Rules to Check:**
{rules}

**Lecture Content to Review:**
```markdown
{content}
```

Perform a comprehensive review checking ALL rules above. Identify every violation and provide specific fixes."""


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
    
    def check_style(self, content: str, rules: str, lecture_name: str) -> Dict[str, Any]:
        """Check style using Anthropic Claude with streaming for long requests"""
        prompt = self._build_prompt(content, rules, lecture_name)
        
        # Use streaming to avoid 10-minute timeout on long requests
        # See: https://docs.anthropic.com/en/docs/build-with-claude/streaming
        full_response = ""
        stop_reason = None
        
        with self.client.messages.stream(
            model=self.model,
            max_tokens=32000,  # Safe limit for all Claude 4+ models (Sonnet 4.5 supports up to 64K)
            temperature=0.1,
            system=self._get_system_prompt(),
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
            print(f"    Consider reducing max-rules-per-request or using rule-categories")
        
        # Parse the Markdown response
        return parse_markdown_response(full_response)
    
    def _get_system_prompt(self) -> str:
        return """You are an expert QuantEcon style guide reviewer with deep knowledge of MyST Markdown, mathematics notation, Python code, and JAX patterns.

Your task is to perform a comprehensive, thorough review of lecture content against the QuantEcon style guide rules. You must:

1. Check EVERY rule carefully and completely
2. Identify ALL violations, even minor ones
3. Provide specific, actionable fixes with exact text replacements
4. Reference the specific rule ID for each issue
4. Reference the specific rule ID for each issue
5. Provide exact text replacements for each violation

Return your response in this EXACT Markdown format:

# Review Results

## Summary
<Brief summary of issues found by category>

## Issues Found
<number>

## Violations

### Violation 1: <rule_id> - <rule_title>
- **Severity:** <critical|mandatory|best_practice|preference>
- **Location:** <Line X or section name>
- **Description:** <Clear description of the violation>
- **Current text:**
```
<EXACT text that violates the rule - must match content precisely>
```
- **Suggested fix:**
```
<EXACT replacement text only - no notes or commentary>
```
- **Explanation:** <Why this change is needed per the rule>

[Repeat for each violation...]

CRITICAL INSTRUCTIONS:
- For "Current text": Copy the EXACT text from the lecture (preserve all spacing, quotes, formatting)
- For "Suggested fix": Provide ONLY the corrected text (no explanations, no notes, no commentary)
- Do NOT include any notes, comments, or explanations within the suggested fixes
- Be precise - fixes will be applied programmatically via text replacement
- Each fix must be independently applicable

Do NOT include a "Corrected Content" section - fixes will be applied programmatically.

Be meticulous and thorough. This is a professional review for publication-quality lectures."""
    
    def _build_prompt(self, content: str, rules: str, lecture_name: str) -> str:
        return f"""Review this QuantEcon lecture for complete style guide compliance.

**Lecture:** {lecture_name}

**Style Guide Rules:**
{rules}

**Lecture Content:**
```markdown
{content}
```

Perform a comprehensive review. Check every single rule against the entire lecture content. Identify all violations and provide specific fixes."""


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
    
    def check_style(self, content: str, rules: str, lecture_name: str) -> Dict[str, Any]:
        """Check style using Google Gemini"""
        prompt = f"""{self._get_system_prompt()}

{self._build_prompt(content, rules, lecture_name)}"""
        
        response = self.model.generate_content(prompt)
        return parse_markdown_response(response.text)
    
    def _get_system_prompt(self) -> str:
        return """You are an expert QuantEcon style guide reviewer. Review lecture content against style guide rules comprehensively.

Return your response in this EXACT Markdown format:

# Review Results

## Summary
<Brief summary of changes>

## Issues Found
<number>

## Violations

### Violation 1: <rule_id> - <rule_title>
- **Severity:** <critical|mandatory|best_practice|preference>
- **Location:** <location>
- **Description:** <description>
- **Current text:**
```
<current text>
```
- **Suggested fix:**
```
<suggested fix>
```
- **Explanation:** <explanation>

[Repeat for each violation...]

## Corrected Content

```markdown
<full corrected lecture>
```
"""
    
    def _build_prompt(self, content: str, rules: str, lecture_name: str) -> str:
        return f"""Review: {lecture_name}

Rules:
{rules}

Content:
```markdown
{content}
```

Check all rules. Find all violations. Provide fixes."""


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
        rules_text: str,
        lecture_name: str
    ) -> Dict[str, Any]:
        """
        Review a lecture against style guide rules
        
        Args:
            content: Full lecture content
            rules_text: Formatted rules text
            lecture_name: Name of the lecture
            
        Returns:
            Dictionary with review results and corrected content
        """
        try:
            result = self.provider.check_style(content, rules_text, lecture_name)
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
    
    def review_in_chunks(
        self,
        content: str,
        rules_chunks: List[str],
        lecture_name: str
    ) -> Dict[str, Any]:
        """
        Review lecture against rules in chunks (for large rule sets)
        
        Args:
            content: Full lecture content
            rules_chunks: List of formatted rule chunks
            lecture_name: Name of the lecture
            
        Returns:
            Combined review results with programmatically applied fixes
        """
        all_violations = []
        
        # Check all rule chunks against original content
        for i, rules_text in enumerate(rules_chunks):
            print(f"  Checking rule chunk {i+1}/{len(rules_chunks)}...")
            # Always check against original content (not corrected from previous chunk)
            result = self.provider.check_style(content, rules_text, lecture_name)
            
            if 'error' in result:
                print(f"  ❌ Error in chunk {i+1}: {result['error']}")
                continue
            
            chunk_issues = len(result.get('violations', []))
            print(f"  ✓ Chunk {i+1} complete: {chunk_issues} issues found")
            
            all_violations.extend(result.get('violations', []))
        
        print(f"\n  📊 Total issues found: {len(all_violations)}")
        
        # Apply ALL fixes at once to the original content
        corrected_content = content
        fix_warnings = []
        
        if all_violations:
            print(f"  🔧 Applying {len(all_violations)} fixes programmatically...")
            
            # Validate fix quality
            validation_warnings = validate_fix_quality(all_violations)
            if validation_warnings:
                print(f"  ⚠️  Fix quality warnings:")
                for warning in validation_warnings[:5]:
                    print(f"      - {warning}")
            
            # Apply fixes
            corrected_content, fix_warnings = apply_fixes(content, all_violations)
            
            if corrected_content == content and all_violations:
                print(f"  ⚠️  Could not apply any fixes - keeping original content")
        
        return {
            'issues_found': len(all_violations),
            'violations': all_violations,
            'corrected_content': corrected_content,
            'fix_warnings': fix_warnings,
            'summary': f"Found {len(all_violations)} issues across {len(rules_chunks)} rule checks",
            'provider': self.provider_name,
            'lecture_name': lecture_name
        }
