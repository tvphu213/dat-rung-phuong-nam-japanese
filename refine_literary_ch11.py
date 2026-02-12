#!/usr/bin/env python3
"""Refine literary quality of Japanese chapter 11 - intense war scene style"""

import json
from pathlib import Path

def refine_literary_quality(content):
    """Apply literary refinements for fierce war atmosphere and breathless urgency"""

    # Fix 1: Aircraft description - more ominous imagery
    content = content.replace(
        '飛行機は黒く見え、',
        '黒いコウノトリのような不気味な機体が'
    )

    # Fix 2: Military terminology - 三色旗の印章 → 軍旗の紋章
    content = content.replace(
        '三色旗の印章',
        '軍旗の紋章'
    )

    # Fix 3: Urgent dialogue - adoptive father's warning (sharp and urgent)
    content = content.replace(
        '「アン!早く伏せろ。何か黒いものを落としている。落としてる...」',
        '「アン！伏せろ！早く！奴ら、何か落としやがったぞ！」'
    )

    # Fix 4: Urgent dialogue - abandon the honey (life first!)
    content = content.replace(
        '「逃げることが先だ」',
        '「命が先だ！捨てちまえ！」'
    )

    # Fix 5: Urgent dialogue - forest burning (more dramatic)
    content = content.replace(
        '「森を焼いてるぞ、坊や!」',
        '「焼き払われるぞ！逃げろ！」'
    )

    # Fix 6: Wild boar scene - dramatic expansion with cinematic description
    content = content.replace(
        'なんてことだ、西洋人じゃない。煙の霧の中から一頭の猪が現れた。',
        'なんてことだ、フランス兵なんかじゃない。煙のカーテンを突き破って現れたのは、一頭の大猪（おおいのしし）だった。牛ほどもあろうかという巨体に、逆立った鬣（たてがみ）。火に追われ、狂ったように突き進んでくる。'
    )

    return content

def main():
    """Refine literary quality of Japanese chapter 11"""
    ja_filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-ja-11.json'

    print(f"Reading {ja_filepath}...")
    with open(ja_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_content = data['content']

    print("Refining literary quality for intense war scene atmosphere...")
    refined_content = refine_literary_quality(original_content)

    if original_content != refined_content:
        data['content'] = refined_content
        print(f"Writing refined content...")
        with open(ja_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Japanese Chapter 11 refined")
        print(f"\nLiterary improvements:")
        print(f"  - Aircraft imagery: 黒いコウノトリのような不気味な機体 (ominous black storks)")
        print(f"  - Military term: 三色旗の印章 → 軍旗の紋章 (military insignia)")
        print(f"  - Urgent warning: アン！伏せろ！早く！奴ら、何か落としやがったぞ！")
        print(f"  - Life priority: 命が先だ！捨てちまえ！(abandon honey, life first!)")
        print(f"  - Forest burning: 焼き払われるぞ！逃げろ！(passive form for intensity)")
        print(f"  - Wild boar: 煙のカーテンを突き破って...巨体...逆立った鬣 (dramatic cinematic)")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
