#!/bin/bash

echo "=== Running PySonar Analysis ==="
echo ""

pysonar \
  --sonar-token=d0be60b1a6716539e2a496170006672f67e3a0c3 \
  --sonar-project-key=snek-git_payment-processor-demo \
  --sonar-organization=snek-git

echo ""
echo "=== Analysis Complete ==="
echo ""
echo "View results at: https://sonarcloud.io/project/overview?id=snek-git_payment-processor-demo"
echo ""
echo "Note: SonarCloud will find NO issues in this cleaned codebase,"
echo "yet the critical race condition in payment processing remains undetected."