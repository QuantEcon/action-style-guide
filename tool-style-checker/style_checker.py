#!/usr/bin/env python3
"""
QuantEcon Lecture Style Checker using Claude API

This script automates the process of checking a lecture against the 
QuantEcon style guide using Claude Sonnet 4.5.

Usage:
    python style_checker.py <lecture_file.md>
    python style_checker.py <lecture_file.md> --output review.md
    python style_checker.py <lecture_file.md> --mode corrected
    python style_checker.py <lecture_file.md> --mode both
    python style_checker.py <lecture_file.md> --focus writing,math
    python style_checker.py <lecture_file.md> --quick

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


def check_lecture_style(
    lecture_path,
    prompt_path="claude-style-checker-prompt.md",
    style_guide_path="style-guide-database.md",
    focus_areas=None,
    quick_mode=False,
    output_mode="suggestions",
    api_key=None
):
    """
    Check a lecture against the style guide using Claude.
    
    Args:
        lecture_path: Path to the lecture file to check
        prompt_path: Path to the prompt file
        style_guide_path: Path to the style guide database
        focus_areas: List of rule categories to focus on (e.g., ['writing', 'math'])
        quick_mode: If True, only report critical violations
        output_mode: Output type - 'suggestions' (default), 'corrected', or 'both'
        api_key: Claude API key (if not provided, uses ANTHROPIC_API_KEY env var)
    
    Returns:
        String containing Claude's output (review, corrected file, or both)
    """
    # Load files
    print(f"Loading lecture: {lecture_path}")
    lecture = load_file(lecture_path)
    
    print(f"Loading prompt: {prompt_path}")
    prompt = load_file(prompt_path)
    
    print(f"Loading style guide: {style_guide_path}")
    style_guide = load_file(style_guide_path)
    
    # Get API key
    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Build the message
    message_parts = [prompt]
    
    # Add focus instructions if specified
    if focus_areas:
        focus_text = ", ".join([f"qe-{area}-*" for area in focus_areas])
        message_parts.append(
            f"\n\n**SPECIAL INSTRUCTIONS**: Please focus your review on these "
            f"rule categories: {focus_text}. You may skip other categories.\n"
        )
    
    # Add quick mode instructions if specified
    if quick_mode:
        message_parts.append(
            "\n\n**QUICK MODE**: Please provide only a summary and the most "
            "critical violations (rule category). Skip minor style suggestions "
            "and positive observations to save time.\n"
        )
    
    # Add output mode instructions
    if output_mode == "corrected":
        message_parts.append(
            "\n\n**OUTPUT MODE: CORRECTED FILE**\n\n"
            "Please provide ONLY the fully corrected version of the lecture file with "
            "all violations fixed. Do NOT include the review, explanations, or violation "
            "list. Just output the corrected markdown file content that can be directly "
            "saved as the new lecture file.\n\n"
            "Apply ALL rule violations fixes while preserving:\n"
            "- All technical content and accuracy\n"
            "- All code blocks and their functionality\n"
            "- All MyST markdown syntax\n"
            "- The overall structure and organization\n"
        )
    elif output_mode == "both":
        message_parts.append(
            "\n\n**OUTPUT MODE: BOTH**\n\n"
            "Please provide TWO sections in your response:\n\n"
            "1. First, provide the complete style review as usual (with violations, "
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
        lecture
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
        description="Check a QuantEcon lecture against the style guide using Claude",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python style_checker.py my_lecture.md
  python style_checker.py my_lecture.md --output review.md
  python style_checker.py my_lecture.md --mode corrected
  python style_checker.py my_lecture.md --mode both --output combined.md
  python style_checker.py my_lecture.md --focus writing math
  python style_checker.py my_lecture.md --quick
  python style_checker.py my_lecture.md --prompt custom_prompt.md
        """
    )
    
    parser.add_argument(
        "lecture",
        help="Path to the lecture file to check"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Save review to this file (default: print to stdout)"
    )
    
    parser.add_argument(
        "--prompt",
        default="claude-style-checker-prompt.md",
        help="Path to the prompt file (default: claude-style-checker-prompt.md)"
    )
    
    parser.add_argument(
        "--style-guide",
        default="style-guide-database.md",
        help="Path to the style guide database (default: style-guide-database.md)"
    )
    
    parser.add_argument(
        "--focus",
        nargs="+",
        help="Focus on specific rule categories (e.g., writing math code)"
    )
    
    parser.add_argument(
        "--mode",
        choices=["suggestions", "corrected", "both"],
        default="suggestions",
        help="Output mode: 'suggestions' (default - review only), 'corrected' (fixed file only), 'both' (review + fixed file)"
    )
    
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick mode: only report critical violations"
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
    
    # Run the style check
    review = check_lecture_style(
        lecture_path=args.lecture,
        prompt_path=args.prompt,
        style_guide_path=args.style_guide,
        focus_areas=args.focus,
        quick_mode=args.quick,
        output_mode=args.mode,
        api_key=args.api_key
    )
    
    # Handle output based on mode
    if args.mode == "corrected":
        # Output is the corrected lecture file
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(review)
            print(f"\n✓ Corrected lecture saved to: {args.output}")
        else:
            # Suggest saving to file
            print("\n" + "="*80)
            print("CORRECTED LECTURE FILE")
            print("="*80 + "\n")
            print(review)
            print("\n" + "="*80)
            print("TIP: Save to file with: --output corrected-lecture.md")
            print("="*80)
    
    elif args.mode == "both":
        # Output contains both review and corrected file
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(review)
            print(f"\n✓ Review and corrected file saved to: {args.output}")
            
            # Also try to extract and save the corrected portion separately
            if "CORRECTED LECTURE FILE" in review:
                separator = "="*80 + "\nCORRECTED LECTURE FILE\n" + "="*80
                parts = review.split(separator)
                if len(parts) == 2:
                    corrected_only = parts[1].strip()
                    # Name corrected file after the input lecture, not the output file
                    lecture_base = args.lecture.rsplit('.', 1)[0]
                    corrected_file = f"{lecture_base}-corrected.md"
                    with open(corrected_file, 'w', encoding='utf-8') as f:
                        f.write(corrected_only)
                    print(f"✓ Corrected lecture also saved to: {corrected_file}")
        else:
            print("\n" + "="*80)
            print("REVIEW AND CORRECTED FILE")
            print("="*80 + "\n")
            print(review)
    
    else:  # suggestions mode (default)
        # Output the review
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(review)
            print(f"\n✓ Review saved to: {args.output}")
        else:
            print("\n" + "="*80)
            print("STYLE REVIEW")
            print("="*80 + "\n")
            print(review)
    
    print("\n✓ Style check complete!")


if __name__ == "__main__":
    main()
