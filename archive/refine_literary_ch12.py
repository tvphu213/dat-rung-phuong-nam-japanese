#!/usr/bin/env python3
"""Refine literary quality of Japanese chapter 12 - authentic forest survival"""

import json
from pathlib import Path

def refine_literary_quality(content):
    """Apply literary refinements for authentic Vietnamese forest culture"""

    # Fix 1: Replace modern "安全帯" with authentic "クロマの帯"
    # The adoptive father uses his traditional checkered headcloth (kroma)
    # to tie An to the tree - rustic but full of love
    content = content.replace(
        '養父の安全帯が枝に結びつけられていなければ、きっと地面に落ちていただろう。',
        '養父が結んでくれたクロマの帯がなければ、きっと地面に落ちていただろう。'
    )

    # Fix 2: Add cultural context to the headcloth wrapping scene
    # Make it clear this is a traditional cloth being repurposed
    content = content.replace(
        '彼は頭に巻いていた布を外し、私の腹に巻いて枝に結びつけた。「これで落ちないな、坊や」',
        '彼は頭に巻いていたクロマ（水玉模様の腰布）を外し、私の腹に巻いて枝にしっかりと結びつけた。「これで落ちないな、坊や」'
    )

    return content

def main():
    """Refine literary quality of Japanese chapter 12"""
    ja_filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-ja-12.json'

    print(f"Reading {ja_filepath}...")
    with open(ja_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_content = data['content']

    print("Refining literary quality for authentic Vietnamese forest culture...")
    refined_content = refine_literary_quality(original_content)

    if original_content != refined_content:
        data['content'] = refined_content
        print(f"Writing refined content...")
        with open(ja_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Japanese Chapter 12 refined")
        print(f"\nLiterary improvements:")
        print(f"  - Replaced 安全帯 → クロマの帯 (authentic traditional cloth belt)")
        print(f"  - Added cultural detail: クロマ（水玉模様の腰布）")
        print(f"  - Shows rustic but loving care: adoptive father using his headcloth to secure An")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
