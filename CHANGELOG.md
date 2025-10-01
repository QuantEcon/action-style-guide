# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v1.0.0
- Production release after testing
- Performance optimizations
- Additional test coverage

## [0.1.8] - 2025-10-01

### Changed - Major Breaking Improvement
- **Migrated from JSON to Markdown format for LLM responses**
  - Eliminates JSON parsing errors (unterminated strings, escaping issues)
  - LLMs generate Markdown naturally without escaping problems
  - More reliable for long responses (50K-70K+ characters)
  - Human-readable format for easier debugging

### Added
- **New Markdown response parser** (`parse_markdown_response()`)
  - Structured format with clear section delimiters
  - Robust regex-based parsing
  - Graceful error handling
- **Comprehensive testing infrastructure**
  - Migrated to pytest framework with fixtures
  - Added `test_markdown_parser.py` (7 tests)
  - Enhanced `test_basic.py` with 6 tests including validation
  - **Integration tests** in `test_llm_integration.py`
    - Real LLM API call tests with sample lecture
    - Multi-provider support (Claude/GPT-4/Gemini)
    - Violation detection and correction validation
    - Marked with `@pytest.mark.integration` (skipped by default)
- **CI/CD Pipeline** (`.github/workflows/ci.yml`)
  - Automated testing on push and PR
  - Python 3.9, 3.10, 3.11, 3.12 matrix
  - Code linting (Black, isort, flake8)
  - Coverage reporting with pytest-cov
- **Configuration files**
  - `pyproject.toml` with pytest and coverage config
  - Test markers for categorization (unit, integration, slow)
- **Comprehensive documentation**
  - `docs/markdown-format-migration.md` - Migration details
  - `docs/ci-cd-setup.md` - CI/CD documentation
  - `docs/llm-integration-testing.md` - Integration test guide
  - `docs/testing-quick-reference.md` - Quick testing reference
  - `tests/README.md` - Complete testing guide

### Updated
- All LLM provider prompts (OpenAI, Anthropic, Gemini) to use Markdown format
- System prompts with clear Markdown structure examples
- Test files consolidated in `tests/` directory
- Documentation updated across all files

### Fixed
- **Completely eliminated JSON parsing errors** that plagued v0.1.7
- No more "Unterminated string" failures
- Proper handling of complex lecture content with code, math, and special characters
- Reliable parsing of long LLM responses

### Technical Details
- Removed `import json` and all `json.loads()` calls from reviewer.py
- Removed `response_format={"type": "json_object"}` from OpenAI
- Removed `response_mime_type: "application/json"` from Gemini
- Parser uses regex with `re.DOTALL` for multi-line content
- Handles nested code blocks in corrected content
- Sample lecture with violations for integration testing

### Dependencies
- Added: `pytest>=7.4.0`
- Added: `pytest-cov>=4.1.0`

## [0.1.7] - 2025-10-01

### Fixed
- **Critical**: Improved JSON parsing to handle malformed responses from Claude
- Added robust error handling for unterminated strings and JSON parse errors
- Detects when responses are truncated (hit max_tokens limit)
- Better extraction of JSON from responses with fallback mechanisms

### Added
- Warning messages when response is truncated due to max_tokens
- Response length logging for debugging
- Preview of raw response in error messages
- Attempt to extract valid JSON even from malformed responses
- More explicit instructions to Claude about proper JSON escaping

### Changed
- Updated system prompt to emphasize proper JSON string escaping
- Added instructions to Claude about handling long content
- Better stop_reason detection from streaming API
- Improved error messages with context and suggestions

### Technical Details
- Tries multiple JSON extraction methods before failing
- Looks for outermost `{}` if direct parsing fails
- Returns structured error with preview instead of crashing
- Checks `stop_reason` to detect max_tokens truncation

## [0.1.6] - 2025-10-01

### Added
- **Comprehensive review summary** displayed at the end of each run
- Shows lecture name, issues found, PR status, and URLs
- Better chunk progress indicators with issue counts per chunk
- Clear status messages for different outcomes (PR created, no issues, etc.)
- Improved visibility of review results in GitHub Actions logs

### Changed
- Enhanced logging in `review_in_chunks()` to show issues found per chunk
- Added final summary section for both single and bulk review modes
- Better error reporting with clear status indicators

### Fixed
- Users can now easily see review outcomes without searching through logs
- PR creation status is clearly indicated
- Total issues count is prominently displayed

