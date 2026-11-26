# Deterministic style-check prototype: results (2026-11-26)

> Evidence appendix for [`ARCHITECTURE-REVIEW.md`](../ARCHITECTURE-REVIEW.md) §5. The prototype scripts were throwaway code
> in an ephemeral scratch environment and are not committed; file names below are kept for reference.

Prototype: `markdown-it-py 4.3.0` + `mdit-py-plugins 0.7.0` (front_matter, myst_blocks, myst_role, dollarmath, amsmath, colon_fence, footnote), with directive bodies re-parsed recursively as MyST does, plus Python `ast` for code cells. No LLM calls. Total code is about 700 lines of Python, written in about 2 hours.

Inputs:
- Corpus: `QuantEcon/lecture-python.myst` → `lectures/*.md` (161 files, shallow clone of `main`).
- Seeded lecture: `QuantEcon/test-action-style-guide` → `lectures/markov_chains_jax.md` (+ `markov_chains_jax.annotated.md`).

Prototype files (not committed):
- `myst.py`: region classifier. It produces prose (with code, math and roles masked), math regions, code cells with tags, directives with context, and links.
- `checks.py`: all rule checks. Each hit carries a `sub` category that separates likely true positives from known traps.
- `run.py`: runs over the corpus and records timing.
- `fix008.py`: in-memory autofix for writing-008, with verification.
- `bold_collide.py`: measures bold/plain symbol collisions.
- `sample.py` and `show001.py`: spot-check helpers.
- Raw hits: `out/corpus.jsonl` (7,703 rows), `out/seeded.jsonl`, `out/testlect.jsonl`.
- Summaries: `out/corpus_summary.txt` and `out/seeded_summary.txt`.

## Runtime and corpus size

| | value |
|---|---|
| Parse all 161 lectures (markdown-it plus recursive directive parse) | 2.0 s |
| Proper-noun lexicon built from corpus prose | 0.3 s |
| All checks (16 rules) | 5.0 s. code-002 AST analysis takes 2.0 s and figures 1.3 s; nothing is optimised. |
| **Total, single core** | **7.3 s for 161 lectures (about 45 ms per lecture)** |

The size statistics below come from Python `len()` on the decoded text. The token estimate is chars / 3.5. That divisor is probably low for math-heavy LaTeX, so the real token counts are likely higher.

| | min | median | p90 | max | total |
|---|---|---|---|---|---|
| chars | 229 | 34,868 | 77,576 | 121,283 | 6.69 M |
| tokens (≈) | 65 | 9,962 | 22,165 | 34,652 | 1.91 M |

The minimum comes from four stub pages: `zreferences.md`, `intro.md`, `status.md` and `troubleshooting.md`. Without them, the smallest real lecture is `cross_product_trick.md`, at about 5.8 k chars (about 1.65 k tokens).

## Per-rule results

"Precision" means spot-check precision against the rule **as written**. Where the rule's intent is doubtful, I also give a second number.

