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
        
        Supported syntax:
        - @qe-style-checker lectures/file.md math,code
        - @qe-style-checker lectures/file.md
        
        Args:
            comment_body: Full comment text
            
        Returns:
            Tuple of (lecture_name, categories) or None if not found.
            Categories is a list like ["writing", "math"] or ["all"] if not specified.
        """
        # @qe-style-checker syntax
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
                        report += f"**Current text:**\n~~~markdown\n{v.get('current_text')}\n~~~\n\n"
                    
                    if v.get('suggested_fix'):
                        report += f"**Suggested fix:**\n~~~markdown\n{v.get('suggested_fix')}\n~~~\n\n"
                    
                    if v.get('explanation'):
                        report += f"**Explanation:** {v.get('explanation')}\n\n"
                    
                    report += "---\n\n"
        
        report += "\n</details>"
        
        return report

    def format_applied_fixes_report(self, review_result: Dict[str, Any], lecture_name: str) -> Optional[str]:
        """
        Format report of automatically applied fixes using region-based diff.
        
        Instead of reporting each rule's violations independently, this compares
        the original content to the final content line-by-line. For each changed
        region, it attributes all contributing rules and shows the true
        original → final text. This eliminates no-op entries and provides
        accurate before/after when multiple rules edit the same line.
        
        Args:
            review_result: Review results dictionary with fix_log, original_content, corrected_content
            lecture_name: Name of the lecture
            
        Returns:
            Detailed markdown report of applied fixes (wrapped in <details>)
        """
        from . import __version__
        
        fix_log = review_result.get('fix_log', [])
        original_content = review_result.get('original_content', '')
        corrected_content = review_result.get('corrected_content', '')
        
        if not fix_log or original_content == corrected_content:
            return None  # No actual changes made
        
        # Build changed regions by diffing original vs final content
        changed_regions = _build_changed_regions(original_content, corrected_content, fix_log)
        
        if not changed_regions:
            return None
        
        # Count total unique rules that contributed
        all_rules = set()
        for region in changed_regions:
            all_rules.update(region['rules'])
        
        # Wrap in collapsible details block
        report = f"<details>\n<summary><b>✅ Applied Fixes Report</b> ({len(changed_regions)} changes from {len(all_rules)} rules - click to expand)</summary>\n\n"
        
        report += f"# Applied Style Guide Fixes\n\n"
        report += f"**Lecture:** {lecture_name}\n"
        report += f"**Action Version:** {__version__}\n"
        report += f"**Review Date:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n"
        report += f"**Changes:** {len(changed_regions)} regions modified\n"
        report += f"**Rules Applied:** {len(all_rules)}\n\n"
        report += "---\n\n"
        report += "## Changes Applied\n\n"
        report += "*Each entry shows the true original text and final result after all applicable rules.*\n\n"
        
        for i, region in enumerate(changed_regions, 1):
            # Header with line info and contributing rules
            rules_str = ', '.join(sorted(region['rules']))
            report += f"### Change {i} — Line {region['start_line']}\n\n"
            report += f"**Rules applied:** {rules_str}\n\n"
            
            # Show descriptions from contributing rules
            if region.get('descriptions'):
                for rule_id, desc in region['descriptions'].items():
                    report += f"- **{rule_id}:** {desc}\n"
                report += "\n"
            
            report += f"**Original text:**\n~~~markdown\n{region['original']}\n~~~\n\n"
            report += f"**After fixes:**\n~~~markdown\n{region['final']}\n~~~\n\n"
            
            # Show explanations from contributing rules
            if region.get('explanations'):
                for rule_id, expl in region['explanations'].items():
                    report += f"**{rule_id} explanation:** {expl}\n\n"
            
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
                    report += f"**Current text:**\n~~~markdown\n{v.get('current_text')}\n~~~\n\n"
                
                if v.get('suggested_fix'):
                    report += f"**Suggested improvement:**\n~~~markdown\n{v.get('suggested_fix')}\n~~~\n\n"
                
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


def _build_changed_regions(original: str, final: str, fix_log: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Build a list of changed regions by comparing original vs final content line-by-line,
    then attribute contributing rules from the fix_log.
    
    Each region contains:
      - start_line: 1-based line number where the change begins
      - original: the original text for this region
      - final: the final text after all fixes
      - rules: set of rule_ids that contributed to this change
      - descriptions: dict of rule_id -> description
      - explanations: dict of rule_id -> explanation
    
    Args:
        original: Original lecture content before any fixes
        final: Final lecture content after all fixes
        fix_log: List of applied fix records with rule attribution
        
    Returns:
        List of changed region dicts
    """
    import difflib
    
    orig_lines = original.splitlines(keepends=True)
    final_lines = final.splitlines(keepends=True)
    
    # Use SequenceMatcher to find changed blocks
    matcher = difflib.SequenceMatcher(None, orig_lines, final_lines)
    
    changed_regions = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            continue
        
        # This is a changed region (replace, insert, or delete)
        orig_text = ''.join(orig_lines[i1:i2]).strip()
        final_text = ''.join(final_lines[j1:j2]).strip()
        start_line = i1 + 1  # Convert to 1-based
        
        # Skip if both are empty after stripping
        if not orig_text and not final_text:
            continue
        
        # Find which rules from fix_log contributed to this region
        rules = set()
        descriptions = {}
        explanations = {}
        
        for fix in fix_log:
            fix_current = fix.get('current_text', '')
            fix_suggested = fix.get('suggested_fix', '')
            
            # Check if this fix's text overlaps with the changed region
            # A fix contributed if its current_text appears in the original region
            # or its suggested_fix appears in the final region
            if _text_overlaps_region(fix_current, orig_text) or \
               _text_overlaps_region(fix_suggested, final_text):
                rule_id = fix['rule_id']
                rules.add(rule_id)
                if fix.get('description'):
                    descriptions[rule_id] = fix['description']
                if fix.get('explanation'):
                    explanations[rule_id] = fix['explanation']
        
        # If no rules matched (shouldn't happen but defensive), still report the change
        if not rules:
            rules.add('unknown')
        
        changed_regions.append({
            'start_line': start_line,
            'original': orig_text if orig_text else '(empty)',
            'final': final_text if final_text else '(empty)',
            'rules': rules,
            'descriptions': descriptions,
            'explanations': explanations,
        })
    
    # Merge adjacent regions that are close together (within 2 lines)
    # This avoids fragmenting a multi-line change into many small entries
    merged = _merge_adjacent_regions(changed_regions)
    
    return merged


