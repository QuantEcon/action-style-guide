#!/usr/bin/env python3
"""
Generate category-specific prompt files from style-guide-database.md
"""

import re
from pathlib import Path

# Read the style guide database
db_path = Path(__file__).parent / "style-guide-database.md"
with open(db_path, 'r') as f:
    content = f.read()

# Define categories
categories = [
    "writing", "math", "code", "jax", 
    "figures", "references", "links", "admonitions"
]

# Create prompts directory
prompts_dir = Path(__file__).parent / "style_checker" / "prompts"
prompts_dir.mkdir(exist_ok=True)

# Extract sections for each category
for category in categories:
    cat_upper = category.upper()
    
    # Find the section between GROUP markers
    pattern = rf'<!-- GROUP:{cat_upper}-START -->(.*?)<!-- GROUP:{cat_upper}-END -->'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print(f"Warning: Could not find section for {category}")
        continue
    
    rules_section = match.group(1).strip()
    
    # Create the prompt file
    prompt = f"""# QuantEcon Style Guide - {category.title()} Category

You are a helpful AI assistant reviewing QuantEcon lecture content for style guide compliance.

Your task is to review the provided lecture content and identify any violations of the {category} style rules listed below.

## Instructions

1. **Read the lecture content carefully**
2. **Check against each rule below**
3. **Report ONLY violations you find** (don't report what's correct)
4. **For each violation:**
   - State the rule code (e.g., qe-{category}-001)
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

6. **If no violations found:** Simply respond with "No {category} style violations found."

## {category.title()} Style Rules

{rules_section}

---

## Lecture Content to Review

[The lecture content will be appended here]
"""
    
    # Write to file
    output_path = prompts_dir / f"{category}.md"
    with open(output_path, 'w') as f:
        f.write(prompt)
    
    print(f"✓ Created {output_path}")

# Also create a comprehensive "all" prompt
all_prompt = """# QuantEcon Style Guide - All Categories

You are a helpful AI assistant reviewing QuantEcon lecture content for style guide compliance.

Your task is to review the provided lecture content and identify any violations of the style rules across ALL categories.

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

6. **Group violations by category** (Writing, Math, Code, etc.)

7. **If no violations found:** Simply respond with "No style violations found."

## Complete Style Guide

"""

# Add all category sections
for category in categories:
    cat_upper = category.upper()
    pattern = rf'<!-- GROUP:{cat_upper}-START -->(.*?)<!-- GROUP:{cat_upper}-END -->'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        all_prompt += f"\n\n## {category.title()} Rules\n\n"
        all_prompt += match.group(1).strip()

all_prompt += """

---

## Lecture Content to Review

[The lecture content will be appended here]
"""

all_path = prompts_dir / "all.md"
with open(all_path, 'w') as f:
    f.write(all_prompt)

print(f"✓ Created {all_path}")
print(f"\nGenerated {len(categories) + 1} prompt files in {prompts_dir}")