| rule | hits / lectures | est. precision (spot-checked n) | detect deterministic? | autofix safe? | key trap |
|---|---|---|---|---|---|
| writing-008 multi-space | 1,927 runs on 1,369 lines / 86 | **~100%** (27/27) | yes | **yes, verified** (see below) | Must skip code/math/roles; trailing double space is a Markdown hard break; 8 residual runs sit next to multi-line inline math |
| writing-001 one sentence/para | 739 / 115 | Boundary detection about 96% (55/57). Clear violations about 30% (8/25) | yes, for boundaries | Only for top-level, non-label hits (192 hits / 55 lectures) | 317 list-item hits (exercise steps), 146 run-in labels ("Part 2.", "**Theorem.**"), 41 blockquote (quoted sources) |
| writing-006 headings | 507 / 124 | Title-case sections: ~95% (35/36). Titles: 3 strict hits, 1 FP | yes, given a proper-noun lexicon | Lowercasing is mechanical given the lexicon; multi-word names need a list | 132/487 naive section hits (27%) contain only proper nouns; 33 more mix proper nouns |
| math-002 `^T` | 157 / 29 | **0% (0/157: every hit reviewed)** | yes | **NO** | `^T` is a horizon/history/power/limit: `\beta^T`, `H^T`, `\sum_{t=0}^T`, `Q^T`, `\mathbb{R}^T` |
| math-002 `^\prime` | 60 / 9 | ~58% (7/12) | yes | **NO** | ′ also marks derivatives (`f^\prime`) and next-period/posterior values (`\pi^\prime`) |
| math-003 pmatrix/Bmatrix | 51 pmatrix / 9 (Bmatrix 0, vmatrix 0) | ~100% | yes | **yes** (`pmatrix`→`bmatrix`) | Misses `\left(\begin{array}` / `\left(\begin{matrix}` (≥13 hits in 3 lectures). `\left[\begin{matrix}` (71) is brackets but not bmatrix: does the rule want it flagged? |
| math-004 bold | 630 / 37 | 100% are bold. Removing bold is wrong for ≥161 of them | yes | Only `\mathbf{1}`→`\mathbb{1}` | 123 `\mathbf{1}` (ones vector, math-008), 38 `\mathbf{0}`. In 27 of 40 (lecture, symbol) pairs, the plain symbol also appears in that lecture, e.g. bold random vector X vs scalar X |
| math-006 align in `$$` | 0 / 0 (8 top-level amsmath envs, which are valid) | n/a | yes, trivial | n/a | Top-level `\begin{align*}` is legal because the amsmath extension is on |
| math-007 `\tag` | 0 / 0 (grep confirms) | n/a | yes, trivial | No: needs a label name plus updating "(1)" references | none |
| code-002 Greek names | 1,998 naive token hits / 136 | User-defined: 987 hits / 49 lectures / 188 distinct names. **Library API: 837 (42%)**. Unknown: 174 (mostly `rng.beta`) | yes (AST) | Only a scope-aware cross-cell rename of user names, plus prose backticks | `alpha=` (499), `np.pi` (140), `scipy.stats.beta`, `rng.beta()`, **`qe.LQ(..., beta=β)`**, `LinearStateSpace(mu_0=, Sigma_0=)`. 7 renames would collide with an existing unicode twin |
| code-003 pip install | 76 install cells / 73. Violations: 3 | Rule-intent: 0/3 | yes | yes (add tag) | All 3 "missing hide-output" cells are `!pip install jax` tagged `skip-execution`, so there is no output to hide. All install cells are at the top. No lecture imports quantecon without installing it |
| code-004 timing | 49 / 14: `time.time` 20 (3), `perf_counter` 4 (1), `%time` 12 (4), `%%time` 13 (6), tic/toc 0 | ~100% as patterns | yes | **NO** | Elapsed values feed later computations (speed-up ratios, `minutes=`). `%time`/`%%time` are not named in the rule |
| code-005 timeit | 2 `%%timeit` / 1 | 100% | yes | NO (a multi-statement cell needs a wrapper function) | none |
| fig-003 titles | 396 / 96: 69 in exercises (allowed), **250 per-panel subplot titles**, 76 single-figure titles | single-figure titles ~100% (12/12) | yes | NO | A caption cannot replace per-panel titles; many titles are dynamic f-strings |
| fig-006 axis labels | 118 / 30 (93 after filtering) | ~100% after filtering (10/10, 10/12 before) | yes | yes, lowercase the first letter after filtering | Excluded: acronyms (KL, US, AIME), proper nouns (Gini, Pareto, Chernoff), single-letter variables (`'K'`, `'Z = X + Y'`) |
| fig-007 spines | 10 / 3 (plus 3 `axis('off')` diagrams excluded) | 10/10 as written; 2 are justified (centred math-style axes) | yes | Mostly; judgment for "specific reason" | `sns.despine()`; `multivariate_normal.md:387-390` |
| fig-008 lw=2 | 758 / 119: 407 no-lw line, 220 lw≠2 constant, 57 marker-only (excluded), 16 alpha bundles, 13 pandas | ~92% as written (11/12) | yes | **NO** (visual design) | Thin reference/45° lines (54 hits), transparent path bundles, marker-only plots, pandas `.plot()` |
| link-002 cross-series URL | 22 / 15 (plus link-001 same-series 10 / 6) | 100% | yes | 18/22 mechanical; 4 carry `#anchor` | `{doc}` cannot express anchors, and target pages cannot be verified without objects.inv |
| admon-002 dropdown | 0 / 0 (413/413 solutions have dropdown) | n/a | yes | yes | none |
| admon-004 prf: | 0 / 0 | n/a | yes | yes | none |
| admon-005 sol→ex label | 0 / 0 (all labels resolve within the file) | n/a | yes | n/a | Labels in other files are not handled |

