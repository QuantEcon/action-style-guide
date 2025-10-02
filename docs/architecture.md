# How It Works - Architecture Diagram

## System Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         GitHub Repository                                │
│                    (lecture-python-programming.myst)                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ User comments:
                                    │ "@quantecon-style-guide aiyagari"
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        GitHub Actions Workflow                           │
│                    (.github/workflows/style-guide.yml)                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Triggers
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    QuantEcon Style Guide Action                          │
│                    (QuantEcon/action-style-guide@v1)                   │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  1. GitHub Handler                                              │   │
│  │     • Parse comment: extract "aiyagari"                         │   │
│  │     • Find file: lectures/aiyagari.md                          │   │
│  │     • Read content from repository                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│                                    ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  2. Style Guide Parser                                          │   │
│  │     • Load style-guide-database.md (48 rules)                  │   │
│  │     • Filter by priority & category                             │   │
│  │     • Format for LLM consumption                                │   │
│  │     • Split into manageable chunks                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│                                    ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  3. LLM Reviewer                                                │   │
│  │     ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │   │
│  │     │   Claude     │  │     GPT-4    │  │    Gemini    │       │   │
│  │     │  (default)   │  │   (OpenAI)   │  │   (Google)   │       │   │
│  │     └──────────────┘  └──────────────┘  └──────────────┘       │   │
│  │                                                                  │   │
│  │     • Send lecture content + rules                              │   │
│  │     • Get structured JSON response:                             │   │
│  │       - Violations found                                        │   │
│  │       - Specific fixes                                          │   │
│  │       - Corrected content                                       │   │
│  │       - Explanations                                            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│                                    ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  4. GitHub Handler (PR Creation)                                │   │
│  │     • Create branch: style-guide/aiyagari-20251001              │   │
│  │     • Commit corrected content                                  │   │
│  │     • Create PR with:                                           │   │
│  │       - Title: "[aiyagari] Style guide review"                 │   │
│  │       - Detailed body with all changes                          │   │
│  │       - Labels: automated, style-guide, review                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Pull Request Created                             │
│                                                                           │
│  Title: [aiyagari] Style guide review                                   │
│                                                                           │
│  ## 📋 Style Guide Review: aiyagari                                      │
│                                                                           │
│  Issues Found: 12                                                        │
│                                                                           │
│  ### 🎯 Issues by Priority                                               │
│  - 🔴 Critical: 2                                                        │
│  - 🟠 Mandatory: 5                                                       │
│  - 🟡 Best Practice: 5                                                   │
│                                                                           │
│  ### 📝 Detailed Changes                                                 │
│  [Full list of violations with fixes]                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. GitHub Handler (`github_handler.py`)
**Purpose**: Interface with GitHub API

**Responsibilities**:
- Parse issue comments to extract lecture names
- Find lecture files in repository
- Read file contents
- Create branches
- Commit changes
- Create pull requests
- Manage labels and formatting

**Key Methods**:
- `extract_lecture_from_comment()` - Parse trigger comments
- `find_lecture_file()` - Locate lecture files
- `create_branch()` - Create PR branches
- `commit_changes()` - Apply fixes
- `create_pull_request()` - Open PRs with formatting
- `format_pr_body()` - Generate PR descriptions

### 2. Style Guide Parser (`parser.py`)
**Purpose**: Load and organize style rules

**Responsibilities**:
- Parse YAML rule database
- Validate rule structure
- Query rules by category/priority
- Format rules for LLM consumption
- Chunk large rule sets

**Key Classes**:
- `StyleRule` - Individual rule representation
- `StyleGuideDatabase` - Complete rule collection

**Key Methods**:
- `load_style_guide()` - Parse YAML file
- `get_rules_by_category()` - Filter rules
- `format_rules_for_llm()` - Prepare for AI

### 3. LLM Reviewer (`reviewer.py`)
**Purpose**: AI-powered style checking

**Responsibilities**:
- Interface with multiple LLM providers
- Send structured prompts
- Parse JSON responses
- Handle chunked processing
- Error recovery

**Supported Providers**:
- **Claude** (Anthropic) - Default, best quality
- **GPT-4** (OpenAI) - High quality, widely used
- **Gemini** (Google) - Cost-effective option

**Key Classes**:
- `LLMProvider` - Abstract base class
- `AnthropicProvider` - Claude implementation
- `OpenAIProvider` - GPT-4 implementation
- `GeminiProvider` - Gemini implementation
- `StyleReviewer` - Main coordinator

### 4. Main Orchestrator (`main.py`)
**Purpose**: Coordinate the entire workflow

**Responsibilities**:
- Parse command-line arguments
- Initialize components
- Handle single vs bulk mode
- Error handling
- GitHub Actions output

**Workflow**:
1. Parse arguments (mode, paths, provider, etc.)
2. Initialize GitHub handler and LLM reviewer
3. Load style guide rules
4. Process lecture(s)
5. Create PR(s) if needed
6. Report results

## Data Flow

### Single Lecture Review

```
Comment → Extract Name → Find File → Read Content
                                          ↓
                                    Load Rules
                                          ↓
                              Format for LLM (chunks)
                                          ↓
                            Send to LLM (multiple rounds)
                                          ↓
                              Collect violations
                                          ↓
                              Generate fixes
                                          ↓
                         Create branch & commit
                                          ↓
                            Create PR with details
```

### Bulk Review

```
Get All Lectures → For Each Lecture:
                       │
                       ├─ Read Content
                       ├─ Review against rules
                       ├─ Collect violations
                       └─ Commit to branch
                            ↓
                   Single PR with all commits
```

## Rule Structure

```yaml
qe-category-nnn:
  title: "Human-readable title"
  category: "category_name"
  type: "rule_type"
  priority: "critical|mandatory|best_practice|preference"
  rule: "Detailed rule description"
  examples:
    correct: "Good example"
    incorrect: "Bad example"
  note: "Additional context"
```

## LLM Response Format

```json
{
  "issues_found": 12,
  "violations": [
    {
      "rule_id": "qe-writing-002",
      "rule_title": "One-Sentence Paragraphs",
      "severity": "critical",
      "description": "Paragraph contains 3 sentences",
      "location": "Line 45",
      "current_text": "Multi-sentence paragraph...",
      "suggested_fix": "Split into 3 paragraphs...",
      "explanation": "Rule requires one sentence per paragraph"
    }
  ],
  "corrected_content": "Full corrected lecture text...",
  "summary": "Fixed 12 issues across 5 categories..."
}
```

## Error Handling

- **File Not Found**: Clear error message, suggest alternatives
- **API Errors**: Retry with exponential backoff
- **Rate Limits**: Wait and retry
- **Invalid JSON**: Fallback parsing strategies
- **GitHub Errors**: Detailed error messages
- **LLM Failures**: Graceful degradation, partial results

## Performance Optimization

- **Chunking**: Split large rule sets into manageable pieces
- **Parallel Processing**: Process rule chunks concurrently (future)
- **Caching**: Cache rule parsing (future)
- **Incremental**: Only review changed files (future)

## Security Considerations

- API keys stored in GitHub Secrets
- No credentials in logs or outputs
- Scoped GitHub tokens
- Rate limit protection
- Input validation
- Safe YAML parsing
