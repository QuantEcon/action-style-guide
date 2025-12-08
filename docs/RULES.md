# Style Guide Rules Reference

> Complete reference of all style rules checked by the action

## Overview

The action checks **48 rules** across **8 categories**. Each rule has a type that determines how it's handled:

- **`rule`** (31 rules) - Actionable, automatically applied ✅
- **`style`** (13 rules) - Suggested, requires judgment 💡
- **`migrate`** (4 rules) - Code modernization patterns 🔄

## Actionable Rules (`rule`) - 31 rules ✅

**These rules are automatically applied by the action.**

| Code | Category | Title | Description |
|------|----------|-------|-------------|
| **Writing (3 rules)** | | | |
| `qe-writing-001` | Writing | One sentence per paragraph | Each paragraph should contain only one sentence |
| `qe-writing-004` | Writing | Avoid unnecessary capitalization | Don't capitalize common nouns in narrative text |
| `qe-writing-005` | Writing | Use bold for emphasis, italic for terms | Reserve bold for emphasis, italic for technical terms |
| **Mathematics (7 rules)** | | | |
| `qe-math-001` | Mathematics | Use \top for transpose | Use `A^\top` instead of `A'` for matrix transpose |
| `qe-math-002` | Mathematics | Use square brackets for matrices | Enclose matrices in `\begin{bmatrix}...\end{bmatrix}` |
| `qe-math-004` | Mathematics | Use curly braces for sequences | Write sequences as `\{x_n\}` not `(x_n)` |
| `qe-math-006` | Mathematics | Use standard function names | Use `\log`, `\max`, `\min` with backslash |
| `qe-math-007` | Mathematics | Use \mathbb for number sets | Write `\mathbb{R}`, `\mathbb{N}` for real/natural numbers |
| `qe-math-008` | Mathematics | Align multi-line equations | Use `aligned` environment within equation blocks |
| `qe-math-009` | Mathematics | Use proper spacing in equations | Add `\,` for spacing, `\quad` for larger gaps |
| **Code (3 rules)** | | | |
| `qe-code-001` | Code | Use Unicode Greek letters | Use `α`, `β`, `γ` instead of `alpha`, `beta`, `gamma` |
| `qe-code-002` | Code | Place package installation before imports | Put `pip install` cells before code that uses packages |
| `qe-code-006` | Code | Import quantecon as qe | Use `import quantecon as qe` convention |
| **JAX (3 rules)** | | | |
| `qe-jax-001` | JAX | Use functional updates for arrays | Use `.at[].set()` instead of in-place modifications |
| `qe-jax-003` | JAX | Use explicit PRNG key management | Pass JAX PRNG keys explicitly, use `jax.random.split()` |
| `qe-jax-007` | JAX | Use jax.jit decorator correctly | Apply `@jax.jit` to pure functions only |
| **Figures (9 rules)** | | | |
| `qe-fig-001` | Figures | Include caption with every figure | Every figure must have a caption using `:caption:` |
| `qe-fig-002` | Figures | Use descriptive figure names | Name figures descriptively: `consumption_path.png` not `fig1.png` |
| `qe-fig-003` | Figures | Caption format: sentence case, no period | Captions in sentence case, no trailing period |
| `qe-fig-004` | Figures | Add alt text for accessibility | Include `:alt:` text for screen readers |
| `qe-fig-005` | Figures | Label axes in plots | All plots must have x-axis and y-axis labels |
| `qe-fig-006` | Figures | Use consistent line widths | Set `linewidth=2` for main plots |
| `qe-fig-007` | Figures | Include figure labels for cross-references | Add `:name:` for figures referenced in text |
| `qe-fig-009` | Figures | Use grid for complex plots | Add `plt.grid(alpha=0.3)` for plots with many data points |
| `qe-fig-010` | Figures | Include legends for multi-line plots | Add legend when plotting multiple series |
| `qe-fig-011` | Figures | Use clear, readable fonts | Set appropriate font sizes for labels and titles |
| **References (1 rule)** | | | |
| `qe-ref-001` | References | Use proper citation syntax | Use `{cite}` for parenthetical, `{cite:t}` for textual citations |
| **Links (2 rules)** | | | |
| `qe-link-001` | Links | Use internal links within series | Use `{doc}` for same-series links, full URLs for cross-series |
| `qe-link-002` | Links | Link to canonical documentation | Link to official docs for external libraries |
| **Admonitions (5 rules)** | | | |
| `qe-admon-001` | Admonitions | Use exercise-start/end pairs | Exercises must use `{exercise-start}` and `{exercise-end}` |
| `qe-admon-002` | Admonitions | Link solutions to exercises | Solutions must reference exercise label with `:label:` |
| `qe-admon-003` | Admonitions | Use dropdown class for solutions | Add `:class: dropdown` to solution blocks |
| `qe-admon-004` | Admonitions | Match tick counts for nested directives | Use 4 backticks when nesting 3-backtick code blocks |
| `qe-admon-005` | Admonitions | Use appropriate admonition types | Choose note/warning/tip based on content importance |

## Advisory Rules (`style`) - 13 rules 💡

**These rules are reported as suggestions requiring human judgment.**

| Code | Category | Title | Description |
|------|----------|-------|-------------|
| **Writing (4 rules)** | | | |
| `qe-writing-002` | Writing | Keep writing clear and concise | Minimize unnecessary words, keep sentences short |
| `qe-writing-003` | Writing | Maintain logical flow | Ensure good logical flow with no abrupt jumps |
| `qe-writing-006` | Writing | Identify opportunities for visual elements | Suggest figures, diagrams when beneficial |
| `qe-writing-007` | Writing | Use MyST admonitions appropriately | Recommend note/warning/tip boxes for key content |
| **Mathematics (2 rules)** | | | |
| `qe-math-003` | Mathematics | Explain notation clearly | Define symbols when first introduced |
| `qe-math-005` | Mathematics | Use appropriate math mode | Choose inline vs display math based on complexity |
| **Code (1 rule)** | | | |
| `qe-code-003` | Code | Add explanatory comments | Include comments for complex operations |
| **JAX (2 rules)** | | | |
| `qe-jax-002` | JAX | Use NamedTuple for parameters | Define model parameters as NamedTuple classes |
| `qe-jax-005` | JAX | Use jax.vmap for vectorization | Apply `jax.vmap` for batch operations instead of loops |
| **Figures (1 rule)** | | | |
| `qe-fig-008` | Figures | Use appropriate figure size | Choose figure size based on content complexity |

## Migration Rules (`migrate`) - 4 rules 🔄

**Legacy code patterns to modernize.**

| Code | Category | Title | Description |
|------|----------|-------|-------------|
| **Code (2 rules)** | | | |
| `qe-code-004` | Code | Use quantecon.Timer() | Replace `tic()`, `toc()` with `qe.Timer()` context manager |
| `qe-code-005` | Code | Use quantecon.timeit() | Replace `%timeit` magic with `qe.timeit()` function |
| **JAX (2 rules)** | | | |
| `qe-jax-004` | JAX | Update to jax.random namespace | Use `jax.random.*` instead of deprecated `jax.random.PRNGKey` patterns |
| `qe-jax-006` | JAX | Modernize JAX imports | Use current JAX import conventions |

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
- **Source database**: `tool-style-guide-development/style-guide-database.md`

Each rule includes:
- ✅ Correct examples
- ❌ Incorrect examples
- Implementation guidance
- Special cases and exceptions
