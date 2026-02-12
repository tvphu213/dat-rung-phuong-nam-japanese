#!/usr/bin/env python3
"""Refine literary quality of Japanese chapter 13 - solemn Southern Vietnamese spirit"""

import json
from pathlib import Path

def refine_literary_quality(content):
    """Apply literary refinements for tragic heroic dignity and steely Southern spirit"""

    # Fix 1: Replace 礼砲 → 弔砲 (funeral/memorial gun salute)
    # The two gunshots are not just ceremony but solemn farewell and vow of revenge
    content = content.replace(
        'ベトミン村主任が予告なしに二発の礼砲を撃った。',
        'ベトミン村主任が予告なしに二発の弔砲を撃った。'
    )

    # Fix 2: Replace 女スパイ → 売国奴の女 (woman who sold out the country)
    # Increase contempt for the traitor Tư Mắm as Ba Ngũ and An feel
    content = content.replace(
        'その女スパイの手が賊のフランス人の背中を叩き、発砲してヴォ・トン兄を殺す命令を出したのだ。',
        'その売国奴の女の手が賊のフランス人の背中を叩き、発砲してヴォ・トン兄を殺す命令を出したのだ。'
    )

    # Fix 3: Enhance the tattoo reading for more solemn/samurai-like dignity
    # Keep original Chinese characters visible, but add Japanese reading with furigana spirit
    # Change養父's reading to match the motto's gravity
    content = content.replace(
        '「むしろ死を受け入れよう。決して恥辱は受けない」。',
        '「寧ろ死すとも、辱めを受けず」。'
    )

    return content

def main():
    """Refine literary quality of Japanese chapter 13"""
    ja_filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-ja-13.json'

    print(f"Reading {ja_filepath}...")
    with open(ja_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_content = data['content']

    print("Refining literary quality for tragic heroic dignity...")
    refined_content = refine_literary_quality(original_content)

    if original_content != refined_content:
        data['content'] = refined_content
        print(f"Writing refined content...")
        with open(ja_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Japanese Chapter 13 refined")
        print(f"\nLiterary improvements:")
        print(f"  - Changed 礼砲 → 弔砲 (solemn funeral gun salute)")
        print(f"  - Changed 女スパイ → 売国奴の女 (contemptuous: woman who betrayed the country)")
        print(f"  - Enhanced motto reading: 「寧ろ死すとも、辱めを受けず」(samurai-like dignity)")
        print(f"  - Conveys 'trầm mặc' (solemn silence) and 'sắt đá' (steely resolve) spirit")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
