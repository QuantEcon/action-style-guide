"""
Simple utility to load markdown prompt templates by category.

Uses the same approach as tool-style-checker:
- Loads concise instruction prompts from prompts/
- Loads detailed rules from rules/
- Combines them for the LLM
"""

from pathlib import Path
from typing import List, Optional


class PromptLoader:
    """Loads category-specific style guide prompts and rules from markdown files."""
    
    VALID_CATEGORIES = [
        "writing", "math", "code", "jax",
        "figures", "references", "links", "admonitions"
    ]
    
    def __init__(self, prompts_dir: Optional[Path] = None, rules_dir: Optional[Path] = None):
        """
        Initialize the prompt loader.
        
        Args:
            prompts_dir: Directory containing prompt markdown files.
                        Defaults to style_checker/prompts/
            rules_dir: Directory containing rule markdown files.
                      Defaults to style_checker/rules/
        """
        if prompts_dir is None:
            prompts_dir = Path(__file__).parent / "prompts"
        if rules_dir is None:
            rules_dir = Path(__file__).parent / "rules"
        
        self.prompts_dir = Path(prompts_dir)
        self.rules_dir = Path(rules_dir)
        
        if not self.prompts_dir.exists():
            raise FileNotFoundError(
                f"Prompts directory not found: {self.prompts_dir}"
            )
        if not self.rules_dir.exists():
            raise FileNotFoundError(
                f"Rules directory not found: {self.rules_dir}"
            )
    
    def load_prompt(self, categories: List[str], lecture_content: str) -> str:
        """
        Load and combine prompts + rules for specified categories.
        
        Uses tool-style-checker approach:
        1. Load concise instruction prompt
        2. Load detailed rules
        3. Combine: prompt + rules + lecture_content
        
        Args:
            categories: List of category names (e.g., ["writing", "math"])
            lecture_content: The lecture markdown content to review
        
        Returns:
            Complete prompt with instructions, rules, and lecture content
        
        Raises:
            ValueError: If invalid category specified
            FileNotFoundError: If prompt or rules file not found
        """
        # Validate categories
        invalid = [c for c in categories if c not in self.VALID_CATEGORIES]
        if invalid:
            raise ValueError(
                f"Invalid categories: {invalid}. "
                f"Valid options: {self.VALID_CATEGORIES}"
            )
        
        # For single category, use simple combination
        if len(categories) == 1:
            return self._load_single_category(categories[0], lecture_content)
        
        # For multiple categories, combine them
        return self._combine_categories(categories, lecture_content)
    
    def _load_single_category(self, category: str, lecture_content: str) -> str:
        """
        Load prompt and rules for a single category.
        
        Follows tool-style-checker pattern:
        - prompt file: category-prompt.md
        - rules file: category-rules.md
        """
        # Load prompt (instruction template)
        prompt_file = self.prompts_dir / f"{category}-prompt.md"
        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        
        with open(prompt_file, 'r') as f:
            prompt = f.read()
        
        # Load rules (detailed specifications)
        rules_file = self.rules_dir / f"{category}-rules.md"
        if not rules_file.exists():
            raise FileNotFoundError(f"Rules file not found: {rules_file}")
        
        with open(rules_file, 'r') as f:
            rules = f.read()
        
        # Combine: prompt + rules + lecture
        # This matches tool-style-checker's approach
        full_prompt = f"""{prompt}

## Style Guide Database

{rules}

## Lecture to Review

{lecture_content}
"""
        return full_prompt
    
    def _combine_categories(self, categories: List[str], lecture_content: str) -> str:
        """
        Combine multiple category prompts and rules into one.
        
        Creates a unified prompt that checks multiple categories while keeping
        the structure similar to single-category reviews.
        """
        cat_list = ", ".join(categories)
        
        # Start with a combined header
        combined_prompt = f"""# QuantEcon Multi-Category Style Checker

You are an expert technical writing editor specializing in QuantEcon lecture materials. 

Your task is to review a lecture document for violations in these categories: **{cat_list}**

## Instructions

1. **Focus on the specified categories only**: {cat_list}

2. **Read the entire lecture carefully** to understand the context.

3. **Check systematically** against all rules in the categories below.

4. **For each violation found**, provide:
   - **Rule Code and Title**: e.g., `qe-writing-001: One sentence per paragraph`
   - **Location**: Line number or section where the violation occurs
   - **Current**: Quote the problematic text exactly
   - **Issue**: Brief explanation of why this violates the rule
   - **Suggested Fix**: Specific corrected version

5. **Prioritize actionable feedback**:
   - Focus on `rule` category violations first (clearly actionable)
   - Include `style` category suggestions when they significantly impact quality
   - For style suggestions, explain your reasoning clearly

6. **Group by category** in your output for clarity

## Output Format

Provide a comprehensive review with violations grouped by category:

```markdown
# Style Review for [filename]

## Summary
- Total violations: [number]
- By category: Writing([n]), Math([n]), Code([n]), etc.

## Violations by Category

### Writing Issues
[violations...]

### Math Issues
[violations...]

[etc for each category checked...]

## Overall Assessment
[Brief summary]
```

---

"""
        
        # Load and append each category's rules
        for category in categories:
            rules_file = self.rules_dir / f"{category}-rules.md"
            
            if not rules_file.exists():
                continue
            
            with open(rules_file, 'r') as f:
                rules = f.read()
            
            combined_prompt += f"## {category.title()} Rules\n\n{rules}\n\n---\n\n"
        
        # Add lecture content
        combined_prompt += f"""## Lecture to Review

{lecture_content}
"""
        
        return combined_prompt


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
