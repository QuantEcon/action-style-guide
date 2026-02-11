"""
Tests for prompt_loader.py — PromptLoader class
"""

import pytest
from style_checker.prompt_loader import PromptLoader, load_prompt


@pytest.fixture
def loader():
    """Create a PromptLoader using the real prompts/rules directories."""
    return PromptLoader()


class TestPromptLoader:
    """Test PromptLoader class"""

    def test_load_single_category(self, loader):
        """Loading a single category should return prompt + rules + lecture"""
        result = loader.load_prompt(["writing"], "# Test Lecture\n\nSome content.")
        assert "# Test Lecture" in result
        assert "Some content." in result
        # Should include rules content
        assert "qe-writing-001" in result

    def test_load_multiple_categories(self, loader):
        """Loading multiple categories should include rules from all"""
        result = loader.load_prompt(["writing", "math"], "# Test\n\nContent.")
        assert "qe-writing-001" in result
        assert "qe-math-001" in result

    def test_all_categories_loadable(self, loader):
        """Every valid category should load without error"""
        for category in PromptLoader.VALID_CATEGORIES:
            result = loader.load_prompt([category], "# Test\n\nContent.")
            assert len(result) > 100, f"Category '{category}' returned suspiciously short prompt"

    def test_invalid_category_raises(self, loader):
        """Invalid category name should raise ValueError"""
        with pytest.raises(ValueError, match="Invalid categories"):
            loader.load_prompt(["nonexistent"], "# Test")

    def test_prompt_includes_lecture_content(self, loader):
        """Lecture content should appear in the final prompt"""
        marker = "UNIQUE_MARKER_12345"
        result = loader.load_prompt(["writing"], f"# Test\n\n{marker}")
        assert marker in result

    def test_prompt_file_has_version(self, loader):
        """All prompt files should have version comments"""
        for category in PromptLoader.VALID_CATEGORIES:
            prompt_file = loader.prompts_dir / f"{category}-prompt.md"
            content = prompt_file.read_text()
            assert "Prompt Version:" in content, \
                f"{category}-prompt.md missing version comment"

    def test_rules_file_has_rules(self, loader):
        """All rules files should contain at least one rule"""
        for category in PromptLoader.VALID_CATEGORIES:
            rules_file = loader.rules_dir / f"{category}-rules.md"
            content = rules_file.read_text()
            assert "### Rule:" in content, \
                f"{category}-rules.md has no rules"


class TestConvenienceFunction:
    """Test the load_prompt() convenience function"""

    def test_load_prompt_function(self):
        """Convenience function should work identically to class method"""
        result = load_prompt(["math"], "# Test\n\nContent.")
        assert "qe-math-001" in result

    def test_load_prompt_invalid_category(self):
        """Convenience function should raise on invalid category"""
        with pytest.raises(ValueError):
            load_prompt(["invalid"], "# Test")
