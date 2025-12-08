# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Production Testing Guide** (`docs/production-testing.md`) - Comprehensive guide for testing the action
  - Local CLI testing workflow
  - GitHub test repository setup (`test-action-style-guide`)
  - Testing checklist and debugging guide
  
- **Test Repository** (`QuantEcon/test-action-style-guide`) - Dedicated repository for action testing
  - Jupyter Book structure with test lectures
  - Workflow for manual and comment-triggered testing
  - Clean and violation test lectures for regression testing
  - Scheduled weekly regression tests

- **PR Labels Input** (`pr-labels`) - Allow custom labels on created PRs
  - New action input: `pr-labels` (comma-separated list)
  - Custom labels added to default labels (automated, style-guide, review)
  - Useful for test repos to add labels like 'do-not-merge'

### Changed

- **Simplified comment trigger syntax** - Now only supports `@qe-style-checker`
  - Removed legacy `@quantecon-style-guide` syntax
  - Removed experimental `@github-actions style-guide` syntax
  - Cleaner codebase with single comment pattern
  - Updated documentation to reflect syntax

### Removed

- **RELEASE-GUIDE.md** - Outdated release documentation removed

## [0.4.0] - 2025-12-08

### Changed

- **Renamed rule classification from "Category" to "Type"** - Clearer terminology throughout
  - Rule files: `**Category:** rule|style` → `**Type:** rule|style`
  - Code: `rule_category` → `rule_type` in reviewer.py, parser_md.py
  - Prompts: Updated all 8 category prompts to use "`rule` type" and "`style` type"
  - Documentation: Updated ARCHITECTURE.md and README.md to use "Type" terminology
  - Tests updated to use new terminology
  - Prevents confusion with topic categories (writing, math, code, etc.)

- **Documented `migrate` type** - Third rule type for legacy pattern updates
  - Used in JAX and code categories for patterns like `tic/toc` → `qe.Timer()`
  - Treated as suggestions (not auto-applied), similar to `style` type
  - Added to Rule Types table in ARCHITECTURE.md
  - Added new "Type: migrate" section in README.md

- **tool-style-checker now shares prompts/rules with main action**
  - Deleted duplicate `tool-style-checker/prompts/` and `tool-style-checker/rules/` directories
  - Tool now loads from `style_checker/prompts/` and `style_checker/rules/`
  - Single source of truth - local testing uses same rules as production
  - Updated README to document shared resource architecture

- **Updated tool-style-guide-development for Type terminology**
  - `build_rules.py`: Updated regex to parse `**Type:**` instead of `**Category:**`
  - `style-guide-database.md`: Renamed "Categories" section to "Types"
  - Generated rule files in `rules/`: Updated all to use `**Type:**`
  - README: Updated documentation to reflect changes

### Added

- **ARCHITECTURE.md** - Comprehensive developer documentation
  - System architecture diagram (Mermaid)
  - Data flow for single and weekly processing modes
  - Component descriptions with key functions
  - Configuration reference (inputs, environment variables)
  - Development guide with testing instructions

- **FUTURE-ENHANCEMENTS.md** - Roadmap and research notes
  - GitHub inline suggestions approach (checkbox-based style suggestions)
  - Incremental PR review mode proposal
  - Batch processing improvements (resume capability, progress reporting)
  - Multi-model support for cost optimization
  - Rule confidence scoring concept

- **docs/README.md** - Documentation index with quick links

### Fixed

- **LLM integration tests** - Updated to use current API signatures
  - Changed from `review_lecture(rules_text=...)` to `review_lecture_single_rule(categories=...)`
  - All 30 tests now passing (23 unit + 7 integration)
  - Added new test for `review_lecture_smart()` method
  - Test coverage improved from 36% to 53%

- **README version badge** - Updated from 0.3.17 to match current version

## [0.3.24] - 2025-10-11

### Fixed

- **qe-writing-002 rule conflict** - Added constraint to prevent violating qe-writing-001
  - qe-writing-002 was breaking long sentences into multiple sentences without blank lines
  - This violated qe-writing-001 (one sentence per paragraph)
  - Added "Important" note: Breaking sentences up requires blank lines between each sentence
  - Changed category from `rule` to `style` for advisory guidance
  - Self-contained constraint (no external links needed)

## [0.3.23] - 2025-10-11

