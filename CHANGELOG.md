# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v1.0.0
- Production release after testing
- Performance optimizations
- Additional test coverage

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
