# GitHub Release Guide - v0.3.0

This guide walks through creating the v0.3.0 release on GitHub.

---

## Pre-Release Checklist

- [x] All tests passing (18/18)
- [x] Version updated to 0.3.0 in `style_checker/__init__.py`
- [x] CHANGELOG.md updated with release date (2025-10-10)
- [x] Documentation updated (README, CONTRIBUTING, examples)
- [x] Architecture review completed
- [x] Release notes prepared

---

## Step 1: Commit and Push Changes

```bash
# Add all changes
git add .

# Commit with version message
git commit -m "Release v0.3.0 - Focused prompts architecture

Major release with breaking changes:
- Focused prompts architecture (48% smaller)
- Sequential category processing
- Claude Sonnet 4.5 exclusive
- Simplified API (removed streaming)
- Rule development workflow
- Category validation

Breaking changes:
- Removed OpenAI/Gemini support
- Removed style-guide-url parameter
- New trigger: @qe-style-checker
- Removed 'all' category keyword

See CHANGELOG.md and RELEASE-NOTES-0.3.0.md for full details."

# Push to main
git push origin main
```

---

## Step 2: Create Git Tag

```bash
# Create annotated tag
git tag -a v0.3.0 -m "Release v0.3.0 - Focused prompts architecture

Major release featuring:
- Focused prompts for better quality and lower costs
- Sequential category processing for reliable results
- Claude Sonnet 4.5 exclusive
- Simplified architecture and API
- Rule development workflow

See RELEASE-NOTES-0.3.0.md for complete details."

# Push tag
git push origin v0.3.0
```

---

## Step 3: Create GitHub Release

### Option A: Using GitHub CLI (gh)

```bash
# Create release with notes
gh release create v0.3.0 \
  --title "v0.3.0 - Focused Prompts Architecture" \
  --notes-file RELEASE-NOTES-0.3.0.md \
  --latest

# Verify release
gh release view v0.3.0
```

### Option B: Using GitHub Web UI

1. **Navigate to Releases**
   - Go to: https://github.com/QuantEcon/action-style-guide/releases
   - Click "Draft a new release"

2. **Fill in Release Details**
   - **Tag**: `v0.3.0` (select from dropdown or create)
   - **Target**: `main` branch
   - **Title**: `v0.3.0 - Focused Prompts Architecture`
   - **Description**: Copy content from `RELEASE-NOTES-0.3.0.md`

3. **Configure Release**
   - [x] Set as the latest release
   - [ ] This is a pre-release (leave unchecked)

4. **Publish**
   - Click "Publish release"

---

## Step 4: Update Major Version Tag (Optional)

To allow users to use `@v0.3` instead of `@v0.3.0`:

```bash
# Delete old v0.3 tag if exists
git tag -d v0.3 2>/dev/null
git push origin :refs/tags/v0.3 2>/dev/null

# Create new v0.3 tag pointing to v0.3.0
git tag -f v0.3 v0.3.0

# Push v0.3 tag
git push origin v0.3 --force
```

This allows workflows to use either:
- `@v0.3.0` (pinned to exact version)
- `@v0.3` (tracks latest 0.3.x version)

---

## Step 5: Verify Release

### Check GitHub

1. Visit: https://github.com/QuantEcon/action-style-guide/releases/tag/v0.3.0
2. Verify:
   - Release notes are displayed correctly
   - Marked as "Latest"
   - Tag shows correct commit
   - Assets include source code archives

### Test Action

Create a test workflow in a lecture repository:

```yaml
name: Test v0.3.0
on: workflow_dispatch

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: QuantEcon/action-style-guide@v0.3.0
        with:
          mode: 'bulk'
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

Run manually and verify it works.

---

## Step 6: Announce Release

### 1. Update Documentation Links

Ensure all examples and documentation reference `@v0.3`:

- README.md examples ✅ (already updated)
- examples/*.yml ✅ (already updated)
- CONTRIBUTING.md ✅ (already updated)

### 2. Create Release Announcement

Post to relevant channels:

**GitHub Discussions:**
```markdown
# 🚀 Version 0.3.0 Released!

We're excited to announce v0.3.0 of the QuantEcon Style Guide Checker!

## What's New

✨ **Focused Prompts Architecture** - 48% smaller prompts, better quality, lower costs
🔄 **Sequential Category Processing** - More reliable results without conflicts
🤖 **Claude Sonnet 4.5 Exclusive** - Simplified to use only the best LLM
🛠️ **Rule Development Workflow** - Easy to maintain and update style rules
⚡ **Simplified API** - Faster and cleaner implementation

⚠️ **Breaking Changes** - Not backward compatible with 0.2.x

See full release notes: https://github.com/QuantEcon/action-style-guide/releases/tag/v0.3.0

Upgrade guide available in RELEASE-NOTES-0.3.0.md
```

**Internal Team:**
```
Version 0.3.0 is now live! 🎉

Major improvements:
- 48% reduction in prompt size
- More reliable sequential processing
- Simpler Claude-only architecture
- Better cost efficiency (~$0.60/lecture vs ~$0.90)

Migration required for existing workflows.
See: https://github.com/QuantEcon/action-style-guide/releases/tag/v0.3.0
```

---

## Post-Release Checklist

- [ ] GitHub release created and published
- [ ] v0.3 tag updated (optional)
- [ ] Release tested in production repo
- [ ] Announcement posted (if applicable)
- [ ] Old version (v0.2.x) deprecated notice added
- [ ] Documentation site updated (if applicable)

---

## Rollback Procedure (If Needed)

If critical issues are found:

```bash
# Delete the release (GitHub UI or gh CLI)
gh release delete v0.3.0 --yes

# Delete tags
git tag -d v0.3.0
git push origin :refs/tags/v0.3.0

# Revert commit if needed
git revert HEAD
git push origin main

# Create hotfix release v0.3.1 with fixes
```

---

## Next Steps

After successful release:

1. Monitor for issues in production usage
2. Gather feedback from users
3. Plan v0.3.1 with minor improvements:
   - Progress percentage for bulk reviews
   - Cost tracking and reporting
   - Additional examples

---

## Quick Reference

**Repository**: https://github.com/QuantEcon/action-style-guide
**Release URL**: https://github.com/QuantEcon/action-style-guide/releases/tag/v0.3.0
**Tag**: v0.3.0
**Commit**: (will be current HEAD after push)
**Release Date**: October 10, 2025

---

**Questions?** Open a discussion or issue on GitHub.
