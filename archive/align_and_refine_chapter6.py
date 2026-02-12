#!/usr/bin/env python3
"""Align and refine Japanese chapter 6 - add paragraph breaks and improve Vo Tong's voice"""

import json
from pathlib import Path

def align_and_refine_chapter6(content):
    """Add natural paragraph breaks and fix Vo Tong's rugged voice"""

    # First, fix Vo Tong's dialogue to be more rugged
    # Change 1: 「銃は敵を撃つためのもので、狩りに使う余分な銃はない!」
    # → 「鉄砲は敵をぶち抜くためのもんだ。狩りに回す余裕なんてねえよ！」
    content = content.replace(
        '「銃は敵を撃つためのもので、狩りに使う余分な銃はない!」',
        '「鉄砲は敵をぶち抜くためのもんだ。狩りに回す余裕なんてねえよ！」'
    )

    # Change 2: Add more rugged tone to other Vo Tong dialogue
    content = content.replace(
        '「必ず手に入れる。服だけをもらうんだ。銃は自衛隊の仲間たちのために残さないと」',
        '「必ず手に入れる。服だけもらうんだ。銃は自衛隊の仲間たちのために残さねえとな」'
    )

    # Change 3: Use 一献 (ikkon) for gibbon serving drinks - add literary touch
    content = content.replace(
        '「ティエウドンに酒を注がせよう?酒を注がせてやれ、ヴォー・トン!」',
        '「ティエウドンに一献注がせよう？一献注がせてやれ、ヴォー・トン！」'
    )

    # Now add natural paragraph breaks
    # Break 1: After opening penguin story line
    content = content.replace(
        'それは二年前、バー水兵兄さんが僕に話してくれた物語の冒頭の言葉だった。今、兄さんの温かい声が再び耳元で響いているようだ。 もう何日も続けて、',
        'それは二年前、バー水兵兄さんが僕に話してくれた物語の冒頭の言葉だった。今、兄さんの温かい声が再び耳元で響いているようだ。\n\nもう何日も続けて、'
    )

    # Break 2: After describing the temple
    content = content.replace(
        '最初は少し怖かったが、二日目には慣れて、怖いものは何もなくなり、かえって気持ちよくなった。 この静かな廟の中では、',
        '最初は少し怖かったが、二日目には慣れて、怖いものは何もなくなり、かえって気持ちよくなった。\n\nこの静かな廟の中では、'
    )

    # Break 3: After waking up at night
    content = content.replace(
        '今回、体を起こして外を見ると、いつものように水路の向こう岸に真っ赤に沈む太陽の光ではなく、菩提樹の枝の後ろからひっそりと姿を見せる冷たい青白い月が、弱々しい光を廟の階段に注いでいた。 もうかなり夜が更けているのだろう。',
        '今回、体を起こして外を見ると、いつものように水路の向こう岸に真っ赤に沈む太陽の光ではなく、菩提樹の枝の後ろからひっそりと姿を見せる冷たい青白い月が、弱々しい光を廟の階段に注いでいた。\n\nもうかなり夜が更けているのだろう。'
    )

    # Break 4: After drinking water
    content = content.replace(
        '冷たい水が顔や首に当たり、僕は徐々に完全に目が覚めた。 僕は廟に這うように戻り、',
        '冷たい水が顔や首に当たり、僕は徐々に完全に目が覚めた。\n\n僕は廟に這うように戻り、'
    )

    # Break 5: After self-questioning
    content = content.replace(
        '僕は壁に頭をもたげ、目を閉じると、親しい若い水兵の歌声が遠くから響いてくるのが聞こえるようだった。 「昔々、小さな船があった',
        '僕は壁に頭をもたげ、目を閉じると、親しい若い水兵の歌声が遠くから響いてくるのが聞こえるようだった。\n\n「昔々、小さな船があった'
    )

    # Break 6: Separate penguin story reminiscence
    content = content.replace(
        'こんな独り言と自問が頭の中で繰り返された。突然、バー水兵兄さんがペンギンの不思議な本能について話してくれた物語を思い出した。',
        'こんな独り言と自問が頭の中で繰り返された。\n\n突然、バー水兵兄さんがペンギンの不思議な本能について話してくれた物語を思い出した。'
    )

    # Break 7: After penguin story quote
    content = content.replace(
        'かつての陽気で夢見がちな水兵の温かく魅力的な声が、僕をいつも夢中にさせて聞かせてくれた。その声が耳元で響いている。',
        'かつての陽気で夢見がちな水兵の温かく魅力的な声が、僕をいつも夢中にさせて聞かせてくれた。その声が耳元で響いている。\n\n'
    )

    # Break 8: After vision of the dock
    content = content.replace(
        '僕はぼんやりと月明かりを見つめていると、ティエンザン川の白い川岸に沿って並ぶ運河埠頭の賑やかな光景が徐々に浮かび上がってきた。',
        '僕はぼんやりと月明かりを見つめていると、ティエンザン川の白い川岸に沿って並ぶ運河埠頭の賑やかな光景が徐々に浮かび上がってきた。\n\n'
    )

    # Break 9: After dialogue about penguin
    content = content.replace(
        '「いいなあ、兄さん。あのペンギンみたいだったら、僕たち子供は迷子になる心配がないのに」僕は手を振ってそう言った。 「あれは可哀想な鳥だよ」',
        '「いいなあ、兄さん。あのペンギンみたいだったら、僕たち子供は迷子になる心配がないのに」僕は手を振ってそう言った。\n\n「あれは可哀想な鳥だよ」'
    )

    # Break 10: After water sailor's philosophy
    content = content.replace(
        '「ペンギンが遠くに行けないのは、翼が二つあるからじゃない。心に翼がない鳥なんだ。背中が曲がり膝が痛む老人のように、いつも故郷に戻って横になりたがっている」',
        '「ペンギンが遠くに行けないのは、翼が二つあるからじゃない。心に翼がない鳥なんだ。背中が曲がり膝が痛む老人のように、いつも故郷に戻って横になりたがっている」\n\n'
    )

    # Break 11: After meeting Ba sailor backstory
    content = content.replace(
        '午後、授業が終わると、先生は僕たち生徒を連れてメコン川に泳ぎに行った。',
        '午後、授業が終わると、先生は僕たち生徒を連れてメコン川に泳ぎに行った。\n\n'
    )

    # Break 12: After sailor's travels
    content = content.replace(
        '「君は冒険が好きみたいだね?」とある時兄さんが訊いた。',
        '「君は冒険が好きみたいだね?」とある時兄さんが訊いた。\n\n'
    )

    # Break 13: After compass gift
    content = content.replace(
        '「それで、いろいろ考えた末、君には方位磁石を買ってきたよ」と兄さんは僕の肩を叩いた。',
        '「それで、いろいろ考えた末、君には方位磁石を買ってきたよ」と兄さんは僕の肩を叩いた。\n\n'
    )

    # Break 14: Before song
    content = content.replace(
        '地平線に山のように高い大波が現れ、恐ろしい速さで近づいてきて、船を覆い、僕を巻き込んで流していく。',
        '地平線に山のように高い大波が現れ、恐ろしい速さで近づいてきて、船を覆い、僕を巻き込んで流していく。\n\n'
    )

    # Break 15: After passing out
    content = content.replace(
        'そして、僕は何もわからなくなった。 「少年が目を覚ましたわ!」',
        'そして、僕は何もわからなくなった。\n\n「少年が目を覚ましたわ!」'
    )

    # Break 16: After waking up in temple
    content = content.replace(
        '「西洋人が来たんですか、兄さん?」僕は微笑んでいる負傷兵に訊いた。手で体を支えて起き上がろうとしたが、震えて崩れ落ちた。',
        '「西洋人が来たんですか、兄さん?」僕は微笑んでいる負傷兵に訊いた。手で体を支えて起き上がろうとしたが、震えて崩れ落ちた。\n\n'
    )

    # Break 17: After nurse's explanation
    content = content.replace(
        '全身がだるく疲れていて、長い病気の後のようだった。救護隊員の話によると、',
        '全身がだるく疲れていて、長い病気の後のようだった。\n\n救護隊員の話によると、'
    )

    # Break 18: After battle description
    content = content.replace(
        '「まあ、大変。負傷した兄さんたちをここに運んだ時、',
        '「まあ、大変。負傷した兄さんたちをここに運んだ時、\n\n'
    )

    # Break 19: After drinking milk
    content = content.replace(
        '僕はミルクを飲み干した。確かに意識がはっきりしてきたが、',
        '僕はミルクを飲み干した。確かに意識がはっきりしてきたが、\n\n'
    )

    # Break 20: After leaving temple
    content = content.replace(
        '事態がここまで来たら、僕も構わない、なるようになれ。',
        '事態がここまで来たら、僕も構わない、なるようになれ。\n\n'
    )

    # Break 21: After walking along canal
    content = content.replace(
        'その夜、僕は野原の真ん中にある放棄された焼畑小屋に入って横になった。',
        'その夜、僕は野原の真ん中にある放棄された焼畑小屋に入って横になった。\n\n'
    )

    # Break 22: After arriving at river
    content = content.replace(
        '僕は自分がどこに向かっているのかわからなかった。',
        '僕は自分がどこに向かっているのかわからなかった。\n\n'
    )

    # Break 23: After seeing campfire scene
    content = content.replace(
        '僕は勇気を出してもう一歩近づいた。',
        '僕は勇気を出してもう一歩近づいた。\n\n'
    )

    # Break 24: After returning the bag
    content = content.replace(
        '「おじいさん?これ、おじいさんのものじゃないですか?」僕は縞模様の革袋を取り出して、老人に差し出した。',
        '「おじいさん?これ、おじいさんのものじゃないですか?」僕は縞模様の革袋を取り出して、老人に差し出した。\n\n'
    )

    # Break 25: After old man's joy
    content = content.replace(
        '「よくやった、坊や!ありがとう、坊や!」老人の喜びの声が暗い夜に遠くまで響いた。',
        '「よくやった、坊や!ありがとう、坊や!」老人の喜びの声が暗い夜に遠くまで響いた。\n\n'
    )

    # Break 26: After examining bag contents
    content = content.replace(
        '一人の男が老人の肩をぱんと叩いた。 「ハイ兄さん?物が持ち主の元に戻ったんだから、何かしなきゃ」',
        '一人の男が老人の肩をぱんと叩いた。\n\n「ハイ兄さん?物が持ち主の元に戻ったんだから、何かしなきゃ」\n\n'
    )

    # Break 27: After questions about home
    content = content.replace(
        '二人の女性が僕の隣に寄ってきた。一人が訊いた。',
        '二人の女性が僕の隣に寄ってきた。一人が訊いた。\n\n'
    )

    # Break 28: After telling battle story
    content = content.replace(
        '彼らがどんな考えを交わしているのかはわからなかった。 「坊やの両親はどこにいるんだい?」',
        '彼らがどんな考えを交わしているのかはわからなかった。\n\n「坊やの両親はどこにいるんだい?」'
    )

    # Break 29: After proud declaration
    content = content.replace(
        '僕自身が言っているのか、バー水兵兄さんが僕の中に乗り移ってその言葉を発したのか、わからなかった。',
        '僕自身が言っているのか、バー水兵兄さんが僕の中に乗り移ってその言葉を発したのか、わからなかった。\n\n'
    )

    # Break 30: After palm reading
    content = content.replace(
        '真っ黒な少年が川岸に走り降りて、船から酒壺と大きな土の椀を取り出した。',
        '真っ黒な少年が川岸に走り降りて、船から酒壺と大きな土の椀を取り出した。\n\n'
    )

    # Break 31: After offering wine
    content = content.replace(
        'コー――僕は前に会った時の名前を覚えていた――が僕の手を引いて近くに座らせた。',
        'コー――僕は前に会った時の名前を覚えていた――が僕の手を引いて近くに座らせた。\n\n'
    )

    # Break 32: Before Vo Tong arrives
    content = content.replace(
        'ちょうどその時、犬が突然跳び上がってオアンオアンと吠えた。',
        'ちょうどその時、犬が突然跳び上がってオアンオアンと吠えた。\n\n'
    )

    # Break 33: After Vo Tong's appearance
    content = content.replace(
        '「最近、何かいい獲物を捕ったか、山林の主よ?」一人が振り返って訊いた。',
        '「最近、何かいい獲物を捕ったか、山林の主よ?」一人が振り返って訊いた。\n\n'
    )

    # Break 34: After asking about gun
    content = content.replace(
        '突然僕が頷いて同意を示すのを見て、ヴォー・トンは立ち止まって僕を指さした。',
        '突然僕が頷いて同意を示すのを見て、ヴォー・トンは立ち止まって僕を指さした。\n\n'
    )

    # Break 35: After old man's response
    content = content.replace(
        '「でも、仲間になるだろう。すぐに、私と一緒に連れて行く。家内はきっと喜ぶだろう」 一群の夜鳥が僕たちの頭上を飛び去った。',
        '「でも、仲間になるだろう。すぐに、私と一緒に連れて行く。家内はきっと喜ぶだろう」\n\n一群の夜鳥が僕たちの頭上を飛び去った。'
    )

    return content

def main():
    """Align and refine Japanese chapter 6"""
    ja_filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-ja-6.json'

    print(f"Reading {ja_filepath}...")
    with open(ja_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_content = data['content']
    original_paragraphs = len(original_content.split('\n\n'))

    print(f"Original paragraph count: {original_paragraphs}")
    print("Aligning and refining literary quality...")

    refined_content = align_and_refine_chapter6(original_content)
    new_paragraphs = len(refined_content.split('\n\n'))

    if original_content != refined_content:
        data['content'] = refined_content
        print(f"Writing refined content...")
        with open(ja_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Japanese Chapter 6 aligned and refined")
        print(f"  Paragraphs: {original_paragraphs} → {new_paragraphs}")
        print(f"\nLiterary refinements:")
        print(f"  - Vo Tong dialogue: 銃は敵を撃つ... → 鉄砲は敵をぶち抜くためのもんだ (rugged voice)")
        print(f"  - Vo Tong dialogue: もらうんだ → もらうんだ...残さねえとな (rough endings)")
        print(f"  - Gibbon serving: 酒を注がせよう → 一献注がせよう (literary touch)")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
