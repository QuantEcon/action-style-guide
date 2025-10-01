# Quick Start Guide

Get started with the QuantEcon Style Guide Checker in 5 minutes!

## Prerequisites

- GitHub repository with lecture files
- API key for one of:
  - Anthropic Claude (recommended) - Get at [console.anthropic.com](https://console.anthropic.com)
  - OpenAI GPT-4 - Get at [platform.openai.com](https://platform.openai.com)
  - Google Gemini - Get at [ai.google.dev](https://ai.google.dev)

## Step 1: Add API Key Secret

1. Go to your repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add one of:
   - **Name**: `ANTHROPIC_API_KEY`, **Value**: Your Claude API key
   - **Name**: `OPENAI_API_KEY`, **Value**: Your OpenAI API key
   - **Name**: `GOOGLE_API_KEY`, **Value**: Your Gemini API key

## Step 2: Add Workflow File

Create `.github/workflows/style-guide.yml` in your repo:

```yaml
name: Style Guide Checker
on:
  issues:
    types: [opened, edited]
  issue_comment:
    types: [created]

jobs:
  review:
    if: contains(github.event.comment.body, '@quantecon-style-guide') || contains(github.event.issue.body, '@quantecon-style-guide')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: read
    steps:
      - uses: QuantEcon/action-style-guide@v1
        with:
          mode: 'single'
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
          comment-body: ${{ github.event.comment.body || github.event.issue.body }}
```

Commit and push this file.

## Step 3: Try It Out!

1. Create a new issue in your repository (or use existing one)
2. Comment: `@quantecon-style-guide aiyagari`
   - Replace `aiyagari` with the name of any lecture file
3. Wait ~30-60 seconds
4. A PR will be created with style guide fixes!

## What Happens Next?

The bot will:
1. ✅ Find your lecture file (e.g., `lectures/aiyagari.md`)
2. 🤖 Review it against all 51+ style guide rules
3. 📝 Create a PR with fixes if issues are found
4. 🏷️ Label the PR as `automated`, `style-guide`, `review`
5. 💬 Add detailed explanation of all changes

## Example PR Output

```markdown
## 📋 Style Guide Review: aiyagari

Issues Found: 12

### 🎯 Issues by Priority
- 🔴 Critical: 2
- 🟠 Mandatory: 5
- 🟡 Best Practice: 5

### 📝 Detailed Changes

#### Writing (3 issues)
1. qe-writing-002 - One-Sentence Paragraphs
   - Location: Line 45
   - Issue: Paragraph contains 3 sentences
   - Fixed: Split into 3 separate paragraphs
```

## Next Steps

### Add Weekly Reviews

Create `.github/workflows/weekly-review.yml`:

```yaml
name: Weekly Style Review
on:
  schedule:
    - cron: '0 0 * * 0'  # Sunday midnight

jobs:
  bulk-review:
    runs-on: ubuntu-latest
    steps:
      - uses: QuantEcon/action-style-guide@v1
        with:
          mode: 'bulk'
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Customize Settings

You can customize:

```yaml
- uses: QuantEcon/action-style-guide@v1
  with:
    mode: 'single'
    lectures-path: 'lectures/'           # Change lecture directory
    llm-provider: 'claude'               # or 'openai', 'gemini'
    llm-model: 'claude-3-5-sonnet-20241022'  # Specific model
    max-rules-per-request: 15            # Rules per AI request
    pr-branch-prefix: 'style-fix'        # Custom branch prefix
    anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
    github-token: ${{ secrets.GITHUB_TOKEN }}
    comment-body: ${{ github.event.comment.body || github.event.issue.body }}
```

## Troubleshooting

### "No lecture file found"
- Check the lecture name in your comment
- Verify file is in `lectures/` directory
- Try full path: `@quantecon-style-guide lectures/aiyagari.md`

### "API key error"
- Verify secret name matches workflow file
- Check API key is valid and has credits
- Test API key with provider's playground

### "Permission denied"
- Add `permissions:` block to workflow (see Step 2)
- Or use a Personal Access Token instead of `GITHUB_TOKEN`

### "Workflow doesn't trigger"
- Ensure workflow file is on main/default branch
- Check workflow syntax with GitHub Actions validator
- Look in Actions tab for error messages

## Tips

1. **Start Small**: Test with one lecture before bulk reviews
2. **Review PRs Carefully**: AI might suggest changes you don't want
3. **Iterate**: Update style-guide.yaml as your standards evolve
4. **Revert if needed**: Each lecture in bulk PRs is a separate commit
5. **Monitor Costs**: LLM API calls cost money, set up billing alerts

## Advanced Usage

### Use Different Provider for Different Repos

```yaml
# Fast lectures - use Gemini (cheaper)
llm-provider: 'gemini'
google-api-key: ${{ secrets.GOOGLE_API_KEY }}

# Complex lectures - use Claude (best quality)
llm-provider: 'claude'
anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Check Specific Rule Categories

```yaml
rule-categories: 'writing,mathematics,code'  # Only these categories
```

### Custom Style Guide

```yaml
style-guide-url: 'https://raw.githubusercontent.com/your-org/custom-rules/main/rules.yaml'
```

## Getting Help

- 📚 [Full Documentation](https://github.com/QuantEcon/action-style-guide)
- 🐛 [Report Issues](https://github.com/QuantEcon/action-style-guide/issues)
- 💬 [Discussions](https://github.com/QuantEcon/action-style-guide/discussions)
- 📖 [QuantEcon Manual](https://manual.quantecon.org)

## Success! 🎉

You're now using AI-powered style guide checking! Every lecture review helps maintain consistency and quality across all QuantEcon materials.
