"""Convert Đất Rừng Phương Nam PDF to Markdown chapter files.

Extracts text from the source PDF using pymupdf4llm, detects chapter
boundaries, splits into per-chapter Markdown files, and runs quality
validation on the output.

Usage:
    python convert.py
    python convert.py --input path/to/file.pdf --output-dir chapters
    python convert.py --dry-run
    python convert.py --help
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime
import json
import logging
import pathlib
import re
import sys

import pymupdf4llm

logger = logging.getLogger(__name__)

# Script metadata
SCRIPT_VERSION = "1.0.0"

# Default paths relative to this script's location
SCRIPT_DIR = pathlib.Path(__file__).parent
DEFAULT_PDF_PATH = SCRIPT_DIR / "517016593-ĐẤT-RỪNG-PHƯƠNG-NAM.pdf"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "chapters"

# ---------------------------------------------------------------------------
# Chapter detection
# ---------------------------------------------------------------------------

# Regex patterns for Vietnamese chapter headers.  The patterns are tried in
# order; the first branch that matches wins.  All matching is case-insensitive
# so "Chương" and "CHƯƠNG" are handled uniformly.
#
# Supported formats:
#   Chương 1 / Chương 12          – Arabic numerals
#   CHƯƠNG IV / Chương IX          – Roman numerals
#   Chương một / Chương mười hai   – Vietnamese number words
#
# The regex captures:
#   group "label"  – full matched header text (e.g. "Chương 3")
#   group "num"    – the numeric/roman/word token following "Chương"
_VIET_NUMBER_WORDS = (
    r"một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười"
    r"|mười\s+một|mười\s+hai|mười\s+ba|mười\s+bốn|mười\s+năm"
    r"|mười\s+sáu|mười\s+bảy|mười\s+tám|mười\s+chín"
    r"|hai\s+mươi|hai\s+mươi\s+\w+"
    r"|ba\s+mươi|ba\s+mươi\s+\w+"
)

CHAPTER_HEADER_RE = re.compile(
    r"(?P<label>"
    r"[Cc][Hh][Ưư][Ơơ][Nn][Gg]"       # "Chương" in any case
    r"\s+"
    r"(?P<num>"
    r"\d+"                               # Arabic numerals
    r"|[IVXLCDM]+"                       # Roman numerals (uppercase)
    r"|" + _VIET_NUMBER_WORDS +          # Vietnamese number words
    r")"
    r")",
    re.IGNORECASE,
)

# Secondary pattern: bold / heading Markdown artefacts that pymupdf4llm may
# wrap around chapter headers (e.g. "## Chương 3" or "**Chương 3**").
# We strip these when extracting the clean title.
_MD_HEADING_PREFIX_RE = re.compile(r"^#{1,6}\s*")
_MD_BOLD_RE = re.compile(r"\*{1,2}(.*?)\*{1,2}")


@dataclasses.dataclass
class Chapter:
    """A single detected chapter with its content boundaries."""

    index: int          # 0-based sequential index
    title: str          # Cleaned chapter title (may be multi-line)
    start: int          # Character offset in full_text (inclusive)
    end: int            # Character offset in full_text (exclusive)

    @property
    def body(self) -> str:
        """Return placeholder; actual text is sliced externally."""
        return ""

    @property
    def char_count(self) -> int:
        return self.end - self.start


def _clean_title(raw: str) -> str:
    """Strip Markdown artefacts from a chapter title line.

    Removes leading ``#`` heading markers and surrounding ``**`` bold markers
    while preserving the actual title text.
    """
    title = _MD_HEADING_PREFIX_RE.sub("", raw).strip()
    # Unwrap bold markers: **Chương 1** → Chương 1
    bold_match = _MD_BOLD_RE.fullmatch(title)
    if bold_match:
        title = bold_match.group(1).strip()
    return title


def _extract_multiline_title(full_text: str, header_end: int, max_extra_lines: int = 2) -> str:
    """Capture additional title lines immediately following the chapter header.

    Some chapters have a subtitle on the next line(s).  We greedily grab up to
    *max_extra_lines* non-blank lines that look like title continuations (short
    and not starting a paragraph).

    Args:
        full_text: The entire document text.
        header_end: Character offset right after the chapter header match.
        max_extra_lines: Maximum number of continuation lines to absorb.

    Returns:
        The extra title text (may be empty string).
    """
    extra_parts: list[str] = []
    pos = header_end

    for _ in range(max_extra_lines):
        # Skip a single newline
        if pos < len(full_text) and full_text[pos] == "\n":
            pos += 1
        # Read next line
        line_end = full_text.find("\n", pos)
        if line_end == -1:
            line_end = len(full_text)
        line = full_text[pos:line_end].strip()

        # A continuation line must be non-empty, relatively short (<120 chars),
        # and not look like a regular paragraph start (no lowercase first word
        # following normal sentence structure – heuristic).
        if not line or len(line) > 120:
            break
        # If the line contains a new chapter header, stop
        if CHAPTER_HEADER_RE.search(line):
            break
        # If line looks like body text (starts lowercase and is long), stop
        if len(line) > 60 and line[0].islower():
            break

        extra_parts.append(_clean_title(line))
        pos = line_end + 1

    return " — ".join(extra_parts) if extra_parts else ""


def detect_chapters(full_text: str) -> list[Chapter]:
    """Detect chapter boundaries in the full document text.

    Strategy:
    1. Find all matches of ``CHAPTER_HEADER_RE`` in *full_text*.
    2. Any text before the first match is treated as a **prologue**.
    3. Any text after the last chapter header (beyond expected body) is kept
       as part of the last chapter (epilogue content is not split separately
       unless a clear header is found).
    4. Multi-line titles are captured via ``_extract_multiline_title``.

    Args:
        full_text: Combined Markdown text of the entire PDF.

    Returns:
        Ordered list of :class:`Chapter` objects.  The list is never empty;
        if no chapter headers are found the entire text is returned as a
        single "Full Document" chapter.
    """
    matches = list(CHAPTER_HEADER_RE.finditer(full_text))

    if not matches:
        logger.warning("No chapter headers detected – returning full document as single chapter")
        return [
            Chapter(index=0, title="Full Document", start=0, end=len(full_text)),
        ]

    chapters: list[Chapter] = []

    # --- Prologue (text before the first chapter header) ---
    first_match_start = matches[0].start()
    prologue_text = full_text[:first_match_start].strip()
    if len(prologue_text) > 200:
        # Only create a prologue chapter if there is substantial content
        chapters.append(
            Chapter(index=0, title="Lời mở đầu", start=0, end=first_match_start)
        )
        logger.info("Prologue detected: %d characters", first_match_start)

    # --- Regular chapters ---
    for i, match in enumerate(matches):
        # Determine where this chapter's content ends
        if i + 1 < len(matches):
            chapter_end = matches[i + 1].start()
        else:
            chapter_end = len(full_text)

        # Build the title from the header match + optional continuation lines
        header_line_end = full_text.find("\n", match.end())
        if header_line_end == -1:
            header_line_end = len(full_text)

        raw_header_line = full_text[match.start():header_line_end]
        title = _clean_title(raw_header_line)

        extra_title = _extract_multiline_title(full_text, header_line_end)
        if extra_title:
            title = f"{title} — {extra_title}"

        chapter_index = len(chapters)
        chapters.append(
            Chapter(
                index=chapter_index,
                title=title,
                start=match.start(),
                end=chapter_end,
            )
        )

    logger.info("Detected %d chapter(s) (including prologue)" if chapters[0].title == "Lời mở đầu"
                else "Detected %d chapter(s)", len(chapters))

    return chapters


def print_chapter_summary(chapters: list[Chapter], full_text: str) -> None:
    """Print a human-readable summary of detected chapters.

    Used by ``--dry-run`` to show what would be generated without writing files.

    Args:
        chapters: List of detected chapters.
        full_text: The full document text (used for character counts).
    """
    total_chars = sum(ch.char_count for ch in chapters)
    print(f"\n{'=' * 65}")
    print(f"  CHAPTER DETECTION SUMMARY")
    print(f"{'=' * 65}")
    print(f"  Total chapters detected: {len(chapters)}")
    print(f"  Total characters:        {total_chars:,}")
    print(f"  Full text length:        {len(full_text):,}")
    coverage = (total_chars / len(full_text) * 100) if full_text else 0
    print(f"  Coverage:                {coverage:.1f}%")
    print(f"{'=' * 65}\n")
    print(f"  {'#':<5} {'Title':<45} {'Chars':>10}")
    print(f"  {'-' * 5} {'-' * 45} {'-' * 10}")
    for ch in chapters:
        idx_str = str(ch.index)
        title_display = ch.title[:44] if len(ch.title) > 44 else ch.title
        print(f"  {idx_str:<5} {title_display:<45} {ch.char_count:>10,}")
    print(f"\n  {'TOTAL':<51} {total_chars:>10,}")
    print()


# ---------------------------------------------------------------------------
# Text cleanup
# ---------------------------------------------------------------------------

# Common PDF page number patterns.  These appear as standalone lines and
# should be stripped entirely.  We match digits optionally surrounded by
# dashes, dots, or whitespace (e.g. "— 42 —", "42", "- 42 -", "..42..").
_PAGE_NUMBER_RE = re.compile(
    r"^\s*[-—.]*\s*\d{1,4}\s*[-—.]*\s*$",
    re.MULTILINE,
)

# Repeated header/footer lines that pymupdf4llm may preserve.  We target
# lines that look like a running header (short, all-caps or title-case,
# repeating the book title or author).
_HEADER_FOOTER_RE = re.compile(
    r"^\s*(?:ĐẤT RỪNG PHƯƠNG NAM|Đất Rừng Phương Nam|NGUYỄN VĂN BA|Đoàn Giỏi)\s*$",
    re.MULTILINE | re.IGNORECASE,
)

# Hyphenated words split across lines (e.g. "thuyền-\nbuồm" → "thuyền buồm").
# In Vietnamese, line-break hyphens typically separate distinct monosyllabic
# words, so we rejoin with a space.  We detect a word-char followed by a hyphen
# at end of line, then whitespace + lowercase continuation.
_HYPHEN_SPLIT_RE = re.compile(
    r"(\w)-\s*\n\s*([a-zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])",
    re.UNICODE,
)

# Excessive blank lines (3+ consecutive newlines → 2 newlines = one blank line).
_EXCESS_BLANKS_RE = re.compile(r"\n{3,}")

# Horizontal rules or decorative separators that pymupdf4llm may produce.
_DECORATIVE_LINE_RE = re.compile(r"^\s*[-_=*]{3,}\s*$", re.MULTILINE)


def clean_chapter_text(raw_text: str) -> str:
    """Clean up PDF extraction artefacts from chapter text.

    Applies the following transformations in order:
    1. Remove page number lines.
    2. Remove repeated header/footer lines.
    3. Remove decorative separator lines.
    4. Rejoin hyphenated words split across line breaks.
    5. Collapse excessive blank lines.
    6. Strip leading/trailing whitespace.

    Args:
        raw_text: Raw chapter text sliced from the full document.

    Returns:
        Cleaned text ready for Markdown output.
    """
    text = raw_text

    # 1. Strip page numbers
    text = _PAGE_NUMBER_RE.sub("", text)

    # 2. Strip repeated headers/footers
    text = _HEADER_FOOTER_RE.sub("", text)

    # 3. Strip decorative separators
    text = _DECORATIVE_LINE_RE.sub("", text)

    # 4. Rejoin hyphenated words (with space – Vietnamese monosyllabic words)
    text = _HYPHEN_SPLIT_RE.sub(r"\1 \2", text)

    # 5. Collapse excessive blank lines (keep max one blank line between paragraphs)
    text = _EXCESS_BLANKS_RE.sub("\n\n", text)

    # 6. Strip leading/trailing whitespace
    text = text.strip()

    return text


def _slugify_title(title: str, max_len: int = 40) -> str:
    """Create a filesystem-safe slug from a chapter title.

    Keeps Vietnamese (Unicode) characters in filenames for readability.
    Only used to make filenames more readable; the canonical identifier
    is the zero-padded chapter number.

    Args:
        title: Chapter title text.
        max_len: Maximum length for the slug portion.

    Returns:
        Lowercase ASCII-safe slug, or empty string if nothing usable.
    """
    # Keep only word characters and spaces, lowercase
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    # Collapse whitespace to hyphens
    slug = re.sub(r"\s+", "-", slug.strip())
    # Truncate
    if len(slug) > max_len:
        slug = slug[:max_len].rstrip("-")
    return slug


# ---------------------------------------------------------------------------
# Markdown file output
# ---------------------------------------------------------------------------


def write_chapters(
    chapters: list[Chapter],
    full_text: str,
    output_dir: pathlib.Path,
) -> list[pathlib.Path]:
    """Write each chapter to a separate Markdown file.

    Creates the output directory if it does not exist.  Each file contains
    the chapter title as an H1 heading followed by the cleaned body text.

    File naming scheme:
    - ``chapter-00-loi-mo-dau.md`` for prologue
    - ``chapter-01.md``, ``chapter-02.md``, … for regular chapters

    Args:
        chapters: Detected chapter list from :func:`detect_chapters`.
        full_text: The full document text (chapters reference offsets into this).
        output_dir: Directory to write Markdown files into.

    Returns:
        List of paths to written files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Remove stale chapter files from previous runs to ensure idempotency.
    # Only removes files matching our naming convention (chapter-*.md).
    for stale in sorted(output_dir.glob("chapter-*.md")):
        stale.unlink()
        logger.debug("Removed stale file: %s", stale.name)

    logger.info("Writing %d chapter(s) to %s", len(chapters), output_dir)

    written_files: list[pathlib.Path] = []

    for chapter in chapters:
        # Extract raw text for this chapter
        raw_body = full_text[chapter.start:chapter.end]

        # Clean up PDF artefacts
        body = clean_chapter_text(raw_body)

        # Build filename with zero-padded index
        slug = _slugify_title(chapter.title)
        if slug:
            filename = f"chapter-{chapter.index:02d}-{slug}.md"
        else:
            filename = f"chapter-{chapter.index:02d}.md"

        file_path = output_dir / filename

        # Remove the chapter header from body to avoid duplication with H1
        body_lines = body.split('\n')
        while body_lines and CHAPTER_HEADER_RE.search(body_lines[0]):
            body_lines.pop(0)
        # Remove leading blank lines after header removal
        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)
        body = '\n'.join(body_lines)

        # Build Markdown content: H1 title + cleaned body
        md_content = f"# {chapter.title}\n\n{body}\n"

        file_path.write_text(md_content, encoding="utf-8")
        written_files.append(file_path)

        logger.info(
            "  Written: %s (%d chars)",
            filename,
            len(body),
        )

    logger.info("All %d chapter file(s) written", len(written_files))
    return written_files


