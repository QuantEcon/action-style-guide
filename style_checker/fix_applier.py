"""
Apply style guide fixes programmatically to lecture content
"""
from typing import List, Dict, Any, Tuple


def apply_fixes(content: str, violations: List[Dict[str, Any]]) -> Tuple[str, List[str], List[Dict[str, Any]]]:
    """
    Apply fixes from violations to content programmatically.

    Strategy: locate each violation's `current_text` in `content`, then apply
    fixes in descending position order using slice-based substitution. Processing
    higher positions first means earlier (lower) positions are unaffected by
    each edit, so the originally-computed positions remain valid throughout.

    Args:
        content: Original lecture content
        violations: List of violations with current_text and suggested_fix

    Returns:
        Tuple of (corrected_content, list of warnings, list of actually applied violations)
    """
    corrected = content
    skipped_count = 0
    warnings = []
    applied_violations = []

    # Debug: Show LLM's original order
    print(f"  ℹ️  LLM identified violations in this rule order:")
    rule_sequence = [v.get('rule_id', 'unknown') for v in violations[:10]]
    print(f"      {', '.join(rule_sequence)}")
    if len(violations) > 10:
        print(f"      ... and {len(violations) - 10} more")

    # Locate each violation's anchor in the source. Skip anything malformed up front.
    violations_with_pos: List[Tuple[int, Dict[str, Any]]] = []
    for v in violations:
        current_text = v.get('current_text', '').strip()
        suggested_fix = v.get('suggested_fix', '').strip()
        rule_id = v.get('rule_id', 'unknown')

        if not current_text:
            warnings.append(f"⚠️  Skipping {rule_id}: No current_text provided")
            skipped_count += 1
            continue

        if not suggested_fix:
            warnings.append(f"⚠️  Skipping {rule_id}: No suggested_fix provided")
            skipped_count += 1
            continue

        if current_text == suggested_fix:
            warnings.append(
                f"ℹ️  Skipping {rule_id}: No change needed (original and fix are identical)"
            )
            skipped_count += 1
            continue

        pos = corrected.find(current_text)
        if pos == -1:
            # Most common cause is the LLM paraphrasing whitespace (collapsing newlines,
            # trimming indentation) so the exact substring isn't present. Surface a clear
            # cause rather than the misleading "text changed since parsing" message the
            # old fallback emitted after silently failing to apply anything.
            warnings.append(
                f"⚠️  Skipping {rule_id}: LLM-quoted current_text not found verbatim "
                f"in source (likely whitespace mismatch) at "
                f"{v.get('location', 'unknown')}"
            )
            skipped_count += 1
            continue

        violations_with_pos.append((pos, v))

    # Descending position order: higher edits don't shift the indices of lower ones.
    violations_with_pos.sort(key=lambda x: x[0], reverse=True)

    # Apply each fix by exact slice — `pos` was captured before any edits, and all
    # edits we've applied so far are at higher positions, so `pos` is still valid.
    # Verify the anchor still matches before substituting (defends against the rare
    # case where two violations overlap or share text at adjacent positions).
    for pos, violation in violations_with_pos:
        current_text = violation.get('current_text', '').strip()
        suggested_fix = violation.get('suggested_fix', '').strip()
        rule_id = violation.get('rule_id', 'unknown')

        end = pos + len(current_text)
        if corrected[pos:end] != current_text:
            # Earlier fix overlapped or removed this region. Skip with a clear message
            # rather than silently picking the wrong occurrence via str.replace().
            warnings.append(
                f"⚠️  Could not apply {rule_id}: position {pos} no longer matches "
                f"current_text (likely overlapped by an earlier fix)"
            )
            skipped_count += 1
            continue

        corrected = corrected[:pos] + suggested_fix + corrected[end:]
        applied_violations.append(violation)
        print(f"    ✓ Applied fix for {rule_id}")

    print(f"\n  📊 Applied {len(applied_violations)}/{len(violations)} fixes")
    if skipped_count > 0:
        print(f"  ⚠️  Skipped {skipped_count} fixes (see warnings)")

    return corrected, warnings, applied_violations


def validate_fix_quality(violations: List[Dict[str, Any]]) -> List[str]:
    """
    Validate that violations have good quality current_text and suggested_fix.
    
    Args:
        violations: List of violations to validate
        
    Returns:
        List of validation warnings
    """
    warnings = []
    
    for i, v in enumerate(violations, 1):
        rule_id = v.get('rule_id', f'violation-{i}')
        current_text = v.get('current_text', '').strip()
        suggested_fix = v.get('suggested_fix', '').strip()
        
        # Check if current_text exists
        if not current_text:
            warnings.append(f"{rule_id}: Missing current_text")
            continue
        
        # Check if suggested_fix exists
        if not suggested_fix:
            warnings.append(f"{rule_id}: Missing suggested_fix")
            continue
        
        # Check if they're identical (no-op fix)
        if current_text == suggested_fix:
            warnings.append(f"{rule_id}: Current text and suggested fix are identical")
            continue
        
        # Check if suggested_fix contains notes/commentary
        commentary_indicators = [
            '# NOTE:', '# TODO:', '# FIX:', '# CHANGED:', 
            '[Note:', '[TODO:', '[Changed:', '// NOTE', '// TODO'
        ]
        for indicator in commentary_indicators:
            if indicator in suggested_fix:
                warnings.append(
                    f"{rule_id}: Suggested fix contains commentary: '{indicator}'"
                )
        
        # Check if current_text is too short (likely not precise enough)
        if len(current_text) < 10:
            warnings.append(
                f"{rule_id}: Current text is very short ({len(current_text)} chars) - "
                f"may match multiple locations"
            )
    
    return warnings
