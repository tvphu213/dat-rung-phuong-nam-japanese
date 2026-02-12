#!/usr/bin/env python3
"""Improve literary style of Japanese chapter 2 based on feedback"""

import json
from pathlib import Path

def improve_literary_style(content):
    """Fix terminology and improve literary quality"""

    # Fix 1: bambooのカーテン → 竹簾
    content = content.replace(
        'bambooのカーテンの隙間から中を覗いた。',
        '竹簾（たけすだれ）の隙間から中を覗いた。'
    )

    # Fix 2: 避難してきた → 疎開してきた (wartime evacuation)
    content = content.replace(
        '避難してきた坊やじゃないか!',
        '疎開してきた坊やじゃないかい！'
    )

    # Fix 3: 将棋 → 中国将棋 (Chinese chess, not Japanese shogi)
    content = content.replace(
        '二人の老人が将棋を指していた。',
        '二人の老人が中国将棋を指していた。'
    )

    # Fix 4: Improve laugh description - more vivid
    content = content.replace(
        '彼女の笑い声は、まるで太鼓を叩くように響き渡った。',
        '彼女の豪快な笑い声は、太鼓の音のように店内に響き渡った。'
    )

    # Fix 5: 私の心臓が沈んだ → 胸が締め付けられる思いだった (more natural Japanese expression)
    content = content.replace(
        '私の心臓が沈んだ。もしかしたら、私は永遠にあの学生に会えないのかもしれない。',
        '胸が締め付けられる思いだった。もしかしたら、私は永遠にあの学生に会えないのかもしれない。'
    )

    # Fix 6: 躊躇しながら → ためらいながら (more natural)
    content = content.replace(
        '私は躊躇しながら竹簾（たけすだれ）の隙間から中を覗いた。',
        '私はためらいながら竹簾（たけすだれ）の隙間から中を覗いた。'
    )

    return content

def main():
    """Improve literary style of Japanese chapter 2"""
    ja_filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-ja-2.json'

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

        print(f"\n✓ Japanese Chapter 2 improved")
        print(f"\nChanges made:")
        print(f"  - bambooのカーテン → 竹簾（たけすだれ）")
        print(f"  - 避難してきた → 疎開してきた")
        print(f"  - 将棋 → 中国将棋")
        print(f"  - 躊躇しながら → ためらいながら")
        print(f"  - Enhanced laugh description")
        print(f"  - 私の心臓が沈んだ → 胸が締め付けられる思いだった")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
