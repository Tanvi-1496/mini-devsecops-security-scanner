# Mini DevSecOps Security Scanner

A lightweight Python CLI tool that scans project directories for common configuration risks, exposed secrets, and repository hygiene issues.

## Objective

Demonstrate practical DevSecOps principles while following Git and GitHub version-control best practices.

## Features

- **Git hygiene check:** Detects whether the scanned directory has a root `.gitignore`.
- **Environment-file detection:** Detects `.env` files.
- **Private-key detection:** Flags common private-key and certificate extensions.
- **Hardcoded-secret detection:** Uses a regular expression to detect common secret assignments.
- **Large-file detection:** Flags files larger than 5 MB.
- **Suspicious-file detection:** Flags common executable/archive extensions.
- **Security scoring:** Produces a score from 0 to 100 with `PASS`, `WARNING`, or `FAIL`.

## Technologies

- Python 3
- Python standard library: `os`, `re`, `sys`, `pathlib`
- pytest for unit testing

## Project Structure

```text
devsecops-security-scanner/
├── scanner.py
├── requirements.txt
├── README.md
├── .gitignore
├── docs/
│   └── security-checks.md
├── sample-project/
│   ├── app.py
│   ├── config.txt
│   └── README.md
└── tests/
    └── test_scanner.py
```

## Installation

Install the test dependency:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the scanner against the included sample project:

```bash
python scanner.py ./sample-project
```

## Expected Scanner Result

The included `sample-project` intentionally has:

- no `.gitignore`
- no `.env` file
- no private-key files
- two harmless dummy secret variables
- no large files
- no suspicious file extensions

Scoring:

```text
Starting score:       100
Missing .gitignore:   -15
2 hardcoded secrets:  -30
Final score:           55/100
Final status:          FAIL
```

Expected output:

```text
Security Checks Results:
  [WARN] .gitignore missing (-15 pts)
  [PASS] No .env file detected
  [PASS] No private key files detected
  [WARN] Hardcoded secret(s) found (2) (-15 pts ea):
      - app.py:5 (password)
      - app.py:6 (api_key)
  [PASS] No large files detected
  [PASS] No suspicious executable/archive extensions detected

--------------------------------------------------
Security Score: 55/100
Final Status:   FAIL
==================================================
```

The `FAIL` status is intentional because the sample project is designed to demonstrate the scanner detecting issues.

## Documentation

See [Security Checks Documentation](docs/security-checks.md).

## Testing

Run all tests from the project root:

```bash
python -m pytest
```

Expected result:

```text
5 passed
```

## Limitations

This is an educational scanner, not a replacement for production SAST or secret-scanning tools.

- Secret detection is based on common variable names and regular expressions.
- False positives are possible.
- File-extension checks do not inspect file contents.
- The scanner does not perform AST-based code analysis.

## Author

DevOps Engineering Internship Candidate
