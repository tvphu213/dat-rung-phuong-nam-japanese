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
