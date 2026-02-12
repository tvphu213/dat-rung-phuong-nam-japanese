#!/usr/bin/env python3
"""Align paragraph structure and refine literary quality for Japanese chapter 4"""

import json
from pathlib import Path

def align_and_refine(content):
    """Add natural paragraph breaks and improve literary quality"""

    # LITERARY IMPROVEMENTS FIRST (before adding breaks to avoid conflicts)

    # Fix 1: フランス軍だ → フランスの奴らだ (more colloquial for wartime)
    content = content.replace(
        '「フランス軍だ!」誰かが叫んだ。',
        '「フランスの奴らだ!」誰かが叫んだ。'
    )

    # Fix 2: 貴重品 → 家財道具 (household items, not just valuables)
    content = content.replace(
        '男たちは貴重品を抱えていた。',
        '男たちは家財道具を抱えていた。'
    )

    # Fix 3: オレンジ色の炎 → 紅蓮の炎 (literary "crimson flames")
    content = content.replace(
        'オレンジ色の炎が夜空を染め、',
        '紅蓮の炎が夜空を染め、'
    )

    # Fix 4: 櫂 → 櫓 (Vietnamese-style oar, not Western paddle)
    content = content.replace(
        'おばさんは櫂を取り、',
        'おばさんは櫓を取り、'
    )
    content = content.replace(
        'トゥ・ベオおばさんは依然として櫂を漕ぎ続けていた。',
        'トゥ・ベオおばさんは依然として櫓を漕ぎ続けていた。'
    )

    # Fix 5: 避難船 → 逃げ舟 (fleeing boats, more colloquial)
    content = content.replace(
        '他の避難船もそこで休んでいた。',
        '他の逃げ舟もそこで休んでいた。'
    )

    # Fix 6: Improve Tu Beo's dialogue - more urgent and warm
    content = content.replace(
        '「坊や!こっちだ!」トゥ・ベオおばさんが私を呼んだ。',
        '「坊ず！こっちへおいで！早く！」トゥ・ベオおばさんが私を呼んだ。'
    )

    # PARAGRAPH ALIGNMENT (add natural breaks for Japanese writing style)

    # Opening - separate the gunshot
    content = content.replace(
        'それは満月の夜だった。市場は普段よりも静かで、ほとんどの人々は早く寝ていた。私はトゥ・ベオおばさんの居酒屋で最後の掃除を終え、自分の寝床に向かおうとしていた。 突然、遠くから銃声が聞こえた。 最初は一発、次に二発、そして連続した銃撃の音が夜の静寂を引き裂いた。 「フランスの奴らだ!」誰かが叫んだ。 市場は一瞬で混乱に陥った。',
        'それは満月の夜だった。市場は普段よりも静かで、ほとんどの人々は早く寝ていた。私はトゥ・ベオおばさんの居酒屋で最後の掃除を終え、自分の寝床に向かおうとしていた。\n\n突然、遠くから銃声が聞こえた。\n\n最初は一発、次に二発、そして連続した銃撃の音が夜の静寂を引き裂いた。\n\n「フランスの奴らだ!」誰かが叫んだ。\n\n市場は一瞬で混乱に陥った。'
    )

    # Separate the chaos description
    content = content.replace(
        '人々が家から飛び出し、船に向かって走り始めた。母親たちは子供たちを抱き、男たちは家財道具を抱えていた。犬が吠え、鶏が騒ぎ、あらゆる方向から悲鳴が聞こえた。 「坊ず！こっちへおいで！早く！」トゥ・ベオおばさんが私を呼んだ。 私は急いで彼女のところに走った。',
        '人々が家から飛び出し、船に向かって走り始めた。母親たちは子供たちを抱き、男たちは家財道具を抱えていた。犬が吠え、鶏が騒ぎ、あらゆる方向から悲鳴が聞こえた。\n\n「坊ず！こっちへおいで！早く！」トゥ・ベオおばさんが私を呼んだ。\n\n私は急いで彼女のところに走った。'
    )

    # Separate packing and fleeing
    content = content.replace(
        'おばさんは大きな体で、重要な物を袋に詰め込んでいた。 「運河に行くんだ!船に乗って逃げなければ!」 私たちは暗闇の中を走った。',
        'おばさんは大きな体で、重要な物を袋に詰め込んでいた。\n\n「運河に行くんだ!船に乗って逃げなければ!」\n\n私たちは暗闇の中を走った。'
    )

    # Separate arriving at canal
    content = content.replace(
        '月明かりが道を照らしていたが、周りは混乱していた。人々がぶつかり合い、物が地面に落ち、赤ん坊の泣き声が夜空に響いた。 運河に着くと、既に多くの人々が船に乗り込もうとしていた。',
        '月明かりが道を照らしていたが、周りは混乱していた。人々がぶつかり合い、物が地面に落ち、赤ん坊の泣き声が夜空に響いた。\n\n運河に着くと、既に多くの人々が船に乗り込もうとしていた。'
    )

    # Separate dialogue at canal
    content = content.replace(
        '小さな船は人でいっぱいになり、今にも沈みそうだった。\n\n「待ってくれ!僕も乗せてくれ!」若い男が叫んだ。 「もう満員だ!次の船を待て!」船頭が答えた。 銃声はどんどん近づいてきた。',
        '小さな船は人でいっぱいになり、今にも沈みそうだった。\n\n「待ってくれ!僕も乗せてくれ!」若い男が叫んだ。\n\n「もう満員だ!次の船を待て!」船頭が答えた。\n\n銃声はどんどん近づいてきた。'
    )

    # Separate fire description
    content = content.replace(
        '今や、市場の端で火の手が上がっているのが見えた。紅蓮の炎が夜空を染め、黒い煙が立ち上っていた。 「あそこだ!」トゥ・ベオおばさんが空いている小さな船を見つけた。 私たちは船に飛び乗った。',
        '今や、市場の端で火の手が上がっているのが見えた。紅蓮の炎が夜空を染め、黒い煙が立ち上っていた。\n\n「あそこだ!」トゥ・ベオおばさんが空いている小さな船を見つけた。\n\n私たちは船に飛び乗った。'
    )

    # Separate rowing scene
    content = content.replace(
        'おばさんは櫓を取り、力強く漕ぎ始めた。船はゆっくりと岸を離れ、運河の中心に向かって進んだ。 後ろを振り返ると、',
        'おばさんは櫓を取り、力強く漕ぎ始めた。船はゆっくりと岸を離れ、運河の中心に向かって進んだ。\n\n後ろを振り返ると、'
    )

    # Separate market burning description
    content = content.replace(
        '市場が炎に包まれているのが見えた。私が過ごした居酒屋、魚を売っていたおばさんたちの場所、子供たちが遊んでいた広場...すべてが火に飲み込まれていた。 「おばさん、どこに行くんですか?」私は尋ねた。 「南だ」おばさんが息を切らしながら答えた。',
        '市場が炎に包まれているのが見えた。私が過ごした居酒屋、魚を売っていたおばさんたちの場所、子供たちが遊んでいた広場...すべてが火に飲み込まれていた。\n\n「おばさん、どこに行くんですか?」私は尋ねた。\n\n「南だ」おばさんが息を切らしながら答えた。'
    )

    # Separate journey description
    content = content.replace(
        '「親戚の村がある。そこまで行けば安全だ」 私たちは暗い運河を進んだ。',
        '「親戚の村がある。そこまで行けば安全だ」\n\n私たちは暗い運河を進んだ。'
    )

    # Separate snake basket dialogue
    content = content.replace(
        '他にも多くの船が同じ方向に逃げていた。時々、銃声がまだ聞こえ、空が一瞬明るくなった。 「坊や、蛇の籠は持ってきたかい?」おばさんが突然尋ねた。\n\n私は慌てて確認した。',
        '他にも多くの船が同じ方向に逃げていた。時々、銃声がまだ聞こえ、空が一瞬明るくなった。\n\n「坊や、蛇の籠は持ってきたかい?」おばさんが突然尋ねた。\n\n私は慌てて確認した。'
    )

    # Separate confirmation
    content = content.replace(
        '幸いなことに、私は本能的に小さな蛇の籠を持って来ていた。 「はい、ここにあります」 「よかった」おばさんが言った。',
        '幸いなことに、私は本能的に小さな蛇の籠を持って来ていた。\n\n「はい、ここにあります」\n\n「よかった」おばさんが言った。'
    )

    # Separate night progression
    content = content.replace(
        '「あれはお前の幸運のお守りだからね」 夜が更けるにつれて、銃声は次第に遠ざかった。',
        '「あれはお前の幸運のお守りだからね」\n\n夜が更けるにつれて、銃声は次第に遠ざかった。'
    )

    # Separate moonlight description
    content = content.replace(
        '私たちは運河を下り続け、市場から離れていった。周りの船も次第に少なくなり、私たちは静かな水路に入った。 月は依然として明るく輝いていた。',
        '私たちは運河を下り続け、市場から離れていった。周りの船も次第に少なくなり、私たちは静かな水路に入った。\n\n月は依然として明るく輝いていた。'
    )

    # Separate worry about people
    content = content.replace(
        'その光が水面に反射し、銀色の道を作っていた。両岸には高い草が生え、時々、夜行性の鳥の鳴き声が聞こえた。 「おばさん、市場の人たちは無事でしょうか?」私は心配して尋ねた。 「きっと大丈夫だ」おばさんが言った。',
        'その光が水面に反射し、銀色の道を作っていた。両岸には高い草が生え、時々、夜行性の鳥の鳴き声が聞こえた。\n\n「おばさん、市場の人たちは無事でしょうか?」私は心配して尋ねた。\n\n「きっと大丈夫だ」おばさんが言った。'
    )

    # Separate reflection
    content = content.replace(
        '「みんな逃げる準備をしていたからね。この戦争では、私たちは常に準備をしていなければならないんだ」 私は静かに座り、過ぎ去る風景を見ていた。',
        '「みんな逃げる準備をしていたからね。この戦争では、私たちは常に準備をしていなければならないんだ」\n\n私は静かに座り、過ぎ去る風景を見ていた。'
    )

    # Separate sleep instruction
    content = content.replace(
        'ほんの数時間前まで、私は市場での平和な生活に慣れていたのに、今は再び逃亡者になっていた。 「坊や、眠りなさい」おばさんが言った。',
        'ほんの数時間前まで、私は市場での平和な生活に慣れていたのに、今は再び逃亡者になっていた。\n\n「坊や、眠りなさい」おばさんが言った。'
    )

    # Separate lying down
    content = content.replace(
        '「まだ長い道のりだ。力を蓄えておかなければ」 私は船底に横になった。',
        '「まだ長い道のりだ。力を蓄えておかなければ」\n\n私は船底に横になった。'
    )

    # Separate realization section
    content = content.replace(
        '小さな蛇の籠を抱きしめながら、揺れる船の上で目を閉じた。遠くで、まだ市場が燃えている光が見えた。\n\nその夜、私は戦争の恐ろしさを初めて本当に理解した。',
        '小さな蛇の籠を抱きしめながら、揺れる船の上で目を閉じた。遠くで、まだ市場が燃えている光が見えた。\n\nその夜、私は戦争の恐ろしさを初めて本当に理解した。'
    )

    # Separate hope section
    content = content.replace(
        'それは銃や爆弾だけではない。それは家を失うこと、安全を失うこと、そして再び不確実な未来に向かって旅立たなければならないことだった。 だが、トゥ・ベオおばさんの優しさと、小さな蛇の存在が、私に勇気を与えてくれた。',
        'それは銃や爆弾だけではない。それは家を失うこと、安全を失うこと、そして再び不確実な未来に向かって旅立たなければならないことだった。\n\nだが、トゥ・ベオおばさんの優しさと、小さな蛇の存在が、私に勇気を与えてくれた。'
    )

    # Separate journey continues
    content = content.replace(
        '私はまだ一人ではなかった。そして、どこかで、父が私を待っているかもしれなかった。 船は静かに南へ向かって進み続けた。',
        '私はまだ一人ではなかった。そして、どこかで、父が私を待っているかもしれなかった。\n\n船は静かに南へ向かって進み続けた。'
    )

    # Separate dawn section
    content = content.replace(
        '月明かりの下で、私たちの旅は続いていった。 夜明け前、私は船の揺れで目を覚ました。',
        '月明かりの下で、私たちの旅は続いていった。\n\n夜明け前、私は船の揺れで目を覚ました。'
    )

    # Separate offering to row
    content = content.replace(
        '空はまだ暗かったが、東の空がわずかに明るくなり始めていた。トゥ・ベオおばさんは依然として櫓を漕ぎ続けていた。 「おばさん、僕も漕ぎましょうか?」私は申し出た。 「いいや、もう少しで休憩する場所に着くよ」おばさんが答えた。 果たして、まもなく私たちは小さな入り江に入った。',
        '空はまだ暗かったが、東の空がわずかに明るくなり始めていた。トゥ・ベオおばさんは依然として櫓を漕ぎ続けていた。\n\n「おばさん、僕も漕ぎましょうか?」私は申し出た。\n\n「いいや、もう少しで休憩する場所に着くよ」おばさんが答えた。\n\n果たして、まもなく私たちは小さな入り江に入った。'
    )

    # Separate rest stop
    content = content.replace(
        'そこには数軒の家が水辺に建っていた。他の逃げ舟もそこで休んでいた。 私たちは船を岸に寄せ、しばらく休憩することにした。',
        'そこには数軒の家が水辺に建っていた。他の逃げ舟もそこで休んでいた。\n\n私たちは船を岸に寄せ、しばらく休憩することにした。'
    )

    # Separate breakfast
    content = content.replace(
        'おばさんは持ってきた食料を取り出し、私たちは簡単な朝食を取った。 「これからどうするんですか?」私は尋ねた。 「まず、親戚の村まで行く」おばさんが言った。',
        'おばさんは持ってきた食料を取り出し、私たちは簡単な朝食を取った。\n\n「これからどうするんですか?」私は尋ねた。\n\n「まず、親戚の村まで行く」おばさんが言った。'
    )

    # Separate gratitude
    content = content.replace(
        '「そこで少し落ち着いたら、お前の父親を探す手伝いをするよ」\n\n私は感謝の気持ちでいっぱいになった。',
        '「そこで少し落ち着いたら、お前の父親を探す手伝いをするよ」\n\n私は感謝の気持ちでいっぱいになった。'
    )

    # Separate final reflection
    content = content.replace(
        'この混乱の中でも、人々の優しさは失われていなかった。 太陽が昇り始め、新しい一日が始まろうとしていた。',
        'この混乱の中でも、人々の優しさは失われていなかった。\n\n太陽が昇り始め、新しい一日が始まろうとしていた。'
    )

    content = content.replace(
        '恐ろしい夜は過ぎ去り、私たちは生き延びた。これからも、旅は続く。だが、私は一人ではない。そして、それが何よりも大切なことだった。',
        '恐ろしい夜は過ぎ去り、私たちは生き延びた。\n\nこれからも、旅は続く。だが、私は一人ではない。そして、それが何よりも大切なことだった。'
    )

    return content

def main():
    """Align and refine Japanese chapter 4"""
    ja_filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-ja-4.json'

    print(f"Reading {ja_filepath}...")
    with open(ja_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_content = data['content']
    original_count = len([p for p in original_content.split('\n\n') if p.strip()])

    print("Aligning paragraphs and refining literary quality...")
    improved_content = align_and_refine(original_content)
    new_count = len([p for p in improved_content.split('\n\n') if p.strip()])

    if original_content != improved_content:
        data['content'] = improved_content
        print(f"Writing improved content...")
        with open(ja_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Japanese Chapter 4 improved")
        print(f"  Paragraphs: {original_count} → {new_count} (+{new_count - original_count})")
        print(f"\nLiterary improvements:")
        print(f"  - フランス軍だ → フランスの奴らだ")
        print(f"  - 貴重品 → 家財道具")
        print(f"  - オレンジ色の炎 → 紅蓮の炎")
        print(f"  - 櫂 → 櫓")
        print(f"  - 避難船 → 逃げ舟")
        print(f"  - 坊や!こっちだ! → 坊ず！こっちへおいで！早く！")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
