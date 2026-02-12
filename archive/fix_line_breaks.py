#!/usr/bin/env python3
"""
Fix incorrect line breaks in Vietnamese JSON chapter files.
Replaces double newlines that split words/phrases incorrectly.
"""

import json
import re
from pathlib import Path

def fix_content(content):
    """Fix line break errors in content"""
    # Known specific fixes for proper nouns and common patterns
    fixes = [
        # Geography / Proper nouns
        (r'Thái\n\nLan', 'Thái Lan'),
        (r'VÕ\n\nTòng', 'VÕ Tòng'),
        (r'Đạo\n\nNgạn', 'Đạo Ngạn'),

        # Common sentence patterns (word at end of sentence + word starting new sentence)
        # These should have space, not paragraph break
        (r'vậy\n\nTôi', 'vậy Tôi'),
        (r'gì\n\nTôi', 'gì Tôi'),
        (r'được\n\nTôi', 'được Tôi'),
        (r'không\n\nKhông', 'không Không'),
        (r'giặc\n\nKhông', 'giặc Không'),
        (r'giặc\n\nAi', 'giặc Ai'),
        (r'chết\n\nNước', 'chết Nước'),
        (r'đoạt\n\nngười', 'đoạt người'),
        (r'Hai\n\nđã', 'Hai đã'),
        (r'tôi\n\nđã', 'tôi đã'),

        # Pattern: lowercase word + \n\n + uppercase word (likely sentence boundary error)
        # We'll handle these with regex
    ]

    result = content
    for pattern, replacement in fixes:
        result = re.sub(pattern, replacement, result)

    # Generic pattern: single lowercase Vietnamese word/syllable followed by \n\n and capitalized word
    # This is likely an incorrect paragraph break in the middle of a sentence
    # Vietnamese syllables are typically 2-10 characters
    result = re.sub(r'([a-zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]{2,10})\n\n([A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ])', r'\1 \2', result)

    return result

def fix_file(filepath):
    """Fix line breaks in a single JSON file"""
    print(f"Processing {filepath.name}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_content = data['content']
    fixed_content = fix_content(original_content)

    if original_content != fixed_content:
        data['content'] = fixed_content
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Fixed {filepath.name}")
        return True
    else:
        print(f"  - No changes needed for {filepath.name}")
        return False

def main():
    """Fix all Vietnamese chapter JSON files"""
    json_dir = Path(__file__).parent / 'chapters' / 'json'

    # Process all Vietnamese chapter files (chapter-1.json through chapter-20.json)
    fixed_count = 0
    for i in range(1, 21):
        filepath = json_dir / f'chapter-{i}.json'
        if filepath.exists():
            if fix_file(filepath):
                fixed_count += 1
        else:
            print(f"Warning: {filepath.name} not found")

    print(f"\n✓ Complete! Fixed {fixed_count} files.")

if __name__ == '__main__':
    main()