### writing-008: autofix verification

`fix008.py` collapses runs of spaces on every flagged line. Before doing so, it shields inline code, `$…$`, roles, HTML and link targets with placeholders. It then re-parses the file and compares the content of every code cell, math region and directive.

Result: 1,369 lines fixed in 86 lectures. **0 files changed any code, math or directive content.** 8 of 1,927 runs (0.4%) were left alone because they sit next to inline math that spans lines; a token-offset fixer would handle them.

### writing-001: what the hits are (739)

Lecture counts below do not add up to 115, because one lecture can have hits in several categories.

| category | hits | lectures | verdict |
|---|---|---|---|
| top-level prose | 192 | 55 | real violations (~96% correct boundaries) |
| list items | 317 | 70 | mostly exercise instructions ("Set x. Simulate y."). The rule does not say whether these count |
| run-in label first ("Part 2.", "Step 1.", "**Theorem.**", "Proof idea.") | 146 | — | the boundary is correct, but splitting is probably unwanted |
| directive bodies (exercise, note, prf:*) | 43 | — | theorem statements split badly |
| blockquotes | 41 | 15 | quoted literature. **Must not be edited** (`wald_friedman.md:269`, a Wald quote with 9 "sentences") |

Boundary failures seen: an enumerator label (`gallant_tauchen.md:965` "a. Show that"). I fixed "2. and 3. Numerically" (`long_run_risk_operator.md:3085`) after seeing it. The abbreviation list covers e.g., i.e., etc., cf., Fig., Eq., initials and similar.

### writing-006: how much needs a proper-noun list

A naive check flags any capitalised word after the first, excluding acronyms, CamelCase and single letters. That flags **487 section headings**:
- **132 (27%)** are correct headings whose only capitals are proper nouns, e.g. `### The Bellman equations`, `## Classifier systems for the Kiyotaki-Wright environment`. Without a lexicon, these are false positives.
- **33 of the remaining 344** title-case hits mix in proper nouns (`### Value Function and Euler Equation`). The fix must keep those capitalised.
- Overall, **about 34% of naive hits need a proper-noun list**.

I built the lexicon automatically: a word counts as a proper noun if it is capitalised mid-sentence in at least 80% of its uses in corpus prose, with at least 3 uses. That gives 336 words with little noise.

Remaining false positives are multi-word names or names of things:
- `phillips_drifts_volatilities_2.md:614` `## Volatility after the Great Moderation`
- `opt_transport.md:688` `## The Python Optimal Transport Package`
- `phillips_two_stories.md:331` `### The Critique` (the Lucas Critique)

Policy questions the rule does not answer:
- 11 hits (6 lectures) capitalise only after a colon (`## Example 1: Ordinary linear ...`). Is that allowed?
- Titles: only 3 hits are strict violations, and 1 of those is a false positive: `optimal_growth_uncertainty.md:22` `# ... and Tobin's q` (q is a variable). Another 17 titles depend only on the preposition convention (`# Intermediate Quantitative Economics with Python`).

### math-002: verbatim `^T` traps (none of the 157 `^T` hits is a transpose)

- `lqcontrol.md:303` `... + \beta^T x_T^\top R_f x_T`: a power, sitting next to a correct `^\top`.
- `phillips_drifts_volatilities.md:595` `$H^T$`: "the volatility paths $H^T$", a history. The same lecture writes transposes as `v_t^\top`.
- `ge_arrow.md:695` `I + Q + Q^2 + \cdots + Q^T`: a matrix power.
- `likelihood_ratio_process.md:2057` `Q_\phi^T = \lambda(\phi)^T (...)`: powers.
- `imp_sample.md:341` `L(\omega^T) = \prod_{t=1}^T ...`: a history plus a limit.
- `turbulence_inference.md:1148` `\mathbb{R}^T`: a space.
- 83 limits (`\sum_{t=0}^T`, `\{x_t\}_{t=0}^T`, `\int_0^T`).

