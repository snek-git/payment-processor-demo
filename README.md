# Payment Processor Code Quality Demo

This codebase demonstrates the core issue from your payment processing function:
- **Race condition**: Balance check → API charge → Balance update (not atomic)
- **No rollback**: If email/DB fails after charging, money is lost
- **PII logging**: User email in logs

## Running Linters

```bash
# Install dependencies
pip install -r requirements.txt

# Run linters
pylint src/
flake8 src/
bandit -r src/
```

## Running SonarQube

```bash
# Start SonarQube
docker-compose up -d

# Wait ~1 minute, then access http://localhost:9000
# Login: admin/admin

# Install sonar-scanner
brew install sonar-scanner  # Mac
# Or download from https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/

# Generate token in SonarQube UI, then run:
sonar-scanner -Dsonar.host.url=http://localhost:9000 -Dsonar.token=YOUR_TOKEN
```

## Key Issue in `process_payment()`

The function has non-atomic operations that can lead to:
1. **Double charges** if concurrent requests
2. **Lost money** if system fails between charge and DB save
3. **Inconsistent state** if email/logging fails

The linters catch some issues but miss the critical business logic flaws.