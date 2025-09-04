#!/bin/bash

echo "=== Code Quality Analysis Demo ==="
echo ""
echo "This demo showcases various code quality issues that can be detected by:"
echo "1. Python linters (pylint, flake8, bandit)"
echo "2. SonarQube"
echo ""

echo "=== Running Python Linters ==="
echo ""

echo "1. PYLINT Analysis:"
echo "-------------------"
pylint src/ --disable=C0103,C0114,C0115,C0116 --output-format=text 2>/dev/null | head -30
echo ""

echo "2. FLAKE8 Analysis:"
echo "-------------------"
flake8 src/ --count --statistics 2>/dev/null | head -20
echo ""

echo "3. BANDIT Security Analysis:"
echo "-----------------------------"
bandit -r src/ -f txt 2>/dev/null | grep -A 3 ">> Issue:" | head -40
echo ""

echo "=== SonarQube Setup Instructions ==="
echo ""
echo "To run SonarQube analysis:"
echo "1. Start SonarQube: docker-compose up -d"
echo "2. Wait ~1 minute for SonarQube to start"
echo "3. Access SonarQube at: http://localhost:9000"
echo "4. Default login: admin/admin (change on first login)"
echo "5. Install sonar-scanner: brew install sonar-scanner (Mac) or download from SonarQube site"
echo "6. Run analysis: sonar-scanner -Dsonar.host.url=http://localhost:9000 -Dsonar.token=YOUR_TOKEN"
echo ""
echo "Note: You'll need to generate a token in SonarQube UI after logging in."