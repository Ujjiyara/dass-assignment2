# Assignment 2: Software Testing

**Roll Number**: 2024115005

## Repository Structure

```
whitebox/          ← Q1: White Box Testing (MoneyPoly)
  diagrams/        ← Hand-drawn Control Flow Graph
  tests/           ← pytest test cases
  report.pdf       ← Report with pylint iterations + 15 errors

integration/       ← Q2: Integration Testing (StreetRace Manager)
  diagrams/        ← Hand-drawn Call Graph
  tests/           ← pytest integration tests
  code/            ← StreetRace modules
  report.pdf       ← Report with call graph + 8 test cases

blackbox/          ← Q3: Black Box API Testing (QuickCart)
  tests/           ← pytest API tests
  report.pdf       ← Bug report with 19 confirmed bugs

moneypoly/         ← Original MoneyPoly source code (with fixes applied)
```

## How to Run

### Prerequisites
- Python 3.12+
- `pytest` and `requests` (`pip install pytest requests`)
- Docker (for Q3 only)

### Q1: White Box Tests
```bash
PYTHONPATH=moneypoly/moneypoly pytest whitebox/tests/ -v
```

### Q2: Integration Tests
```bash
PYTHONPATH=integration/code pytest integration/tests/ -v
```

### Q3: Black Box API Tests
```bash
# Start the QuickCart API server first
docker run -p 8080:8080 quickcart

# Run the tests
pytest blackbox/tests/ -v
```

## Git Repository
https://github.com/Ujjiyara/dass-assignment2