## [0.1.5] - 2025-10-01

### Fixed
- **Critical**: Fixed hardcoded fallback to old Claude 3.5 Sonnet model in StyleReviewer
- Now correctly uses Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`) when no model is specified
- Resolves issue where v0.1.3 model upgrade wasn't being applied

### Technical Details
- Updated `StyleReviewer.__init__()` to pass `None` to `AnthropicProvider` when no model specified
- This allows the provider's default model (Sonnet 4.5) to be used
- Previous code: `model or "claude-3-5-sonnet-20241022"` (always fell back to old model)
- New code: Only passes model if explicitly specified by user

## [0.1.4] - 2025-10-01

### Fixed
- **Critical**: Implemented streaming for Claude API requests to avoid 10-minute timeout
- Resolves error: "Streaming is required for operations that may take longer than 10 minutes"

### Changed
- Claude API now uses streaming (`messages.stream`) instead of blocking calls
- Improved handling of long-running style checks with high `max_tokens`

### Technical Details
- Updated `AnthropicProvider.check_style()` to use `client.messages.stream()`
- Streams text chunks and assembles complete response before parsing
- Required for requests with 32K max_tokens that may exceed 10-minute limit
- See: https://docs.anthropic.com/en/docs/build-with-claude/streaming

## [0.1.3] - 2025-10-01

### Changed
- **Major Upgrade**: Updated default model to Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
  - Latest and most capable Claude model (released September 2025)
  - Increased max_tokens from 8,192 to 32,000 (Sonnet 4.5 supports up to 64,000)
  - 8x more output capacity than previous Sonnet 3.5
  - Highest intelligence across most tasks
  - Best for complex agents and coding

### Added
- Updated model documentation with Claude 4 family models
- Added comparison of all latest models (Sonnet 4.5, Opus 4.1, etc.)
- Note about Claude Sonnet 4.5 being the recommended default

### Deprecated
- Claude 3.5 Sonnet (`claude-3-5-sonnet-20241022`) is now deprecated in favor of Sonnet 4.5

## [0.1.2] - 2025-10-01

### Fixed
- **Critical**: Reduced `max_tokens` from 16000 to 8192 for Claude 3.5 Sonnet compatibility
- Resolves API error: "max_tokens: 16000 > 8192, which is the maximum allowed"

### Added
- Comprehensive LLM model documentation in README
- Token limit information for all supported models
- Model selection guidance based on lecture length and requirements
- Documentation for troubleshooting token limit errors

### Changed
- Enhanced trigger configuration to support `@quantecon-style-guide` in both issue bodies and comments
- Updated workflow examples to include `issues` events (opened, edited)

## [0.1.1] - 2025-10-01

### Fixed
- Module import path issue when running in GitHub Actions
- Added action path to Python sys.path
- Set PYTHONPATH environment variable in action.yml
- Resolves `ModuleNotFoundError: No module named 'style_checker'`

## [0.1.0] - 2025-10-01

### Added
- Initial development release of QuantEcon Style Guide Checker
- AI-powered style guide compliance checking using LLM
- Support for multiple LLM providers:
  - Anthropic Claude (default)
  - OpenAI GPT-4
  - Google Gemini
- Single lecture review mode via issue comments
- Bulk review mode for all lectures (scheduled weekly)
- Automatic PR creation with detailed change descriptions
- GitHub Actions integration
- Comprehensive style guide rule database (56 rules)
- Rule categories: writing, titles, formatting, mathematics, code, JAX, exercises, references, index, binary packages, environment
- Flexible comment syntax for triggering reviews
- Individual commits per lecture in bulk reviews
- Proper PR labeling and formatting
- Example workflows for adoption

### Features
- **Rule Parser**: Loads and validates YAML-based style guide rules
- **LLM Integration**: Intelligent context-aware style checking
- **GitHub Handler**: Complete PR and issue management
- **Updatable Rules**: Easy to modify and extend style guide
- **Chunked Processing**: Handles large rule sets efficiently
- **Error Handling**: Graceful degradation on failures
- **Detailed Reporting**: Comprehensive PR descriptions with rule references

### Documentation
- Complete README with usage instructions
- Contributing guidelines
- Example workflows for both modes
- API documentation in code
- Style guide rule format specification
- Quick start guide
- Architecture documentation
- GitHub App setup guide

### Notes
- This is a development/testing release
- Please report any issues or feedback
- Production release (v1.0.0) will follow after testing period