# ---------------------------------------------------------------------------
# Quality validation
# ---------------------------------------------------------------------------

# Vietnamese diacritical characters (lowercase + uppercase).  Used to verify
# that text extraction preserved Vietnamese encoding correctly.
_VIETNAMESE_DIACRITICS_RE = re.compile(
    r"[àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ"
    r"ÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ]",
)

# Garbled / problematic characters: U+FFFD (replacement character) and
# ASCII control characters (excluding tab, newline, carriage return).
_GARBLED_CHARS_RE = re.compile(r"[\ufffd\x00-\x08\x0b\x0c\x0e-\x1f]")

# Minimum character count for a chapter body to be considered non-empty.
_MIN_CHAPTER_CHARS = 100

# Minimum number of Vietnamese diacritical characters expected per chapter.
_MIN_DIACRITIC_COUNT = 10

# Chapters below this threshold (relative to the median chapter size) are
# flagged as suspiciously short.  The value represents the fraction of the
# median chapter size.
_SHORT_CHAPTER_FRACTION = 0.1


def validate_chapter(chapter_text: str, chapter_title: str) -> dict:
    """Validate a single chapter's conversion quality.

    Checks:
    1. Non-empty content (at least ``_MIN_CHAPTER_CHARS`` characters).
    2. Vietnamese diacritics present (at least ``_MIN_DIACRITIC_COUNT``).
    3. No garbled / replacement characters.

    Args:
        chapter_text: The cleaned chapter body text.
        chapter_title: Chapter title for log messages.

    Returns:
        Dict with keys ``valid`` (bool), ``issues`` (list of str),
        ``char_count`` (int), ``diacritic_count`` (int),
        ``garbled_count`` (int).
    """
    issues: list[str] = []

    char_count = len(chapter_text.strip())
    diacritic_count = len(_VIETNAMESE_DIACRITICS_RE.findall(chapter_text))
    garbled_count = len(_GARBLED_CHARS_RE.findall(chapter_text))

    # Check 1: Non-empty content
    if char_count < _MIN_CHAPTER_CHARS:
        issues.append(
            f"Suspiciously short content ({char_count} chars, "
            f"minimum {_MIN_CHAPTER_CHARS})"
        )

    # Check 2: Vietnamese diacritics present
    if diacritic_count < _MIN_DIACRITIC_COUNT:
        issues.append(
            f"Very few Vietnamese diacritics ({diacritic_count}, "
            f"minimum {_MIN_DIACRITIC_COUNT})"
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
        "diacritic_count": diacritic_count,
        "garbled_count": garbled_count,
    }


