#!/usr/bin/env python3
"""Fix all Japanese chapters 2-20: Remove HTML tags and add proper paragraph breaks"""

import json
import re
from pathlib import Path

def fix_japanese_formatting(content):
    """Remove HTML tags and add proper paragraph breaks"""
    # Remove all <p> and </p> tags
    content = content.replace('<p>', '')
    content = content.replace('</p>', '\n\n')

    # Clean up any trailing whitespace
    content = content.strip()

    # Fix multiple consecutive newlines (more than 2)
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content

def main():
    """Fix Japanese chapters 2-20"""
    chapters_dir = Path(__file__).parent / 'chapters' / 'json'

    results = []

    for chapter_num in range(2, 21):
        filepath = chapters_dir / f'chapter-ja-{chapter_num}.json'

        if not filepath.exists():
            print(f'⚠️  Chapter {chapter_num}: File not found')
            continue

        print(f'Processing Chapter {chapter_num}...')

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        original_content = data['content']

        # Check if it needs fixing
        if '<p>' not in original_content:
            print(f'  ✓ Chapter {chapter_num}: Already clean, skipping')
            continue

        # Fix formatting
        fixed_content = fix_japanese_formatting(original_content)

        if original_content != fixed_content:
            data['content'] = fixed_content

            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # Statistics
            p_tags_before = original_content.count('<p>')
            breaks_after = fixed_content.count('\n\n')

            result = f'  ✓ Chapter {chapter_num:2d}: {p_tags_before:3d} <p> tags → {breaks_after:3d} paragraph breaks'
            print(result)
            results.append((chapter_num, p_tags_before, breaks_after))
        else:
            print(f'  - Chapter {chapter_num}: No changes needed')

    # Summary
    print('\n' + '='*60)
    print('SUMMARY:')
    print('='*60)
    for chapter_num, p_tags, breaks in results:
        print(f'Chapter {chapter_num:2d}: {p_tags:3d} <p> → {breaks:3d} \\n\\n')
    print(f'\nTotal chapters fixed: {len(results)}')

if __name__ == '__main__':
    main()
