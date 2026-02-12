#!/bin/bash
# Test script to verify all Vietnamese chapters are accessible

echo "=== Testing Vietnamese Chapters ==="
echo ""

failed=0
passed=0

for num in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
    url="http://localhost:8000/chapters/vi/chapter${num}.txt"
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")

    if [ "$status" = "200" ]; then
        echo "✓ Chapter $num: OK (HTTP $status)"
        ((passed++))
    else
        echo "✗ Chapter $num: FAILED (HTTP $status)"
        ((failed++))
    fi
done

echo ""
echo "=== Summary ==="
echo "Passed: $passed/20"
echo "Failed: $failed/20"

if [ $failed -eq 0 ]; then
    echo "✓ All Vietnamese chapters are accessible!"
    exit 0
else
    echo "✗ Some chapters failed to load"
    exit 1
fi
