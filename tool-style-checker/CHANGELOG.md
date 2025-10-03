# Changelog

All notable changes to the Claude Style Checker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.0] - 2025-10-03

### Added
- **Three Output Modes**: Added `--mode` parameter with three options:
  - `suggestions` (default): Returns style review with violations and suggested fixes
  - `corrected`: Returns fully corrected lecture file
  - `both`: Returns both review and corrected file
- Separate file extraction in `both` mode: automatically creates `{input}-corrected.md` file
- Comprehensive mode documentation in `docs/MODES-GUIDE.md`
- Mode-specific prompt instructions to Claude for better output formatting

### Changed
- Updated `check_lecture_style()` function to accept `output_mode` parameter
- Enhanced output handling in `main()` to process different modes appropriately
- Corrected file in `both` mode now named after input lecture file, not output file
- Reorganized documentation into `docs/` folder
- Streamlined README.md to focus on quickstart and essential information

### Fixed
- File naming convention for corrected files in `both` mode now based on input lecture name

## [1.0.0] - 2025-10-02

### Added
- Initial release of Claude Style Checker
- Core `style_checker.py` script with command-line interface
- Integration with Claude Sonnet 4.5 API (`claude-sonnet-4-20250514`)
- Comprehensive style guide database (43KB, 42 rules across 8 categories):
  - Writing Style (9 rules)
  - Mathematical Notation (7 rules)
  - Code Blocks (8 rules)
  - JAX Code (4 rules)
  - Figures and Images (4 rules)
  - References and Citations (4 rules)
  - Links and Resources (3 rules)
  - Admonitions (3 rules)
- Detailed prompt system for Claude with false-positive prevention
- Quick mode (`--quick`) for critical issues only
- Focus mode (`--focus`) to target specific rule categories
- Support for MyST Markdown format (Jupyter Book compatible)
- Comprehensive documentation:
  - Installation guide
  - Usage examples
  - Troubleshooting section
  - FAQ

### Features
- Detects and reports style guide violations with severity levels
- Provides suggested corrections with before/after examples
- Summary statistics (total violations, critical issues)
- Environment variable support for API key (`ANTHROPIC_API_KEY`)
- File output support via `--output` parameter
- Graceful error handling and user-friendly messages

### Documentation
- `README.md`: Project overview and quick start
- `docs/DOCUMENTATION.md`: Complete user guide (33KB)
- `claude-style-checker-prompt.md`: Prompt engineering documentation
- `style-guide-database.md`: Complete style rule reference

### Technical Details
- Python 3.7+ compatibility
- Anthropic SDK integration
- Character count tracking for API efficiency
- Temperature set to 0 for consistent output
- 16,000 token limit for responses
- Supports custom prompt and style guide file paths

---

## Version History

- **1.1.0** (2025-10-03): Three output modes, enhanced workflows, documentation reorganization
- **1.0.0** (2025-10-02): Initial release with core functionality
