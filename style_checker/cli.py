"""
qestyle — Local CLI for the QuantEcon Style Guide Checker

Shares the same review engine (StyleReviewer), prompts, and rules as the
GitHub Action, so results are identical.

Usage:
    qestyle lecture.md                          # Review, apply fixes, write report
    qestyle lecture.md --categories writing     # Check specific categories only
    qestyle lecture.md --dry-run                # Report only, don't modify the file

Install from GitHub:
    pip install git+https://github.com/QuantEcon/action-style-guide.git
"""

import argparse
import subprocess
import sys
import os
import unicodedata
from pathlib import Path
from datetime import datetime

from style_checker import __version__
from style_checker.reviewer import StyleReviewer


# All available categories (matches reviewer.RULE_EVALUATION_ORDER keys)
ALL_CATEGORIES = [
    "writing", "math", "code", "jax",
    "figures", "references", "links", "admonitions",
]


def display_width(s: str) -> int:
    """Calculate terminal display width, accounting for wide/emoji characters."""
    w = 0
    for c in s:
        # Variation selector-16 (U+FE0F) forces emoji presentation (width 2),
        # so add 1 to compensate for the base char already counted as 1
        if c == '\ufe0f':
            w += 1
            continue
        # Other zero-width characters
        if unicodedata.category(c) in ('Mn', 'Me', 'Cf') or c == '\ufe0e':
            continue
        eaw = unicodedata.east_asian_width(c)
        if eaw in ('W', 'F'):
            w += 2
        else:
            w += 1
    return w


def pad_to_width(s: str, target: int) -> str:
    """Pad string with spaces to reach target display width."""
    return s + ' ' * max(0, target - display_width(s))