The corpus already uses `^\top` 1,576 times. A blind `^T`→`^\top` autofix would corrupt 119 lines in 29 lectures.

`^\prime` is mixed:
- transposes: `lagrangian_lqdp.md:173` (`B^\prime \mu_{t+1}`), `two_computation.md:410`
- not transposes: `navy_captain.md:698` (`\pi^{\prime}` is the posterior), `cass_koopmans_1.md:977` (`f^{\prime}` is a derivative), `mccall_q.md:304`

Bare `'` transposes (`cross_product_trick.md:84` `H'Q^{-1} H`) were **not attempted**. They cannot be told apart from `k'` and `f'(x)` without semantics.

### math-004: verbatim trap

`lln_clt.md:536` `\mathbb P\{\mathbf X_1 \leq \mathbf x_1,\ldots\}`: bold marks random vectors, and the plain `X`, `x` are scalars in the same lecture. 27 of 40 (lecture, bold-symbol) pairs have this collision risk.

### code-002: verbatim traps (must NOT be renamed)

- `lagrangian_lqdp.md:476` `lq = LQ(Q, R, A, B, beta=β)`. QuantEcon's own API requires `beta=`. So does `markov_perf.md:455` `qe.LQ(Q1, R1, Λ1, B1, beta=beta)`, where only the value can change.
- `kalman_2.md:511` `mu_0=μ_sim_0, Sigma_0=Σ_sim_0`: `LinearStateSpace` keyword arguments.
- `imp_sample.md:816` `rng.beta(2, 5, n)`; `exchangeable.md:1255` `from scipy.stats import beta as beta_dist`.
- 499 matplotlib `alpha=` keyword arguments.

Rename collisions: the unicode twin already exists in `ge_arrow.md` (mu), `markov_perf.md` (beta), `misspecified_recovery.md` (alpha), `os_egm.md`, `os_egm_jax.md` and `robust_permanent_income.md` (mu), and `ross_recovery.md` (rho).

The corpus convention already favours unicode: 151 of 161 lectures use Greek-letter identifiers.

### Figures: verbatim traps

- `kalman_2.md:467` `ax[1].set_title('Inferred work ethic over time')`: a per-panel title. A figure caption cannot replace it.
- `perm_income_cons.md:566` `ax[0].plot(ysim.T, alpha=.1, color="g")`: a bundle of sample paths. `lw=2` would make it a blob.
- `newton_method.md:184` `ax.plot(k_grid, k_grid, "k--", lw=1, alpha=0.7, label="45")`: a 45° reference line.

## Seeded lecture (`markov_chains_jax.md`) vs. catalogue

**Warning:** the catalogue's line numbers are stale, offset by between +3 and +74 lines. For example, W1 is listed at 16 but sits at 19; L3 is listed at 226 but sits at 383. I matched entries by content.

| catalogue item | rule | caught? | note |
|---|---|---|---|
| W1+W2 (same paragraph, l.19) | writing-001 | ✅ | |
| W3 (l.90) | writing-001 | ✅ | |
| W11 `## A Larger Economic Model` (l.373) | writing-006 | ✅ | |
| W12 double space (l.90) | writing-008 | ❌, correctly | **The double space is not in the file.** grep finds none. The ground truth is wrong |
| M1 pmatrix (l.84) | math-003 | ✅ | |
| M2 `\mathbf` (l.413-419) | math-004 | ✅ (7 hits) | |
| M3 `\mathbf{L}^T` (l.416) | math-002 | ✅ | |
| M4 `\tag{1}` (l.170) | math-007 | ✅ | |
| C1 alpha/beta (l.95-96) | code-002 | ✅ | `alpha=0.3` in `ax.axhline` (l.237) is correctly classed as library |
| C2 pip without hide-output (l.33) | code-003 | ✅ | |
| C3, C4 `time.time()` (l.153-155, 330-332) | code-004 | ✅ ✅ | |
| C5 `%timeit` (l.512) | code-005 | ✅ | |
| C6/F1 `set_title` (l.219) | fig-003 | ✅ | |
| F3 axis labels (l.220-221) | fig-006 | ✅ | |
| F4 missing lw (l.~109) | fig-008 | ❌, correctly | **Phantom.** The only `.plot(` call (l.232) has `lw=2` |
| L2 python.quantecon.org URL (l.381) | link-001 | ✅ | The catalogue says "use `{doc}`", but link-001 says use `[](doc)` for same-series links |
| L3 intro.quantecon.org URL (l.383) | link-002 | ✅ | |
| A1 / FP8 dropdown controls | admon-002 | ✅ no false positive | |
| FP3 no align / FP9 `{doc}` controls | math-006 / link-002 | ✅ no false positive | |

