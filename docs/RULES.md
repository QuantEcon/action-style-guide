# Style Guide Rules Reference

> Complete reference of all style rules checked by the action.
> This document is generated from the rule files in `style_checker/rules/`.

## Overview

The action checks **49 rules** across **8 categories**. Each rule has a type that determines how it's handled:

- **`rule`** (32 rules) - Actionable, automatically applied ✅
- **`style`** (13 rules) - Suggested, requires judgment 💡
- **`migrate`** (4 rules) - Code modernization patterns 🔄

## Actionable Rules (`rule`) - 32 rules ✅

**These rules are automatically applied by the action.**

| Code | Category | Title |
|------|----------|-------|
| **Writing (5 rules)** | | |
| `qe-writing-001` | Writing | Use one sentence per paragraph |
| `qe-writing-004` | Writing | Avoid unnecessary capitalization in narrative text |
| `qe-writing-005` | Writing | Use bold for definitions, italic for emphasis |
| `qe-writing-006` | Writing | Capitalize lecture titles properly |
| `qe-writing-008` | Writing | Remove excessive whitespace between words |
| **Mathematics (8 rules)** | | |
| `qe-math-001` | Mathematics | Prefer UTF-8 unicode for simple parameter mentions, be consistent |
| `qe-math-002` | Mathematics | Use \top for transpose notation |
| `qe-math-003` | Mathematics | Use square brackets for matrix notation |
| `qe-math-004` | Mathematics | Do not use bold face for matrices or vectors |
| `qe-math-005` | Mathematics | Use curly brackets for sequences |
| `qe-math-006` | Mathematics | Use aligned environment correctly for PDF compatibility |
| `qe-math-007` | Mathematics | Use automatic equation numbering, not manual tags |
| `qe-math-008` | Mathematics | Explain special notation (vectors/matrices) |
| **Code (3 rules)** | | |
| `qe-code-002` | Code | Use Unicode symbols for Greek letters in code |
| `qe-code-003` | Code | Package installation at lecture top |
| `qe-code-006` | Code | Binary packages require installation notes |
| **JAX (1 rule)** | | |
| `qe-jax-002` | JAX | Use NamedTuple for model parameters |
| **Figures (9 rules)** | | |
| `qe-fig-003` | Figures | No matplotlib embedded titles |
| `qe-fig-004` | Figures | Caption formatting conventions |
| `qe-fig-005` | Figures | Descriptive figure names for cross-referencing |
| `qe-fig-006` | Figures | Lowercase axis labels |
| `qe-fig-007` | Figures | Keep figure box and spines |
| `qe-fig-008` | Figures | Use lw=2 for line charts |
| `qe-fig-009` | Figures | Figure sizing |
| `qe-fig-010` | Figures | Plotly figures require latex directive |
| `qe-fig-011` | Figures | Use image directive when nested in other directives |
| **References (1 rule)** | | |
| `qe-ref-001` | References | Use correct citation style |
| **Links (1 rule)** | | |
| `qe-link-002` | Links | Use doc links for cross-series references |
| **Admonitions (4 rules)** | | |
| `qe-admon-001` | Admonitions | Use gated syntax for executable code in exercises |
| `qe-admon-003` | Admonitions | Use tick count management for nested directives |
| `qe-admon-004` | Admonitions | Use prf prefix for proof directives |
| `qe-admon-005` | Admonitions | Link solutions to exercises |

## Advisory Rules (`style`) - 13 rules 💡

**These rules are reported as suggestions requiring human judgment.**

| Code | Category | Title |
|------|----------|-------|
| **Writing (3 rules)** | | |
| `qe-writing-002` | Writing | Keep writing clear, concise, and valuable |
| `qe-writing-003` | Writing | Maintain logical flow |
| `qe-writing-007` | Writing | Use visual elements to enhance understanding |
| **Mathematics (1 rule)** | | |
| `qe-math-009` | Mathematics | Choose simplicity in mathematical notation |
| **Code (1 rule)** | | |
| `qe-code-001` | Code | Follow PEP8 unless closer to mathematical notation |
| **JAX (4 rules)** | | |
| `qe-jax-001` | JAX | Use functional programming patterns |
| `qe-jax-003` | JAX | Use generate_path for sequence generation |
| `qe-jax-005` | JAX | Use jax.lax for control flow |
| `qe-jax-007` | JAX | Use consistent function naming for updates |
| **Figures (2 rules)** | | |
| `qe-fig-001` | Figures | Do not set figure size unless necessary |
| `qe-fig-002` | Figures | Prefer code-generated figures |
| **Links (1 rule)** | | |
| `qe-link-001` | Links | Use markdown style links for lectures in same lecture series |
| **Admonitions (1 rule)** | | |
| `qe-admon-002` | Admonitions | Use dropdown class for solutions |

## Migration Rules (`migrate`) - 4 rules 🔄

**Legacy code patterns to modernize.**

| Code | Category | Title |
|------|----------|-------|
| **Code (2 rules)** | | |
| `qe-code-004` | Code | Use quantecon Timer context manager |
| `qe-code-005` | Code | Use quantecon timeit for benchmarking |
| **JAX (2 rules)** | | |
| `qe-jax-004` | JAX | Use functional update patterns |
| `qe-jax-006` | JAX | Explicit PRNG key management |

## Using Rules in Comments

You can specify which categories to check when triggering the action:

```markdown
@qe-style-checker lecture_name writing,math
@qe-style-checker *.md code,jax
@qe-style-checker intro.md figures
```

Available categories: `writing`, `math`, `code`, `jax`, `figures`, `references`, `links`, `admonitions`

## Rule Details

For complete rule details including examples and implementation notes, see:
- **Individual rule files**: `style_checker/rules/*.md`

Each rule includes:
- ✅ Correct examples
- ❌ Incorrect examples
- Implementation guidance
- Special cases and exceptions
