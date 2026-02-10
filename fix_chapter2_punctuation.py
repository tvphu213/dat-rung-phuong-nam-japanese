#!/usr/bin/env python3
"""Fix punctuation errors in chapter-2.json"""

import json
from pathlib import Path

def fix_punctuation(content):
    """Fix all punctuation issues in content"""

    # Fix 1: Add period after "đấy"
    content = content.replace(
        'Dì khâu cho mày đấy Bà ta đứng dậy',
        'Dì khâu cho mày đấy. Bà ta đứng dậy'
    )

    # Fix 2: Add period after "vậy"
    content = content.replace(
        'nói một mình như vậy Cứ mỗi người',
        'nói một mình như vậy. Cứ mỗi người'
    )

    return content

def main():
    """Fix chapter-2.json"""
    filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-2.json'

    print(f"Reading {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("Fixing punctuation...")
    original_content = data['content']
    fixed_content = fix_punctuation(original_content)

    if original_content != fixed_content:
        data['content'] = fixed_content
        print(f"Writing fixed content...")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✓ Fixed chapter-2.json")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