### Fixed

- **qe-writing-002 rule conflict** - Added explicit exception to prevent breaking sentences
  - qe-writing-002 was breaking long sentences into multiple sentences
  - This violated qe-writing-001 (one sentence per paragraph)
  - Added "Important" section: Do NOT break sentences, instead simplify within single sentence
  - Provides guidance: remove words, simplify clauses, use direct phrasing, restructure
  - Prevents conflicting edits between rules processed sequentially

## [0.3.23] - 2025-10-11

### Changed

- **Remove redundant CRITICAL instruction** - Removed ambiguous "Current text and Suggested fix MUST be different" note
  - Instruction was redundant (obviously fixes should change something)
  - Was causing confusion and potentially skipping valid fixes
  - Validation is already handled by `validate_fix_quality()` function
  - Cleaner, simpler prompt with less confusion
  - Updated writing prompt version to 0.3.23

## [0.3.22] - 2025-10-11

### Fixed

- **Whitespace fix application** - Clarified CRITICAL instruction to allow subtle visual differences
  - Changed from "MUST be different" (ambiguous) to "must change something"
  - Added explicit note: "Even if the visual difference is subtle (like whitespace changes), ensure the suggested fix actually corrects the violation"
  - Fixes issue where whitespace fixes were being skipped because they looked "the same"
  - LLM was interpreting "different" too strictly, avoiding reporting valid whitespace violations
  - Updated writing prompt version to 0.3.22

## [0.3.21] - 2025-10-11

### Fixed

