# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.1] - 2025-10-10

### Fixed

- **Streaming Fallback**: Added automatic fallback to streaming API for large lectures
  - Anthropic now requires streaming for requests that may take longer than 10 minutes
  - Non-streaming API tried first for better performance
  - Automatically falls back to streaming if required
  - Fixes error: "Streaming is required for operations that may take longer than 10 minutes"
  - Particularly important for very large lectures (40K+ characters)

## [0.3.0] - 2025-10-10

### Breaking Changes 🚨

This is a major release with breaking changes. Version 0.3.0 is not backward compatible with 0.2.x.

- **Removed**: Legacy trigger `@quantecon-style-guide` (use `@qe-style-checker` instead)
- **Removed**: `style-guide-url` input parameter (rules now built-in)
- **Removed**: `all` category keyword (omit categories to check all)
- **Removed**: `style-guide-database.md` (replaced by focused prompts + rules)
- **Removed**: OpenAI and Google Gemini provider support (now Claude Sonnet 4.5 only)
- **Removed**: `llm-provider`, `openai-api-key`, and `google-api-key` inputs
- **Changed**: `anthropic-api-key` is now required (was optional)
- **Changed**: Updated to `@v0.3` in workflow examples

### Added

- **Focused Prompts Architecture**: Hand-written prompts + detailed rules for better quality and lower costs
  - 8 category-specific prompts (~85 lines each) in `style_checker/prompts/`
  - 8 detailed rule files (~120-235 lines each) in `style_checker/rules/`
  - Total: 1901 lines (48% reduction from auto-generated 3610 lines)
  - Matches proven `tool-style-checker` pattern
- **Sequential Category Processing**: Categories are now processed one at a time, feeding updated content between each
  - Ensures all fixes are applied without conflicts
  - Later categories see changes from earlier categories
  - More reliable and complete results
  - Matches `tool-style-checker` approach
- **Smart Prompt Loading**: `PromptLoader` class combines prompts + rules dynamically
- **Better Test Organization**: All tests consolidated in `tests/` directory
- **Rule Development Workflow**: New `tool-style-guide-development/` folder for managing style guide rules
  - `style-guide-database.md`: Single source of truth for rule development
  - `build_rules.py`: Script to generate category-specific rule files
  - `README.md`: Complete workflow documentation
  - Separates rule development from action runtime
  - Enables independent updates to style guide content

### Changed

- **Simplified Configuration**: Removed unnecessary inputs for cleaner setup
- **Claude Sonnet 4.5 Exclusive**: Simplified to use only the best LLM for style checking
  - Default model: `claude-sonnet-4-5-20250929`
  - Excellent comprehension for nuanced style rules
  - Can add other providers in future releases if needed
- **Simplified Architecture**: Removed runtime database parsing
  - Action reads directly from `style_checker/rules/*.md` files
  - No more `StyleGuideDatabase` object or parsing overhead
  - Faster startup and clearer code flow
  - `parser_md.py` kept for backward compatibility in tests
- **Simplified API Calls**: Removed streaming interface
  - Focused prompts are small enough (~5-12K tokens) for standard API calls
  - Cleaner code without streaming context managers
  - Better error handling and debugging
  - Streaming was only needed for old large auto-generated prompts
- **Updated Documentation**: All references updated to v0.3.0
- **Cleaner Repository**: Removed outdated documentation and legacy code
- **Improved README**: Clearer quick start, removed verbose content

### Removed

- Deprecated `generate_prompts.py` (replaced by focused prompts)
- Verbose CHANGELOG entries condensed
- Outdated migration documentation
- Legacy syntax references

### Migration from 0.2.x

1. Update workflow to use `@v0.3` instead of `@v0.2`
2. Remove `style-guide-url` parameter from workflow configuration
3. Use `@qe-style-checker` trigger (not `@quantecon-style-guide`)
4. Remove `all` category - omit categories to check all

## [0.2.1] - 2025-10-03

### Fixed
- GitHub Actions deprecation warning (replaced `::set-output` with `GITHUB_OUTPUT`)

### Changed
- Documentation cleanup and updates

### Removed
- Deprecated `parser.py` module

## [0.2.0] - 2025-10-02

### Added
- Semantic group parallelization (2-3x faster, 25% cheaper)
- Markdown-based style guide database
- Parallel processing of up to 4 groups simultaneously

### Changed
- Migrated from YAML to Markdown format
- Simplified main.py (removed chunking logic)

### Removed
- Old YAML parser and database
- Deprecated chunking methods

## [0.1.8] - 2025-10-01

### Changed
- Migrated from JSON to Markdown format for LLM responses

### Added
- Comprehensive testing infrastructure
- CI/CD pipeline
- Integration tests

## [0.1.7] - 2025-10-01

### Fixed
- Improved JSON parsing for malformed Claude responses

## [0.1.6] - 2025-10-01

### Added
- Comprehensive review summary
- Better progress indicators

## [0.1.5] - 2025-10-01

### Fixed
- Hardcoded fallback to old Claude model

## [0.1.4] - 2025-10-01

### Fixed
- Implemented streaming for Claude API requests

## [0.1.3] - 2025-10-01

### Changed
- Updated default model to Claude Sonnet 4.5

## [0.1.2] - 2025-10-01

### Fixed
- Reduced max_tokens for Claude 3.5 Sonnet compatibility

## [0.1.1] - 2025-10-01

### Fixed
- Module import path issue in GitHub Actions

## [0.1.0] - 2025-10-01

### Added
- Initial development release
- AI-powered style guide checking
- Single lecture and bulk review modes
- Automatic PR creation
