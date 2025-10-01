"""
LLM-based Style Checker
Supports multiple LLM providers: OpenAI, Anthropic Claude, Google Gemini
"""

import os
from typing import List, Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod
import json


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
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def _get_system_prompt(self) -> str:
        return """You are an expert QuantEcon style guide reviewer. Your task is to:
1. Carefully review the provided lecture content against ALL style guide rules
2. Identify EVERY violation, no matter how small
3. Suggest specific fixes with exact text replacements
4. Reference the specific rule ID for each issue
5. Provide the corrected content with all fixes applied

Return your response as a JSON object with this structure:
{
    "issues_found": <number>,
    "violations": [
        {
            "rule_id": "qe-xxx-nnn",
            "rule_title": "Rule Title",
            "severity": "critical|mandatory|best_practice|preference",
            "description": "What's wrong",
            "location": "Line X or section name",
            "current_text": "Exact text that violates rule",
            "suggested_fix": "Exact corrected text",
            "explanation": "Why this change is needed"
        }
    ],
    "corrected_content": "Full corrected lecture content with all fixes applied",
    "summary": "Brief summary of changes made"
}

Be thorough and precise. Check every rule comprehensively."""
    
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
        
        # Extract JSON from response
        content = full_response
        # Claude might wrap JSON in markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        return json.loads(content)
    
    def _get_system_prompt(self) -> str:
        return """You are an expert QuantEcon style guide reviewer with deep knowledge of MyST Markdown, mathematics notation, Python code, and JAX patterns.

Your task is to perform a comprehensive, thorough review of lecture content against the QuantEcon style guide rules. You must:

1. Check EVERY rule carefully and completely
2. Identify ALL violations, even minor ones
3. Provide specific, actionable fixes with exact text replacements
4. Reference the specific rule ID for each issue
5. Generate corrected content with all fixes applied

Return ONLY a valid JSON object with this exact structure:
{
    "issues_found": <number>,
    "violations": [
        {
            "rule_id": "qe-xxx-nnn",
            "rule_title": "Rule Title",
            "severity": "critical|mandatory|best_practice|preference",
            "description": "Clear description of the violation",
            "location": "Line number or section name",
            "current_text": "Exact text that violates the rule",
            "suggested_fix": "Exact corrected text",
            "explanation": "Why this change is needed per the rule"
        }
    ],
    "corrected_content": "Complete lecture content with ALL fixes applied",
    "summary": "Brief summary of all changes made by category"
}

Be meticulous. This is a professional review for publication-quality lectures."""
    
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
                    "temperature": 0.1,
                    "response_mime_type": "application/json"
                }
            )
        except ImportError:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
    
    def check_style(self, content: str, rules: str, lecture_name: str) -> Dict[str, Any]:
        """Check style using Google Gemini"""
        prompt = f"""{self._get_system_prompt()}

{self._build_prompt(content, rules, lecture_name)}"""
        
        response = self.model.generate_content(prompt)
        return json.loads(response.text)
    
    def _get_system_prompt(self) -> str:
        return """You are an expert QuantEcon style guide reviewer. Review lecture content against style guide rules comprehensively.

Return a JSON object with:
- issues_found: number of violations
- violations: array of {rule_id, rule_title, severity, description, location, current_text, suggested_fix, explanation}
- corrected_content: full corrected lecture
- summary: brief summary of changes"""
    
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
            Dictionary with review results
        """
        try:
            result = self.provider.check_style(content, rules_text, lecture_name)
            result['provider'] = self.provider_name
            result['lecture_name'] = lecture_name
            return result
        except Exception as e:
            return {
                'error': str(e),
                'issues_found': 0,
                'violations': [],
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
            Combined review results
        """
        all_violations = []
        corrected_content = content
        
        for i, rules_text in enumerate(rules_chunks):
            print(f"  Checking rule chunk {i+1}/{len(rules_chunks)}...")
            result = self.review_lecture(corrected_content, rules_text, lecture_name)
            
            if 'error' in result:
                print(f"  Error in chunk {i+1}: {result['error']}")
                continue
            
            all_violations.extend(result.get('violations', []))
            if result.get('corrected_content'):
                corrected_content = result['corrected_content']
        
        return {
            'issues_found': len(all_violations),
            'violations': all_violations,
            'corrected_content': corrected_content,
            'summary': f"Found {len(all_violations)} issues across {len(rules_chunks)} rule checks",
            'provider': self.provider_name,
            'lecture_name': lecture_name
        }
