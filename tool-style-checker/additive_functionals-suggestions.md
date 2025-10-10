
================================================================================
WRITING CATEGORY REVIEW
================================================================================

# Writing Style Review for additive_functionals.md

## Summary
- Total writing violations: 15 issues found
- Critical issues: 12 issues require attention

## Critical Writing Issues

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 45-47 / Section "Overview"
**Current**: "Many economic time series display persistent growth that prevents them from being  asymptotically stationary and ergodic. For example, outputs, prices, and dividends typically display  irregular but persistent growth."
**Issue**: Multiple sentences in one paragraph
**Fix**: Split into separate paragraphs:
"Many economic time series display persistent growth that prevents them from being asymptotically stationary and ergodic.

For example, outputs, prices, and dividends typically display irregular but persistent growth."

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 49-51 / Section "Overview"
**Current**: "Asymptotic stationarity and ergodicity are key assumptions needed to make it possible to learn by applying statistical methods. But  there are good ways to model time series that have persistent growth that still enable statistical learning based on a law of large numbers for an asymptotically stationary and ergodic process."
**Issue**: Multiple sentences in one paragraph
**Fix**: Split into separate paragraphs:
"Asymptotic stationarity and ergodicity are key assumptions needed to make it possible to learn by applying statistical methods.

But there are good ways to model time series that have persistent growth that still enable statistical learning based on a law of large numbers for an asymptotically stationary and ergodic process."

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 53-55 / Section "Overview"
**Current**: "Thus, {cite}`Hansen_2012_Eca`  described  two classes of time series models that accommodate growth. They are"
**Issue**: Multiple sentences in one paragraph
**Fix**: Split into separate paragraphs:
"Thus, {cite}`Hansen_2012_Eca` described two classes of time series models that accommodate growth.

They are"

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 60-62 / Section "Overview"
**Current**: "These two classes of processes are closely connected. If a process $\{y_t\}$ is an additive functional and $\phi_t = \exp(y_t)$, then $\{\phi_t\}$ is a multiplicative functional."
**Issue**: Multiple sentences in one paragraph
**Fix**: Split into separate paragraphs:
"These two classes of processes are closely connected.

If a process $\{y_t\}$ is an additive functional and $\phi_t = \exp(y_t)$, then $\{\phi_t\}$ is a multiplicative functional."

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 64-66 / Section "Overview"
**Current**: "In this lecture, we describe both  additive functionals and multiplicative functionals. We also describe and compute decompositions of additive and multiplicative processes into four components:"
**Issue**: Multiple sentences in one paragraph
**Fix**: Split into separate paragraphs:
"In this lecture, we describe both additive functionals and multiplicative functionals.

We also describe and compute decompositions of additive and multiplicative processes into four components:"

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 73-75 / Section "Overview"
**Current**: "We describe how to construct,  simulate,  and interpret these components. More details about  these concepts and algorithms  can be found in Hansen  {cite}`Hansen_2012_Eca` and Hansen and Sargent {cite}`Hans_Sarg_book`."
**Issue**: Multiple sentences in one paragraph
**Fix**: Split into separate paragraphs:
"We describe how to construct, simulate, and interpret these components.

More details about these concepts and algorithms can be found in Hansen {cite}`Hansen_2012_Eca` and Hansen and Sargent {cite}`Hans_Sarg_book`."

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 86-88 / Section "A particular additive functional"
**Current**: "{cite}`Hansen_2012_Eca` describes a general class of additive functionals. This lecture focuses on a subclass of these: a scalar process $\{y_t\}_{t=0}^\infty$ whose increments are driven by a Gaussian vector autoregression."
**Issue**: Multiple sentences in one paragraph
**Fix**: Split into separate paragraphs:
"{cite}`Hansen_2012_Eca` describes a general class of additive functionals.

This lecture focuses on a subclass of these: a scalar process $\{y_t\}_{t=0}^\infty$ whose increments are driven by a Gaussian vector autoregression."

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 90-92 / Section "A particular additive functional"
**Current**: "Our special additive functional displays interesting time series behavior while also being easy to construct, simulate, and analyze by using linear state-space tools. We construct our  additive functional from two pieces, the first of which is a **first-order vector autoregression** (VAR)"
**Issue**: Multiple sentences in one paragraph
**Fix**: Split into separate paragraphs:
"Our special additive functional displays interesting time series behavior while also being easy to construct, simulate, and analyze by using linear state-space tools.