def validate_chapters(
    chapters: list[Chapter],
    full_text: str,
    cleaned_texts: list[str],
) -> dict:
    """Run quality validation on all chapters and produce a report.

    In addition to per-chapter checks, this function:
    - Flags suspiciously short chapters (below ``_SHORT_CHAPTER_FRACTION``
      of the median chapter size).
    - Compares total extracted character count against the full PDF text
      length (coverage check).

    Args:
        chapters: Detected chapter list.
        full_text: Full document text (for coverage comparison).
        cleaned_texts: List of cleaned chapter body texts, parallel to *chapters*.

    Returns:
        Quality report dict with ``chapters`` (list of per-chapter results),
        ``summary`` (aggregate statistics), and ``coverage`` info.
    """
    # Per-chapter validation
    chapter_results: list[dict] = []
    for chapter, cleaned in zip(chapters, cleaned_texts):
        result = validate_chapter(cleaned, chapter.title)
        result["index"] = chapter.index
        chapter_results.append(result)

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

    # Coverage comparison
    total_extracted_chars = sum(r["char_count"] for r in chapter_results)
    full_text_length = len(full_text)
    coverage_pct = (
        (total_extracted_chars / full_text_length * 100) if full_text_length > 0 else 0.0
    )

    total_valid = sum(1 for r in chapter_results if r["valid"])
    total_issues = sum(len(r["issues"]) for r in chapter_results)
    total_diacritics = sum(r["diacritic_count"] for r in chapter_results)
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
            "total_characters": total_extracted_chars,
            "total_diacritics": total_diacritics,
            "total_garbled": total_garbled,
        },
        "coverage": {
            "extracted_chars": total_extracted_chars,
            "full_text_chars": full_text_length,
            "coverage_pct": round(coverage_pct, 2),
        },
    }

    # Log summary
    logger.info(
        "Quality validation: %d/%d chapters valid, %d issue(s)",
        total_valid,
        len(chapter_results),
        total_issues,
    )
    logger.info(
        "Coverage: %d / %d chars (%.1f%%)",
        total_extracted_chars,
        full_text_length,
        coverage_pct,
    )

    return report


