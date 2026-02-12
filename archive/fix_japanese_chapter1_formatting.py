#!/usr/bin/env python3
"""Fix Japanese chapter 1 formatting to match Vietnamese structure"""

import json
import re
from pathlib import Path

def fix_japanese_formatting(content):
    """Remove HTML tags and add proper paragraph breaks"""

    # Remove all <p> and </p> tags
    content = content.replace('<p>', '')
    content = content.replace('</p>', '\n\n')

    # Clean up any trailing whitespace
    content = content.strip()

    # Fix multiple consecutive newlines (more than 2)
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content

def main():
    """Fix Japanese chapter 1 formatting"""
    ja_filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-ja-1.json'

    print(f"Reading {ja_filepath}...")
    with open(ja_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("Fixing formatting...")
    original_content = data['content']
    fixed_content = fix_japanese_formatting(original_content)

    if original_content != fixed_content:
        data['content'] = fixed_content
        print(f"Writing fixed content...")
        with open(ja_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✓ Fixed chapter-ja-1.json")

        # Show statistics
        para_count_before = original_content.count('<p>')
        para_count_after = fixed_content.count('\n\n') + 1
        print(f"\nStatistics:")
        print(f"  Original: {para_count_before} HTML paragraphs")
        print(f"  Fixed: {para_count_after} text paragraphs")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
