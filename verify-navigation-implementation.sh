#!/bin/bash

# Automated Implementation Verification Script for Subtask 6-1
# This script verifies that all required navigation components are present in index.html

echo "=========================================="
echo "Navigation Implementation Verification"
echo "Subtask 6-1: Test complete navigation flows"
echo "=========================================="
echo ""

FILE="./index.html"
PASS=0
FAIL=0

# Function to check for pattern in file
check_pattern() {
    local description=$1
    local pattern=$2

    if grep -q "$pattern" "$FILE"; then
        echo "✅ PASS: $description"
        ((PASS++))
        return 0
    else
        echo "❌ FAIL: $description"
        ((FAIL++))
        return 1
    fi
}

echo "=== URL Routing Functions ==="
check_pattern "getChapterFromURL function exists" "function getChapterFromURL()"
check_pattern "updateURL functionality (hash update)" "window.location.hash.*chapter"
check_pattern "popstate event listener" "addEventListener.*popstate"
echo ""

echo "=== Navigation Functions ==="
check_pattern "navigateToChapter function exists" "function navigateToChapter"
check_pattern "navigatePrevious function exists" "function navigatePrevious"
check_pattern "navigateNext function exists" "function navigateNext"
echo ""

echo "=== UI Components - Pagination Controls ==="
check_pattern "Pagination controls CSS class" "\.pagination-controls"
check_pattern "Previous button in HTML" '<button.*class="pagination-btn prev-btn"'
check_pattern "Next button in HTML" '<button.*class="pagination-btn next-btn"'
check_pattern "Chapter selector dropdown" '<select.*class="chapter-selector"'
check_pattern "navigatePrevious onclick handler" 'onclick="navigatePrevious()"'
check_pattern "navigateNext onclick handler" 'onclick="navigateNext()"'
check_pattern "navigateToChapter onchange handler" 'onchange="navigateToChapter'

# Count pagination control instances (should be 4: top/bottom for each tab)
PAGINATION_COUNT=$(grep -c 'class="pagination-controls"' "$FILE")
if [ "$PAGINATION_COUNT" -eq 4 ]; then
    echo "✅ PASS: Found 4 pagination control sections (top/bottom for both tabs)"
    ((PASS++))
else
    echo "❌ FAIL: Expected 4 pagination controls, found $PAGINATION_COUNT"
    ((FAIL++))
fi
echo ""

echo "=== Display & State Management ==="
check_pattern "displaySingleChapter function exists" "function displaySingleChapter"
check_pattern "updateNavigationState function exists" "function updateNavigationState"
check_pattern "updateDropdownSelection function exists" "function updateDropdownSelection"
check_pattern "populateChapterDropdown function exists" "function populateChapterDropdown"
echo ""

echo "=== localStorage Integration ==="
check_pattern "saveReadingPosition function exists" "function saveReadingPosition"
check_pattern "loadReadingPosition function exists" "function loadReadingPosition"
check_pattern "localStorage.setItem for chapter" "localStorage\.setItem.*currentChapter"
check_pattern "localStorage.getItem for chapter" "localStorage\.getItem.*currentChapter"
echo ""

echo "=== Responsive CSS ==="
check_pattern "Pagination button styling" "\.pagination-btn"
check_pattern "Disabled button state styling" "\.pagination-btn:disabled"
check_pattern "Chapter selector styling" "\.chapter-selector"
check_pattern "Tablet breakpoint (768px)" "@media.*max-width.*768px"
check_pattern "Mobile breakpoint (480px)" "@media.*max-width.*480px"
echo ""

echo "=== Error Handling ==="
check_pattern "Try-catch for localStorage" "try {.*localStorage"
check_pattern "Chapter number validation" "parseInt.*10"
echo ""

echo "=========================================="
echo "VERIFICATION SUMMARY"
echo "=========================================="
echo "✅ Passed: $PASS"
echo "❌ Failed: $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "🎉 SUCCESS: All implementation checks passed!"
    echo "✅ Code is ready for manual browser testing"
    exit 0
else
    echo "⚠️  WARNING: Some implementation checks failed"
    echo "Please review the failures above"
    exit 1
fi
