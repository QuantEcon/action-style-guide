# Future Enhancements

> Planned improvements and enhancement ideas for the QuantEcon Style Guide Checker.

## High Priority

### 1. Large-Context Model Batch Evaluation

**Status:** Research / Testing needed

**Description:** The current architecture makes **49 separate LLM calls** per full review (one per rule), because Claude Sonnet 4.5 (~200K context) was found to silently skip rules when given multiple rules at once. With next-generation models like Claude Opus 4.6 (1M+ context), we should test whether batch evaluation becomes reliable — potentially reducing 49 calls to 1-8 calls.

**Current Architecture (Single-Rule):**
- One LLM call per rule, 49 calls total for a full review
- Each call sends: category prompt + one rule + full lecture document (~5-12K tokens)
- Fixes applied between rules — Rule N+1 sees the document with Rule N's fixes
- Total input: ~400K tokens across all calls (document sent 49 times)
- Proven reliable: every rule gets checked, no silent skips

**Why This Matters:**
- **Latency**: 49 sequential API calls take minutes; 1-8 calls could take seconds
- **Cost**: The full document is repeated in every call; batch sends it once
- **New models**: 1M+ context windows change the feasibility calculus
- **But**: Context window size ≠ attention quality. "Lost in the middle" is a real phenomenon — rules in the middle of a long list may get less attention

**Testing Roadmap — Three Progressive Strategies:**

#### Strategy A: Category-Level Batching (8 calls) — Test First

Send all rules for one category in a single call. 8 calls instead of 49.

```
Call 1: writing prompt + 8 writing rules + document
Call 2: math prompt + 9 math rules + document (with writing fixes applied)
...
Call 8: admonitions prompt + 5 admonition rules + document (with all prior fixes)
```

**Advantages:**
- Rules within a category are thematically related — model attends to them as a group
- Still allows sequential fix application *between* categories
- Modest complexity increase over current approach
- 6x reduction in API calls