def format_report(result: dict, lecture_path: str, dry_run: bool) -> str:
    """
    Format review results into a readable Markdown report.

    Report structure:
    1. Header with metadata
    2. Style Suggestions (unapplied — require human judgment)
    3. Warnings (if any)
    4. Applied Fixes summary (record of what was changed, at end)

    Args:
        result: Dictionary returned by StyleReviewer.review_lecture_single_rule()
        lecture_path: Path to the reviewed lecture file
        dry_run: If True, fixes were NOT applied (report-only mode)

    Returns:
        Markdown-formatted report string
    """
    lines = []
    lines.append(f"# Style Guide Report: {Path(lecture_path).name}")
    lines.append(f"")
    lines.append(f"- **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"- **Version:** qestyle v{__version__}")
    lines.append(f"- **Issues found:** {result.get('issues_found', 0)}")
    if dry_run:
        lines.append(f"- **Mode:** dry-run (no changes applied)")
    else:
        lines.append(f"- **Mode:** fix (rule violations applied to file)")
    lines.append(f"")

    rule_violations = result.get('rule_violations', [])
    style_violations = result.get('style_violations', [])
    warnings = result.get('warnings', [])

    # --- Style suggestions FIRST (these need human attention) ---
    if style_violations:
        lines.append(f"## 📝 Style Suggestions ({len(style_violations)})")
        lines.append(f"")
        lines.append("> **Action required:** These suggestions require human review and judgment.")
        lines.append(f"")

        for i, v in enumerate(style_violations, 1):
            lines.append(f"### {i}. {v.get('rule_id', 'unknown')} — {v.get('rule_title', '')}")
            if v.get('location'):
                lines.append(f"**Location:** {v['location']}")
            if v.get('description'):
                lines.append(f"**Description:** {v['description']}")
            if v.get('current_text'):
                lines.append(f"")
                lines.append(f"```")
                lines.append(v['current_text'])
                lines.append(f"```")
                lines.append(f"")
            if v.get('suggested_fix'):
                lines.append(f"**Suggestion:**")
                lines.append(f"")
                lines.append(f"```")
                lines.append(v['suggested_fix'])
                lines.append(f"```")
                lines.append(f"")
            if v.get('explanation'):
                lines.append(f"**Explanation:** {v['explanation']}")
            lines.append(f"")

    # --- Warnings ---
    if warnings:
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## Warnings ({len(warnings)})")
        lines.append(f"")
        for w in warnings:
            lines.append(f"- {w}")
        lines.append(f"")

    # --- Applied fixes AT THE END (diagnostic record) ---
    if rule_violations:
        lines.append(f"---")
        lines.append(f"")
        if dry_run:
            lines.append(f"## 🔧 Rule Violations ({len(rule_violations)})")
            lines.append(f"")
            lines.append("> **Fixable:** These violations can be auto-fixed (run without `--dry-run`).")
        else:
            lines.append(f"## ✅ Applied Fixes ({len(rule_violations)})")
            lines.append(f"")
            lines.append("> **No action required:** The following rule violations were automatically fixed in the lecture file.")
        lines.append(f"")

        for i, v in enumerate(rule_violations, 1):
            lines.append(f"### {i}. {v.get('rule_id', 'unknown')} — {v.get('rule_title', '')}")
            if v.get('location'):
                lines.append(f"**Location:** {v['location']}")
            if v.get('description'):
                lines.append(f"**Description:** {v['description']}")
            if v.get('current_text'):
                lines.append(f"**Current text:**")
                lines.append(f"")
                lines.append(f"```")
                lines.append(v['current_text'])
                lines.append(f"```")
                lines.append(f"")
            if v.get('suggested_fix'):
                if dry_run:
                    lines.append(f"**Suggested fix:**")
                else:
                    lines.append(f"**Applied fix:**")
                lines.append(f"")
                lines.append(f"```")
                lines.append(v['suggested_fix'])
                lines.append(f"```")
                lines.append(f"")
            if v.get('explanation'):
                lines.append(f"**Explanation:** {v['explanation']}")
            lines.append(f"")

    if not rule_violations and not style_violations:
        lines.append("No issues found — lecture complies with the style guide.")
        lines.append(f"")

    return "\n".join(lines)


def default_report_path(lecture_path: Path) -> Path:
    """Return the default report file path: qestyle-{stem}.md next to the lecture."""
    return lecture_path.parent / f"qestyle-{lecture_path.stem}.md"


def check_git_dirty(lecture_path: Path) -> bool:
    """
    Check if the lecture file has uncommitted changes in git.

    Returns True if the file has uncommitted changes (staged or unstaged),
    False if it's clean or not in a git repo.
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", str(lecture_path)],
            capture_output=True, text=True,
            cwd=lecture_path.parent,
            timeout=5,
        )
        # Non-zero exit = not a git repo or git error — skip the check
        if result.returncode != 0:
            return False
        # If output is non-empty, the file has uncommitted changes
        return bool(result.stdout.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired):
        # git not installed or timed out — skip the check
        return False


def main():
    """CLI entry point for qestyle."""
    parser = argparse.ArgumentParser(
        prog="qestyle",
        description="QuantEcon Style Guide Checker — local CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  qestyle lecture.md                          # Review, apply fixes, write report
  qestyle lecture.md --categories writing     # Check writing rules only
  qestyle lecture.md --dry-run                # Report only, don't modify the file
  qestyle lecture.md -o custom-report.md      # Write report to a custom path

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
        "--dry-run",
        action="store_true",
        help="Report only — do not apply fixes to the file",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Write report to this path (default: qestyle-{lecture}.md)",
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
    lecture_path = Path(args.lecture).resolve()
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

    # --- Check for uncommitted changes (only in fix mode) ---
    if not args.dry_run and check_git_dirty(lecture_path):
        title = f"Uncommitted changes: {lecture_path.name}"
        hint1 = "git commit  -- save your current changes first"
        hint2 = "git stash   -- temporarily shelve changes"
        body  = "qestyle will modify this file directly."
        # Use plain ASCII for reliable width calculation
        content_lines = [title, body, hint1, hint2]
        inner = max(len(l) for l in content_lines) + 4
        print()
        print(f"  ┌{'─' * inner}┐")
        print(f"  │  {title:<{inner - 2}}│")
        print(f"  │{' ' * inner}│")
        print(f"  │  {body:<{inner - 2}}│")
        print(f"  │{' ' * inner}│")
        print(f"  │  {hint1:<{inner - 2}}│")
        print(f"  │  {hint2:<{inner - 2}}│")
        print(f"  └{'─' * inner}┘")
        print()
        try:
            answer = input("  Continue anyway? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            answer = ""
        if answer not in ("y", "yes"):
            print("\n  Aborted — commit or stash your changes, then try again.\n")
            sys.exit(0)
        print()

    # --- Run review ---
    print(f"📋 qestyle v{__version__}")
    print(f"   Lecture:    {lecture_path.name}")
    print(f"   Categories: {', '.join(categories)}")
    if args.dry_run:
        print("   Mode:       dry-run (report only, no changes)")
    else:
        print("   Mode:       fix (rule violations will be applied)")
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
    rule_count = len(result.get("rule_violations", []))
    style_count = len(result.get("style_violations", []))

    print(f"\n✅ Review complete — {issues_found} issue(s) found")

    # --- Apply fixes (default behavior, unless --dry-run) ---
    fixes_applied = False
    if not args.dry_run and result.get("corrected_content"):
        corrected = result["corrected_content"]
        if corrected != content:
            lecture_path.write_text(corrected, encoding="utf-8")
            fixes_applied = True
            print(f"   🔧 Applied {rule_count} fix(es) to {lecture_path.name}")
            print(f"      Restore original: git checkout {lecture_path.name}")
        else:
            print("   No fixable changes to apply")
    elif args.dry_run and rule_count > 0:
        print(f"   🔧 {rule_count} fix(es) available (run without --dry-run to apply)")

    if style_count > 0:
        print(f"   📝 {style_count} style suggestion(s) for human review")

    # --- Write report ---
    report = format_report(result, str(lecture_path), dry_run=args.dry_run)

    if args.output:
        report_path = Path(args.output)
    else:
        report_path = default_report_path(lecture_path)

    report_path.write_text(report, encoding="utf-8")
    print(f"   📄 Report: {report_path}")
    print()


if __name__ == "__main__":
    main()
