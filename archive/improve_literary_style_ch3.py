#!/usr/bin/env python3
"""Improve literary style of Japanese chapter 3 based on feedback"""

import json
from pathlib import Path

def improve_literary_style(content):
    """Fix terminology and improve literary quality"""

    # Fix 1: 避難してきた → 疎開してきた (wartime evacuation)
    content = content.replace(
        '避難してきた坊やじゃないか!',
        '疎開してきた坊やじゃないかい！'
    )

    # Fix 2: fascinated (English) → 魅了されて (proper Japanese)
    content = content.replace(
        '私は人混みの後ろから、fascinated に見ていた。',
        '私は人混みの後ろから、魅了されて見ていた。'
    )

    # Fix 3: 躊躇したが → ためらったが (more natural)
    content = content.replace(
        '私は躊躇したが、老人の優しい目を見て、',
        '私はためらったが、老人の優しい目を見て、'
    )

    return content

def main():
    """Improve literary style of Japanese chapter 3"""
    ja_filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-ja-3.json'

    print(f"Reading {ja_filepath}...")
    with open(ja_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_content = data['content']

    print("Improving literary style...")
    improved_content = improve_literary_style(original_content)

    if original_content != improved_content:
        data['content'] = improved_content
        print(f"Writing improved content...")
        with open(ja_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Japanese Chapter 3 improved")
        print(f"\nChanges made:")
        print(f"  - 避難してきた → 疎開してきた")
        print(f"  - fascinated → 魅了されて")
        print(f"  - 躊躇したが → ためらったが")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