Recall: **18/18** catalogued items for implemented rules that actually exist in the file. Two further items (W12, F4) do not exist.

The rules as written also find **true violations that the catalogue leaves out**. An LLM that finds them would be scored as false positives:
- 10 more Title-Case section headings (`## Definitions and Setup`, `### Stochastic Matrices`, `### The Power Method`, …).
- 4 more multi-sentence paragraphs: l.205 "… This is a powerful result.", l.255, l.377, and l.489 (in an exercise).
- `$P^T$` at l.423, a real transpose.
- `psi`, `psi_0`, `psi_star` and similar under code-002 (about 90 hits).

`test-lecture-clean.md`, the fixture that "should pass all checks", breaks the rules as written:
- 5 multi-sentence paragraphs
- 4 title-case `##` headings
- `alpha = 0.5`, `beta = 0.95`
- `ax.set_title('Utility Function')`
- `ax.set_xlabel('State $x$')`

Other catalogue doubts:
- A3 (admon-001): the `{exercise}` holds no code; only its gated solution does.
- A4 (admon-003): 4 backticks with nothing nested is harmless.

## Rule text that looks inconsistent once real usage is seen

1. **writing-008 vs writing-006.** The "correct" example in writing-008 is `## Section Heading With Extra Spaces`, which is Title Case for a `##` heading and so violates writing-006.
2. **writing-004.** The "correct" example `The bellman equation is a fundamental tool.` lowercases a proper noun; writing-008 repeats it. "Bellman" is capitalised in at least 80% of corpus uses.
3. **link-002 examples.**
   - `{doc}\`intro:linear_equations.html#solving-systems\`` is invalid: `{doc}` takes a docname, not `.html` with an anchor.
   - `{doc}\`intermediate:kalman\``: this repo's `_config.yml` intersphinx has no `intermediate` key (only intro, advanced, jax, programming), and from inside the intermediate series it would be a link-001 case anyway.
4. **math-002** names `'`/`^\prime` as transpose markers with no guidance. In economics these mostly mean derivative or next period, and `^T` here always meant horizon, history or power.
5. **math-004 vs math-008.** "Remove bold" applied to `\mathbf{1}` gives the scalar 1. The rules should cross-reference: 123 hits in 23 lectures.
6. **fig-003** has no exception for per-panel subplot titles, which are 250 of the 327 non-exercise hits.
7. **fig-008** "values other than 2" conflicts with thin reference lines and transparent path bundles, which are used across 119 lectures.
8. **code-002** has no carve-out for library keyword arguments or attributes, including QuantEcon's own `qe.LQ(beta=)`.
9. **code-003** requires `hide-output`; the corpus's JAX install cells use `skip-execution`.
10. **code-004 / code-005** do not mention `%time` / `%%time` (25 uses in 10 lectures). Are they allowed?
11. **writing-001** is silent on list items, blockquotes, theorem statements and run-in labels. These make up 74% of the hits.
12. **writing-006** is silent on capitals after a colon, and on the minor-word convention for titles ("with").

## Not measured / limitations

- Bare `'` transposes in math: not attempted.
- `\left(\begin{array}` matrices across line breaks: only a same-line grep (13).
- Link target existence: needs network access to objects.inv.
- admon-005 across files: not handled.
- The writing-001 parser lacks the deflist plugin. Definition lists, which the corpus has enabled, would parse as paragraphs; I saw no effect in the samples.
- Precision figures are small-sample spot checks (5–27 per category) read by me, not a labelled set.
- The math-002 `^T` result (0/157) is exhaustive: I reviewed every non-limit line, and the 83 limits are self-evident.
