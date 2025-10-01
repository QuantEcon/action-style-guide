"""
Apply style guide fixes programmatically to lecture content
"""
from typing import List, Dict, Any, Tuple


def apply_fixes(content: str, violations: List[Dict[str, Any]]) -> Tuple[str, List[str]]:
    """
    Apply fixes from violations to content programmatically.
    
    Args:
        content: Original lecture content
        violations: List of violations with current_text and suggested_fix
        
    Returns:
        Tuple of (corrected_content, list of warnings)
    """
    corrected = content
    applied_count = 0
    skipped_count = 0
    warnings = []
    
    # Sort violations by position in content (reverse order to avoid offset issues)
    # We'll try to apply them in the order they appear
    violations_with_pos = []
    for v in violations:
        current_text = v.get('current_text', '').strip()
        if not current_text:
            warnings.append(f"⚠️  Skipping {v.get('rule_id', 'unknown')}: No current_text provided")
            skipped_count += 1
            continue
        
        # Find position of current_text in content
        pos = corrected.find(current_text)
        if pos == -1:
            # Try with normalized whitespace
            normalized_current = ' '.join(current_text.split())
            normalized_content = ' '.join(corrected.split())
            pos = normalized_content.find(normalized_current)
            
            if pos == -1:
                warnings.append(
                    f"⚠️  Skipping {v.get('rule_id', 'unknown')}: "
                    f"Could not find exact match in content (Location: {v.get('location', 'unknown')})"
                )
                skipped_count += 1
                continue
        
        violations_with_pos.append((pos, v))
    
    # Sort by position (descending) so we can apply fixes without affecting earlier positions
    violations_with_pos.sort(reverse=True, key=lambda x: x[0])
    
    # Apply fixes
    for pos, violation in violations_with_pos:
        current_text = violation.get('current_text', '').strip()
        suggested_fix = violation.get('suggested_fix', '').strip()
        
        if not suggested_fix:
            warnings.append(
                f"⚠️  Skipping {violation.get('rule_id', 'unknown')}: "
                f"No suggested_fix provided"
            )
            skipped_count += 1
            continue
        
        # Apply the fix
        try:
            # Find and replace
            if current_text in corrected:
                corrected = corrected.replace(current_text, suggested_fix, 1)
                applied_count += 1
                print(f"    ✓ Applied fix for {violation.get('rule_id', 'unknown')}")
            else:
                warnings.append(
                    f"⚠️  Could not apply {violation.get('rule_id', 'unknown')}: "
                    f"Text changed since parsing"
                )
                skipped_count += 1
        except Exception as e:
            warnings.append(
                f"⚠️  Error applying {violation.get('rule_id', 'unknown')}: {str(e)}"
            )
            skipped_count += 1
    
    # Summary
    print(f"\n  📊 Applied {applied_count}/{len(violations)} fixes")
    if skipped_count > 0:
        print(f"  ⚠️  Skipped {skipped_count} fixes (see warnings)")
    
    return corrected, warnings


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
