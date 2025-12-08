"""
Main entry point for the style guide checker
Orchestrates the review process
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Optional
from datetime import datetime

# Add the action directory to Python path for imports
action_path = Path(__file__).parent.parent
sys.path.insert(0, str(action_path))

from style_checker.reviewer import StyleReviewer
from style_checker.github_handler import GitHubHandler
from style_checker import __version__


def review_single_lecture(
    lecture_name: str,
    gh_handler: GitHubHandler,
    reviewer: StyleReviewer,
    lectures_path: str,
    create_pr: bool,
    pr_branch_prefix: str,
    categories: Optional[List[str]] = None
) -> dict:
    """
    Review a single lecture and optionally create PR.
    
    Args:
        lecture_name: Name of the lecture to review
        gh_handler: GitHub API handler
        reviewer: LLM-based style reviewer
        lectures_path: Path to lectures directory
        create_pr: Whether to create a PR with fixes
        pr_branch_prefix: Prefix for PR branch name
        categories: Optional list of categories to check (e.g., ["writing", "math"])
                   If None or ["all"], uses sequential category processing
    
    Returns:
        Dictionary with review results and PR info
    """
    print(f"\n{'='*60}")
    print(f"📚 Reviewing lecture: {lecture_name}")
    print(f"{'='*60}\n")
    
    # Find lecture file
    lecture_file = gh_handler.find_lecture_file(lecture_name, lectures_path)
    if not lecture_file:
        print(f"❌ Lecture file not found: {lecture_name}")
        return {'error': 'File not found', 'lecture': lecture_name}
    
    print(f"📄 Found lecture file: {lecture_file}")
    
    # Get lecture content
    content = gh_handler.get_lecture_content(lecture_file)
    print(f"📖 Loaded {len(content)} characters")
    
    # Perform review
    if not categories or categories == ['all']:
        # Use smart sequential category processing (default behavior)
        review_result = reviewer.review_lecture_smart(content, lecture_name)
    else:
        # Use single-rule evaluation for comprehensive coverage
        print(f"🎯 Checking specific categories: {', '.join(categories)}")
        review_result = reviewer.review_lecture_single_rule(content, categories, lecture_name)
    
    issues_found = review_result.get('issues_found', 0)
    print(f"\n📊 Review complete: {issues_found} issues found")
    
    if 'error' in review_result:
        print(f"❌ Error during review: {review_result['error']}")
        print(f"❌ Review failed - exiting with error")
        return review_result
    
    # Create PR if requested
    if create_pr and issues_found > 0:
        print(f"\n📝 Creating pull request...")
        
        # Create branch
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        branch_name = f"{pr_branch_prefix}/{lecture_name}-{timestamp}"
        gh_handler.create_branch(branch_name)
        print(f"✓ Created branch: {branch_name}")
        
        # Commit changes
        commit_msg = gh_handler.format_commit_message(
            review_result.get('violations', []),
            lecture_name
        )
        gh_handler.commit_changes(
            lecture_file,
            review_result.get('corrected_content', content),
            commit_msg,
            branch_name
        )
        print(f"✓ Committed changes")
        
        # Create PR with concise summary
        pr_title = f"[{lecture_name}] Style guide review"
        pr_body = gh_handler.format_pr_body(review_result, lecture_name)
        
        # Parse PR labels
        pr_labels = ['automated', 'style-guide', 'review']
        if args.pr_labels:
            custom_labels = [l.strip() for l in args.pr_labels.split(',') if l.strip()]
            pr_labels.extend(custom_labels)
        
        pr_number, pr_url = gh_handler.create_pull_request(
            title=pr_title,
            body=pr_body,
            head_branch=branch_name,
            labels=pr_labels
        )
        print(f"✓ Created PR #{pr_number}: {pr_url}")
        
        # Add applied fixes report (rule category) as a collapsible comment
        applied_fixes_report = gh_handler.format_applied_fixes_report(review_result, lecture_name)
        if applied_fixes_report:
            gh_handler.add_comment_to_pr(pr_number, applied_fixes_report)
            print(f"✓ Added applied fixes report as PR comment")
        
        # Add style suggestions report (style category) as an open, visible comment
        style_suggestions_report = gh_handler.format_style_suggestions_report(review_result, lecture_name)
        if style_suggestions_report:
            gh_handler.add_comment_to_pr(pr_number, style_suggestions_report)
            print(f"✓ Added style suggestions report as PR comment")
        
        review_result['pr_number'] = pr_number
        review_result['pr_url'] = pr_url
    elif create_pr and issues_found == 0:
        print(f"✅ No issues found - no PR needed")
    
    return review_result


def review_bulk_lectures(
    gh_handler: GitHubHandler,
    reviewer: StyleReviewer,
    lectures_path: str,
    create_pr: bool,
    pr_branch_prefix: str,
    pr_labels: str = ''
) -> dict:
    """
    Review all lectures in directory and create single PR
    
    Returns:
        Dictionary with summary of all reviews and PR info
    """
    print(f"\n{'='*60}")
    print(f"📚 Bulk Review: All Lectures")
    print(f"{'='*60}\n")
    
    # Get all lectures
    lectures = gh_handler.get_all_lectures(lectures_path)
    print(f"Found {len(lectures)} lecture files")
    
    if not lectures:
        print("❌ No lectures found")
        return {'error': 'No lectures found'}
    
    # Create branch for all changes
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    branch_name = f"{pr_branch_prefix}/bulk-review-{timestamp}"
    
    if create_pr:
        gh_handler.create_branch(branch_name)
        print(f"✓ Created branch: {branch_name}\n")
    
    # Review each lecture
    all_results = []
    total_issues = 0
    
    for i, lecture_file in enumerate(lectures, 1):
        lecture_name = Path(lecture_file).stem
        print(f"\n[{i}/{len(lectures)}] Reviewing: {lecture_name}")
        
        try:
            # Get content
            content = gh_handler.get_lecture_content(lecture_file)
            
            # Review using sequential category processing
            result = reviewer.review_lecture_smart(content, lecture_name)
            
            issues_found = result.get('issues_found', 0)
            total_issues += issues_found
            print(f"  → {issues_found} issues found")
            
            # Commit if there are changes
            if create_pr and issues_found > 0:
                commit_msg = gh_handler.format_commit_message(
                    result.get('violations', []),
                    lecture_name
                )
                gh_handler.commit_changes(
                    lecture_file,
                    result.get('corrected_content', content),
                    commit_msg,
                    branch_name
                )
                print(f"  ✓ Committed fixes")
            
            all_results.append(result)
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            all_results.append({'error': str(e), 'lecture': lecture_name})
    
    # Create single PR with all changes
    if create_pr and total_issues > 0:
        print(f"\n📝 Creating pull request for bulk review...")
        
        pr_title = f"Style guide bulk review ({len(lectures)} lectures)"
        pr_body = format_bulk_pr_body(all_results, total_issues)
        
        # Parse PR labels
        labels = ['automated', 'style-guide', 'bulk-review']
        if pr_labels:
            custom_labels = [l.strip() for l in pr_labels.split(',') if l.strip()]
            labels.extend(custom_labels)
        
        pr_number, pr_url = gh_handler.create_pull_request(
            title=pr_title,
            body=pr_body,
            head_branch=branch_name,
            labels=labels
        )
        print(f"✓ Created PR #{pr_number}: {pr_url}")
        
        return {
            'lectures_reviewed': len(lectures),
            'total_issues': total_issues,
            'pr_number': pr_number,
            'pr_url': pr_url,
            'results': all_results
        }
    
    return {
        'lectures_reviewed': len(lectures),
        'total_issues': total_issues,
        'results': all_results
    }


def format_bulk_pr_body(results: List[dict], total_issues: int) -> str:
    """Format PR body for bulk review"""
    body = "## 📋 Bulk Style Guide Review\n\n"
    body += f"Automated review of all lectures in the repository.\n\n"
    body += f"### 📊 Summary\n\n"
    body += f"- **Total Issues:** {total_issues}\n"
    body += f"- **Lectures Reviewed:** {len(results)}\n"
    body += f"- **Review Date:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
    
    # Group results
    with_issues = [r for r in results if r.get('issues_found', 0) > 0]
    clean = [r for r in results if r.get('issues_found', 0) == 0]
    errors = [r for r in results if 'error' in r]
    
    if with_issues:
        body += f"### 📝 Lectures with Issues ({len(with_issues)})\n\n"
        for result in with_issues:
            name = result.get('lecture_name', 'Unknown')
            issues = result.get('issues_found', 0)
            body += f"- **{name}**: {issues} issues\n"
        body += "\n"
    
    if clean:
        body += f"### ✅ Clean Lectures ({len(clean)})\n\n"
        for result in clean[:10]:  # Show first 10
            name = result.get('lecture_name', 'Unknown')
            body += f"- {name}\n"
        if len(clean) > 10:
            body += f"- ... and {len(clean) - 10} more\n"
        body += "\n"
    
    if errors:
        body += f"### ❌ Errors ({len(errors)})\n\n"
        for result in errors:
            name = result.get('lecture', 'Unknown')
            error = result.get('error', 'Unknown error')
            body += f"- **{name}**: {error}\n"
        body += "\n"
    
    body += "---\n\n"
    body += "*🤖 This PR was automatically generated by the QuantEcon Style Guide Checker*\n"
    body += "*Each lecture fix is in a separate commit for easy review and reversion*\n"
    
    return body


def main():
    """Main entry point"""
    # Print version information
    print("=" * 70)
    print(f"📋 QuantEcon Style Guide Checker v{__version__}")
    print("=" * 70)
    print()
    
    parser = argparse.ArgumentParser(description='QuantEcon Style Guide Checker')
    parser.add_argument('--mode', required=True, choices=['single', 'bulk'],
                       help='Review mode: single lecture or bulk')
    parser.add_argument('--lectures-path', default='lectures/',
                       help='Path to lectures directory')
    parser.add_argument('--llm-model', help='Specific Claude model (default: claude-sonnet-4-5-20250929)')
    parser.add_argument('--rule-categories', default='',
                       help='Comma-separated rule categories to check')
    parser.add_argument('--create-pr', default='true',
                       help='Whether to create PR')
    parser.add_argument('--pr-branch-prefix', default='style-guide',
                       help='Prefix for PR branches')
    parser.add_argument('--pr-labels', default='',
                       help='Comma-separated PR labels')
    parser.add_argument('--comment-body', help='Issue comment body (for single mode)')
    parser.add_argument('--repository', required=True,
                       help='GitHub repository (owner/repo)')
    parser.add_argument('--github-ref', help='GitHub ref')
    
    args = parser.parse_args()
    
    # Setup
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("❌ GITHUB_TOKEN not set")
        sys.exit(1)
    
    create_pr = args.create_pr.lower() == 'true'
    
    # Initialize handlers
    gh_handler = GitHubHandler(github_token, args.repository)
    reviewer = StyleReviewer(model=args.llm_model)
    
    # Run review
    try:
        if args.mode == 'single':
            # Extract lecture name and categories from comment
            if args.comment_body:
                result = gh_handler.extract_lecture_from_comment(args.comment_body)
                if not result:
                    print("❌ Could not extract lecture name from comment")
                    sys.exit(1)
                
                lecture_name, categories = result
                print(f"📝 Lecture: {lecture_name}")
                print(f"🏷️  Categories: {', '.join(categories)}")
            else:
                print("❌ --comment-body required for single mode")
                sys.exit(1)
            
            result = review_single_lecture(
                lecture_name=lecture_name,
                gh_handler=gh_handler,
                reviewer=reviewer,
                lectures_path=args.lectures_path,
                create_pr=create_pr,
                pr_branch_prefix=args.pr_branch_prefix,
                categories=categories
            )
            
            # Set outputs for GitHub Actions (using environment file)
            github_output = os.environ.get('GITHUB_OUTPUT')
            if github_output:
                with open(github_output, 'a') as f:
                    if 'pr_number' in result:
                        f.write(f"pr-number={result['pr_number']}\n")
                        f.write(f"pr-url={result['pr_url']}\n")
                    f.write(f"issues-found={result.get('issues_found', 0)}\n")
                    f.write(f"lectures-reviewed=1\n")
            
            # Print summary
            print(f"\n{'='*60}")
            print(f"📊 REVIEW SUMMARY")
            print(f"{'='*60}")
            print(f"Lecture: {lecture_name}")
            print(f"Issues found: {result.get('issues_found', 0)}")
            if 'pr_number' in result:
                print(f"Pull Request: #{result['pr_number']}")
                print(f"URL: {result['pr_url']}")
                print(f"Status: ✅ PR created successfully")
            elif result.get('issues_found', 0) == 0:
                print(f"Status: ✅ No issues found - lecture complies with style guide")
            elif not create_pr:
                print(f"Status: ℹ️  Issues found but PR creation disabled")
            else:
                print(f"Status: ⚠️  Issues found but no PR created")
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                print(f"{'='*60}\n")
                sys.exit(1)  # Exit with failure code
            print(f"{'='*60}\n")
            
        else:  # bulk mode
            result = review_bulk_lectures(
                gh_handler=gh_handler,
                reviewer=reviewer,
                lectures_path=args.lectures_path,
                create_pr=create_pr,
                pr_branch_prefix=args.pr_branch_prefix,
                pr_labels=args.pr_labels
            )
            
            # Set outputs for GitHub Actions (using environment file)
            github_output = os.environ.get('GITHUB_OUTPUT')
            if github_output:
                with open(github_output, 'a') as f:
                    if 'pr_number' in result:
                        f.write(f"pr-number={result['pr_number']}\n")
                        f.write(f"pr-url={result['pr_url']}\n")
                    f.write(f"issues-found={result.get('total_issues', 0)}\n")
                    f.write(f"lectures-reviewed={result.get('lectures_reviewed', 0)}\n")
            
            # Print summary
            print(f"\n{'='*60}")
            print(f"📊 BULK REVIEW SUMMARY")
            print(f"{'='*60}")
            print(f"Lectures reviewed: {result.get('lectures_reviewed', 0)}")
            print(f"Total issues found: {result.get('total_issues', 0)}")
            print(f"Lectures with issues: {result.get('lectures_with_issues', 0)}")
            if 'pr_number' in result:
                print(f"Pull Request: #{result['pr_number']}")
                print(f"URL: {result['pr_url']}")
                print(f"Status: ✅ PR created with fixes for all lectures")
            elif result.get('total_issues', 0) == 0:
                print(f"Status: ✅ All lectures comply with style guide")
            elif not create_pr:
                print(f"Status: ℹ️  Issues found but PR creation disabled")
            else:
                print(f"Status: ⚠️  Issues found but no PR created")
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                print(f"{'='*60}\n")
                sys.exit(1)  # Exit with failure code
            print(f"{'='*60}\n")
        
        print(f"\n{'='*60}")
        print(f"✅ Review complete!")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