def _text_overlaps_region(text: str, region_text: str) -> bool:
    """
    Check if a fix's text overlaps with a changed region.
    
    Uses two strategies:
    1. Direct substring match of the fix text within the region text
    2. Line-based overlap: check if substantial lines from the fix appear in the region
    """
    if not text or not region_text:
        return False
    
    # Strategy 1: Direct substring containment (either direction)
    if text in region_text or region_text in text:
        return True
    
    # Strategy 2: Check if any meaningful part of fix text overlaps region
    # Split fix text into lines and check if any line appears in region
    fix_lines = [l.strip() for l in text.split('\n') if l.strip()]
    region_lines = [l.strip() for l in region_text.split('\n') if l.strip()]
    
    for fix_line in fix_lines:
        if len(fix_line) >= 10:  # Only match substantial lines
            for region_line in region_lines:
                if fix_line in region_line or region_line in fix_line:
                    return True
    
    return False


def _merge_adjacent_regions(regions: List[Dict[str, Any]], gap: int = 2) -> List[Dict[str, Any]]:
    """
    Merge changed regions that are within `gap` lines of each other.
    This consolidates edits into coherent chunks.
    """
    if not regions:
        return []
    
    merged = [regions[0]]
    
    for region in regions[1:]:
        prev = merged[-1]
        # Estimate end of previous region
        prev_end = prev['start_line'] + prev['original'].count('\n')
        
        if region['start_line'] <= prev_end + gap:
            # Merge: combine texts and rules
            prev['original'] = prev['original'] + '\n\n' + region['original']
            prev['final'] = prev['final'] + '\n\n' + region['final']
            prev['rules'].update(region['rules'])
            prev['descriptions'].update(region.get('descriptions', {}))
            prev['explanations'].update(region.get('explanations', {}))
        else:
            merged.append(region)
    
    return merged
