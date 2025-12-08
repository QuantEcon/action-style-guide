#!/usr/bin/env python3
"""
QuantEcon Lecture Style Checker using Claude API

A focused style checking tool that reviews lectures against specific QuantEcon 
style guide categories using Claude Sonnet 4.5.

Usage:
    python style_checker.py <lecture_file.md> --focus <category>
    python style_checker.py <lecture_file.md> --focus writing --mode corrected
    python style_checker.py <lecture_file.md> --focus math --mode both

Available categories: writing, math, code, jax, figures, references, links, admonitions

Requirements:
    pip install anthropic
    
Environment:
    Set ANTHROPIC_API_KEY environment variable with your Claude API key
"""

import os
import sys
import argparse
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("Error: anthropic package not installed.")
    print("Install it with: pip install anthropic")
    sys.exit(1)


def load_file(filepath):
    """Load a file and return its contents."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        sys.exit(1)


def get_main_action_path():
    """Get the path to the main style_checker directory."""
    # This tool lives in tool-style-checker/, main action is in style_checker/
    tool_dir = Path(__file__).parent
    repo_root = tool_dir.parent
    return repo_root / "style_checker"


def check_lecture_style(
    lecture_content,
    category,
    api_key=None
):
    """
    Check a lecture against the style guide using Claude.
    
    Args:
        lecture_content: Content of the lecture to check (string)
        category: Single category to focus on (e.g., 'writing', 'math', 'code')
        api_key: Claude API key (if not provided, uses ANTHROPIC_API_KEY env var)
    
    Returns:
        String containing Claude's output (both review and corrected file)
    """
    # Load focused prompt and rules from the MAIN ACTION (single source of truth)
    main_action_path = get_main_action_path()
    prompt_path = main_action_path / "prompts" / f"{category}-prompt.md"
    rules_path = main_action_path / "rules" / f"{category}-rules.md"
    
    print(f"  Using focused prompt: {prompt_path}")
    prompt = load_file(prompt_path)
    print(f"  Using focused rules: {rules_path}")
    style_guide = load_file(rules_path)
    
    # Get API key
    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Build the message
    message_parts = [prompt]
    
    # Always request both analysis and corrected output
    message_parts.append(
        "\n\n**OUTPUT FORMAT**\n\n"
        "Please provide TWO sections in your response:\n\n"
        "1. First, provide the complete style review (with violations, "
        "issues, and recommendations)\n\n"
        "2. Then, after a clear separator line, provide the fully corrected version "
        "of the lecture file with all violations fixed.\n\n"
        "Format your response like this:\n"
        "```\n"
        "# Style Guide Review\n"
        "[... your full review here ...]\n\n"
        "================================================================================\n"
        "CORRECTED LECTURE FILE\n"
        "================================================================================\n\n"
        "[... complete corrected lecture content ...]\n"
        "```\n"
    )
    
    message_parts.extend([
        "\n\n## Style Guide Database\n\n",
        style_guide,
        "\n\n## Lecture to Review\n\n",
        lecture_content
    ])
    
    full_message = "".join(message_parts)
    
    # Call Claude API
    print("\nSending request to Claude Sonnet 4.5...")
    print(f"Message size: {len(full_message):,} characters")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=16000,
            temperature=0,  # More consistent/deterministic output
            messages=[
                {
                    "role": "user",
                    "content": full_message
                }
            ]
        )
        
        return response.content[0].text
        
    except anthropic.APIError as e:
        print(f"\nClaude API Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Check a QuantEcon lecture against a specific style guide category using Claude",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single category - creates lecture-suggestions.md and lecture-corrected.md
  python style_checker.py my_lecture.md --focus writing
  python style_checker.py my_lecture.md --focus math
  python style_checker.py my_lecture.md --focus code
  
  # Multiple categories (sequential processing)
  python style_checker.py my_lecture.md --focus writing,math
  python style_checker.py my_lecture.md --focus writing,math,code

Available categories:
  writing     - Writing style and grammar
  math        - Mathematical notation
  code        - Code formatting and structure
  jax         - JAX library specific conventions
  figures     - Figure and visualization formatting
  references  - Bibliography and citations
  links       - Hyperlink formatting
  admonitions - Note/warning boxes
  
Output files (always created):
  {lecture-name}-suggestions.md  - Detailed review with violations and fixes
  {lecture-name}-corrected.md    - Fully corrected version of the lecture
  
Sequential processing (multiple categories):
  - Categories are processed in the order specified
  - Each category's corrections feed into the next category
  - All analyses are combined in {lecture-name}-suggestions.md
  - Final corrected version saved to {lecture-name}-corrected.md
        """
    )
    
    parser.add_argument(
        "lecture",
        help="Path to the lecture file to check"
    )
    
    parser.add_argument(
        "-f", "--focus",
        required=True,
        help="Category/categories to focus on (comma-separated). Available: writing, math, code, jax, figures, references, links, admonitions"
    )
    
    parser.add_argument(
        "--api-key",
        help="Claude API key (overrides ANTHROPIC_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    # Check that lecture file exists
    if not os.path.exists(args.lecture):
        print(f"Error: Lecture file not found: {args.lecture}")
        sys.exit(1)
    
    # Parse categories from comma-separated list
    categories = [cat.strip() for cat in args.focus.split(',')]
    
    # Validate all categories
    valid_categories = ["writing", "math", "code", "jax", "figures", "references", "links", "admonitions"]
    for cat in categories:
        if cat not in valid_categories:
            print(f"Error: Invalid category '{cat}'")
            print(f"Valid categories: {', '.join(valid_categories)}")
            sys.exit(1)
    
    # Load original lecture content
    print(f"Loading lecture: {args.lecture}")
    original_lecture = load_file(args.lecture)
    
    # Get base filename for output files
    lecture_base = args.lecture.rsplit('.', 1)[0]
    suggestions_file = f"{lecture_base}-suggestions.md"
    corrected_file = f"{lecture_base}-corrected.md"
    
    # Initialize variables for sequential processing
    current_content = original_lecture
    all_analyses = []
    
    # Process each category sequentially
    print(f"\nProcessing {len(categories)} categor{'y' if len(categories) == 1 else 'ies'}: {', '.join(categories)}\n")
    
    for idx, category in enumerate(categories, 1):
        print(f"{'='*80}")
        print(f"Processing category {idx}/{len(categories)}: {category}")
        print(f"{'='*80}")
        
        # Use progressively corrected content for sequential processing
        content_to_check = current_content
        
        # Run the style check for this category (always gets both analysis and corrected)
        review = check_lecture_style(
            lecture_content=content_to_check,
            category=category,
            api_key=args.api_key
        )
        
        # Extract corrected portion and analysis
        corrected_only = None
        if "CORRECTED LECTURE FILE" in review:
            separator = "="*80 + "\nCORRECTED LECTURE FILE\n" + "="*80
            parts = review.split(separator)
            if len(parts) == 2:
                analysis_part = parts[0].strip()
                corrected_only = parts[1].strip()
                
                # Store analysis with category header
                category_header = f"\n{'='*80}\n{category.upper()} CATEGORY REVIEW\n{'='*80}\n\n"
                all_analyses.append(category_header + analysis_part)
                
                # Update current_content for next category
                current_content = corrected_only
                print(f"  ✓ Category '{category}' analysis and corrections complete")
            else:
                all_analyses.append(review)
                print(f"  ⚠️ Could not extract corrected content for '{category}'")
        else:
            all_analyses.append(review)
            print(f"  ⚠️ No corrected content found for '{category}'")
        
        print()  # Blank line between categories
    
    # Save both output files
    print(f"{'='*80}")
    print("Saving results...")
    print(f"{'='*80}\n")
    
    # Save combined analysis
    combined_analysis = "\n\n".join(all_analyses)
    with open(suggestions_file, 'w', encoding='utf-8') as f:
        f.write(combined_analysis)
    print(f"✓ Suggestions saved to: {suggestions_file}")
    print(f"  ({len(categories)} category review{'s' if len(categories) > 1 else ''})")
    
    # Save final corrected content
    with open(corrected_file, 'w', encoding='utf-8') as f:
        f.write(current_content)
    print(f"✓ Corrected lecture saved to: {corrected_file}")
    print(f"  ({len(categories)} sequential correction{'s' if len(categories) > 1 else ''} applied)")
    
    print("\n✓ Style check complete!")


if __name__ == "__main__":
    main()