def print_quality_summary(report: dict) -> None:
    """Print a human-readable quality validation summary to stdout.

    Displays per-chapter validation status, summary statistics, and
    content coverage information in a formatted table.

    Args:
        report: Quality report dict from :func:`validate_chapters`.
    """
    summary = report["summary"]
    coverage = report["coverage"]
    chapters = report["chapters"]

    print(f"\n{'=' * 70}")
    print(f"  QUALITY VALIDATION REPORT  (v{report.get('script_version', '?')})")
    print(f"{'=' * 70}")
    print(f"  Timestamp: {report.get('timestamp', 'N/A')}")
    print()

    # Per-chapter table
    print(f"  {'#':<5} {'Status':<8} {'Title':<35} {'Chars':>8} {'Diacr.':>8}")
    print(f"  {'-' * 5} {'-' * 8} {'-' * 35} {'-' * 8} {'-' * 8}")
    for ch in chapters:
        status = "✓ OK" if ch["valid"] else "✗ FAIL"
        title = ch["title"][:34] if len(ch["title"]) > 34 else ch["title"]
        print(
            f"  {ch['index']:<5} {status:<8} {title:<35} "
            f"{ch['char_count']:>8,} {ch['diacritic_count']:>8,}"
        )
        for issue in ch["issues"]:
            print(f"         ↳ {issue}")

    # Summary
    print(f"\n  {'─' * 70}")
    print(f"  Chapters:   {summary['total_chapters']} total, "
          f"{summary['valid_chapters']} valid, "
          f"{summary['invalid_chapters']} with issues")
    print(f"  Characters: {summary['total_characters']:,} extracted")
    print(f"  Diacritics: {summary['total_diacritics']:,} Vietnamese diacritical chars")
    if summary["total_garbled"] > 0:
        print(f"  ⚠ Garbled:  {summary['total_garbled']} replacement/control chars found")
    print(f"  Coverage:   {coverage['extracted_chars']:,} / {coverage['full_text_chars']:,} "
          f"chars ({coverage['coverage_pct']:.1f}%)")

    # Overall verdict
    all_valid = summary["invalid_chapters"] == 0
    print(f"\n  {'─' * 70}")
    if all_valid:
        print("  ✓ ALL CHAPTERS PASSED VALIDATION")
    else:
        print(f"  ✗ {summary['invalid_chapters']} CHAPTER(S) HAVE ISSUES")
    print(f"{'=' * 70}\n")


