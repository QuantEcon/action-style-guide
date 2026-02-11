#!/usr/bin/env python3
"""
Test comment parsing for @qe-style-checker syntax.

Tests the actual GitHubHandler.extract_lecture_from_comment() method,
not a reimplemented copy.
"""

import pytest
from unittest.mock import patch, MagicMock
from style_checker.github_handler import GitHubHandler


@pytest.fixture
def handler():
    """Create a GitHubHandler without connecting to GitHub."""
    with patch.object(GitHubHandler, '__init__', lambda self, *a, **kw: None):
        h = GitHubHandler.__new__(GitHubHandler)
        # Set the class attribute that extract_lecture_from_comment uses
        h.VALID_CATEGORIES = GitHubHandler.VALID_CATEGORIES
        return h


class TestCommentParsing:
    """Test GitHubHandler.extract_lecture_from_comment()"""

    def test_basic_syntax(self, handler):
        """@qe-style-checker lecture_name"""
        result = handler.extract_lecture_from_comment("@qe-style-checker aiyagari")
        assert result == ("aiyagari", ["all"])

    def test_with_categories(self, handler):
        """@qe-style-checker lecture_name writing,math"""
        result = handler.extract_lecture_from_comment("@qe-style-checker aiyagari writing,math")
        assert result == ("aiyagari", ["writing", "math"])

    def test_with_path(self, handler):
        """@qe-style-checker lectures/lecture.md categories"""
        result = handler.extract_lecture_from_comment("@qe-style-checker lectures/aiyagari.md code,jax")
        assert result == ("aiyagari", ["code", "jax"])

    def test_with_backticks(self, handler):
        """@qe-style-checker `lecture_name` all"""
        result = handler.extract_lecture_from_comment("@qe-style-checker `aiyagari` all")
        assert result == ("aiyagari", ["all"])

    def test_backticks_no_categories(self, handler):
        """@qe-style-checker `lecture_name`"""
        result = handler.extract_lecture_from_comment("@qe-style-checker `aiyagari`")
        assert result == ("aiyagari", ["all"])

    def test_regular_comment_returns_none(self, handler):
        """Non-trigger comments should return None"""
        assert handler.extract_lecture_from_comment("Just a regular comment") is None

    def test_wrong_trigger_returns_none(self, handler):
        """Wrong trigger prefix should return None"""
        assert handler.extract_lecture_from_comment("@something-else aiyagari") is None

    def test_single_category(self, handler):
        """Single category without comma"""
        result = handler.extract_lecture_from_comment("@qe-style-checker intro writing")
        assert result == ("intro", ["writing"])

    def test_all_categories_keyword(self, handler):
        """Explicit 'all' keyword"""
        result = handler.extract_lecture_from_comment("@qe-style-checker intro all")
        assert result == ("intro", ["all"])

    def test_md_extension_stripped(self, handler):
        """The .md extension should be stripped from lecture name"""
        result = handler.extract_lecture_from_comment("@qe-style-checker intro.md")
        assert result == ("intro", ["all"])

    def test_invalid_category_returns_none(self, handler):
        """Invalid category names should return None"""
        result = handler.extract_lecture_from_comment("@qe-style-checker intro invalid_cat")
        assert result is None
