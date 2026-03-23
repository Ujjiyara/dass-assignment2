# Assignment 2: Software Testing

**Roll Number**: 2024115005

## Repository Structure

```
whitebox/          ← Q1: White Box Testing (MoneyPoly)
  diagrams/        ← Hand-drawn Control Flow Graph
  tests/           ← pytest test cases
  code/            ← MoneyPoly source code
  report.pdf       ← Report with pylint iterations + 15 errors

integration/       ← Q2: Integration Testing (StreetRace Manager)
...
### Q1: White Box Tests
```bash
PYTHONPATH=whitebox/code pytest whitebox/tests/ -v
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
