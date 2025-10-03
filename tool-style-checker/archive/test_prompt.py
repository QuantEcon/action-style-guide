#!/usr/bin/env python3
"""
Simple Prompt Tester

Test different prompt files against a lecture to see which works best.

Usage:
    python test_prompt.py prompts/my_prompt.md test_lecture.md
"""

import os
import sys
from pathlib import Path
from anthropic import Anthropic

def main():
    if len(sys.argv) != 3:
        print("Usage: python test_prompt.py <prompt_file.md> <lecture_file.md>")
        print("\nExample:")
        print("  python test_prompt.py prompts/strict.md test_lecture.md")
        sys.exit(1)
    
    prompt_file = Path(sys.argv[1])
    lecture_file = Path(sys.argv[2])
    
    # Check files exist
    if not prompt_file.exists():
        print(f"❌ Prompt file not found: {prompt_file}")
        sys.exit(1)
    
    if not lecture_file.exists():
        print(f"❌ Lecture file not found: {lecture_file}")
        sys.exit(1)
    
    # Check API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        print("\nSet it with:")
        print("  export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Read files
    with open(prompt_file, 'r') as f:
        prompt = f.read()
    
    with open(lecture_file, 'r') as f:
        lecture = f.read()
    
    # Build the full prompt
    full_prompt = f"""{prompt}

# Lecture to Review

{lecture}

---

Please review the lecture above according to the style guide rules provided."""
    
    # Call Claude
    print(f"\n📝 Testing prompt: {prompt_file.name}")
    print(f"📚 Against lecture: {lecture_file.name}")
    print(f"\n{'='*60}")
    print("Sending to Claude Sonnet 4.5...")
    print(f"{'='*60}\n")
    
    client = Anthropic(api_key=api_key)
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )
        
        response = message.content[0].text
        
        # Display results
        print("🤖 CLAUDE'S RESPONSE:\n")
        print(response)
        print(f"\n{'='*60}")
        print(f"✅ Done!")
        print(f"   Input tokens:  {message.usage.input_tokens:,}")
        print(f"   Output tokens: {message.usage.output_tokens:,}")
        print(f"   Cost: ${(message.usage.input_tokens * 0.000003 + message.usage.output_tokens * 0.000015):.4f}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
