#!/usr/bin/env python3
"""Fix dialogue paragraph breaks in Japanese chapter 1"""

import json
from pathlib import Path

def main():
    """Fix the dialogue section that's stuck together"""
    ja_filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-ja-1.json'

    print(f"Reading {ja_filepath}...")
    with open(ja_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_content = data['content']
    content = original_content

    # Fix the long dialogue section that's all in one paragraph
    # This is the section where the woman talks to the boy about the boat leaving

    # Split after the woman's first long speech
    content = content.replace(
        '「ああ、緊急の命令でも受けたみたいだったよ。とても急いでたみたいだ!」 「おばさんは、皆がどこに行くと言ってたか聞きましたか?」私は尋ね返した。',
        '「ああ、緊急の命令でも受けたみたいだったよ。とても急いでたみたいだ!」\n\n「おばさんは、皆がどこに行くと言ってたか聞きましたか?」私は尋ね返した。'
    )

    # Split after the boy's question
    content = content.replace(
        '「おばさんは、皆がどこに行くと言ってたか聞きましたか?」私は尋ね返した。 「軍事のことだからね、分かるわけないよ!お前も知らないの?言われなかったの?」',
        '「おばさんは、皆がどこに行くと言ってたか聞きましたか?」私は尋ね返した。\n\n「軍事のことだからね、分かるわけないよ!お前も知らないの?言われなかったの?」'
    )

    # Split after the woman's response
    content = content.replace(
        '「軍事のことだからね、分かるわけないよ!お前も知らないの?言われなかったの?」 「いいえ、おばさん!」',
        '「軍事のことだからね、分かるわけないよ!お前も知らないの?言われなかったの?」\n\n「いいえ、おばさん!」'
    )

    # Split after the boy's "no"
    content = content.replace(
        '「いいえ、おばさん!」 「お前には父母や兄弟が船にいたのかい?」',
        '「いいえ、おばさん!」\n\n「お前には父母や兄弟が船にいたのかい?」'
    )

    # Split after the woman's question about family
    content = content.replace(
        '「お前には父母や兄弟が船にいたのかい?」 「いいえ。渡し船に乗っていただけです」女性は唇を長く伸ばした。',
        '「お前には父母や兄弟が船にいたのかい?」\n\n「いいえ。渡し船に乗っていただけです」女性は唇を長く伸ばした。'
    )

    # Split after the boy's answer and woman's reaction
    content = content.replace(
        '「いいえ。渡し船に乗っていただけです」女性は唇を長く伸ばした。 「道理でね...人には人の用事があるんだよ。誰が遊びに夢中になって、あちこちうろつけって言ったんだい?」',
        '「いいえ。渡し船に乗っていただけです」女性は唇を長く伸ばした。\n\n「道理でね...人には人の用事があるんだよ。誰が遊びに夢中になって、あちこちうろつけって言ったんだい?」'
    )

    if original_content != content:
        data['content'] = content
        print(f"Writing fixed content...")
        with open(ja_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Count changes
        orig_paragraphs = original_content.count('\n\n')
        new_paragraphs = content.count('\n\n')
        print(f"✓ Fixed dialogue breaks")
        print(f"  Paragraphs: {orig_paragraphs} → {new_paragraphs} (+{new_paragraphs - orig_paragraphs})")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