def setup_logging(verbose: bool = False) -> None:
    """Configure logging with appropriate level and format."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def extract_pages(pdf_path: pathlib.Path) -> list[dict]:
    """Extract all pages from the PDF as Markdown chunks.

    Uses pymupdf4llm with page_chunks=True so each page is returned
    as a separate dict containing at minimum a 'text' key with the
    Markdown-formatted content for that page.

    Args:
        pdf_path: Path to the source PDF file.

    Returns:
        List of page chunk dicts from pymupdf4llm.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        RuntimeError: If pymupdf4llm extraction fails.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    logger.info("Extracting Markdown from PDF: %s", pdf_path.name)
    logger.info("PDF size: %.1f MB", pdf_path.stat().st_size / (1024 * 1024))

    try:
        chunks = pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)
    except Exception as exc:
        raise RuntimeError(f"pymupdf4llm extraction failed: {exc}") from exc

    logger.info("Extracted %d page chunks", len(chunks))

    total_chars = sum(
        len(chunk.get("text", "") if isinstance(chunk, dict) else str(chunk))
        for chunk in chunks
    )
    logger.info("Total extracted text: %d characters", total_chars)

    return chunks


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Argument list (defaults to sys.argv[1:]).

    Returns:
        Parsed argument namespace.
    """
    parser = argparse.ArgumentParser(
        description="Convert Đất Rừng Phương Nam PDF to Markdown chapter files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python convert.py\n"
            "  python convert.py --input my-file.pdf --output-dir out/\n"
            "  python convert.py --dry-run --verbose\n"
        ),
    )
    parser.add_argument(
        "--input",
        type=pathlib.Path,
        default=DEFAULT_PDF_PATH,
        help=f"Path to the source PDF file (default: {DEFAULT_PDF_PATH.name})",
    )
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for output Markdown files (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Extract and detect chapters but do not write output files",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable debug-level logging",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Entry point for the conversion pipeline.

    Args:
        argv: Optional argument list for testing.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    args = parse_args(argv)
    setup_logging(verbose=args.verbose)

    logger.info("Starting PDF-to-Markdown conversion")
    logger.info("Input:  %s", args.input)
    logger.info("Output: %s", args.output_dir)
    if args.dry_run:
        logger.info("Mode:   DRY RUN (no files will be written)")

    try:
        chunks = extract_pages(args.input)
    except (FileNotFoundError, RuntimeError) as exc:
        logger.error("%s", exc)
        return 1

    # Combine all page text for downstream processing
    full_text = "\n".join(
        chunk.get("text", "") if isinstance(chunk, dict) else str(chunk)
        for chunk in chunks
    )
    logger.info("Full document: %d characters across %d pages", len(full_text), len(chunks))

    # Chapter detection and splitting
    chapters = detect_chapters(full_text)
    if not chapters:
        logger.error("No chapters detected – aborting")
        return 1

    if args.dry_run:
        print_chapter_summary(chapters, full_text)
        logger.info("Dry run complete – no files written")
        return 0

    # Write chapter Markdown files
    written_files = write_chapters(chapters, full_text, args.output_dir)

    # Quality validation – build cleaned texts for each chapter
    cleaned_texts = [
        clean_chapter_text(full_text[ch.start:ch.end]) for ch in chapters
    ]
    quality_report = validate_chapters(chapters, full_text, cleaned_texts)

    # Write quality report alongside the script
    report_path = SCRIPT_DIR / "quality-report.json"
    report_path.write_text(
        json.dumps(quality_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    logger.info("Quality report written to %s", report_path)

    # Print human-readable quality summary to stdout
    print_quality_summary(quality_report)

    logger.info("Conversion complete: %d chapters written to %s", len(written_files), args.output_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
