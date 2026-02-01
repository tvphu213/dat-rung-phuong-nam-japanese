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

import argparse
import logging
import pathlib
import sys

import pymupdf4llm

logger = logging.getLogger(__name__)

# Default paths relative to this script's location
SCRIPT_DIR = pathlib.Path(__file__).parent
DEFAULT_PDF_PATH = SCRIPT_DIR.parent.parent.parent / "517016593-ĐẤT-RỪNG-PHƯƠNG-NAM.pdf"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "chapters"


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

    # TODO(subtask-2-2): Chapter detection and splitting
    # TODO(subtask-2-3): Markdown file output with cleanup
    # TODO(subtask-3-1): Quality validation
    # TODO(subtask-3-2): Quality report generation

    logger.info("Extraction complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
