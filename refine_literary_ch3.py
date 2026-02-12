#!/usr/bin/env python3
"""Refine literary quality of Japanese chapter 3 - make it more authentic"""

import json
from pathlib import Path

def refine_literary_quality(content):
    """Refine literary expressions and dialogue to sound more authentic"""

    # Fix 1: 魅了されて → うっとりと見入っていた (more natural expression for "fascinated")
    content = content.replace(
        '私は人混みの後ろから、魅了されて見ていた。',
        '私は人混みの後ろから、うっとりと見入っていた。'
    )

    # Fix 2: 老人の手の動きは優雅で → 老人の手つきはしなやかで (more refined)
    content = content.replace(
        '老人の手の動きは優雅で、まるで蛇と踊っているようだった。',
        '老人の手つきはしなやかで、まるで蛇と舞っているかのようだった。'
    )

    # Fix 3: 青竹蛇 → 緑色の毒蛇 (more authentic, but keep some exotic feel)
    # Actually, let's keep 青竹蛇 as it has a literary/exotic quality suitable for the old man's speech

    # Fix 4: 旅そのものが、私たちを成長させるのだ → 道中そのものが、人を育てるものなのだよ
    # (elderly wise man's voice)
    content = content.replace(
        'その日、私は蛇売りの老人から、旅についての大切な教訓を学んだ。旅は目的地に着くことだけではない。旅そのものが、私たちを成長させるのだ。',
        'その日、私は蛇売りの老人から、旅についての大切な教訓を学んだ。旅は目的地に着くことだけではない。道中そのものが、人を育てるものなのだ。'
    )

    # Fix 5: 蛇は道を知っている → 蛇は道を心得ているものだ (deeper meaning)
    content = content.replace(
        '「この蛇は幸運をもたらすと言われている。それに、蛇は道を知っている。彼らは本能的に正しい方向を感じ取ることができるんだ」',
        '「この蛇は幸運をもたらすと言われている。それに、蛇は道を心得ているものだ。彼らは本能的に正しい方向を感じ取ることができるんだよ」'
    )

    # Fix 6: 私はもはや、船団に置き去りにされた迷子の子供ではなかった → more concise
    content = content.replace(
        '私はもはや、船団に置き去りにされた迷子の子供ではなかった。私は旅人となり、自分の道を見つけようとしていたのだ。',
        '私はもう、置き去りにされた迷子などではなかった。私は旅人となり、自分の道を見つけようとしていたのだ。'
    )

    # Additional refinement: Make old man's dialogue more wise/experienced
    # Change んだ to んだよ for warmer tone in old man's speech
    content = content.replace(
        '「蛇は水辺が好きなんだよ。夕方になると、彼らは出てきて獵をする」',
        '「蛇は水辺が好きなんだ。夕方になると、出てきて獵をするんだよ」'
    )

    return content

def main():
    """Refine literary quality of Japanese chapter 3"""
    ja_filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-ja-3.json'

    print(f"Reading {ja_filepath}...")
    with open(ja_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_content = data['content']

    print("Refining literary quality...")
    refined_content = refine_literary_quality(original_content)

    if original_content != refined_content:
        data['content'] = refined_content
        print(f"Writing refined content...")
        with open(ja_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Japanese Chapter 3 refined")
        print(f"\nChanges made:")
        print(f"  - 魅了されて → うっとりと見入っていた (more natural)")
        print(f"  - 手の動きは優雅で → 手つきはしなやかで (more refined)")
        print(f"  - 蛇と踊っている → 蛇と舞っている (literary 'dance')")
        print(f"  - 旅そのもの...成長させる → 道中そのもの...育てる (wise elder voice)")
        print(f"  - 蛇は道を知っている → 蛇は道を心得ている (deeper meaning)")
        print(f"  - 船団に置き去りにされた迷子 → 置き去りにされた迷子 (more concise)")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
