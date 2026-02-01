#!/usr/bin/env bash
# End-to-end verification script for Đất Rừng Phương Nam PDF-to-Markdown conversion.
#
# Run this AFTER `python convert.py` has completed successfully.
#
# Usage:
#   bash verify_e2e.sh
#
# Exit codes:
#   0 - All checks passed
#   1 - One or more checks failed

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHAPTERS_DIR="${SCRIPT_DIR}/chapters"
QUALITY_REPORT="${SCRIPT_DIR}/quality-report.json"

PASS=0
FAIL=0
WARN=0

pass() { ((PASS++)); printf "  ✓ PASS: %s\n" "$1"; }
fail() { ((FAIL++)); printf "  ✗ FAIL: %s\n" "$1"; }
warn() { ((WARN++)); printf "  ⚠ WARN: %s\n" "$1"; }

echo ""
echo "================================================================="
echo "  END-TO-END VERIFICATION"
echo "================================================================="
echo "  Chapters dir: ${CHAPTERS_DIR}"
echo "  Quality report: ${QUALITY_REPORT}"
echo ""

# ---------------------------------------------------------------
# Check 1: chapters/ directory exists
# ---------------------------------------------------------------
echo "--- Check 1: chapters/ directory exists ---"
if [ -d "${CHAPTERS_DIR}" ]; then
    pass "chapters/ directory exists"
else
    fail "chapters/ directory not found"
    echo ""
    echo "FATAL: Cannot continue without chapters/ directory."
    echo "Run 'python convert.py' first."
    exit 1
fi

# ---------------------------------------------------------------
# Check 2: Chapter file count
# ---------------------------------------------------------------
echo "--- Check 2: Chapter files exist ---"
FILE_COUNT=$(find "${CHAPTERS_DIR}" -name '*.md' -type f | wc -l)
echo "  Found ${FILE_COUNT} .md file(s)"
if [ "${FILE_COUNT}" -gt 0 ]; then
    pass "Chapter files found: ${FILE_COUNT}"
else
    fail "No .md files found in chapters/"
    exit 1
fi

# Expected range for Đất Rừng Phương Nam: ~20-40 chapters
if [ "${FILE_COUNT}" -ge 10 ] && [ "${FILE_COUNT}" -le 50 ]; then
    pass "Chapter count (${FILE_COUNT}) is within expected range (10-50)"
else
    warn "Chapter count (${FILE_COUNT}) outside expected range (10-50)"
fi

# List all chapter files
echo "  Chapter files:"
find "${CHAPTERS_DIR}" -name '*.md' -type f | sort | while read -r f; do
    echo "    $(basename "$f")"
done

# ---------------------------------------------------------------
# Check 3: All files are non-empty
# ---------------------------------------------------------------
echo ""
echo "--- Check 3: No empty files ---"
EMPTY_FILES=$(find "${CHAPTERS_DIR}" -name '*.md' -type f -empty)
if [ -z "${EMPTY_FILES}" ]; then
    pass "No empty .md files"
else
    fail "Empty files found:"
    echo "${EMPTY_FILES}" | while read -r f; do echo "    ${f}"; done
fi

# ---------------------------------------------------------------
# Check 4: All files are valid UTF-8
# ---------------------------------------------------------------
echo ""
echo "--- Check 4: UTF-8 encoding ---"
UTF8_FAIL=0
find "${CHAPTERS_DIR}" -name '*.md' -type f | sort | while read -r f; do
    FILE_TYPE=$(file --mime-encoding "$f")
    if echo "${FILE_TYPE}" | grep -qi 'utf-8'; then
        : # OK
    else
        echo "    NOT UTF-8: ${FILE_TYPE}"
        # Write a marker so the parent shell knows
        echo "FAIL" >> /tmp/verify_e2e_utf8_$$
    fi
done
if [ -f /tmp/verify_e2e_utf8_$$ ]; then
    fail "Some files are not UTF-8 encoded"
    rm -f /tmp/verify_e2e_utf8_$$
else
    pass "All files are UTF-8 encoded"
fi

# ---------------------------------------------------------------
# Check 5: Vietnamese diacritics present in every file
# ---------------------------------------------------------------
echo ""
echo "--- Check 5: Vietnamese diacritics in every file ---"
DIACRITIC_MISSING=0
find "${CHAPTERS_DIR}" -name '*.md' -type f | sort | while read -r f; do
    # Count Vietnamese diacritical characters
    COUNT=$(grep -oP '[àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ]' "$f" 2>/dev/null | wc -l || true)
    if [ "${COUNT}" -lt 10 ]; then
        echo "    LOW DIACRITICS (${COUNT}): $(basename "$f")"
        echo "FAIL" >> /tmp/verify_e2e_diacritics_$$
    fi