**Risks:**
- Categories with many rules (figures: 11, math: 9) may still see skips
- Output parsing becomes more complex (multiple rules' violations in one response)

**Test plan:**
- Run category-level batching on 5-10 real lectures
- Compare violations found vs single-rule baseline
- Measure: rule skip rate, fix quality, response parsing reliability
- Accept if skip rate < 5% across all categories

#### Strategy B: Two-Pass Detect-Then-Fix (2+ calls) — Test Second

First pass sends all 49 rules in one call for **detection only** (no fixes requested). Second pass does targeted single-rule calls only for rules that found violations.

```
Pass 1: All rules + document → "List which rules have violations" (1 call)
Pass 2: For each violated rule → single-rule prompt for precise fixes (N calls)
```

**Advantages:**
- Clean lectures (no violations) complete in 1 call instead of 49
- Focuses expensive fix-generation calls on actual violations
- Maintains fix quality from single-rule approach where it matters

**Risks:**
- False negatives in Pass 1 mean violations are missed entirely
- Still requires single-rule calls for fix generation
- Net benefit depends on violation rate — highly compliant lectures benefit most

**Test plan:**
- Run Pass 1 on lectures with known violations (from single-rule baseline)
- Measure detection recall: what % of known violations does Pass 1 catch?
- Accept if recall > 90% (remaining 10% caught by periodic full single-rule runs)

#### Strategy C: Full Single-Call Batch (1 call) — Test Last

All 49 rules + document in one call. Maximum speed, maximum risk.

```
Single call: master prompt + all 49 rules + document → all violations + fixes
```

**Advantages:**
- Fastest possible: one call per lecture
- Simplest architecture (no sequencing logic)
- Model sees full rule set — may catch rule interactions

**Risks:**
- Silent rule skips (the original problem with Sonnet 4.5)
- Fix conflicts: two rules editing the same text with no sequencing
- Very long structured output — parsing fragility
- Hardest to debug when things go wrong

**Test plan:**
- Run on 10+ lectures, compare violations found vs single-rule baseline
- Measure: skip rate per rule, fix conflict rate, output parsing success
- Require < 2% skip rate and < 5% fix conflict rate to adopt
- Consider a "verification call" that asks the model to confirm it checked all 49 rules

**Key Design Decisions to Make:**

1. **Fix sequencing**: Batch modes lose the "each rule sees prior fixes" guarantee. Is this actually important? Test by comparing fix quality with/without sequential application.

2. **Output format**: Single-rule responses are simple markdown. Batch responses need clear per-rule sections. May need structured output (JSON mode) for reliability.

3. **Fallback strategy**: Should we always fall back to single-rule for rules that batch mode tends to skip? This could be a per-rule configuration.

4. **Model selection**: This enhancement pairs with Multi-Model Support (#7). Different models may have different batch reliability thresholds.

**Estimated Effort:** Medium (1-2 weeks including testing)
- Prompt engineering for batch mode
- Response parsing updates
- Comparison testing infrastructure
- Decision criteria and cutover plan

### 2. GitHub Inline Suggestions

**Status:** Research needed

**Description:** GitHub's [suggested changes feature](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/incorporating-feedback-in-your-pull-request#applying-suggested-changes) allows reviewers to propose code changes inline that can be accepted with a single click.

**Current Limitation (verified via GitHub API docs):** 
- Suggested changes can only be added to lines that appear in the PR's diff
- GitHub's [Pull Request Review Comments API](https://docs.github.com/en/rest/pulls/comments) requires `line` and `path` parameters referencing diff positions
- Our action creates the PR with fixes already applied, so the diff shows corrected content
- We cannot suggest changes on the "original" problematic lines - they don't exist in our diff

**Potential Approaches:**

1. **Checkbox-Based Style Suggestions (Recommended):**
   - Post `style` suggestions as a checkbox list in PR comment
   - User checks which suggestions they want applied
   - User comments `/apply-style` to trigger
   - Action parses checked items and creates commit with those fixes
   - Example format:
     ```markdown
     ### Style Suggestions
     Select the suggestions you'd like to apply, then comment `/apply-style`:
     
     - [ ] **Line 45**: Consider splitting this long sentence for clarity
       > Current: "This is a very long sentence that..."
       > Suggested: "This is a shorter sentence. The remaining content..."
     - [ ] **Line 89**: Add transition word for better flow
     - [x] **Line 112**: Simplify passive voice (pre-selected as recommended)
     ```
   - Pro: User control, native GitHub UI, parseable via API
   - Con: Requires follow-up action trigger

2. **Two-PR Strategy:**
   - First PR: Contains only `rule` type automatic fixes
   - Second PR (or comments): Contains `style` suggestions as GitHub suggestion blocks
   - Pro: Clean separation
   - Con: More complex workflow, suggestions still limited to diff lines

3. **Suggestion Block Format in Comments:**
   ```markdown
   ```suggestion
   Corrected text here
   ```
   ```
   - Pro: Native GitHub integration
   - Con: Only works on diff lines

4. **Easy-Copy Markdown Blocks:**
   - Current approach but improved formatting
   - Clear "Copy" indication with fenced blocks
   - Pro: Works everywhere
   - Con: Manual copy-paste required

**Recommendation:** 
1. **Near-term:** Improve formatting of style suggestions with clear copy-friendly blocks (useful regardless of other approaches)
2. **Future:** Implement checkbox-based style suggestions with `/apply-style` trigger for user-controlled application

### 3. Complete Test Suite with Nox

**Status:** Planned

**Description:** Migrate from direct pytest to nox for:
- Multi-Python version testing
- Linting automation  
- Documentation building
- Release automation
- **Test coverage improvement** (current: 53%, target: 80%+)

**Coverage Focus Areas:**
- `github_handler.py` (40% → 80%)
- `main.py` (6% → 60%)
- `fix_applier.py` (79% → 90%)

**Proposed `noxfile.py`:**
```python
import nox

@nox.session(python=["3.9", "3.10", "3.11", "3.12"])
def tests(session):
    session.install("-r", "requirements.txt")
    session.run("pytest", "tests/", "-v")

@nox.session
def lint(session):
    session.install("ruff", "black", "mypy")
    session.run("ruff", "check", "style_checker/")
    session.run("black", "--check", "style_checker/")
    session.run("mypy", "style_checker/")

@nox.session
def integration(session):
    session.install("-r", "requirements.txt")
    session.run("pytest", "-m", "integration", "-v")
```

## Medium Priority

### 4. Token Usage and Cost Tracking

**Status:** Planned

**Description:** Add token usage tracking and cost estimation to help monitor and optimize API usage.

**Current Limitation:**
- No visibility into token consumption per review
- Unable to estimate costs before running
- Difficult to optimize prompt efficiency
- No data for budget planning

**Proposed Features:**

1. **Token Tracking per Review:**
   - Track input/output tokens for each LLM call
   - Aggregate by rule, category, and lecture
   - Report in PR comment and logs
   
2. **Cost Estimation:**
   - Calculate estimated cost based on Claude pricing
   - Show breakdown: input tokens vs output tokens
   - Display per-lecture and total costs
   
3. **Usage Report Format:**
   ```markdown
   ### Token Usage Summary
   
   **Total Cost:** ~$0.15
   
   | Category | Rules Checked | Input Tokens | Output Tokens | Cost |
   |----------|---------------|--------------|---------------|------|
   | math     | 9             | 8,234        | 1,456         | $0.04 |
   | code     | 4             | 6,891        | 892           | $0.03 |
   | writing  | 12            | 12,456       | 2,134         | $0.08 |
   
   **Details:**
   - Claude Sonnet 4.5 pricing: $3/MTok (input), $15/MTok (output)
   - Average tokens per rule: 1,850 input, 450 output
   ```

4. **Optimization Insights:**
   - Identify expensive rules for prompt optimization
   - Track token usage trends over time
   - Compare before/after prompt changes
   
5. **Budget Controls (Optional):**
   - Set token/cost limits per run
   - Warning when approaching limits
   - Abort if limit exceeded

**Implementation:**
- Parse `usage` field from Anthropic API responses
- Aggregate in `reviewer.py` during review
- Add to PR comment via `github_handler.py`
- Store in action outputs for workflow access
- Optional: Log to file for historical tracking

**Benefits:**
- Visibility into API costs
- Data-driven prompt optimization
- Budget planning and control
- Justify infrastructure costs

**Estimated Effort:** Small (1-2 days)
- API already returns usage data
- Just needs aggregation and reporting
- No LLM changes required

### 5. Incremental Review Mode (PR Integration)

**Description:** Integrate style checking into the normal PR workflow, reviewing only files changed in a PR.

**Current Behavior:**
- `single` mode: Manually triggered via `@qe-style-checker lecture_name` comment on an issue
- `bulk` mode: Reviews all/multiple lectures (typically scheduled weekly)
- Neither mode automatically runs when a PR is opened or updated

**Proposed PR Integration:**
- Trigger on `pull_request` events (opened, synchronize)
- Automatically identify which lecture files were modified in the PR
- Review only those files (not the entire lecture series)
- Post results as PR review comments or status check

**Rule Subset Consideration:**
Some rules require full-document context and don't work well on diffs alone:

| Works on Diffs | Needs Full Document |
|----------------|---------------------|
| Math notation (`\top`, brackets) | One sentence per paragraph (qe-writing-001) |
| Code style (Unicode Greek) | Logical flow between sections |
| Link formatting | Consistent terminology |
| Admonition syntax | Reference completeness |
| Figure captions | Overall structure |

**Options:**
1. **Diff-only mode**: Only check rules that work at line-level (fast, limited)
2. **Full-file mode**: Check full file for any file with changes (thorough, slower)
3. **Hybrid**: Line-level rules on diff, flag that document-level rules need manual review
4. **Configurable**: Let repository choose which approach via workflow input

**Implementation:**
- New workflow trigger: `on: pull_request`
- Parse PR diff via GitHub API to identify changed `.md` files in `lectures/`
- Filter to only lecture files (not READMEs, configs, etc.)
- New `--mode pr` or `--diff-only` flag
- Tag rules with `scope: line` vs `scope: document` metadata

**Benefits:**
- Catches style issues before merge
- Fits natural development workflow
- No manual trigger needed
- Faster feedback loop

### 6. Batch Processing Improvements

**Description:** Improve bulk review mode for large lecture series.

**Current Behavior:**
- `bulk` mode processes all lectures in a repository sequentially
- Creates a single timestamped branch (e.g., `style-guide/bulk-review-20250109-143022`)
- Each lecture reviewed one at a time via `review_lecture_smart()`
- Each lecture with fixes gets its own commit (for easy reversion)
- Single PR created at the end with summary of all results
- Typically triggered on schedule (weekly cron job)

**Current Limitations:**
| Limitation | Impact |
|------------|--------|
| No parallelism | Slow for large repos (30+ lectures) |
| No resume capability | If it fails at lecture 25/50, restart from scratch |
| No progress persistence | Can't pause and continue later |
| No rate limiting | Could hit API limits on very large repos |
| Silent failures | Errors logged but easy to miss in large output |

**Proposed Improvements:**

1. **Resume Capability (High Value):**
   - Track progress in a state file (JSON in repo or Actions cache)
   - Store: last processed lecture, branch name, timestamp
   - `--resume` flag to continue from last checkpoint
   - Useful for recovering from failures or timeouts

2. **Progress Reporting:**
   - Real-time progress: `[15/47] Reviewing: intro_to_python.md`
   - Estimated time remaining based on average per-lecture time
   - Summary stats during run (issues found so far, errors)

3. **Parallel Processing (Lower Priority):**
   - Process N lectures concurrently (e.g., 3-5)
   - Requires careful rate limiting for LLM API
   - Complexity: managing concurrent commits to same branch
   - May not be worth the complexity initially

4. **Partial Failure Handling:**
   - Continue on error (current behavior, but improve)
   - Retry failed lectures once before giving up
   - Separate "failed lectures" section in PR body
   - Option to create PR even if some lectures failed

**Recommendation:** Start with resume capability and improved progress reporting. These provide the most value with modest complexity. Parallel processing can wait until bulk runs are proven slow enough to warrant the complexity.

## Lower Priority

### 7. Rule Confidence Scoring

**Description:** Track how reliably each rule performs to guide refinement efforts.

**Goal:** Identify which rules work well and which need improvement, so we can:
- Demote unreliable rules from `rule` → `style` type
- Prioritize prompt engineering efforts
- Build confidence in automated fixes

**Potential Metrics:**
- Fix application success rate (did the replacement work?)
- PR acceptance rate (was the fix merged or reverted?)
- Manual override frequency (did author change the fix?)
- False positive reports

**Data Collection Options:**

1. **Manual Tracking (Simple):**
   - Periodic review of merged PRs
   - Note which fixes were kept vs modified
   - Track in a spreadsheet or markdown file
   - Pro: No infrastructure, works now
   - Con: Manual effort, not systematic

2. **Reaction-Based Feedback:**
   - Add 👍/👎 instructions to suggestion comments
   - Parse reactions via GitHub API
   - Pro: Low friction for users
   - Con: Relies on users reacting, reaction API parsing

3. **PR Outcome Tracking:**
   - Track if style-guide PRs are merged, closed, or modified
   - Compare final merged content to original suggestions
   - Pro: Automated, objective
   - Con: Merge doesn't mean fix was good; needs storage

4. **Structured Feedback Form:**
   - Link to a form in PR comments for detailed feedback
   - Pro: Rich data
   - Con: High friction, low response rate

**Storage Considerations:**
- GitHub doesn't provide persistent storage natively
- Options: JSON file in repo, GitHub Actions cache, external service
- Simpler is better for now

**Recommendation:** Start with manual tracking during active development. Consider reaction-based feedback once rules stabilize. Full automation is lower priority.

### 8. Multi-Model Support

**Description:** Allow selection of different LLM models as part of cost optimization and quality tuning.

**Context:** Currently using Claude Sonnet 4.5 for all rules. Different rules have different complexity:
- Simple mechanical checks (e.g., `\top` → `^\top`) could use cheaper/faster models
- Complex stylistic judgments benefit from more capable models
- Cost scales with token usage and model tier

**Candidates:**
| Model | Strengths | Use Case |
|-------|-----------|----------|
| Claude Opus | Highest quality, best reasoning | Complex style rules, document-level analysis |
| Claude Sonnet | Good balance (current default) | Most rules |
| Claude Haiku | Fast, cheap | Simple mechanical rules |
| OpenAI GPT-4o | Strong reasoning, wide adoption | Comparison, redundancy |
| OpenAI GPT-5 | Next-gen capabilities (when available) | Evaluate for quality improvements |
| Google Gemini 2.5 | Competitive quality, long context | Alternative provider, large documents |
| Google Gemini 3 | Next-gen (when available) | Evaluate for cost/quality tradeoffs |

**Implementation Approaches:**

1. **Per-Category Model Selection:**
   - Configure model in each category's prompt or workflow
   - Example: `math` category uses Haiku, `writing` uses Sonnet
   - Pro: Simple, coarse-grained
   - Con: All rules in category use same model

2. **Per-Rule Model Selection:**
   - Tag each rule with preferred model tier
   - Example: `qe-math-001` (mechanical) → Haiku, `qe-writing-003` (stylistic) → Sonnet
   - Pro: Fine-grained optimization
   - Con: More complex, more metadata to maintain

3. **Cost-Based Routing:**
   - Set budget limits, route to cheaper models when budget consumed
   - Pro: Automatic cost control
   - Con: Variable quality within same run

**Cost Considerations:**
- Track token usage per rule/category
- Estimate cost before bulk runs
- Set budget alerts or limits

**Recommendation:** Start with per-category model selection (simplest). Measure actual cost/quality tradeoffs before adding complexity. This pairs well with Rule Confidence Scoring (#7) to identify which rules can safely use cheaper models.

## Completed Enhancements

- ✅ Sequential category processing (v0.3.0)
- ✅ Single-rule evaluation (v0.3.11)
- ✅ Rule vs style type separation (v0.3.14)
- ✅ Programmatic fix application (v0.3.3)
- ✅ Focused prompts architecture (v0.3.0)
- ✅ CLI tool integration - `tool-style-checker/` shares prompts/rules with main action
- ✅ Documentation sync - single source of truth, stale generated files removed
- ✅ LLM integration tests fixed - updated to current API, all 30 tests passing
