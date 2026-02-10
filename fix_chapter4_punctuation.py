#!/usr/bin/env python3
"""Fix punctuation errors in chapter-4.json"""

import json
from pathlib import Path

def fix_punctuation(content):
    """Fix all punctuation issues in content"""

    # Fix 1: Add period after "gì"
    content = content.replace(
        'chẳng coi ra mùi gì Thực tình thì',
        'chẳng coi ra mùi gì. Thực tình thì'
    )

    # Fix 2: Remove space before period
    content = content.replace(
        'câu trả lời .',
        'câu trả lời.'
    )

    # Fix 3: Add period and fix capitalization
    content = content.replace(
        'con số từ một đến một trăm thôi Nhưng phải',
        'con số từ một đến một trăm thôi. Nhưng phải'
    )

    # Fix 4: Fix space before period
    content = content.replace(
        'không phải nói . Chúng nó',
        'không phải nói. Chúng nó'
    )

    # Fix 5: Remove space before period after exclamation
    content = content.replace(
        'tuyên truyền nghe nữa chứ! .',
        'tuyên truyền nghe nữa chứ!'
    )

    # Fix 6: Fix space before comma
    content = content.replace(
        'của mọi người , chẳng đáng',
        'của mọi người, chẳng đáng'
    )

    # Fix 7: Remove space before period
    content = content.replace(
        'bàn tay run run vờ cầm đôi đũa, dôi mắt trừng trừng nhìn tôi .',
        'bàn tay run run vờ cầm đôi đũa, dôi mắt trừng trừng nhìn tôi.'
    )

    return content

def main():
    """Fix chapter-4.json"""
    filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-4.json'

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
        print("✓ Fixed chapter-4.json")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