done
if [ -f /tmp/verify_e2e_diacritics_$$ ]; then
    fail "Some files have too few Vietnamese diacritics"
    rm -f /tmp/verify_e2e_diacritics_$$
else
    pass "Vietnamese diacritics present in all files"
fi

# ---------------------------------------------------------------
# Check 6: No garbled/replacement characters (U+FFFD)
# ---------------------------------------------------------------
echo ""
echo "--- Check 6: No garbled/replacement characters ---"
GARBLED_TOTAL=0
find "${CHAPTERS_DIR}" -name '*.md' -type f | sort | while read -r f; do
    # Check for U+FFFD replacement character
    COUNT=$(grep -oP '\x{FFFD}' "$f" 2>/dev/null | wc -l || true)
    if [ "${COUNT}" -gt 0 ]; then
        echo "    GARBLED (${COUNT} U+FFFD): $(basename "$f")"
        echo "FAIL" >> /tmp/verify_e2e_garbled_$$
    fi
done
if [ -f /tmp/verify_e2e_garbled_$$ ]; then
    fail "Garbled replacement characters found"
    rm -f /tmp/verify_e2e_garbled_$$
else
    pass "No U+FFFD replacement characters found"
fi

# ---------------------------------------------------------------
# Check 7: quality-report.json exists and shows all valid
# ---------------------------------------------------------------
echo ""
echo "--- Check 7: Quality report ---"
if [ -f "${QUALITY_REPORT}" ]; then
    pass "quality-report.json exists"

    # Check that all chapters are valid using jq
    if command -v jq &>/dev/null; then
        TOTAL=$(jq '.summary.total_chapters' "${QUALITY_REPORT}" 2>/dev/null || echo "?")
        VALID=$(jq '.summary.valid_chapters' "${QUALITY_REPORT}" 2>/dev/null || echo "?")
        INVALID=$(jq '.summary.invalid_chapters' "${QUALITY_REPORT}" 2>/dev/null || echo "?")
        COVERAGE=$(jq '.coverage.coverage_pct' "${QUALITY_REPORT}" 2>/dev/null || echo "?")

        echo "  Report summary:"
        echo "    Total chapters:   ${TOTAL}"
        echo "    Valid chapters:   ${VALID}"
        echo "    Invalid chapters: ${INVALID}"
        echo "    Coverage:         ${COVERAGE}%"

        if [ "${INVALID}" = "0" ]; then
            pass "All chapters valid in quality report"
        else
            fail "${INVALID} chapter(s) have issues in quality report"
            # Show which chapters have issues
            jq -r '.chapters[] | select(.valid == false) | "    Chapter \(.index): \(.title) - \(.issues | join(", "))"' "${QUALITY_REPORT}" 2>/dev/null || true
        fi
    else
        warn "jq not available - cannot parse quality-report.json programmatically"
        echo "  Manual inspection required: cat quality-report.json"
    fi
else
    fail "quality-report.json not found"
fi

# ---------------------------------------------------------------
# Check 8: Content spot-check (sample lines from chapters)
# ---------------------------------------------------------------
echo ""
echo "--- Check 8: Content spot-check ---"
echo "  First 3 lines of content from up to 3 chapter files:"
SAMPLE_COUNT=0
find "${CHAPTERS_DIR}" -name '*.md' -type f | sort | head -3 | while read -r f; do
    echo ""
    echo "  === $(basename "$f") ==="
    # Skip the H1 heading line and show first 3 non-empty content lines
    grep -v '^#' "$f" | grep -v '^\s*$' | head -3 | sed 's/^/    /'
done

echo ""
echo "  Last chapter content sample:"
LAST_FILE=$(find "${CHAPTERS_DIR}" -name '*.md' -type f | sort | tail -1)
if [ -n "${LAST_FILE}" ]; then
    echo "  === $(basename "${LAST_FILE}") ==="
    grep -v '^#' "${LAST_FILE}" | grep -v '^\s*$' | head -3 | sed 's/^/    /'
fi

# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------
echo ""
echo "================================================================="
echo "  VERIFICATION SUMMARY"
echo "================================================================="
echo "  Passed:   ${PASS}"
echo "  Failed:   ${FAIL}"
echo "  Warnings: ${WARN}"
echo ""
if [ "${FAIL}" -eq 0 ]; then
    echo "  ✓ ALL CHECKS PASSED"
    echo "================================================================="
    exit 0
else
    echo "  ✗ ${FAIL} CHECK(S) FAILED"
    echo "================================================================="
    exit 1
fi
