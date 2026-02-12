#!/bin/bash
# test_performance.sh
# Automated performance verification for dynamic .txt loading

echo "=== Performance Verification Test ==="

# Test 1: File size
echo -e "\n1. File Size Test:"
FILE_SIZE=$(stat -f%z index.html 2>/dev/null || stat -c%s index.html 2>/dev/null)
FILE_SIZE_KB=$((FILE_SIZE / 1024))
echo "   index.html size: ${FILE_SIZE} bytes (${FILE_SIZE_KB}KB)"
if [ "$FILE_SIZE" -lt 102400 ]; then
    echo "   ✅ PASSED: File size < 100KB (requirement met)"
    if [ "$FILE_SIZE" -lt 51200 ]; then
        echo "   🎯 BONUS: File size < 50KB (exceeded target!)"
    fi
else
    echo "   ❌ FAILED: File size >= 100KB"
    exit 1
fi

# Test 2: Lazy loading attributes
echo -e "\n2. Lazy Loading Attributes Test:"
LAZY_COUNT=$(grep -c 'data-loaded="false"' index.html)
echo "   data-loaded attributes: $LAZY_COUNT"
if [ "$LAZY_COUNT" -eq 40 ]; then
    echo "   ✅ PASSED: 40 chapters have lazy loading (20 Vietnamese + 20 Japanese)"
else
    echo "   ❌ FAILED: Expected 40, got $LAZY_COUNT"
    exit 1
fi

# Test 3: Dynamic loading function
echo -e "\n3. Dynamic Loading Function Test:"
if grep -q "async function loadChapter" index.html; then
    echo "   ✅ PASSED: loadChapter() async function exists"
else
    echo "   ❌ FAILED: loadChapter() function not found"
    exit 1
fi

# Test 4: Paragraph parsing function
echo -e "\n4. Paragraph Parsing Function Test:"
if grep -q "function parseTextContent" index.html; then
    echo "   ✅ PASSED: parseTextContent() function exists"
else
    echo "   ❌ FAILED: parseTextContent() function not found"
    exit 1
fi

# Test 5: Auto-load implementation
echo -e "\n5. Auto-load Implementation Test:"
if grep -q "DOMContentLoaded" index.html; then
    echo "   ✅ PASSED: DOMContentLoaded event listener exists"
else
    echo "   ❌ FAILED: Auto-load not implemented"
    exit 1
fi

# Test 6: Error handling
echo -e "\n6. Error Handling Test:"
if grep -q "try {" index.html && grep -q "catch" index.html; then
    echo "   ✅ PASSED: try-catch error handling implemented"
else
    echo "   ❌ FAILED: Error handling not found"
    exit 1
fi

# Test 7: Loading spinner
echo -e "\n7. Loading Spinner Test:"
if grep -q "loading-spinner" index.html; then
    echo "   ✅ PASSED: Loading spinner CSS/HTML exists"
else
    echo "   ❌ FAILED: Loading spinner not found"
    exit 1
fi

# Test 8: Chapter containers
echo -e "\n8. Chapter Container Test:"
VI_CHAPTERS=$(grep -c 'id="chapter-[0-9]' index.html)
JA_CHAPTERS=$(grep -c 'id="chapter-ja-[0-9]' index.html)
echo "   Vietnamese chapters: $VI_CHAPTERS"
echo "   Japanese chapters: $JA_CHAPTERS"
if [ "$VI_CHAPTERS" -eq 20 ] && [ "$JA_CHAPTERS" -eq 20 ]; then
    echo "   ✅ PASSED: All 40 chapter containers exist"
else
    echo "   ❌ FAILED: Expected 20 Vietnamese + 20 Japanese"
    exit 1
fi

# Performance Summary
echo -e "\n=== PERFORMANCE SUMMARY ==="
ORIGINAL_SIZE=928
CURRENT_SIZE_KB=$((FILE_SIZE / 1024))
REDUCTION=$((100 - (CURRENT_SIZE_KB * 100 / ORIGINAL_SIZE)))
echo "   Original size: ${ORIGINAL_SIZE}KB"
echo "   Current size: ${CURRENT_SIZE_KB}KB"
echo "   Reduction: ${REDUCTION}% 🎉"

echo -e "\n=== ALL AUTOMATED TESTS PASSED ✅ ==="
echo -e "\n📊 Performance Verification Complete!"
echo -e "\nNext Steps for Manual Testing:"
echo "1. Start server: python3 -m http.server 8000"
echo "2. Open browser: http://localhost:8000/"
echo "3. Open DevTools Network tab (F12)"
echo "4. Hard refresh (Ctrl+Shift+R)"
echo "5. Verify only 2 initial requests: index.html + chapter1.txt"
echo "6. Click Chapter 2, verify lazy loading (new .txt request)"
echo "7. Click Chapter 2 again, verify NO new request (cached)"
echo "8. Switch to 日本語 tab, test Japanese chapters"
echo "9. Verify paragraph spacing visually"
