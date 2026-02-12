#!/usr/bin/env python3
"""Clean up repository for production release 1"""

import os
import shutil
from pathlib import Path

def cleanup_for_production():
    """Move development files to archive, keep only production essentials"""

    base_dir = Path(__file__).parent
    archive_dir = base_dir / 'archive'

    # Create archive directory
    archive_dir.mkdir(exist_ok=True)

    # Files/folders to KEEP in production
    keep_items = {
        'chapters',           # Essential content
        'index.html',         # Main application
        'README.md',          # Documentation
        'requirements.txt',   # Dependencies
        '.gitignore',         # Git config
        '.git',               # Git repository
        'archive',            # Archive folder itself
        'cleanup_for_production.py',  # This script
    }

    # Patterns to archive
    archive_patterns = [
        # Python development scripts
        'align_*.py',
        'fix_*.py',
        'improve_*.py',
        'refine_*.py',
        'standardize_*.py',

        # Test files
        'test*.html',
        'test*.sh',
        'verify*.html',
        'verify*.sh',

        # Documentation/reports (keep in archive for reference)
        '*-SUMMARY.md',
        '*-REPORT.md',
        '*-VERIFICATION*.md',
        '*-COMPLETION*.md',
        '*-SIGNOFF.md',
        '*-COMPLETE.txt',
        '*_results.txt',
        '*CHECKLIST.md',
        '*GUIDE.md',
        '*WORKFLOW*.md',

        # Backup files
        '*.backup',

        # Development directories
        'scripts',
        '.auto-claude',
        '.claude',
    ]

    archived_count = 0

    print("=== Production Cleanup ===\n")
    print("Archiving development files...\n")

    # Process each item in root directory
    for item in base_dir.iterdir():
        if item.name in keep_items:
            continue

        # Check if matches archive patterns
        should_archive = False
        for pattern in archive_patterns:
            if item.match(pattern):
                should_archive = True
                break

        if should_archive:
            target = archive_dir / item.name

            # Move to archive
            if item.is_file():
                shutil.move(str(item), str(target))
                print(f"✓ Archived: {item.name}")
            elif item.is_dir():
                if target.exists():
                    shutil.rmtree(target)
                shutil.move(str(item), str(target))
                print(f"✓ Archived directory: {item.name}/")

            archived_count += 1

    print(f"\n✓ Archived {archived_count} items")

    # Create production README in archive
    archive_readme = archive_dir / 'README.md'
    with open(archive_readme, 'w', encoding='utf-8') as f:
        f.write("""# Development Archive

This directory contains development files, scripts, and reports from the translation project.

## Contents

- **Python Scripts**: Refinement and alignment scripts used during development
- **Test Files**: HTML and shell scripts for testing and verification
- **Reports**: Completion summaries, verification reports, and QA documentation
- **Development Tools**: Scripts and utilities used in the build process

These files are preserved for reference but are not needed for production deployment.
""")

    print(f"\n✓ Created archive/README.md")

    # List final production structure
    print("\n=== Production Structure ===\n")
    print("Production files:")
    for item in sorted(base_dir.iterdir()):
        if item.name.startswith('.git'):
            continue
        if item.is_file():
            size_kb = item.stat().st_size / 1024
            print(f"  - {item.name} ({size_kb:.1f} KB)")
        elif item.is_dir():
            print(f"  - {item.name}/ (directory)")

    print("\n✓ Production cleanup complete!")
    print(f"✓ Development files archived in: archive/")

if __name__ == '__main__':
    cleanup_for_production()
