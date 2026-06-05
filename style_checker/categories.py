"""
Single source of truth for the style-rule category names.

Every category here must have a corresponding `{name}-rules.md` file in
`style_checker/rules/` and a matching entry in
`reviewer.RULE_EVALUATION_ORDER`. The consistency between this tuple and
`RULE_EVALUATION_ORDER.keys()` is enforced by a test in `tests/test_reviewer.py`.
"""

# Ordered — index is the default category processing order used by
# `StyleReviewer.review_lecture_smart`.
VALID_CATEGORIES = (
    "writing",
    "math",
    "code",
    "jax",
    "figures",
    "references",
    "links",
    "admonitions",
)
