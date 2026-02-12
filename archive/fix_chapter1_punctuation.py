#!/usr/bin/env python3
"""Fix punctuation errors in chapter-1.json"""

import json
from pathlib import Path

def fix_punctuation(content):
    """Fix all punctuation issues in content"""

    # Fix 1: Add period after "nghĩ như vậy"
    content = content.replace(
        'tôi vẫn thường vơ vẩn nghĩ như vậy Tôi lạc tới xóm chợ này',
        'tôi vẫn thường vơ vẩn nghĩ như vậy. Tôi lạc tới xóm chợ này'
    )

    # Fix 2: Remove period after question mark
    content = content.replace(
        'Có muốn lên bờ không?.',
        'Có muốn lên bờ không?"'
    )

    # Fix 3: Add period after "nhé"
    content = content.replace(
        '– Đừng đi đâu nhé Uống cà phê xong',
        '– Đừng đi đâu nhé. Uống cà phê xong'
    )

    # Fix 4: Add period at end of sentence
    content = content.replace(
        'không nhậu ra ngoài một giọt chớ\n\n– Bác có',
        'không nhậu ra ngoài một giọt chớ.\n\n– Bác có'
    )

    # Fix 5: Add period at end of dialogue
    content = content.replace(
        '– Không. Cháu có cười gì đâu\n\n– Bộ mày',
        '– Không. Cháu có cười gì đâu.\n\n– Bộ mày'
    )

    # Fix 6: Add period after "khán giả"
    content = content.replace(
        'cúi chào khán giả Chiếc vòng sắt',
        'cúi chào khán giả. Chiếc vòng sắt'
    )

    # Fix 7: Add period after "cuội"
    content = content.replace(
        'những hòn cuội Tôi hồi hộp qua',
        'những hòn cuội. Tôi hồi hộp qua'
    )

    # Fix 8: Add period after "lại"
    content = content.replace(
        'khiến em nhắm mắt lại Bà xẩm cầm',
        'khiến em nhắm mắt lại. Bà xẩm cầm'
    )

    # Fix 9: Add exclamation after "Chao ôi"
    content = content.replace(
        'Chao ôi Chợ gì mà lạ lùng',
        'Chao ôi! Chợ gì mà lạ lùng'
    )

    return content

def main():
    """Fix chapter-1.json"""
    filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-1.json'

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
        print("✓ Fixed chapter-1.json")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
