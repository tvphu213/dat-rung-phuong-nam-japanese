#!/usr/bin/env python3
"""Fix punctuation errors in chapter-3.json"""

import json
from pathlib import Path

def fix_punctuation(content):
    """Fix all punctuation issues in content"""

    # Fix 1: Add period after "lưa thưa"
    content = content.replace(
        'nhóm họp lưa thưa Nhiều gia đình',
        'nhóm họp lưa thưa. Nhiều gia đình'
    )

    # Fix 2: Remove space before period
    content = content.replace(
        'chung quanh . Ai',
        'chung quanh. Ai'
    )

    # Fix 3: Add period after "về"
    content = content.replace(
        'xách về Lão Ba Ngù',
        'xách về. Lão Ba Ngù'
    )

    # Fix 4: Fix double period issue
    content = content.replace(
        'kia! .',
        'kia!'
    )

    # Fix 5: Fix "nói. bậy" to "nói bậy."
    content = content.replace(
        'đừng có nói. bậy Bộ mày',
        'đừng có nói bậy. Bộ mày'
    )

    # Fix 6: Fix double colon to single period
    content = content.replace(
        'Rầm.:: Rầm',
        'Rầm… Rầm'
    )

    # Fix 7: Remove space before period
    content = content.replace(
        'chân trời . Chắc',
        'chân trời. Chắc'
    )

    # Fix 8: Fix "sôi. lên" to "sôi lên"
    content = content.replace(
        'cho sôi. lên, thả tỏi',
        'cho sôi lên, thả tỏi'
    )

    # Fix 9: Add period after "to"
    content = content.replace(
        'ngay dưới một gốc cây to Tôi vốn ghét',
        'ngay dưới một gốc cây to. Tôi vốn ghét'
    )

    # Fix 10: Add period after "tôi"
    content = content.replace(
        'đứng ngay trên đầu tôi Mỗi lần',
        'đứng ngay trên đầu tôi. Mỗi lần'
    )

    # Fix 11: Add period after "tôi"
    content = content.replace(
        'cạnh chân tôi chúng quơ râu',
        'cạnh chân tôi. Chúng quơ râu'
    )

    # Fix 12: Fix lowercase after question mark
    content = content.replace(
        'trong cái túi bí ẩn này? đằng nào',
        'trong cái túi bí ẩn này? Đằng nào'
    )

    # Fix 13: Add period after "được"
    content = content.replace(
        'như có thể sờ được Tôi trở ra',
        'như có thể sờ được. Tôi trở ra'
    )

    # Fix 14: Fix "hy.vọng" to "hi vọng"
    content = content.replace(
        'lúc, hy.vọng sẽ gặp',
        'lúc, hi vọng sẽ gặp'
    )

    # Fix 15: Remove space before period
    content = content.replace(
        'đâu cả . Nhìn về',
        'đâu cả. Nhìn về'
    )

    # Fix 16: Fix double period
    content = content.replace(
        'bóc. . boóc',
        'bóc mấy cái'
    )

    # Fix 17: Remove space before period
    content = content.replace(
        'lên, con . Lúc',
        'lên, con. Lúc'
    )

    # Fix 18: Fix "gừ gừ . mấy"
    content = content.replace(
        'gừ gừ . mấy tiếng',
        'gừ gừ mấy tiếng'
    )

    # Fix 19: Add period after "nhưng"
    content = content.replace(
        'nằm im nhưng Nghe tiếng',
        'nằm im. Nghe tiếng'
    )

    return content

def main():
    """Fix chapter-3.json"""
    filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-3.json'

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
        print("✓ Fixed chapter-3.json")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
