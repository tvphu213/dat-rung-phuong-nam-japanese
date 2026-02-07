#!/usr/bin/env python3
"""Rebuild index.html with proper paragraph structure.

Reads chapter files and combines sentences in the same paragraph into a single <p> tag,
instead of creating separate <p> tags for each sentence.

Usage:
    python rebuild_html.py
    python rebuild_html.py --vi-dir chapters/vi --ja-dir chapters/ja
    python rebuild_html.py --output dist/index.html
    python rebuild_html.py --dry-run
    python rebuild_html.py --help
"""

from __future__ import annotations

import argparse
import logging
import pathlib
import re
import sys

logger = logging.getLogger(__name__)

# Script metadata
SCRIPT_VERSION = "1.0.0"

# Default paths relative to this script's location
SCRIPT_DIR = pathlib.Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
DEFAULT_VI_DIR = PROJECT_DIR / "chapters" / "vi"
DEFAULT_JA_DIR = PROJECT_DIR / "chapters" / "ja"
DEFAULT_OUTPUT_FILE = PROJECT_DIR / "index.html"

# ---------------------------------------------------------------------------
# Argument parsing and logging setup
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Optional argument list for testing. If None, uses sys.argv.

    Returns:
        Parsed argument namespace containing all CLI options.
    """
    parser = argparse.ArgumentParser(
        description="Rebuild index.html with proper paragraph structure from chapter files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --vi-dir chapters/vi --ja-dir chapters/ja
  %(prog)s --output dist/index.html
  %(prog)s --dry-run --verbose
        """,
    )

    parser.add_argument(
        "--vi-dir",
        type=pathlib.Path,
        default=DEFAULT_VI_DIR,
        metavar="PATH",
        help=f"Directory containing Vietnamese chapter files (default: {DEFAULT_VI_DIR.relative_to(PROJECT_DIR)})",
    )

    parser.add_argument(
        "--ja-dir",
        type=pathlib.Path,
        default=DEFAULT_JA_DIR,
        metavar="PATH",
        help=f"Directory containing Japanese chapter files (default: {DEFAULT_JA_DIR.relative_to(PROJECT_DIR)})",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=pathlib.Path,
        default=DEFAULT_OUTPUT_FILE,
        metavar="FILE",
        help=f"Output HTML file path (default: {DEFAULT_OUTPUT_FILE.relative_to(PROJECT_DIR)})",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate HTML without writing to file (useful for testing)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging output",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {SCRIPT_VERSION}",
    )

    return parser.parse_args(argv)


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the script.

    Args:
        verbose: If True, set logging level to DEBUG; otherwise INFO.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )


# ---------------------------------------------------------------------------
# Chapter processing
# ---------------------------------------------------------------------------


