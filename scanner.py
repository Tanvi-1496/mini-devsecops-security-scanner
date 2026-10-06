"""
Mini DevSecOps Security Scanner

A lightweight CLI tool that scans a project directory for common
configuration risks, exposed secrets, and file hygiene issues.
"""

import os
import re
import sys
from pathlib import Path

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

PRIVATE_KEY_EXTENSIONS = {".pem", ".key", ".p12", ".pfx", ".asc"}
SUSPICIOUS_EXTENSIONS = {".exe", ".dll", ".so", ".bin", ".zip", ".tar", ".gz"}

SECRET_PATTERN = re.compile(
    r"""(?i)(password|secret|api_key|access_token|private_key|token)\s*=\s*["']([^"']+)["']"""
)


def scan_directory(target_path):
    """Traverse the target directory and return scan findings."""
    path = Path(target_path)

    if not path.exists():
        raise FileNotFoundError(f"Directory does not exist: {target_path}")
    if not path.is_dir():
        raise NotADirectoryError(
            f"Provided path is not a directory: {target_path}"
        )

    results = {
        "gitignore_present": (path / ".gitignore").is_file(),
        "env_file_detected": False,
        "private_keys": [],
        "hardcoded_secrets": [],
        "large_files": [],
        "suspicious_files": [],
    }

    for current_root, _, files in os.walk(path):
        for file_name in files:
            file_path = Path(current_root) / file_name

            try:
                relative_path = file_path.relative_to(path)
            except ValueError:
                relative_path = file_path

            extension = file_path.suffix.lower()

            if file_name == ".env" or file_name.endswith(".env"):
                results["env_file_detected"] = True

            if extension in PRIVATE_KEY_EXTENSIONS:
                results["private_keys"].append(str(relative_path))

            if extension in SUSPICIOUS_EXTENSIONS:
                results["suspicious_files"].append(str(relative_path))

            try:
                if file_path.stat().st_size > MAX_FILE_SIZE_BYTES:
                    results["large_files"].append(str(relative_path))
            except OSError:
                continue

            scan_file_content(file_path, relative_path, results)

    return results


def scan_file_content(file_path, relative_path, results):
    """Search readable text files for common hardcoded-secret patterns."""
    extension = file_path.suffix.lower()

    if extension in SUSPICIOUS_EXTENSIONS or extension in PRIVATE_KEY_EXTENSIONS:
        return

    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as file:
            for line_number, line in enumerate(file, start=1):
                match = SECRET_PATTERN.search(line)
                if match:
                    key_name = match.group(1)
                    results["hardcoded_secrets"].append(
                        f"{relative_path}:{line_number} ({key_name})"
                    )
    except (OSError, UnicodeError):
        pass


def calculate_score(results):
    """Calculate a security score and return (score, status)."""
    score = 100

    if not results["gitignore_present"]:
        score -= 15
    if results["env_file_detected"]:
        score -= 20

    score -= len(results["private_keys"]) * 20
    score -= len(results["hardcoded_secrets"]) * 15
    score -= len(results["large_files"]) * 10
    score -= len(results["suspicious_files"]) * 10

    score = max(0, min(100, score))

    if score >= 85:
        status = "PASS"
    elif score >= 60:
        status = "WARNING"
    else:
        status = "FAIL"

    return score, status


def print_report(target_path, results, score, status):
    """Print the scan report."""
    print("=" * 50)
    print("          Mini DevSecOps Security Scanner")
    print("=" * 50)
    print(f"Target Directory: {target_path}\n")
    print("Security Checks Results:")

    if results["gitignore_present"]:
        print("  [PASS] .gitignore file present")
    else:
        print("  [WARN] .gitignore missing (-15 pts)")

    if results["env_file_detected"]:
        print("  [WARN] Exposed .env file detected (-20 pts)")
    else:
        print("  [PASS] No .env file detected")

    if results["private_keys"]:
        print(
            f"  [WARN] Private key file(s) found "
            f"({len(results['private_keys'])}) (-20 pts ea):"
        )
        for key in results["private_keys"]:
            print(f"      - {key}")
    else:
        print("  [PASS] No private key files detected")

    if results["hardcoded_secrets"]:
        print(
            f"  [WARN] Hardcoded secret(s) found "
            f"({len(results['hardcoded_secrets'])}) (-15 pts ea):"
        )
        for secret in results["hardcoded_secrets"]:
            print(f"      - {secret}")
    else:
        print("  [PASS] No hardcoded secrets detected")

    if results["large_files"]:
        print(
            f"  [WARN] Large file(s) (>5MB) detected "
            f"({len(results['large_files'])}) (-10 pts ea):"
        )
        for file_name in results["large_files"]:
            print(f"      - {file_name}")
    else:
        print("  [PASS] No large files detected")

    if results["suspicious_files"]:
        print(
            f"  [WARN] Suspicious file extension(s) detected "
            f"({len(results['suspicious_files'])}) (-10 pts ea):"
        )
        for file_name in results["suspicious_files"]:
            print(f"      - {file_name}")
    else:
        print("  [PASS] No suspicious executable/archive extensions detected")

    print("\n" + "-" * 50)
    print(f"Security Score: {score}/100")
    print(f"Final Status:   {status}")
    print("=" * 50)


def main():
    if len(sys.argv) < 2:
        print("Error: Missing target directory argument.")
        print("Usage: python scanner.py <target_directory_path>")
        sys.exit(2)

    target_directory = sys.argv[1]

    try:
        results = scan_directory(target_directory)
        score, status = calculate_score(results)
        print_report(target_directory, results, score, status)

        sys.exit(1 if status == "FAIL" else 0)

    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"Error: {error}")
        sys.exit(2)


if __name__ == "__main__":
    main()
