"""
qestyle — Local CLI for the QuantEcon Style Guide Checker

Shares the same review engine (StyleReviewer), prompts, and rules as the
GitHub Action, so results are identical.

Usage:
    qestyle lecture.md                          # Report all categories
    qestyle lecture.md --categories writing     # Report specific categories
    qestyle lecture.md --fix                    # Apply rule-type fixes in place

Install from GitHub:
    pip install git+https://github.com/QuantEcon/action-style-guide.git
"""

import argparse
import sys
import os
from pathlib import Path
from datetime import datetime

from style_checker import __version__
from style_checker.reviewer import StyleReviewer


# All available categories (matches reviewer.RULE_EVALUATION_ORDER keys)
ALL_CATEGORIES = [
    "writing", "math", "code", "jax",
    "figures", "references", "links", "admonitions",
]


def format_report(result: dict, lecture_path: str, fix_mode: bool) -> str:
    """
    Format review results into a readable Markdown report.

    Args:
        result: Dictionary returned by StyleReviewer.review_lecture_single_rule()
        lecture_path: Path to the reviewed lecture file
        fix_mode: Whether --fix was used (affects report wording)

    Returns:
        Markdown-formatted report string
    """
    lines = []
    lines.append(f"# Style Guide Report: {Path(lecture_path).name}")
    lines.append(f"")
    lines.append(f"- **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"- **Version:** qestyle v{__version__}")
    lines.append(f"- **Issues found:** {result.get('issues_found', 0)}")
    lines.append(f"")

    rule_violations = result.get('rule_violations', [])
    style_violations = result.get('style_violations', [])
    warnings = result.get('warnings', [])

    # Rule violations (auto-fixable)
    if rule_violations:
        if fix_mode:
            lines.append(f"## Applied Fixes ({len(rule_violations)})")
            lines.append(f"")
            lines.append("The following rule violations were automatically fixed:")
        else:
            lines.append(f"## Rule Violations ({len(rule_violations)})")
            lines.append(f"")
            lines.append("These violations can be auto-fixed with `qestyle --fix`:")
        lines.append(f"")

        for i, v in enumerate(rule_violations, 1):
            lines.append(f"### {i}. {v.get('rule_id', 'unknown')} — {v.get('rule_title', '')}")
            if v.get('location'):
                lines.append(f"**Location:** {v['location']}")
            if v.get('description'):
                lines.append(f"**Description:** {v['description']}")
            if v.get('current_text'):
                lines.append(f"**Current text:**")
                lines.append(f"```")
                lines.append(v['current_text'])
                lines.append(f"```")
            if v.get('suggested_fix'):
                lines.append(f"**Suggested fix:**")
                lines.append(f"```")
                lines.append(v['suggested_fix'])
                lines.append(f"```")
            if v.get('explanation'):
                lines.append(f"**Explanation:** {v['explanation']}")
            lines.append(f"")

    # Style suggestions (human review)
    if style_violations:
        lines.append(f"## Style Suggestions ({len(style_violations)})")
        lines.append(f"")
        lines.append("These are advisory suggestions that require human judgment:")
        lines.append(f"")

        for i, v in enumerate(style_violations, 1):
            lines.append(f"### {i}. {v.get('rule_id', 'unknown')} — {v.get('rule_title', '')}")
            if v.get('location'):
                lines.append(f"**Location:** {v['location']}")
            if v.get('description'):
                lines.append(f"**Description:** {v['description']}")
            if v.get('current_text'):
                lines.append(f"```")
                lines.append(v['current_text'])
                lines.append(f"```")
            if v.get('suggested_fix'):
                lines.append(f"**Suggestion:**")
                lines.append(f"```")
                lines.append(v['suggested_fix'])
                lines.append(f"```")
            if v.get('explanation'):
                lines.append(f"**Explanation:** {v['explanation']}")
            lines.append(f"")

    # Warnings
    if warnings:
        lines.append(f"## Warnings ({len(warnings)})")
        lines.append(f"")
        for w in warnings:
            lines.append(f"- {w}")
        lines.append(f"")

    if not rule_violations and not style_violations:
        lines.append("No issues found — lecture complies with the style guide.")
        lines.append(f"")

    return "\n".join(lines)


def main():
    """CLI entry point for qestyle."""
    parser = argparse.ArgumentParser(
        prog="qestyle",
        description="QuantEcon Style Guide Checker — local CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  qestyle lecture.md                          # Report all categories
  qestyle lecture.md --categories writing     # Report writing rules only
  qestyle lecture.md --categories math,code   # Report math and code rules
  qestyle lecture.md --fix                    # Apply rule-type fixes in place

Categories:
  writing, math, code, jax, figures, references, links, admonitions
        """,
    )

    parser.add_argument(
        "lecture",
        help="Path to the lecture .md file to check",
    )
    parser.add_argument(
        "-c", "--categories",
        default=None,
        help="Comma-separated categories to check (default: all)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply rule-type fixes to the lecture file in place",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Write report to this file instead of stdout",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="Anthropic API key (overrides ANTHROPIC_API_KEY env var)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Claude model to use (default: claude-sonnet-4-5-20250929)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="LLM temperature, 0=deterministic (default: 0)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"qestyle {__version__}",
    )

    args = parser.parse_args()

    # --- Validate inputs ---
    lecture_path = Path(args.lecture)
    if not lecture_path.exists():
        print(f"Error: file not found: {lecture_path}", file=sys.stderr)
        sys.exit(1)

    # Parse categories
    if args.categories:
        categories = [c.strip() for c in args.categories.split(",")]
        invalid = [c for c in categories if c not in ALL_CATEGORIES]
        if invalid:
            print(f"Error: invalid categories: {', '.join(invalid)}", file=sys.stderr)
            print(f"Valid categories: {', '.join(ALL_CATEGORIES)}", file=sys.stderr)
            sys.exit(1)
    else:
        categories = list(ALL_CATEGORIES)

    # API key
    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'", file=sys.stderr)
        sys.exit(1)

    # --- Run review ---
    print(f"qestyle v{__version__}")
    print(f"Lecture: {lecture_path}")
    print(f"Categories: {', '.join(categories)}")
    if args.fix:
        print("Mode: fix (rule-type violations will be applied)")
    else:
        print("Mode: report only")
    print()

    # Read lecture content
    content = lecture_path.read_text(encoding="utf-8")
    lecture_name = lecture_path.stem

    # Initialize reviewer (same engine as the GitHub Action)
    reviewer = StyleReviewer(
        api_key=api_key,
        model=args.model,
        temperature=args.temperature,
    )

    # Run the review
    result = reviewer.review_lecture_single_rule(content, categories, lecture_name)

    issues_found = result.get("issues_found", 0)
    print(f"\nReview complete: {issues_found} issue(s) found")

    # --- Apply fixes if requested ---
    if args.fix and result.get("corrected_content"):
        corrected = result["corrected_content"]
        if corrected != content:
            lecture_path.write_text(corrected, encoding="utf-8")
            rule_count = len(result.get("rule_violations", []))
            print(f"Applied {rule_count} fix(es) to {lecture_path}")
        else:
            print("No fixable changes to apply")

    # --- Write report ---
    report = format_report(result, str(lecture_path), fix_mode=args.fix)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding="utf-8")
        print(f"Report written to {output_path}")
    else:
        print()
        print(report)


if __name__ == "__main__":
    main()
