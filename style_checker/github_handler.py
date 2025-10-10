"""
GitHub Integration Handler
Manages PRs, issues, and comments
"""

import os
import re
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from github import Github, GithubException
from datetime import datetime


class GitHubHandler:
    """Handles GitHub API interactions for PR and issue management"""
    
    # Valid category names (must match files in style_checker/rules/)
    VALID_CATEGORIES = {
        'writing', 'math', 'code', 'jax',
        'figures', 'references', 'links', 'admonitions'
    }
    
    def __init__(self, token: str, repository: str):
        """
        Initialize GitHub handler
        
        Args:
            token: GitHub token or GitHub App token
            repository: Repository in format 'owner/repo'
        """
        self.github = Github(token)
        self.repo = self.github.get_repo(repository)
        self.repository = repository
    
    def extract_lecture_from_comment(self, comment_body: str) -> Optional[Tuple[str, List[str]]]:
        """
        Extract lecture name and categories from issue comment.
        
        Supports both old and new syntax:
        - Old: @quantecon-style-guide lecture_name
        - New: @qe-style-checker lecture_name writing,math
        
        Args:
            comment_body: Full comment text
            
        Returns:
            Tuple of (lecture_name, categories) or None if not found.
            Categories is a list like ["writing", "math"] or ["all"] if not specified.
        """
        # New syntax: @qe-style-checker lecture_name [categories]
        new_patterns = [
            r'@qe-style-checker\s+(\S+)\s+([\w,]+)',  # With categories
            r'@qe-style-checker\s+`(\S+)`\s+([\w,]+)',  # With backticks and categories
            r'@qe-style-checker\s+lectures/(\S+)\s+([\w,]+)',  # With lectures/ prefix and categories
            r'@qe-style-checker\s+(\S+)',  # Without categories (default to "all")
            r'@qe-style-checker\s+`(\S+)`',  # With backticks only
            r'@qe-style-checker\s+lectures/(\S+)',  # With lectures/ prefix only
        ]
        
        for pattern in new_patterns:
            match = re.search(pattern, comment_body)
            if match:
                lecture = match.group(1)
                # Clean up lecture name
                lecture = lecture.replace('.md', '')  # Remove .md extension
                lecture = lecture.replace('lectures/', '')  # Remove lectures/ prefix
                lecture = lecture.strip('`')  # Remove backticks
                
                # Parse categories if provided (group 2)
                if len(match.groups()) > 1 and match.group(2):
                    categories = [cat.strip() for cat in match.group(2).split(',')]
                    
                    # Validate categories
                    if categories != ['all']:
                        invalid = [c for c in categories if c not in self.VALID_CATEGORIES]
                        if invalid:
                            print(f"⚠️  Invalid categories: {', '.join(invalid)}")
                            print(f"   Valid categories: {', '.join(sorted(self.VALID_CATEGORIES))}")
                            return None
                else:
                    categories = ['all']  # Default to all categories
                
                return (lecture, categories)
        
        # Fall back to old syntax for backward compatibility
        old_patterns = [
            r'@quantecon-style-guide\s+(\S+)',  # Basic pattern
            r'@quantecon-style-guide\s+`(\S+)`',  # With backticks
            r'@quantecon-style-guide\s+lectures/(\S+)',  # With lectures/ prefix
        ]
        
        for pattern in old_patterns:
            match = re.search(pattern, comment_body)
            if match:
                lecture = match.group(1)
                # Clean up lecture name
                lecture = lecture.replace('.md', '')  # Remove .md extension
                lecture = lecture.replace('lectures/', '')  # Remove lectures/ prefix
                lecture = lecture.strip('`')  # Remove backticks
                return (lecture, ['all'])  # Old syntax defaults to all
        
        return None
    
    def find_lecture_file(self, lecture_name: str, lectures_path: str = 'lectures/') -> Optional[str]:
        """
        Find the full path to a lecture file
        
        Args:
            lecture_name: Base name of lecture (e.g., 'aiyagari')
            lectures_path: Path to lectures directory
            
        Returns:
            Full path to lecture file or None
        """
        possible_paths = [
            f"{lectures_path}{lecture_name}.md",
            f"{lectures_path}{lecture_name}.myst",
            f"{lecture_name}.md",
            f"{lecture_name}.myst"
        ]
        
        for path in possible_paths:
            try:
                self.repo.get_contents(path)
                return path
            except GithubException:
                continue
        
        return None
    
    def get_lecture_content(self, file_path: str) -> str:
        """
        Get content of a lecture file
        
        Args:
            file_path: Path to lecture file
            
        Returns:
            File content as string
        """
        try:
            content = self.repo.get_contents(file_path)
            return content.decoded_content.decode('utf-8')
        except GithubException as e:
            raise Exception(f"Failed to get lecture content: {e}")
    
    def create_branch(self, branch_name: str, base_branch: str = 'main') -> str:
        """
        Create a new branch
        
        Args:
            branch_name: Name for new branch
            base_branch: Base branch to branch from
            
        Returns:
            Created branch name
        """
        try:
            # Get base branch reference
            base_ref = self.repo.get_git_ref(f'heads/{base_branch}')
            base_sha = base_ref.object.sha
            
            # Create new branch
            self.repo.create_git_ref(f'refs/heads/{branch_name}', base_sha)
            return branch_name
        except GithubException as e:
            if 'Reference already exists' in str(e):
                # Branch exists, use it
                return branch_name
            raise Exception(f"Failed to create branch: {e}")
    
    def commit_changes(
        self,
        file_path: str,
        new_content: str,
        commit_message: str,
        branch: str
    ) -> None:
        """
        Commit changes to a file
        
        Args:
            file_path: Path to file to update
            new_content: New content for the file
            commit_message: Commit message
            branch: Branch to commit to
        """
        try:
            # Get current file to get SHA
            contents = self.repo.get_contents(file_path, ref=branch)
            
            # Update file
            self.repo.update_file(
                path=file_path,
                message=commit_message,
                content=new_content,
                sha=contents.sha,
                branch=branch
            )
        except GithubException as e:
            raise Exception(f"Failed to commit changes: {e}")
    
    def commit_file(
        self,
        file_path: str,
        content: str,
        commit_message: str,
        branch: str
    ) -> None:
        """
        Create a new file in the repository
        
        Args:
            file_path: Path for the new file
            content: Content of the file
            commit_message: Commit message
            branch: Branch to commit to
        """
        try:
            self.repo.create_file(
                path=file_path,
                message=commit_message,
                content=content,
                branch=branch
            )
        except GithubException as e:
            raise Exception(f"Failed to create file: {e}")
    
    def create_pull_request(
        self,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = 'main',
        labels: List[str] = None
    ) -> Tuple[int, str]:
        """
        Create a pull request
        
        Args:
            title: PR title
            body: PR description
            head_branch: Head branch (source)
            base_branch: Base branch (target)
            labels: Labels to add
            
        Returns:
            Tuple of (PR number, PR URL)
        """
        try:
            pr = self.repo.create_pull(
                title=title,
                body=body,
                head=head_branch,
                base=base_branch
            )
            
            # Add labels if provided
            if labels:
                # Ensure labels exist
                existing_labels = {label.name for label in self.repo.get_labels()}
                for label in labels:
                    if label not in existing_labels:
                        try:
                            self.repo.create_label(name=label, color='0e8a16')
                        except GithubException:
                            pass  # Label might have been created by another process
                
                pr.add_to_labels(*labels)
            
            return pr.number, pr.html_url
        except GithubException as e:
            raise Exception(f"Failed to create PR: {e}")
    
    def add_comment_to_pr(self, pr_number: int, comment: str) -> None:
        """
        Add a comment to a pull request
        
        Args:
            pr_number: PR number
            comment: Comment text
        """
        try:
            pr = self.repo.get_pull(pr_number)
            pr.create_issue_comment(comment)
        except GithubException as e:
            raise Exception(f"Failed to add comment: {e}")
    
    def format_pr_body(self, review_result: Dict[str, Any], lecture_name: str) -> str:
        """
        Format PR body from review results
        
        Args:
            review_result: Review results dictionary
            lecture_name: Name of the lecture
            
        Returns:
            Formatted PR body (limited to 60KB to avoid GitHub's 65KB limit)
        """
        from . import __version__
        
        MAX_PR_BODY_SIZE = 60000  # Leave some buffer below GitHub's 65536 limit
        
        body = f"## 📋 Style Guide Review: {lecture_name}\n\n"
        body += f"This PR addresses style guide compliance issues found in the `{lecture_name}` lecture.\n\n"
        
        issues_found = review_result.get('issues_found', 0)
        
        if issues_found == 0:
            body += "✅ **No issues found!** This lecture is fully compliant with the style guide.\n"
            return body
        
        body += f"### 📊 Summary\n\n"
        body += f"- **Issues Found:** {issues_found}\n"
        body += f"- **Provider:** {review_result.get('provider', 'N/A')}\n"
        body += f"- **Action Version:** {__version__}\n"
        body += f"- **Review Date:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        
        # Group violations by rule and category
        violations = review_result.get('violations', [])
        by_rule = {}
        by_category = {}
        
        for v in violations:
            rule_id = v.get('rule_id', 'unknown')
            category = rule_id.split('-')[1] if '-' in rule_id else 'other'
            
            # Group by rule
            if rule_id not in by_rule:
                by_rule[rule_id] = {
                    'title': v.get('rule_title', ''),
                    'violations': []
                }
            by_rule[rule_id]['violations'].append(v)
            
            # Group by category
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(v)
        
        # Summary by category
        body += "### 📝 Changes by Category\n\n"
        for category, items in sorted(by_category.items()):
            body += f"- **{category.title()}:** {len(items)} issues\n"
        body += "\n"
        
        # Summarize by rule (more concise than individual violations)
        body += "### 🔍 Issues by Rule\n\n"
        
        for rule_id, data in sorted(by_rule.items()):
            count = len(data['violations'])
            body += f"**{rule_id}** - {data['title']} ({count} occurrence{'s' if count != 1 else ''})\n"
            
            # Show first 2 examples only
            for i, v in enumerate(data['violations'][:2], 1):
                location = v.get('location', 'Unknown')
                body += f"  - {location}\n"
            
            if count > 2:
                body += f"  - *(and {count - 2} more)*\n"
            body += "\n"
        
        # Add LLM summary if available
        if review_result.get('summary'):
            body += f"### � Review Summary\n\n{review_result.get('summary')}\n\n"
        
        # Check size and truncate if needed
        if len(body) > MAX_PR_BODY_SIZE:
            truncation_msg = "\n\n---\n\n*⚠️ PR description truncated due to length. View the full diff for complete details.*\n"
            body = body[:MAX_PR_BODY_SIZE - len(truncation_msg)] + truncation_msg
        
        body += "---\n\n"
        body += "*🤖 This PR was automatically generated by the QuantEcon Style Guide Checker*\n"
        body += "*📚 Review the changes in the diff for complete details*\n"
        
        return body
    
    def format_detailed_report(self, review_result: Dict[str, Any], lecture_name: str) -> str:
        """
        Format detailed review report with all violation details.
        This is posted as a PR comment (collapsible) for easy access without cluttering.
        
        Args:
            review_result: Review results dictionary
            lecture_name: Name of the lecture
            
        Returns:
            Detailed markdown report with all violations (wrapped in <details>)
        """
        from . import __version__
        
        # Wrap in collapsible details block
        report = f"<details>\n<summary><b>📊 Detailed Style Review Report</b> (click to expand)</summary>\n\n"
        
        report += f"# Detailed Style Guide Review Report\n\n"
        report += f"**Lecture:** {lecture_name}\n"
        report += f"**Action Version:** {__version__}\n"
        report += f"**Provider:** {review_result.get('provider', 'N/A')}\n"
        report += f"**Review Date:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n"
        report += f"**Issues Found:** {review_result.get('issues_found', 0)}\n\n"
        
        if review_result.get('summary'):
            report += f"## Review Summary\n\n{review_result.get('summary')}\n\n"
        
        report += "---\n\n"
        report += "## Detailed Violations\n\n"
        
        violations = review_result.get('violations', [])
        
        if not violations:
            report += "*No violations found.*\n"
        else:
            # Group by category for organization
            by_category = {}
            for v in violations:
                rule_id = v.get('rule_id', 'unknown')
                category = rule_id.split('-')[1] if '-' in rule_id else 'other'
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append(v)
            
            # Output each violation with full details
            for category, items in sorted(by_category.items()):
                report += f"### {category.title()} ({len(items)} issues)\n\n"
                
                for i, v in enumerate(items, 1):
                    report += f"#### {i}. {v.get('rule_id')} - {v.get('rule_title')}\n\n"
                    report += f"**Location:** {v.get('location', 'Unknown')}\n\n"
                    report += f"**Severity:** {v.get('severity', 'N/A')}\n\n"
                    
                    if v.get('description'):
                        report += f"**Description:** {v.get('description')}\n\n"
                    
                    if v.get('current_text'):
                        report += f"**Current text:**\n```markdown\n{v.get('current_text')}\n```\n\n"
                    
                    if v.get('suggested_fix'):
                        report += f"**Suggested fix:**\n```markdown\n{v.get('suggested_fix')}\n```\n\n"
                    
                    if v.get('explanation'):
                        report += f"**Explanation:** {v.get('explanation')}\n\n"
                    
                    report += "---\n\n"
        
        report += "\n</details>"
        
        return report

    def format_applied_fixes_report(self, review_result: Dict[str, Any], lecture_name: str) -> str:
        """
        Format report of automatically applied fixes (rule category violations).
        This is posted as a collapsible PR comment for reference.
        
        Args:
            review_result: Review results dictionary with rule_violations
            lecture_name: Name of the lecture
            
        Returns:
            Detailed markdown report of applied fixes (wrapped in <details>)
        """
        from . import __version__
        
        rule_violations = review_result.get('rule_violations', [])
        
        if not rule_violations:
            return None  # No comment needed if no fixes were applied
        
        # Wrap in collapsible details block
        report = f"<details>\n<summary><b>✅ Applied Fixes Report</b> ({len(rule_violations)} fixes applied - click to expand)</summary>\n\n"
        
        report += f"# Applied Style Guide Fixes\n\n"
        report += f"**Lecture:** {lecture_name}\n"
        report += f"**Action Version:** {__version__}\n"
        report += f"**Review Date:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n"
        report += f"**Fixes Applied:** {len(rule_violations)}\n\n"
        report += "---\n\n"
        report += "## Automatically Applied Fixes\n\n"
        report += "*The following mechanical fixes have been automatically applied to the lecture content.*\n\n"
        
        # Group by category for organization
        by_category = {}
        for v in rule_violations:
            rule_id = v.get('rule_id', 'unknown')
            category = rule_id.split('-')[1] if '-' in rule_id else 'other'
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(v)
        
        # Output each violation with full details
        for category, items in sorted(by_category.items()):
            report += f"### {category.title()} ({len(items)} fixes)\n\n"
            
            for i, v in enumerate(items, 1):
                report += f"#### {i}. {v.get('rule_id')} - {v.get('rule_title')}\n\n"
                report += f"**Location:** {v.get('location', 'Unknown')}\n\n"
                
                if v.get('description'):
                    report += f"**Description:** {v.get('description')}\n\n"
                
                if v.get('current_text'):
                    report += f"**Original text:**\n```markdown\n{v.get('current_text')}\n```\n\n"
                
                if v.get('suggested_fix'):
                    report += f"**Applied fix:**\n```markdown\n{v.get('suggested_fix')}\n```\n\n"
                
                if v.get('explanation'):
                    report += f"**Explanation:** {v.get('explanation')}\n\n"
                
                report += "---\n\n"
        
        report += "\n</details>"
        
        return report

    def format_style_suggestions_report(self, review_result: Dict[str, Any], lecture_name: str) -> str:
        """
        Format report of style suggestions (style category violations).
        This is posted as an OPEN PR comment for immediate human review.
        
        Args:
            review_result: Review results dictionary with style_violations
            lecture_name: Name of the lecture
            
        Returns:
            Open markdown report of style suggestions (NOT collapsible - visible by default)
        """
        from . import __version__
        
        style_violations = review_result.get('style_violations', [])
        
        if not style_violations:
            return None  # No comment needed if no suggestions
        
        # NO <details> wrapper - open and visible by default
        report = f"# 🎨 Style Suggestions for Human Review\n\n"
        report += f"**Lecture:** {lecture_name}\n"
        report += f"**Action Version:** {__version__}\n"
        report += f"**Review Date:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n"
        report += f"**Suggestions:** {len(style_violations)}\n\n"
        report += "---\n\n"
        report += "⚠️ **These suggestions require human review before applying.**\n\n"
        report += "*Style improvements are subjective - please review each suggestion carefully.*\n\n"
        
        # Group by category for organization
        by_category = {}
        for v in style_violations:
            rule_id = v.get('rule_id', 'unknown')
            category = rule_id.split('-')[1] if '-' in rule_id else 'other'
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(v)
        
        # Output each violation with full details
        for category, items in sorted(by_category.items()):
            report += f"## {category.title()} ({len(items)} suggestions)\n\n"
            
            for i, v in enumerate(items, 1):
                report += f"### {i}. {v.get('rule_id')} - {v.get('rule_title')}\n\n"
                report += f"**Location:** {v.get('location', 'Unknown')}\n\n"
                report += f"**Severity:** {v.get('severity', 'N/A')}\n\n"
                
                if v.get('description'):
                    report += f"**Description:** {v.get('description')}\n\n"
                
                if v.get('current_text'):
                    report += f"**Current text:**\n```markdown\n{v.get('current_text')}\n```\n\n"
                
                if v.get('suggested_fix'):
                    report += f"**Suggested improvement:**\n```markdown\n{v.get('suggested_fix')}\n```\n\n"
                
                if v.get('explanation'):
                    report += f"**Explanation:** {v.get('explanation')}\n\n"
                
                report += "---\n\n"
        
        return report

    def format_pr_body(self, review_result: Dict[str, Any], lecture_name: str) -> str:
        """
        Format concise PR body with summary statistics.
        Detailed report is added as a separate PR comment.
        
        Args:
            review_result: Review results dictionary
            lecture_name: Name of the lecture
            
        Returns:
            Concise PR body with summary
        """
        from . import __version__
        
        body = f"## 📋 Style Guide Review: {lecture_name}\n\n"
        body += f"This PR addresses style guide compliance issues found in the `{lecture_name}` lecture.\n\n"
        
        issues_found = review_result.get('issues_found', 0)
        
        if issues_found == 0:
            body += "✅ **No issues found!** This lecture is fully compliant with the style guide.\n"
            return body
        
        body += f"### 📊 Summary\n\n"
        body += f"- **Issues Found:** {issues_found}\n"
        body += f"- **Provider:** {review_result.get('provider', 'N/A')}\n"
        body += f"- **Action Version:** {__version__}\n"
        body += f"- **Review Date:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        
        # Group violations by rule and category
        violations = review_result.get('violations', [])
        by_rule = {}
        by_category = {}
        
        for v in violations:
            rule_id = v.get('rule_id', 'unknown')
            category = rule_id.split('-')[1] if '-' in rule_id else 'other'
            
            # Group by rule
            if rule_id not in by_rule:
                by_rule[rule_id] = {
                    'title': v.get('rule_title', ''),
                    'count': 0
                }
            by_rule[rule_id]['count'] += 1
            
            # Group by category
            if category not in by_category:
                by_category[category] = 0
            by_category[category] += 1
        
        # Summary by category
        body += "### 📝 Changes by Category\n\n"
        for category, count in sorted(by_category.items()):
            body += f"- **{category.title()}:** {count} issue{'s' if count != 1 else ''}\n"
        body += "\n"
        
        # Summarize by rule
        body += "### 🔍 Issues by Rule\n\n"
        
        for rule_id, data in sorted(by_rule.items()):
            count = data['count']
            body += f"- **{rule_id}** - {data['title']}: {count} occurrence{'s' if count != 1 else ''}\n"
        body += "\n"
        
        # Add LLM summary if available
        if review_result.get('summary'):
            body += f"### 💬 Review Summary\n\n{review_result.get('summary')}\n\n"
        
        body += "---\n\n"
        body += "*🤖 This PR was automatically generated by the QuantEcon Style Guide Checker*\n"
        body += "*📊 See the comment below for complete violation details*\n"
        
        return body

    def format_commit_message(self, violations: List[Dict], lecture_name: str) -> str:
        """
        Format commit message from violations
        
        Args:
            violations: List of violations
            lecture_name: Name of lecture
            
        Returns:
            Formatted commit message
        """
        if not violations:
            return f"style: no issues found in {lecture_name}"
        
        # Group by category
        by_category = {}
        for v in violations:
            category = v.get('rule_id', '').split('-')[1] if '-' in v.get('rule_id', '') else 'other'
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(v)
        
        # Create commit message
        msg = f"style: fix {len(violations)} issues in {lecture_name}\n\n"
        
        for category, items in sorted(by_category.items()):
            msg += f"- {category}: {len(items)} fixes\n"
        
        msg += f"\nRules addressed:\n"
        for v in violations[:10]:  # Limit to first 10
            msg += f"- {v.get('rule_id')}: {v.get('rule_title')}\n"
        
        if len(violations) > 10:
            msg += f"- ... and {len(violations) - 10} more\n"
        
        return msg
    
    def get_all_lectures(self, lectures_path: str = 'lectures/') -> List[str]:
        """
        Get all lecture files in the repository
        
        Args:
            lectures_path: Path to lectures directory
            
        Returns:
            List of lecture file paths
        """
        lectures = []
        
        try:
            contents = self.repo.get_contents(lectures_path)
            for content in contents:
                if content.type == 'file' and (content.name.endswith('.md') or content.name.endswith('.myst')):
                    lectures.append(content.path)
        except GithubException as e:
            print(f"Warning: Could not list lectures: {e}")
        
        return lectures
