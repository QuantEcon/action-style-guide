---
title: Rules Reference
---

# Rules Reference

Complete reference of all 49 style rules checked by the action. Rules are defined in `style_checker/rules/` and are read directly by the LLM — no code changes needed to add or modify rules.

## Overview

| Type | Count | Behavior |
|------|-------|----------|
| **`rule`** — Actionable ✅ | 32 | Automatically applied |
| **`style`** — Advisory 💡 | 13 | Reported as suggestions |
| **`migrate`** — Modernization 🔄 | 4 | Reported as suggestions |

## Actionable Rules (`rule`) — 32 rules ✅

These rules are automatically applied by the action.

### Writing (5 rules)

| Code | Title |
|------|-------|
| `qe-writing-001` | Use one sentence per paragraph |
| `qe-writing-004` | Avoid unnecessary capitalization in narrative text |
| `qe-writing-005` | Use bold for definitions, italic for emphasis |
| `qe-writing-006` | Capitalize lecture titles properly |
| `qe-writing-008` | Remove excessive whitespace between words |

### Mathematics (8 rules)

| Code | Title |
|------|-------|
| `qe-math-001` | Prefer UTF-8 unicode for simple parameter mentions, be consistent |
| `qe-math-002` | Use `\top` for transpose notation |
| `qe-math-003` | Use square brackets for matrix notation |
| `qe-math-004` | Do not use bold face for matrices or vectors |
| `qe-math-005` | Use curly brackets for sequences |
| `qe-math-006` | Use aligned environment correctly for PDF compatibility |
| `qe-math-007` | Use automatic equation numbering, not manual tags |
| `qe-math-008` | Explain special notation (vectors/matrices) |

### Code (3 rules)

| Code | Title |
|------|-------|
| `qe-code-002` | Use Unicode symbols for Greek letters in code |
| `qe-code-003` | Package installation at lecture top |
| `qe-code-006` | Binary packages require installation notes |

### JAX (1 rule)

| Code | Title |
|------|-------|
| `qe-jax-002` | Use NamedTuple for model parameters |

### Figures (9 rules)

| Code | Title |
|------|-------|
| `qe-fig-003` | No matplotlib embedded titles |
| `qe-fig-004` | Caption formatting conventions |
| `qe-fig-005` | Descriptive figure names for cross-referencing |
| `qe-fig-006` | Lowercase axis labels |
| `qe-fig-007` | Keep figure box and spines |
| `qe-fig-008` | Use `lw=2` for line charts |
| `qe-fig-009` | Figure sizing |
| `qe-fig-010` | Plotly figures require latex directive |
| `qe-fig-011` | Use image directive when nested in other directives |

### References (1 rule)

| Code | Title |
|------|-------|
| `qe-ref-001` | Use correct citation style |

### Links (1 rule)

| Code | Title |
|------|-------|
| `qe-link-002` | Use doc links for cross-series references |

### Admonitions (4 rules)

| Code | Title |
|------|-------|
| `qe-admon-001` | Use gated syntax for executable code in exercises |
| `qe-admon-003` | Use tick count management for nested directives |
| `qe-admon-004` | Use `prf` prefix for proof directives |
| `qe-admon-005` | Link solutions to exercises |

## Advisory Rules (`style`) — 13 rules 💡

These rules are reported as suggestions requiring human judgment.

### Writing (3 rules)

| Code | Title |
|------|-------|
| `qe-writing-002` | Keep writing clear, concise, and valuable |
| `qe-writing-003` | Maintain logical flow |
| `qe-writing-007` | Use visual elements to enhance understanding |

### Mathematics (1 rule)

| Code | Title |
|------|-------|
| `qe-math-009` | Choose simplicity in mathematical notation |

### Code (1 rule)

| Code | Title |
|------|-------|
| `qe-code-001` | Follow PEP8 unless closer to mathematical notation |

### JAX (4 rules)

| Code | Title |
|------|-------|
| `qe-jax-001` | Use functional programming patterns |
| `qe-jax-003` | Use `generate_path` for sequence generation |
| `qe-jax-005` | Use `jax.lax` for control flow |
| `qe-jax-007` | Use consistent function naming for updates |

### Figures (2 rules)

| Code | Title |
|------|-------|
| `qe-fig-001` | Do not set figure size unless necessary |
| `qe-fig-002` | Prefer code-generated figures |

### Links (1 rule)

| Code | Title |
|------|-------|
| `qe-link-001` | Use markdown style links for lectures in same lecture series |

### Admonitions (1 rule)

| Code | Title |
|------|-------|
| `qe-admon-002` | Use dropdown class for solutions |

## Migration Rules (`migrate`) — 4 rules 🔄

Legacy code patterns to modernize.

### Code (2 rules)

| Code | Title |
|------|-------|
| `qe-code-004` | Use `quantecon.Timer` context manager |
| `qe-code-005` | Use `quantecon.timeit` for benchmarking |

### JAX (2 rules)

| Code | Title |
|------|-------|
| `qe-jax-004` | Use functional update patterns |
| `qe-jax-006` | Explicit PRNG key management |

## Rule Definitions

Full rule definitions with examples are in `style_checker/rules/`:

- [writing-rules.md](https://github.com/QuantEcon/action-style-guide/blob/main/style_checker/rules/writing-rules.md)
- [math-rules.md](https://github.com/QuantEcon/action-style-guide/blob/main/style_checker/rules/math-rules.md)
- [code-rules.md](https://github.com/QuantEcon/action-style-guide/blob/main/style_checker/rules/code-rules.md)
- [jax-rules.md](https://github.com/QuantEcon/action-style-guide/blob/main/style_checker/rules/jax-rules.md)
- [figures-rules.md](https://github.com/QuantEcon/action-style-guide/blob/main/style_checker/rules/figures-rules.md)
- [references-rules.md](https://github.com/QuantEcon/action-style-guide/blob/main/style_checker/rules/references-rules.md)
- [links-rules.md](https://github.com/QuantEcon/action-style-guide/blob/main/style_checker/rules/links-rules.md)
- [admonitions-rules.md](https://github.com/QuantEcon/action-style-guide/blob/main/style_checker/rules/admonitions-rules.md)
