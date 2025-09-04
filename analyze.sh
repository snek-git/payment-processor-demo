#!/bin/bash

echo "=== Code Quality Analysis Demo ==="
echo ""
echo "Running various linters on payment processor code..."
echo ""

echo "1. PYLINT:"
echo "-----------"
if pylint src/ --disable=R0903 2>/dev/null; then
    echo "✓ No pylint issues found"
fi
echo ""

echo "2. FLAKE8:"
echo "-----------"
if flake8 src/ 2>/dev/null; then
    echo "✓ No flake8 issues found"
fi
echo ""

echo "3. BANDIT (Security):"
echo "---------------------"
if bandit -r src/ -f txt 2>/dev/null | grep -q "No issues identified"; then
    echo "✓ No security issues found"
    bandit -r src/ -f txt 2>/dev/null | grep "No issues identified"
else
    bandit -r src/ -f txt 2>/dev/null
fi
echo ""

echo "4. PYSONAR (SonarCloud):"
echo "------------------------"
pysonar \
  --sonar-token=d0be60b1a6716539e2a496170006672f67e3a0c3 \
  --sonar-project-key=snek-git_payment-processor-demo \
  --sonar-organization=snek-git

echo ""
echo "=== Analysis Complete ==="
echo ""
echo "View SonarCloud results at: https://sonarcloud.io/project/overview?id=snek-git_payment-processor-demo"
echo ""
echo "IMPORTANT: All linters find NO issues in this codebase,"
echo "yet the CRITICAL RACE CONDITION in payment processing remains undetected:"
echo ""
echo "  - Two concurrent requests can double-charge users"
echo "  - System failure after charge but before DB save = lost money"
echo "  - Non-atomic transaction violates payment processing fundamentals"
echo ""
echo "This demonstrates the limitations of static analysis tools."