We construct our additive functional from two pieces, the first of which is a **first-order vector autoregression** (VAR)"

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 108-110 / Section "A particular additive functional"
**Current**: "The second piece is an equation that expresses increments of $\{y_t\}_{t=0}^\infty$ as linear functions of * a scalar constant $\nu$,"
**Issue**: Multiple sentences in one paragraph (continuing with bullet points)
**Fix**: Split into separate paragraphs:
"The second piece is an equation that expresses increments of $\{y_t\}_{t=0}^\infty$ as linear functions of

* a scalar constant $\nu$,"

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 120-122 / Section "A particular additive functional"
**Current**: "Here $y_0 \sim {\cal N}(\mu_{y0}, \Sigma_{y0})$ is a random initial condition for $y$. The nonstationary random process $\{y_t\}_{t=0}^\infty$ displays systematic but random *arithmetic growth*."
**Issue**: Multiple sentences in one paragraph
**Fix**: Split into separate paragraphs:
"Here $y_0 \sim {\cal N}(\mu_{y0}, \Sigma_{y0})$ is a random initial condition for $y$.

The nonstationary random process $\{y_t\}_{t=0}^\infty$ displays systematic but random *arithmetic growth*."

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 126-128 / Section "Linear state-space representation"
**Current**: "A convenient way to represent our additive functional is to use a [linear state space system](https://python-intro.quantecon.org/linear_models.html). To do this, we set up state and observation vectors"
**Issue**: Multiple sentences in one paragraph
**Fix**: Split into separate paragraphs:
"A convenient way to represent our additive functional is to use a [linear state space system](https://python-intro.quantecon.org/linear_models.html).

To do this, we set up state and observation vectors"

### qe-writing-001: Use one sentence per paragraph
**Location**: Line 175-177 / Section "Linear state-space representation"
**Current**: "To study it, we could map it into an instance of [LinearStateSpace](https://github.com/QuantEcon/QuantEcon.py/blob/master/quantecon/lss.py) from [QuantEcon.py](http://quantecon.org/quantecon-py). But here we will use a different set of code for simulation, for reasons described below."
**Issue**: Multiple sentences in one paragraph
**Fix**: Split into separate paragraphs:
"To study it, we could map it into an instance of [LinearStateSpace](https://github.com/QuantEcon/QuantEcon.py/blob/master/quantecon/lss.py) from [QuantEcon.py](http://quantecon.org/quantecon-py).

But here we will use a different set of code for simulation, for reasons described below."

## Writing Style Suggestions

### qe-writing-002: Keep writing clear, concise, and valuable
**Location**: Line 90-92 / Section "A particular additive functional"
**Current**: "Our special additive functional displays interesting time series behavior while also being easy to construct, simulate, and analyze by using linear state-space tools."
**Suggestion**: Remove unnecessary words: "Our additive functional displays interesting time series behavior while being easy to construct, simulate, and analyze using linear state-space tools."

### qe-writing-002: Keep writing clear, concise, and valuable
**Location**: Line 73-75 / Section "Overview"
**Current**: "More details about  these concepts and algorithms  can be found in Hansen  {cite}`Hansen_2012_Eca` and Hansen and Sargent {cite}`Hans_Sarg_book`."
**Suggestion**: Remove extra spaces and simplify: "More details about these concepts and algorithms can be found in Hansen {cite}`Hansen_2012_Eca` and Hansen and Sargent {cite}`Hans_Sarg_book`."

### qe-writing-002: Keep writing clear, concise, and valuable
**Location**: Line 53 / Section "Overview"
**Current**: "Thus, {cite}`Hansen_2012_Eca`  described  two classes of time series models that accommodate growth."
**Suggestion**: Remove extra spaces: "Thus, {cite}`Hansen_2012_Eca` described two classes of time series models that accommodate growth."

## Positive Observations
The lecture demonstrates good use of mathematical notation and code examples. The logical progression from additive to multiplicative functionals is well-structured, and the decomposition explanations are thorough.

## Writing Summary
The main issue is consistent violation of the one-sentence-per-paragraph rule throughout the document. The writing is generally clear and technical content is well-presented, but breaking up multi-sentence paragraphs would significantly improve readability. Minor spacing issues and some verbose constructions could also be addressed for better conciseness.