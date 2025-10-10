"""
Simple utility to load markdown prompt templates by category.
"""

from pathlib import Path
from typing import List, Optional


class PromptLoader:
    """Loads category-specific style guide prompts from markdown files."""
    
    VALID_CATEGORIES = [
        "writing", "math", "code", "jax",
        "figures", "references", "links", "admonitions", "all"
    ]
    
    def __init__(self, prompts_dir: Optional[Path] = None):
        """
        Initialize the prompt loader.
        
        Args:
            prompts_dir: Directory containing prompt markdown files.
                        Defaults to style_checker/prompts/
        """
        if prompts_dir is None:
            prompts_dir = Path(__file__).parent / "prompts"
        
        self.prompts_dir = Path(prompts_dir)
        
        if not self.prompts_dir.exists():
            raise FileNotFoundError(
                f"Prompts directory not found: {self.prompts_dir}"
            )
    
    def load_prompt(self, categories: List[str], lecture_content: str) -> str:
        """
        Load and combine prompts for specified categories.
        
        Args:
            categories: List of category names (e.g., ["writing", "math"])
                       Use ["all"] for all categories.
            lecture_content: The lecture markdown content to review
        
        Returns:
            Complete prompt with instructions and lecture content
        
        Raises:
            ValueError: If invalid category specified
            FileNotFoundError: If prompt file not found
        """
        # Validate categories
        invalid = [c for c in categories if c not in self.VALID_CATEGORIES]
        if invalid:
            raise ValueError(
                f"Invalid categories: {invalid}. "
                f"Valid options: {self.VALID_CATEGORIES}"
            )
        
        # Special case: "all" means use the comprehensive prompt
        if "all" in categories:
            return self._load_single_prompt("all", lecture_content)
        
        # For multiple categories, combine them
        if len(categories) == 1:
            return self._load_single_prompt(categories[0], lecture_content)
        
        # Combine multiple category prompts
        return self._combine_prompts(categories, lecture_content)
    
    def _load_single_prompt(self, category: str, lecture_content: str) -> str:
        """Load a single category prompt file."""
        prompt_file = self.prompts_dir / f"{category}.md"
        
        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        
        with open(prompt_file, 'r') as f:
            template = f.read()
        
        # Replace the placeholder with actual content
        if "[The lecture content will be appended here]" in template:
            return template.replace(
                "[The lecture content will be appended here]",
                lecture_content
            )
        
        # Fallback: just append
        return f"{template}\n\n{lecture_content}"
    
    def _combine_prompts(self, categories: List[str], lecture_content: str) -> str:
        """
        Combine multiple category prompts into one.
        
        This creates a unified prompt that checks multiple categories.
        """
        # Start with a header
        cat_list = ", ".join(categories)
        combined = f"""# QuantEcon Style Guide - Multiple Categories Review

You are a helpful AI assistant reviewing QuantEcon lecture content for style guide compliance.

Your task is to review the provided lecture content and identify any violations of the style rules in these categories: **{cat_list}**

## Instructions

1. **Read the lecture content carefully**
2. **Check against all rules below**
3. **Report ONLY violations you find** (don't report what's correct)
4. **For each violation:**
   - State the rule code (e.g., qe-writing-001)
   - Quote the problematic text
   - Explain what's wrong
   - Suggest a fix (if applicable)

5. **Output format:**
   ```
   ### Rule: [rule-code]
   **Issue:** [Brief description]
   **Location:** [Quote the problematic text]
   **Suggestion:** [How to fix it]
   ```

6. **Group violations by category**

7. **If no violations found:** Simply respond with "No style violations found."

---

"""
        
        # Load each category's rules section
        for category in categories:
            prompt_file = self.prompts_dir / f"{category}.md"
            
            if not prompt_file.exists():
                continue
            
            with open(prompt_file, 'r') as f:
                content = f.read()
            
            # Extract just the rules section (between "## {Category} Rules" and "---")
            import re
            pattern = rf'## {category.title()} (?:Style )?Rules\s*\n\n(.*?)(?=\n---\n|\Z)'
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                combined += f"## {category.title()} Rules\n\n{match.group(1).strip()}\n\n"
        
        # Add lecture content
        combined += """---

## Lecture Content to Review

"""
        combined += lecture_content
        
        return combined


def load_prompt(categories: List[str], lecture_content: str) -> str:
    """
    Convenience function to load prompts.
    
    Args:
        categories: List of category names (e.g., ["writing", "math"])
        lecture_content: The lecture markdown content to review
    
    Returns:
        Complete prompt ready for LLM
    """
    loader = PromptLoader()
    return loader.load_prompt(categories, lecture_content)
