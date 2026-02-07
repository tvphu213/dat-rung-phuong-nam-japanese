"""Validate Japanese text quality in Đất Rừng Phương Nam translation chapters.

Validates Japanese chapter files by checking for proper Japanese character
presence (hiragana, katakana, kanji) and detecting garbled/replacement
characters. Generates quality reports for Japanese translations.

Usage:
    python validate_japanese.py
    python validate_japanese.py --chapters-dir chapters/ja
    python validate_japanese.py --chapters-dir chapters/ja --output-report report.json
    python validate_japanese.py --dry-run
    python validate_japanese.py --help
"""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import pathlib
import re
import sys

logger = logging.getLogger(__name__)

# Script metadata
SCRIPT_VERSION = "1.0.0"

# Default paths relative to this script's location
SCRIPT_DIR = pathlib.Path(__file__).parent
DEFAULT_CHAPTERS_DIR = SCRIPT_DIR / "chapters" / "ja"
DEFAULT_OUTPUT_REPORT = SCRIPT_DIR / "japanese-quality-report.json"

# ---------------------------------------------------------------------------
# Japanese character detection
# ---------------------------------------------------------------------------

# Japanese character ranges (hiragana, katakana, kanji).  Used to verify
# that translation contains proper Japanese text.
#
# Character ranges:
#   Hiragana: U+3040-U+309F  – Basic Japanese phonetic script
#   Katakana: U+30A0-U+30FF  – Japanese phonetic script for foreign words
#   Kanji:    U+4E00-U+9FFF  – Chinese characters used in Japanese
#
# This pattern matches any single Japanese character from these ranges.
JAPANESE_CHARS_RE = re.compile(
    r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]"
)

# Garbled / problematic characters: U+FFFD (replacement character) and
# ASCII control characters (excluding tab, newline, carriage return).
# This pattern is reused from convert.py for consistency.
GARBLED_CHARS_RE = re.compile(r"[\ufffd\x00-\x08\x0b\x0c\x0e-\x1f]")

# Minimum character count for a chapter to be considered non-empty.
_MIN_CHAPTER_CHARS = 100

# Minimum Japanese character count for content to be considered valid Japanese.
_MIN_JAPANESE_CHARS = 50

# Fraction threshold: chapters below this fraction of the median length
# are flagged as suspiciously short.
_SHORT_CHAPTER_FRACTION = 0.5


# ---------------------------------------------------------------------------
# Japanese validation
# ---------------------------------------------------------------------------


def validate_japanese_chapter(chapter_text: str, chapter_title: str) -> dict:
    """Validate a single Japanese chapter's translation quality.

    Checks:
    1. Non-empty content (at least ``_MIN_CHAPTER_CHARS`` characters).
    2. Japanese characters present (at least ``_MIN_JAPANESE_CHARS``).
    3. No garbled / replacement characters.

    Args:
        chapter_text: The Japanese chapter body text.
        chapter_title: Chapter title for log messages.

    Returns:
        Dict with keys ``valid`` (bool), ``issues`` (list of str),
        ``char_count`` (int), ``japanese_char_count`` (int),
        ``garbled_count`` (int).
    """
    issues: list[str] = []

    char_count = len(chapter_text.strip())
    japanese_char_count = len(JAPANESE_CHARS_RE.findall(chapter_text))
    garbled_count = len(GARBLED_CHARS_RE.findall(chapter_text))

    # Check 1: Non-empty content
    if char_count < _MIN_CHAPTER_CHARS:
        issues.append(
            f"Suspiciously short content ({char_count} chars, "
            f"minimum {_MIN_CHAPTER_CHARS})"
        )

    # Check 2: Japanese characters present
    if japanese_char_count < _MIN_JAPANESE_CHARS:
        issues.append(
            f"Very few Japanese characters ({japanese_char_count}, "
            f"minimum {_MIN_JAPANESE_CHARS})"
        )

    # Check 3: No garbled / replacement characters
    if garbled_count > 0:
        issues.append(
            f"{garbled_count} garbled/replacement character(s) found"
        )

    for issue in issues:
        logger.warning("Chapter '%s': %s", chapter_title, issue)

    return {
        "title": chapter_title,
        "valid": len(issues) == 0,
        "issues": issues,
        "char_count": char_count,
        "japanese_char_count": japanese_char_count,
        "garbled_count": garbled_count,
    }