def read_chapter_paragraphs(file_path, aggressive_merge=True):
    """Read a chapter file and return list of paragraphs.

    If aggressive_merge is True, combines short consecutive lines into larger paragraphs
    to reduce spacing. Otherwise, treats blank lines as paragraph separators.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    if not aggressive_merge:
        # Original logic: blank lines separate paragraphs
        paragraphs = []
        current_para = []
        for line in lines:
            line = line.strip()
            if line:
                current_para.append(line)
            else:
                if current_para:
                    paragraphs.append(' '.join(current_para))
                    current_para = []
        if current_para:
            paragraphs.append(' '.join(current_para))
        return paragraphs

    # Aggressive merge: combine short lines more aggressively
    paragraphs = []
    current_para = []
    blank_count = 0

    for line in lines:
        line = line.strip()
        if line:
            current_para.append(line)
            blank_count = 0
        else:
            blank_count += 1
            # Only start new paragraph after 2+ consecutive blank lines,
            # OR if current paragraph is getting too long (10+ lines)
            if blank_count >= 2 or len(current_para) >= 10:
                if current_para:
                    paragraphs.append(' '.join(current_para))
                    current_para = []

    # Don't forget the last paragraph
    if current_para:
        paragraphs.append(' '.join(current_para))

    return paragraphs


def generate_html(vi_dir: pathlib.Path, ja_dir: pathlib.Path) -> str:
    """Generate the complete HTML file.

    Args:
        vi_dir: Directory containing Vietnamese chapter files.
        ja_dir: Directory containing Japanese chapter files.

    Returns:
        Complete HTML document as a string.
    """
    logger.info("Reading Vietnamese chapters from: %s", vi_dir)
    logger.info("Reading Japanese chapters from: %s", ja_dir)

    # Read all Vietnamese chapters
    vi_chapters = []
    for i in range(1, 21):
        file_path = vi_dir / f"chapter{i}.txt"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract title (first line) and content (rest)
                lines = content.strip().split('\n', 1)
                title = lines[0].strip()
                # Keep Vietnamese content as-is (no <p> tags, plain text)
                chapter_content = lines[1].strip() if len(lines) > 1 else ""
                vi_chapters.append((title, chapter_content))

    # Read all Japanese chapters with aggressive merging
    ja_chapters = []
    for i in range(1, 21):
        file_path = ja_dir / f"chapter{i}_ja.txt"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract title (first line) and content (rest)
                lines = content.strip().split('\n', 1)
                title = lines[0].strip()
                # Parse content into paragraphs with aggressive merging
                if len(lines) > 1:
                    chapter_lines = lines[1].split('\n')
                    paragraphs = []
                    current_para = []
                    blank_count = 0

                    for line in chapter_lines:
                        line = line.strip()
                        if line:
                            current_para.append(line)
                            blank_count = 0
                        else:
                            blank_count += 1
                            # Only start new paragraph after 2+ consecutive blank lines,
                            # OR if current paragraph is getting too long
                            if blank_count >= 2 or len(current_para) >= 10:
                                if current_para:
                                    paragraphs.append(' '.join(current_para))
                                    current_para = []

                    # Don't forget the last paragraph
                    if current_para:
                        paragraphs.append(' '.join(current_para))
                else:
                    paragraphs = []

                ja_chapters.append((title, paragraphs))

    # Generate HTML
    html = '''<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Đất Rừng Phương Nam - Đoàn Giỏi</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --forest-green: #2d5016;
            --light-green: #4a7c2c;
            --earth-brown: #8b7355;
            --sand-beige: #f5e6d3;
            --text-dark: #2c2c2c;
            --text-light: #555;
            --accent-gold: #d4af37;
        }

        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            background: linear-gradient(135deg, #f5e6d3 0%, #e8d5c4 100%);
            color: var(--text-dark);
            line-height: 1.8;
        }

        .container {
            max-width: 1200px;
            width: 100%;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 30px rgba(0, 0, 0, 0.1);
            min-height: 100vh;
        }

        header {
            background: linear-gradient(135deg, var(--forest-green) 0%, var(--light-green) 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            letter-spacing: 2px;
        }

        .subtitle {
            font-size: 1.2rem;
            font-style: italic;
            opacity: 0.9;
            font-family: 'Arial', sans-serif;
        }

        .tabs {
            display: flex;
            background: var(--earth-brown);
            border-bottom: 3px solid var(--forest-green);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .tab-button {
            flex: 1;
            padding: 1rem 2rem;
            background: var(--earth-brown);
            color: white;
            border: none;
            cursor: pointer;
            font-size: 1.1rem;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            transition: all 0.3s ease;
            border-right: 1px solid rgba(255, 255, 255, 0.2);
        }

        .tab-button:last-child {
            border-right: none;
        }

        .tab-button:hover {
            background: var(--light-green);
        }

        .tab-button.active {
            background: var(--forest-green);
            box-shadow: inset 0 -3px 0 var(--accent-gold);
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.5s ease;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .toc {
            background: var(--sand-beige);
            padding: 2rem;
            border-bottom: 2px solid var(--earth-brown);
        }

        .toc h2 {
            color: var(--forest-green);
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
            border-bottom: 2px solid var(--light-green);
            padding-bottom: 0.5rem;
        }

        .toc-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 0.8rem;
        }

        .toc-item {
            background: white;
            padding: 0.8rem 1rem;
            border-left: 4px solid var(--light-green);
            cursor: pointer;
            transition: all 0.3s ease;
            border-radius: 0 4px 4px 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .toc-item:hover {
            background: var(--light-green);
            color: white;
            transform: translateX(5px);
            border-left-color: var(--accent-gold);
        }

        .chapter {
            padding: 3rem 2rem;
            max-width: 800px;
            margin: 0 auto;
        }

        .chapter-title {
            color: var(--forest-green);
            font-size: 2rem;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 3px solid var(--light-green);
            text-align: center;
        }

        .chapter-content {
            font-size: 1.1rem;
            color: var(--text-dark);
            white-space: pre-wrap;
        }

        .chapter-content p {
            margin-bottom: 0.5rem;
            text-align: justify;
            line-height: 1.8;
        }

        .back-to-top {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: var(--forest-green);
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            font-size: 1.5rem;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            opacity: 0;
            visibility: hidden;
        }

        .back-to-top.visible {
            opacity: 1;
            visibility: visible;
        }

        .back-to-top:hover {
            background: var(--light-green);
            transform: translateY(-5px);
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 1.8rem;
            }

            .subtitle {
                font-size: 1rem;
            }

            .tab-button {
                padding: 0.8rem 1rem;
                font-size: 1rem;
            }

            .chapter {
                padding: 2rem 1rem;
            }

            .chapter-title {
                font-size: 1.5rem;
            }

            .chapter-content {
                font-size: 1rem;
            }

            .toc-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 480px) {
            h1 {
                font-size: 1.5rem;
                letter-spacing: 1px;
            }

            header {
                padding: 2rem 1rem;
            }

            .tab-button {
                font-size: 0.9rem;
                padding: 0.7rem 0.5rem;
            }
        }
    </style>
</head>

<body>
    <div class="container">
        <header>
            <h1>Đất Rừng Phương Nam</h1>
            <p class="subtitle">南部の森と大地 - Đoàn Giỏi</p>
        </header>

        <div class="tabs">
            <button class="tab-button active" onclick="switchTab('vietnamese')">Tiếng Việt</button>
            <button class="tab-button" onclick="switchTab('japanese')">日本語</button>
        </div>

        <!-- Vietnamese Content -->
        <div id="vietnamese-content" class="tab-content active">
            <div class="toc">
                <h2>📚 Mục lục</h2>
                <div class="toc-grid">
'''

    # Add Vietnamese TOC
    for i, (title, _) in enumerate(vi_chapters, 1):
        html += f'                    <div class="toc-item" onclick="scrollToChapter({i})">{title}</div>\n'

    html += '''                </div>
            </div>

'''

    # Add Vietnamese chapters
    for i, (title, content) in enumerate(vi_chapters, 1):
        html += f'''            <div class="chapter" id="chapter-{i}">
                <h2 class="chapter-title">{title}</h2>
                <div class="chapter-content">{content}</div>
            </div>

'''

    html += '''        </div>

        <!-- Japanese Content -->
        <div id="japanese-content" class="tab-content">
            <div class="toc">
                <h2>📚 目次</h2>
                <div class="toc-grid">
'''

    # Add Japanese TOC
    for i, (title, _) in enumerate(ja_chapters, 1):
        html += f'                    <div class="toc-item" onclick="scrollToChapter({i})">{title}</div>\n'

    html += '''                </div>
            </div>

'''

    # Add Japanese chapters
    for i, (title, paragraphs) in enumerate(ja_chapters, 1):
        html += f'''            <div class="chapter" id="chapter-ja-{i}">
                <h3 class="chapter-title">{title}</h3>
                <div class="chapter-content">
'''
        for para in paragraphs:
            html += f'                    <p>{para}</p>\n'

        html += '''                </div>
            </div>

'''

    html += '''        </div>

        <button class="back-to-top" onclick="scrollToTop()" aria-label="Back to top" title="Back to top">↑</button>
    </div>

    <script>
        function switchTab(tab) {
            const vietnameseContent = document.getElementById('vietnamese-content');
            const japaneseContent = document.getElementById('japanese-content');
            const tabButtons = document.querySelectorAll('.tab-button');

            if (tab === 'vietnamese') {
                vietnameseContent.classList.add('active');
                japaneseContent.classList.remove('active');
                tabButtons[0].classList.add('active');
                tabButtons[1].classList.remove('active');
            } else {
                vietnameseContent.classList.remove('active');
                japaneseContent.classList.add('active');
                tabButtons[0].classList.remove('active');
                tabButtons[1].classList.add('active');
            }

            scrollToTop();
        }

        function scrollToChapter(chapterNum) {
            const activeTab = document.querySelector('.tab-content.active');
            const isJapanese = activeTab.id === 'japanese-content';
            const chapterId = isJapanese ? `chapter-ja-${chapterNum}` : `chapter-${chapterNum}`;
            const chapter = document.getElementById(chapterId);

            if (chapter) {
                chapter.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }

        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Show/hide back-to-top button
        window.addEventListener('scroll', function () {
            const backToTop = document.querySelector('.back-to-top');
            if (window.pageYOffset > 300) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });
    </script>
</body>

</html>'''

    logger.info("HTML generation complete: %d bytes", len(html))
    return html


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the rebuild_html script.

    Args:
        argv: Optional argument list for testing. If None, uses sys.argv.

    Returns:
        Exit code: 0 for success, non-zero for failure.
    """
    args = parse_args(argv)
    setup_logging(args.verbose)

    logger.info("Starting HTML rebuild (version %s)", SCRIPT_VERSION)
    logger.debug("Vietnamese chapters directory: %s", args.vi_dir)
    logger.debug("Japanese chapters directory: %s", args.ja_dir)
    logger.debug("Output file: %s", args.output)

    # Validate input directories
    if not args.vi_dir.exists():
        logger.error("Vietnamese chapters directory not found: %s", args.vi_dir)
        return 1
    if not args.ja_dir.exists():
        logger.error("Japanese chapters directory not found: %s", args.ja_dir)
        return 1

    # Generate HTML
    try:
        html = generate_html(args.vi_dir, args.ja_dir)
    except Exception as e:
        logger.error("Failed to generate HTML: %s", e)
        logger.debug("Exception details:", exc_info=True)
        return 1

    # Write output (unless dry-run)
    if args.dry_run:
        logger.info("Dry-run mode: skipping file write")
        logger.info("Generated HTML size: %d bytes", len(html))
    else:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(html)
            logger.info("✅ Successfully wrote %s", args.output)
            logger.info("   File size: %d bytes", len(html))
        except Exception as e:
            logger.error("Failed to write output file: %s", e)
            logger.debug("Exception details:", exc_info=True)
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
