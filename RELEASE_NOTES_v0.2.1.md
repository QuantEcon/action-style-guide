# Release v0.2.1 - Maintenance & Documentation Update

**Release Date:** October 2, 2025

A maintenance release that fixes GitHub Actions deprecation warnings, removes deprecated code, and updates all documentation for consistency with v0.2.0.

## 🐛 Bug Fixes

### GitHub Actions Deprecation Warning Fixed
- **Issue**: GitHub Actions workflows showing deprecation warnings for `set-output` command
- **Solution**: Migrated to `GITHUB_OUTPUT` environment file (modern approach)
- **Impact**: Eliminates warnings, improves security (prevents command injection)
- **Compatibility**: Fully backward compatible for local testing

### max-rules-per-request Parameter Removed
- **Issue**: Workflows using v0.2 tag were failing with "unrecognized arguments" error
- **Solution**: Completely removed deprecated parameter from `action.yml` and CLI
- **Why**: Semantic grouping (v0.2.0) makes this parameter obsolete
- **Impact**: v0.2 workflows now work correctly

## 🧹 Code Cleanup

### Removed Deprecated Code
- **Deleted**: `style_checker/parser.py` (157 lines of deprecated YAML parser)
- **Benefit**: Cleaner, more focused codebase
- **Impact**: Test coverage improved from 35% → 40%
- **Verification**: Zero imports remaining, all 23 tests passing

## 📚 Documentation Updates

### Comprehensive Audit & Updates
All documentation now accurately reflects v0.2.0 semantic grouping architecture:

- ✅ `docs/architecture.md` - Updated to document `parser_md.py` and semantic groups
- ✅ `docs/ci-cd-setup.md` - Updated test coverage statistics
- ✅ `docs/testing-quick-reference.md` - Current coverage summary
- ✅ `CONTRIBUTING.md` - Markdown database format examples
- ✅ `README.md` - All examples use `@v0.2`
- ✅ `examples/*.yml` - Updated workflow examples

## 📊 Improvements

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Test Coverage** | 35% | 40% | +5% ↑ |
| **Codebase Size** | 921 lines | 764 lines | -157 lines ↓ |
| **Deprecated Code** | 157 lines | 0 lines | ✅ Clean |
| **Tests Passing** | 23/23 | 23/23 | ✅ Stable |

## 🔄 Migration from v0.2.0

**No breaking changes!** Simply update your workflow:

```yaml
# Before
- uses: QuantEcon/action-style-guide@v0.2.0

# After  
- uses: QuantEcon/action-style-guide@v0.2.1
```

Or use the floating tag (automatically gets latest v0.2.x):
```yaml
- uses: QuantEcon/action-style-guide@v0.2
```

## ✅ Testing

- **All 23 tests passing** ✅
- **40% code coverage** (98% on parser_md.py)
- **No deprecation warnings** in GitHub Actions
- **No breaking changes**

## 🎯 What's Next

This maintenance release sets a solid foundation for v1.0.0:
- Clean, focused codebase
- Modern GitHub Actions patterns
- Comprehensive, accurate documentation
- Excellent test coverage on core modules

---

**Full Changelog**: https://github.com/QuantEcon/action-style-guide/compare/v0.2.0...v0.2.1