- **Parser support for tilde fences** - Updated violation parser to handle both backtick and tilde code fences
  - Parser now accepts `~~~markdown` (as instructed in prompts) in addition to ` ```markdown`
  - Fixes issue where Current text and Suggested fix weren't being extracted from LLM responses
  - Regex patterns updated: `(?:```|~~~)` to match either fence type
  - Ensures PR comments display violations correctly

## [0.3.20] - 2025-10-11

### Changed

- **Writing prompt improvements** - Updated to reflect single-rule processing architecture and simplified language
  - Changed from "check all writing rules" to "check one specific rule" 
  - Emphasizes checking ONLY the provided rule, not other issues
  - Clarified that rules are processed one at a time sequentially
  - Simplified rule/style category descriptions (removed verbose explanations)
  - Changed "Quality over quantity" to "Apply the rule appropriately"
  - More concise and actionable instructions
  - Updated version comment to `0.3.19` and added "Single rule per LLM call" description
  - Better focused output with rule-specific summary messages

### Fixed

- **qe-writing-001 false positives** - Simplified rule definition to prevent reporting already-correct text
  - Removed verbose "CRITICAL - Do NOT report" sections
  - Changed "Check for" to focus on violations requiring fixes
  - Simplified examples by removing redundant "DO NOT report" comments
  - More concise rule definition following "simplicity above all" principle

## [0.3.19] - 2025-10-11

### Fixed

- **Duplicate explanation in PR comments** - Removed list formatting from violation output templates
  - Updated all 8 category prompts to use paragraph format instead of list items
  - Changed from `- **Severity:** error` to `**Severity:** error` (no bullet point)
  - Eliminates duplicate explanation text that appeared in PR comments
  - Cleaner, more readable output format
  - Affects: writing, math, code, jax, figures, references, links, admonitions prompts

## [0.3.18] - 2025-10-11

### Fixed

- **qe-writing-001 false positives** - Clarified "Check for" criteria to prevent reporting already-correct text
  - Updated rule to specify: "Only report when blank lines need to be ADDED to separate sentences"
  - Simplified language by removing verbose "DO NOT report" sections
  - Focuses on the actual violation: multiple sentences in a single paragraph block (no blank lines between them)
  - Fixes issue where LLM would report correctly-formatted text as violations

## [0.3.17] - 2025-10-11

### Changed

- **LLM prompt output format** - Updated all prompts to use tilde fences in output examples
  - Changed from triple backticks to `~~~markdown` for "Current text" and "Suggested fix" blocks in prompt templates
  - LLM now generates responses that match GitHub handler's tilde fence format
  - Ensures consistency between what LLM is instructed to output and what GitHub handler expects
  - Affects all 8 category prompts: writing, math, code, jax, figures, references, links, admonitions
  - Completes migration from 4-backtick approach (v0.3.15) to tilde fence standard (v0.3.16)

## [0.3.16] - 2025-10-10

### Changed

- **PR comment fence markers** - Use tilde (`~~~`) fences instead of backticks for markdown blocks
  - Changed all PR comment code blocks from ` ````markdown` to `~~~markdown`
  - Uses tildes for outer fences, preserving backticks for MyST Markdown content
  - Prevents fence depth conflicts with nested directives (e.g., ` ```{code-cell}`, ` ```{note}`)
  - More elegant solution per GitHub Flavored Markdown spec
  - Updated all prompt files to instruct LLM to use tilde fences
  - Updated tests to verify tilde fence usage

## [0.3.15] - 2025-10-10

### Changed

- **PR comment markdown formatting** - Use four backticks for code blocks
  - Changed all PR comment markdown code blocks from ` ```markdown` to ` ````markdown`
  - Prevents rendering issues when MyST Markdown content contains nested directives with three-backtick code blocks
  - Affects `format_detailed_report()`, `format_applied_fixes_report()`, and `format_style_suggestions_report()`

## [0.3.14] - 2025-10-10

### Added

- **Separate handling for rule vs style category violations** - Two-comment PR system
  - **Rule category violations (mechanical fixes)**: Automatically applied to lecture content
    - Rules: qe-writing-001, 002, 004, 005, 006, 008
    - Applied fixes posted as collapsible PR comment for reference
    - Includes all fix details (original text, applied fix, explanation)
  - **Style category violations (subjective suggestions)**: Collected but NOT auto-applied
    - Rules: qe-writing-003 (logical flow), 007 (visual elements)
    - Suggestions posted as OPEN PR comment requiring human review
    - Prevents "over enthusiastic" LLM from making subjective changes
  - Updated `extract_individual_rules()` to capture category field from rule definitions
  - Modified `review_lecture_single_rule()` to filter fixes by category before applying
  - Added `format_applied_fixes_report()` and `format_style_suggestions_report()` methods
  - Two separate PR comments: one collapsible (applied), one open (suggestions)

### Changed

- **PR comment structure redesigned** - Replaced single detailed report with two targeted comments
  - Previous: One collapsible comment with ALL violations (mixed rule and style)
  - Now: Separate comments for automatic fixes vs suggestions requiring human review
  - Applied fixes comment: Collapsed by default (reference only, already applied)
  - Style suggestions comment: Open by default (immediate visibility for review)

## [0.3.13] - 2025-10-10

### Added

- **Hardcoded rule evaluation order** - Rules now checked in optimal sequence
  - Defined `RULE_EVALUATION_ORDER` constant in `reviewer.py`
  - Writing rules checked in priority: 008 → 001 → 004 → 006 → 005 → 002 → 003 → 007
  - Order: mechanical → structural → stylistic → creative
  - Previously: Rules checked in file order (001, 002, 003...) regardless of priority
  - Now: Rules extracted and checked in optimal order for best results
  - Whitespace (008) checked FIRST, visual elements (007) checked LAST
  - Easy to maintain: update constant to change order, no need to reorder file

## [0.3.12] - 2025-10-10

### Fixed

- **Sequential fix application in single-rule evaluation** - Critical bug fix
  - Previous implementation collected ALL violations from ALL rules, then applied fixes at the end
  - This meant rule 002 was checking against ORIGINAL content, not content fixed by rule 001
  - **Now applies fixes immediately after each rule** before checking the next rule
  - Rule 001 → find violations → apply fixes → Rule 002 checks the UPDATED content
  - Ensures proper sequential processing: each rule sees the results of previous fixes
  - More accurate detection as later rules work with already-cleaned content

## [0.3.11] - 2025-10-10

### Changed

- **REVERTED: Rule renumbering from v0.3.10** - Restored original rule numbers
  - Testing showed renumbering didn't solve the problem - LLM still fixated on one rule (002 instead of 001)
  - Maintaining sequential rule numbers based on evaluation order creates unnecessary maintenance burden
  - Restored original numbering: 001=paragraph, 002=clarity, 003=flow, 004=caps, 005=bold/italic, 006=titles, 007=visual, 008=whitespace
  - **Root cause confirmed**: LLM cannot reliably check multiple rules in a single pass, regardless of numbering or explicit STEP-by-STEP instructions

### Added

- **Single-rule evaluation approach** - New architecture for guaranteed rule coverage
  - Instead of asking LLM to check all rules at once, loop through rules one at a time
  - Each rule gets its own focused LLM call with that specific rule injected at bottom of prompt
  - Guarantees every rule is evaluated independently
  - Trade-off: 8× API calls for writing category, but reliable comprehensive coverage
  - More expensive but ensures no rules are skipped or ignored
  
### Removed

- **Removed STEP-by-STEP sequential evaluation instructions** - Didn't work
  - LLM consistently ignores explicit ordering instructions when given multiple rules
  - Simplified prompt back to basic "check systematically" approach
  - Single-rule architecture makes sequential ordering unnecessary

## [0.3.10] - 2025-10-10

### Changed

- **BREAKING: Renumbered writing rules to match evaluation priority** - LLM was ignoring STEP-by-STEP order
  - `qe-writing-001`: Whitespace formatting (was 008) - STEP 1
  - `qe-writing-002`: Paragraph structure (was 001) - STEP 2
  - `qe-writing-003`: Capitalization (was 004) - STEP 3
  - `qe-writing-004`: Title capitalization (was 006) - STEP 4
  - `qe-writing-005`: Bold/italic formatting (unchanged) - STEP 5
  - `qe-writing-006`: Clarity and conciseness (was 002) - STEP 6
  - `qe-writing-007`: Logical flow (was 003) - STEP 7
  - `qe-writing-008`: Visual elements (was 007) - STEP 8
  - **Rationale**: Testing revealed LLM was completely ignoring STEP instructions and always checking rule 001 first (29 violations for 001, zero for 008 despite explicit STEP 1: check 008 first). Hypothesis: LLM is biased toward checking lower-numbered rules first. By aligning rule numbers with evaluation priority, we work with this behavior instead of fighting it.
  - Rules now match their evaluation order: 001 is checked in STEP 1, 002 in STEP 2, etc.

### Added

- **Prompt version tracking** - Added version comment to prompts for better debugging
  - Format: `<!-- Prompt Version: 0.3.10 | Last Updated: 2025-10-10 | Description -->`
  - Displayed in logs: "✓ Using writing prompt v0.3.10"
  - Helps verify correct prompt is loaded (important for GitHub Actions cache)
  - Replaces previous "SEQUENTIAL RULE EVALUATION" detection check

## [0.3.9] - 2025-10-10

### Changed

- **Added action version to PR description** - PR body now includes version number in summary section

### Fixed

- **Fixed PR body length error** - Exceeded GitHub's 65KB limit for PR descriptions
  - Changed from listing all violation details to summarizing by rule
  - Groups violations by rule and shows first 2 examples only
  - Shows count of occurrences per rule (e.g., "15 occurrences")
  - Includes automatic truncation at 60KB with warning if still too long
  - Reduces PR body size by ~90% for large violation counts
  - Users can still see all details in the diff

## [0.3.8] - 2025-10-10

### Changed

- **Strengthened rule evaluation order in writing prompt** - Made order mandatory
  - Changed from "for optimal results" to "CRITICAL: Apply rules in this EXACT order"
  - Changed from bullet points to numbered list for emphasis
  - Added "This sequence is MANDATORY, not optional"
  - Added "Do NOT skip ahead or check rules out of sequence"
  - Added instruction to check each rule in order before moving to next
  - Prevents LLM from applying rules out of sequence

### Added

- **Prevent identical current/fix violations** - Quality control for LLM responses
  - Added CRITICAL instruction: "Current text" and "Suggested fix" MUST be different
  - If LLM cannot provide different fix, must NOT report as violation
  - Prevents confusing quality warnings where current and fix are identical

### Fixed

- **Action now fails on errors** - Exit with code 1 when LLM errors occur
  - Previously printed error but continued with exit code 0
  - Now properly exits with failure code when errors detected
  - Helps catch issues like "Overloaded" API errors
  - Both single and bulk modes now fail appropriately on errors

## [0.3.7] - 2025-10-10

### Changed

- **Updated qe-writing-001** - Clarified paragraph block definition to prevent false positives
  - Strengthened definition: "Each paragraph block (text separated by blank lines)"
  - Added explicit statement: "Line breaks within text (without blank lines) do NOT create new paragraphs"
  - Added example showing CORRECT usage (text already following the rule)
  - Added "Key distinction" section explaining blank lines vs line breaks
  - Updated implementation note to emphasize paragraph blocks are defined by blank lines
  - Fixes issue where LLM incorrectly flagged already-correct text as violations

### Fixed

- **qe-writing-001 false positives** - LLM now correctly understands paragraph block boundaries
  - Previously flagged correct text (sentences separated by blank lines) as violations
  - Added clearer examples and stronger language about blank lines vs line breaks

## [0.3.6] - 2025-10-10

### Added

- **Order of Evaluation** - Added rule evaluation sequence to writing prompt
  - Added explicit evaluation order to writing-prompt.md (instruction #3)
  - Rules now processed from mechanical fixes → structural → stylistic → creative
  - Sequence: whitespace → paragraph structure → capitalization → titles → formatting → clarity → flow → visual
  - Improves consistency and quality of LLM-generated suggestions
  - Each rule benefits from corrections made by earlier rules in the sequence
  - Kept in prompt only (single source of truth, easier maintenance)

- **Version Display** - Action now prints version at startup
  - Shows full version number in GitHub Action output (e.g., "v0.3.6")
  - Helps identify which version is running when using floating tags like `@v0.3`
  - Version defined in `style_checker/__init__.py`

### Changed

- **Version bumped** to 0.3.6

## [0.3.5] - 2025-10-10

### Changed

- **Updated qe-writing-001** - Clarified line break handling
  - Added clarification that sentences can span multiple lines in markdown source
  - Rule focuses on logical paragraph structure (one sentence per paragraph block), not physical line breaks
  - Added example showing single sentence spanning multiple lines
  - Updated implementation note to explain paragraph definition
  - Paragraphs are defined by blank lines, not line breaks within the text

## [0.3.4] - 2025-10-10

### Added

- **New writing rule: qe-writing-008** - Whitespace linting
  - Detects multiple consecutive spaces between words in MyST Markdown source
  - Suggests reducing excessive whitespace to single spaces
  - Improves markdown source consistency and readability
  - Excludes code blocks, inline code, math blocks, and intentional formatting
  - Linting-focused rule (doesn't affect HTML output, only source quality)

### Changed

- **Updated qe-writing-001** - Clarified scope
  - Added "Associated rules" section referencing qe-writing-008 for whitespace issues
  - Updated implementation note to reference the new whitespace rule
  - Focuses on sentence structure and paragraph organization
- **Updated writing prompt** - Added whitespace formatting to checklist

## [0.3.3] - 2025-10-10

### Changed

- **Removed "Corrected Content" from LLM responses** - Major performance improvement
  - Prompts no longer request full corrected lecture in response
  - Fixes applied programmatically using existing `apply_fixes()` function
  - Reduces output tokens by ~50% (e.g., 40K char lecture now ~20K tokens cheaper)
  - Faster API responses and lower costs
  - Matches `tool-style-checker` architecture for consistency
  - Parser updated to not expect "Corrected Content" section
  - All 8 prompt files updated to new streamlined format

### Performance Impact

- **Token savings**: ~20,000 output tokens saved per 40K character lecture
- **Cost reduction**: Approximately 50% reduction in output token costs
- **Speed improvement**: Faster API responses (less content to generate)
- **Same functionality**: Fixes still applied, just more efficiently

## [0.3.2] - 2025-10-10

### Fixed

- **CRITICAL BUG FIX**: Parser format mismatch causing 100% failure in violation detection
  - **Issue**: v0.3.0 and v0.3.1 reported "No issues found" even when violations existed
  - **Root Cause**: Prompts requested free-form format but parser expected structured format
  - **Impact**: Parser couldn't extract violations from Claude responses → always reported 0 issues
  - **Solution**: Updated all 8 prompt files to request parser-compatible output format
  - Prompts now explicitly request `## Issues Found\n[NUMBER]` with structured violations
  - Parser can now successfully extract violation count and details
  - Fixes complete failure of violation detection in v0.3.0 and v0.3.1
  - See `BUG-REPORT-PARSER-FORMAT-MISMATCH.md` for detailed analysis

### Changed

- All prompt files now include explicit, detailed output format specifications
- Format matches what `parse_markdown_response()` expects for reliable parsing

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
