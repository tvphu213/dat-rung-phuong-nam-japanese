#!/usr/bin/env python3
"""Refine literary quality of Japanese chapter 9 - forest heroic style"""

import json
from pathlib import Path

def refine_literary_quality(content):
    """Apply literary refinements for heroic forest atmosphere and rugged character voices"""

    # Fix 1: Add ケオ (kèo) terminology - horizontal beam for bee traps
    # 「枝」を「ケオ（蜂の巣を誘う横木）」に
    content = content.replace(
        '「ケオって何ですか、母さん?」 「ああ、ケオも白千層の枝のことだよ。',
        '「ケオって何ですか、母さん?」 「ああ、ケオ（蜂の巣を誘う横木）も白千層の枝のことだよ。'
    )

    # Fix 2: Change 薬 to 燻し薬 (smoking medicine) for A ngụy
    content = content.replace(
        'それから紙包みを開け、アグイという粘りのある黄褐色の薬を取り出した',
        'それから紙包みを開け、アグイという粘りのある黄褐色の燻し薬を取り出した'
    )

    content = content.replace(
        '薬の煙の臭いがひどい!',
        '燻し薬の煙の臭いがひどい!'
    )

    content = content.replace(
        '養父は薬をつけた葦を持って蜂の巣に近づけた。',
        '養父は燻し薬をつけた葦を持って蜂の巣に近づけた。'
    )

    # Fix 3: Tía's rugged voice - observation lesson
    content = content.replace(
        '「注意して観察していれば、長い間にわかるようになる」',
        '「じっくり観察しな。長いこと森に居りゃあ、自然と身体が覚えていくもんだ」'
    )

    # Fix 4: Cò's sharp voice - watching bees
    content = content.replace(
        '「今、よく見てろ。あの高いチャムの木の二つの枝の間をな!そう!それだ。その空いてる場所だけ見てろよ。もうすぐ来るから!」',
        '「ほら、あすこの高いチャムの木の枝の間をよく見てろ！瞬きすんじゃねえぞ！そう、そこだ！その空いてる場所だけ見てろよ。もうすぐ来るからな！」'
    )

    # Fix 5: Cinematic description - bee hive breaking (use Japanese idiom)
    content = content.replace(
        '本当だ!「蜂の巣が壊れたよう」とよく言うが、蜂の巣が壊れるとはまさにこの時のことだ。何が何だかわからない。蜂がぶんぶんと飛び、真っ黒になり、乱れ飛び、ござのような黒い輪になった。',
        'まさに「蜂の巣をつついたよう」な大騒ぎだ。空を埋め尽くすほどの黒い群れが、唸りを上げて荒れ狂う。何が何だかわからない。ござのような黒い輪になって、乱れ飛んでいる。'
    )

    # Fix 6: Chapter ending - serene beauty with literary touch
    content = content.replace(
        '青い羽の数羽のインコが、赤い嘴のオウムの群れと、菩提樹の熟した実を取り合っている。時折、黄色い実が二、三個落ちて転がり、私の足元にビー玉のように転がってきた。',
        '瑠璃色のインコと真っ赤なくちばしのオウムたちが、熟した木の実を奪い合っている。足元に転がってきた黄色い実は、まるで忘れ去られた宝石のようだった。'
    )

    # Additional refinement: Make Tía's explanation more rugged
    content = content.replace(
        '「でたらめだ!でたらめ!間違ってる。蜂は採集場所が近いか遠いかを知らせているだけだ。花粉を詰めるか、蜜蝋を作るか、蜜を採るかは、どれも採集することだ。蜂にとって重要なのは、飛行経路が遠いか近いかだけだ、わかるか?」',
        '「でたらめだ！そんなもん間違ってる。蜂は採集場所が近いか遠いかを知らせてるだけだ。花粉だろうが蜜蝋だろうが蜜だろうが、どれも採集することに変わりはねえ。蜂にとって肝心なのは、飛行経路が遠いか近いかだけなんだよ、わかるか？」'
    )

    return content

def main():
    """Refine literary quality of Japanese chapter 9"""
    ja_filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-ja-9.json'

    print(f"Reading {ja_filepath}...")
    with open(ja_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_content = data['content']

    print("Refining literary quality for heroic forest atmosphere...")
    refined_content = refine_literary_quality(original_content)

    if original_content != refined_content:
        data['content'] = refined_content
        print(f"Writing refined content...")
        with open(ja_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Japanese Chapter 9 refined")
        print(f"\nLiterary improvements:")
        print(f"  - Terminology: ケオ（蜂の巣を誘う横木）added for authentic touch")
        print(f"  - Medicine: 薬 → 燻し薬 (smoking medicine)")
        print(f"  - Tía's voice: じっくり観察しな...自然と身体が覚えていくもんだ (rugged wisdom)")
        print(f"  - Cò's voice: 瞬きすんじゃねえぞ！(sharp and lively)")
        print(f"  - Cinematic: 蜂の巣をつついたよう (Japanese idiom)")
        print(f"  - Ending: 瑠璃色...忘れ去られた宝石のよう (literary beauty)")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
