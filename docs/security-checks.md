# Security Checks Documentation

This document describes the security checks implemented by the Mini DevSecOps Security Scanner.

## 1. Missing `.gitignore`

**What it does:** Checks whether a `.gitignore` file exists in the root of the scanned directory.

**Why it matters:** A `.gitignore` helps prevent temporary files, dependencies, build artifacts, and environment files from being accidentally committed.

**Warning trigger:** No root `.gitignore` file is found.

**Limitation:** The scanner checks only for the file's presence. It does not evaluate the quality of its rules.

## 2. Exposed `.env` Files

**What it does:** Detects files named `.env` or files whose names end with `.env`.

**Why it matters:** Environment files can contain credentials, API keys, database URLs, and other sensitive configuration.

**Warning trigger:** A matching `.env` file is found inside the scanned directory.

**Limitation:** The rule is intentionally simple and does not determine whether the file contains actual credentials.

## 3. Private-Key File Detection

**What it does:** Detects files with `.pem`, `.key`, `.p12`, `.pfx`, or `.asc` extensions.

**Why it matters:** Private keys and certificates can provide unauthorized access if exposed.

**Warning trigger:** A file uses one of the configured private-key extensions.

**Limitation:** Detection is based on file extension rather than file-content analysis.

## 4. Hardcoded Secret Detection

**What it does:** Scans readable text files for assignments using sensitive names such as `password`, `secret`, `api_key`, `access_token`, `private_key`, or `token`.

**Why it matters:** Hardcoded credentials can remain in source code and Git history.

**Warning trigger:** A line matches a pattern such as:

```python
api_key = "example_value"
```

**Limitation:** Regex-based detection can produce false positives and can miss obfuscated or unusually formatted secrets.

## 5. Large and Suspicious Files

**What it does:** Flags files larger than 5 MB and files using configured executable/archive extensions such as `.exe`, `.dll`, `.so`, `.bin`, `.zip`, `.tar`, and `.gz`.

**Why it matters:** Unexpected binaries can increase repository size and may deserve additional review.

**Warning trigger:** A file exceeds 5 MB or uses a configured suspicious extension.

**Limitation:** Some legitimate project assets can match these rules, so findings require human review.

## Security Score

The scanner starts with a score of 100.

| Finding | Penalty |
|---|---:|
| Missing `.gitignore` | -15 |
| `.env` detected | -20 |
| Each private-key file | -20 |
| Each hardcoded secret | -15 |
| Each large file | -10 |
| Each suspicious file | -10 |

Status thresholds:

- **PASS:** 85–100
- **WARNING:** 60–84
- **FAIL:** 0–59
