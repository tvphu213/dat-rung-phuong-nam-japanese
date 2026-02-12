#!/usr/bin/env python3
"""Standardize Võ Tòng character name to 武松 (kanji) across all chapters"""

import json
from pathlib import Path
import re

def standardize_name(content):
    """Replace all katakana variations with 武松"""
    # Replace ヴォー・トン (with long vowel mark)
    content = content.replace('ヴォー・トン', '武松')

    # Replace ヴォ・トン (without long vowel mark)
    content = content.replace('ヴォ・トン', '武松')

    return content

def main():
    """Standardize Võ Tòng name across all chapters"""
    chapters_dir = Path(__file__).parent / 'chapters' / 'json'

    # Find all chapters that contain either variation
    affected_chapters = []

    for chapter_file in sorted(chapters_dir.glob('chapter-ja-*.json')):
        with open(chapter_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        original_content = data['content']
        original_title = data.get('title', '')

        # Check if this chapter contains either variation in content or title
        if ('ヴォー・トン' in original_content or 'ヴォ・トン' in original_content or
            'ヴォー・トン' in original_title or 'ヴォ・トン' in original_title):
            affected_chapters.append(chapter_file)

            # Standardize to 武松 in both content and title
            new_content = standardize_name(original_content)
            new_title = standardize_name(original_title)

            # Count replacements
            count_long = original_content.count('ヴォー・トン') + original_title.count('ヴォー・トン')
            count_short = original_content.count('ヴォ・トン') + original_title.count('ヴォ・トン')

            # Update the file
            data['content'] = new_content
            if original_title != new_title:
                data['title'] = new_title
            with open(chapter_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"✓ {chapter_file.name}")
            if count_long > 0:
                print(f"  - Replaced {count_long} instances of ヴォー・トン → 武松")
            if count_short > 0:
                print(f"  - Replaced {count_short} instances of ヴォ・トン → 武松")

    print(f"\n✓ Standardized {len(affected_chapters)} chapters")
    print(f"All instances now use: 武松 (Võ Tòng - from Water Margin 水滸傳)")

if __name__ == '__main__':
    main()
