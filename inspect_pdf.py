"""Inspect PDF structure for Đất Rừng Phương Nam conversion.

Converts the first 5 pages with pymupdf4llm to determine:
1. Chapter header format and patterns
2. Text extraction quality
3. Vietnamese diacritic preservation
4. Page structure (headers, footers, artifacts)

Output is saved to _inspection_output.txt for analysis.
"""

import re
import pathlib
import pymupdf4llm

PDF_PATH = pathlib.Path(__file__).parent.parent.parent.parent / "517016593-ĐẤT-RỪNG-PHƯƠNG-NAM.pdf"
OUTPUT_PATH = pathlib.Path(__file__).parent / "_inspection_output.txt"
PAGES_TO_INSPECT = 5

VIETNAMESE_DIACRITICS_RE = re.compile(
    r"[àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]",
    re.IGNORECASE,
)

CHAPTER_PATTERNS = [
    r"Chương\s+\d+",
    r"CHƯƠNG\s+\d+",
    r"CHƯƠNG\s+[IVXLCDM]+",
    r"Chương\s+(một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)",
]
CHAPTER_REGEX = re.compile("|".join(CHAPTER_PATTERNS), re.IGNORECASE)


def inspect_pdf() -> str:
    """Inspect the first N pages of the PDF and return analysis."""
    if not PDF_PATH.exists():
        return f"ERROR: PDF not found at {PDF_PATH}"

    lines: list[str] = []
    lines.append("=" * 70)
    lines.append("PDF INSPECTION REPORT")
    lines.append(f"Source: {PDF_PATH.name}")
    lines.append("=" * 70)

    # Convert first N pages with page_chunks=True
    chunks = pymupdf4llm.to_markdown(
        str(PDF_PATH),
        page_chunks=True,
        pages=list(range(PAGES_TO_INSPECT)),
    )

    lines.append(f"\nTotal pages inspected: {len(chunks)}")
    lines.append("")

    all_text = ""
    chapter_matches: list[str] = []

    for i, chunk in enumerate(chunks):
        page_text = chunk.get("text", "") if isinstance(chunk, dict) else str(chunk)
        all_text += page_text

        lines.append("-" * 50)
        lines.append(f"PAGE {i + 1}")
        lines.append("-" * 50)

        # Show raw text (first 2000 chars per page)
        preview = page_text[:2000]
        lines.append(f"Text length: {len(page_text)} chars")
        lines.append(f"Preview:\n{preview}")
        if len(page_text) > 2000:
            lines.append(f"... (truncated, {len(page_text) - 2000} more chars)")
        lines.append("")

        # Check for chapter headers
        matches = CHAPTER_REGEX.findall(page_text)
        if matches:
            chapter_matches.extend(matches)
            lines.append(f"  ** CHAPTER HEADERS FOUND: {matches}")

    # Analysis section
    lines.append("\n" + "=" * 70)
    lines.append("ANALYSIS")
    lines.append("=" * 70)

    # Vietnamese diacritics check
    viet_chars = VIETNAMESE_DIACRITICS_RE.findall(all_text)
    lines.append(f"\n1. VIETNAMESE DIACRITICS:")
    lines.append(f"   Total found: {len(viet_chars)}")
    if viet_chars:
        unique = sorted(set(c.lower() for c in viet_chars))
        lines.append(f"   Unique diacritical chars: {' '.join(unique)}")
        lines.append(f"   Sample: {''.join(viet_chars[:50])}")
    lines.append(f"   Status: {'OK - diacritics preserved' if len(viet_chars) > 10 else 'WARNING - few diacritics found'}")

    # Chapter header detection
    lines.append(f"\n2. CHAPTER HEADER PATTERN:")
    if chapter_matches:
        lines.append(f"   Matches found: {chapter_matches}")
        lines.append(f"   Pattern used: {CHAPTER_REGEX.pattern}")
    else:
        lines.append("   No chapter headers found in first 5 pages.")
        lines.append("   NOTE: Chapter headers may start later in the document.")
        lines.append("   May need to scan more pages or adjust patterns.")

    # Garbled character check
    garbled = re.findall(r"[\ufffd\x00-\x08\x0b\x0c\x0e-\x1f]", all_text)
    lines.append(f"\n3. TEXT QUALITY:")
    lines.append(f"   Total text length: {len(all_text)} chars")
    lines.append(f"   Garbled/replacement chars: {len(garbled)}")
    lines.append(f"   Status: {'OK - clean text' if len(garbled) == 0 else 'WARNING - garbled characters detected'}")

    # Page structure notes
    lines.append(f"\n4. PAGE STRUCTURE NOTES:")
    for i, chunk in enumerate(chunks):
        page_text = chunk.get("text", "") if isinstance(chunk, dict) else str(chunk)
        page_lines = page_text.strip().split("\n")
        first_line = page_lines[0].strip() if page_lines else "(empty)"
        last_line = page_lines[-1].strip() if page_lines else "(empty)"
        lines.append(f"   Page {i + 1}: {len(page_lines)} lines | first: '{first_line[:60]}' | last: '{last_line[:60]}'")

    # Extended scan: look for chapter headers in pages 5-30
    lines.append(f"\n5. EXTENDED CHAPTER SCAN (pages 5-30):")
    try:
        extended_chunks = pymupdf4llm.to_markdown(
            str(PDF_PATH),
            page_chunks=True,
            pages=list(range(5, 30)),
        )
        for i, chunk in enumerate(extended_chunks):
            page_text = chunk.get("text", "") if isinstance(chunk, dict) else str(chunk)
            matches = CHAPTER_REGEX.findall(page_text)
            if matches:
                lines.append(f"   Page {i + 6}: CHAPTER HEADER: {matches}")
                # Show context around the match
                for m in re.finditer(CHAPTER_REGEX, page_text):
                    start = max(0, m.start() - 30)
                    end = min(len(page_text), m.end() + 80)
                    context = page_text[start:end].replace("\n", " | ")
                    lines.append(f"     Context: ...{context}...")
    except Exception as e:
        lines.append(f"   Error during extended scan: {e}")

    report = "\n".join(lines)
    return report


def main() -> None:
    report = inspect_pdf()
    print(report)

    OUTPUT_PATH.write_text(report, encoding="utf-8")
    print(f"\nInspection output saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
