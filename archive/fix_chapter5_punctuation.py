#!/usr/bin/env python3
"""Fix punctuation errors in chapter-5.json"""

import json
from pathlib import Path

def fix_punctuation(content):
    """Fix all punctuation issues in content"""

    # Fix 1: Remove space before period
    content = content.replace(
        'vẫn buồn . Cái hy vọng',
        'vẫn buồn. Cái hy vọng'
    )

    # Fix 2: Fix double period
    content = content.replace(
        'nước mắt. .',
        'nước mắt.'
    )

    # Fix 3: Fix "Lần .đầu" to "Lần đầu"
    content = content.replace(
        'Lần .đầu tiên',
        'Lần đầu tiên'
    )

    # Fix 4: Remove space before period
    content = content.replace(
        'độc lập rồi? . Thằng An',
        'độc lập rồi? Thằng An'
    )

    # Fix 5: Fix lowercase after period
    content = content.replace(
        'như vậy Tôi không muốn',
        'như vậy. Tôi không muốn'
    )

    # Fix 6: Fix "độc !ập" to "độc lập"
    content = content.replace(
        'độc !ập',
        'độc lập'
    )

    # Fix 7: Remove space before period
    content = content.replace(
        'có một không hai đó . Thực ra',
        'có một không hai đó. Thực ra'
    )

    # Fix 8: Remove space before period
    content = content.replace(
        'như giặc tới vậy? . Má tôi',
        'như giặc tới vậy? Má tôi'
    )

    # Fix 9: Fix double period
    content = content.replace(
        'pập pập. . một tràng dài',
        'pập pập. Một tràng dài'
    )

    # Fix 10: Remove space before period
    content = content.replace(
        'ghê rợn . Trẻ con',
        'ghê rợn. Trẻ con'
    )

    # Fix 11: Fix "nổi.lên"
    content = content.replace(
        'nổi.lên dồn dập Ở chỗ',
        'nổi lên dồn dập ở chỗ'
    )

    # Fix 12: Add comma
    content = content.replace(
        'yêu nước yêu độc lập',
        'yêu nước, yêu độc lập'
    )

    # Fix 13: Fix double period
    content = content.replace(
        'tiếng nổ . . Đùng',
        'tiếng nổ. Đùng'
    )

    # Fix 14: Remove space before period
    content = content.replace(
        'Trẻ con thì không phải nói . Chúng nó',
        'Trẻ con thì không phải nói. Chúng nó'
    )

    # Fix 15: Remove space before period
    content = content.replace(
        'lòe lên . Má tôi',
        'lòe lên. Má tôi'
    )

    # Fix 16: Remove space before period
    content = content.replace(
        'khua lách . Ngựa nhảy',
        'khua lách. Ngựa nhảy'
    )

    # Fix 17: Fix double period
    content = content.replace(
        'kêu khóc. . Tất cả',
        'kêu khóc. Tất cả'
    )

    # Fix 18: Add missing space
    content = content.replace(
        'cần thiết,ông vất',
        'cần thiết, ông vất'
    )

    # Fix 19: Fix "tài sản .quí báu"
    content = content.replace(
        'tài sản .quí báu',
        'tài sản quí báu'
    )

    # Fix 20: Add period after "giận má tôi"
    content = content.replace(
        'giận má tôi Đến chai',
        'giận má tôi. Đến chai'
    )

    # Fix 21: Remove space before period
    content = content.replace(
        'trở tay" . Một tiếng',
        'trở tay". Một tiếng'
    )

    # Fix 22: Fix "ơil" to "ơi!"
    content = content.replace(
        'bà con ơil',
        'bà con ơi!'
    )

    # Fix 23: Remove space before period
    content = content.replace(
        'nhất . Thôi',
        'nhất. Thôi'
    )

    # Fix 24: Fix double period
    content = content.replace(
        'giùm tôi. .',
        'giùm tôi.'
    )

    # Fix 25: Fix double period
    content = content.replace(
        'Đi đi. . nước mất',
        'Đi đi. Nước mất'
    )

    # Fix 26: Fix missing space after period
    content = content.replace(
        'dừng lại.ngủ giữa',
        'dừng lại. Ngủ giữa'
    )

    # Fix 27: Add period after "không"
    content = content.replace(
        'có gặp không Tôi trượt',
        'có gặp không. Tôi trượt'
    )

    # Fix 28: Add period after "đâu"
    content = content.replace(
        'mình đi đâu Đến một ngã ba',
        'mình đi đâu. Đến một ngã ba'
    )

    # Fix 29: Fix comma to period
    content = content.replace(
        'mưa. Trời lại lấc',
        'mưa. Trời lại lấc'
    )

    # Fix 30: Fix double period
    content = content.replace(
        'ngang qua. . Tôi đã',
        'ngang qua. Tôi đã'
    )

    return content

def main():
    """Fix chapter-5.json"""
    filepath = Path(__file__).parent / 'chapters' / 'json' / 'chapter-5.json'

    print(f"Reading {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("Fixing punctuation...")
    original_content = data['content']
    fixed_content = fix_punctuation(original_content)

    if original_content != fixed_content:
        data['content'] = fixed_content
        print(f"Writing fixed content...")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✓ Fixed chapter-5.json")
    else:
        print("- No changes needed")

if __name__ == '__main__':
    main()
