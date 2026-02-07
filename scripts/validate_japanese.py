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


def validate_japanese_chapters(chapters_dir: pathlib.Path) -> dict:
    """Run quality validation on all Japanese chapter files and produce a report.

    Reads all ``.md`` chapter files from the specified directory, validates
    each one via :func:`validate_japanese_chapter`, and aggregates results.
    In addition to per-chapter checks, this function flags suspiciously short
    chapters (below ``_SHORT_CHAPTER_FRACTION`` of the median chapter size).

    Args:
        chapters_dir: Path to directory containing Japanese chapter .md files.

    Returns:
        Quality report dict with ``chapters`` (list of per-chapter results),
        ``summary`` (aggregate statistics), and ``timestamp`` (ISO-8601).
        Each chapter result includes ``filename``, ``valid``, ``issues``,
        ``char_count``, ``japanese_char_count``, and ``garbled_count``.
    """
    # Find all .md files in chapters directory
    if not chapters_dir.exists():
        logger.error("Chapters directory does not exist: %s", chapters_dir)
        return {
            "script_version": SCRIPT_VERSION,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "chapters": [],
            "summary": {
                "total_chapters": 0,
                "valid_chapters": 0,
                "invalid_chapters": 0,
                "total_issues": 0,
                "total_characters": 0,
                "total_japanese_chars": 0,
                "total_garbled": 0,
            },
            "error": f"Chapters directory not found: {chapters_dir}",
        }

    chapter_files = sorted(chapters_dir.glob("*.md"))
    if not chapter_files:
        logger.warning("No .md files found in: %s", chapters_dir)

    logger.info("Found %d chapter file(s) in: %s", len(chapter_files), chapters_dir)

    # Per-chapter validation
    chapter_results: list[dict] = []
    for chapter_file in chapter_files:
        try:
            chapter_text = chapter_file.read_text(encoding="utf-8")
            # Extract title from filename (e.g. "01-chuong-1.md" → "01-chuong-1")
            title = chapter_file.stem
            result = validate_japanese_chapter(chapter_text, title)
            result["filename"] = chapter_file.name
            chapter_results.append(result)
            logger.info(
                "Validated '%s': %s (%d chars, %d Japanese chars)",
                chapter_file.name,
                "VALID" if result["valid"] else "INVALID",
                result["char_count"],
                result["japanese_char_count"],
            )
        except Exception as exc:
            logger.error("Failed to read/validate '%s': %s", chapter_file.name, exc)
            chapter_results.append({
                "filename": chapter_file.name,
                "title": chapter_file.stem,
                "valid": False,
                "issues": [f"Failed to read file: {exc}"],
                "char_count": 0,
                "japanese_char_count": 0,
                "garbled_count": 0,
            })

    # Detect suspiciously short chapters relative to the median
    char_counts = [r["char_count"] for r in chapter_results if r["char_count"] > 0]
    if char_counts:
        sorted_counts = sorted(char_counts)
        median_chars = sorted_counts[len(sorted_counts) // 2]
        threshold = max(_MIN_CHAPTER_CHARS, median_chars * _SHORT_CHAPTER_FRACTION)

        for result in chapter_results:
            if (
                result["char_count"] > 0
                and result["char_count"] < threshold
                and result["valid"]
            ):
                issue = (
                    f"Short relative to median "
                    f"({result['char_count']} chars vs median {median_chars})"
                )
                result["issues"].append(issue)
                result["valid"] = False
                logger.warning("Chapter '%s': %s", result["title"], issue)

    # Aggregate statistics
    total_valid = sum(1 for r in chapter_results if r["valid"])
    total_issues = sum(len(r["issues"]) for r in chapter_results)
    total_chars = sum(r["char_count"] for r in chapter_results)
    total_japanese = sum(r["japanese_char_count"] for r in chapter_results)
    total_garbled = sum(r["garbled_count"] for r in chapter_results)

    report = {
        "script_version": SCRIPT_VERSION,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "chapters": chapter_results,
        "summary": {
            "total_chapters": len(chapter_results),
            "valid_chapters": total_valid,
            "invalid_chapters": len(chapter_results) - total_valid,
            "total_issues": total_issues,
            "total_characters": total_chars,
            "total_japanese_chars": total_japanese,
            "total_garbled": total_garbled,
        },
    }

    logger.info(
        "Validation complete: %d/%d chapters valid, %d total issues",
        total_valid,
        len(chapter_results),
        total_issues,
    )

    return report


def print_japanese_quality_summary(report: dict) -> None:
    """Print a human-readable Japanese quality validation summary to stdout.

    Displays per-chapter validation status, summary statistics, and
    Japanese character metrics in a formatted table.

    Args:
        report: Quality report dict from :func:`validate_japanese_chapters`.
    """
    summary = report["summary"]
    chapters = report["chapters"]

    print(f"\n{'=' * 75}")
    print(f"  JAPANESE QUALITY VALIDATION REPORT  (v{report.get('script_version', '?')})")
    print(f"{'=' * 75}")
    print(f"  Timestamp: {report.get('timestamp', 'N/A')}")
    print()

    # Per-chapter table
    print(f"  {'#':<5} {'Status':<8} {'Title':<30} {'Chars':>10} {'JP Chars':>10}")
    print(f"  {'-' * 5} {'-' * 8} {'-' * 30} {'-' * 10} {'-' * 10}")
    for i, ch in enumerate(chapters):
        status = "✓ OK" if ch["valid"] else "✗ FAIL"
        title = ch["title"][:29] if len(ch["title"]) > 29 else ch["title"]
        print(
            f"  {i:<5} {status:<8} {title:<30} "
            f"{ch['char_count']:>10,} {ch['japanese_char_count']:>10,}"
        )
        for issue in ch["issues"]:
            print(f"         ↳ {issue}")

    # Summary
    print(f"\n  {'─' * 75}")
    print(f"  Chapters:        {summary['total_chapters']} total, "
          f"{summary['valid_chapters']} valid, "
          f"{summary['invalid_chapters']} with issues")
    print(f"  Characters:      {summary['total_characters']:,} total")
    print(f"  Japanese chars:  {summary['total_japanese_chars']:,}")
    if summary["total_garbled"] > 0:
        print(f"  ⚠ Garbled:       {summary['total_garbled']} replacement/control chars found")

    # Overall verdict
    all_valid = summary["invalid_chapters"] == 0
    print(f"\n  {'─' * 75}")
    if all_valid:
        print("  ✓ ALL CHAPTERS PASSED JAPANESE VALIDATION")
    else:
        print(f"  ✗ {summary['invalid_chapters']} CHAPTER(S) HAVE ISSUES")
    print(f"{'=' * 75}\n")


def setup_logging(verbose: bool = False) -> None:
    """Configure logging with appropriate level and format."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Argument list (defaults to sys.argv[1:]).

    Returns:
        Parsed argument namespace.
    """
    parser = argparse.ArgumentParser(
        description="Validate Japanese text quality in Đất Rừng Phương Nam translation chapters.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python validate_japanese.py\n"
            "  python validate_japanese.py --chapters-dir chapters/ja\n"
            "  python validate_japanese.py --chapters-dir chapters/ja --output-report report.json\n"
            "  python validate_japanese.py --dry-run --verbose\n"
        ),
    )
    parser.add_argument(
        "--chapters-dir",
        type=pathlib.Path,
        default=DEFAULT_CHAPTERS_DIR,
        help=f"Directory containing Japanese chapter .md files (default: {DEFAULT_CHAPTERS_DIR})",
    )
    parser.add_argument(
        "--output-report",
        type=pathlib.Path,
        default=DEFAULT_OUTPUT_REPORT,
        help=f"Path for JSON quality report output (default: {DEFAULT_OUTPUT_REPORT})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run validation but do not write report file",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable debug-level logging",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Entry point for Japanese quality validation.

    Args:
        argv: Optional argument list for testing.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    args = parse_args(argv)
    setup_logging(verbose=args.verbose)

    logger.info("Starting Japanese quality validation")
    logger.info("Chapters directory: %s", args.chapters_dir)
    if args.dry_run:
        logger.info("Mode: DRY RUN (no report file will be written)")

    # Run validation
    quality_report = validate_japanese_chapters(args.chapters_dir)

    # Check for error condition
    if "error" in quality_report:
        logger.error("Validation failed: %s", quality_report["error"])
        return 1

    # Write report file (unless dry-run)
    if not args.dry_run:
        args.output_report.parent.mkdir(parents=True, exist_ok=True)
        args.output_report.write_text(
            json.dumps(quality_report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        logger.info("Quality report written to %s", args.output_report)

    # Print human-readable summary to stdout
    print_japanese_quality_summary(quality_report)

    summary = quality_report["summary"]
    logger.info(
        "Validation complete: %d/%d chapters valid",
        summary["valid_chapters"],
        summary["total_chapters"],
    )

    # Return non-zero exit code if any chapters failed validation
    return 1 if summary["invalid_chapters"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
