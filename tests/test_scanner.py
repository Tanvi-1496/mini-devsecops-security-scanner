import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scanner import calculate_score, scan_directory


@pytest.fixture
def temp_repo(tmp_path):
    """Create a temporary repository directory for tests."""
    repo_dir = tmp_path / "test_repo"
    repo_dir.mkdir()
    return repo_dir


def test_gitignore_detection(temp_repo):
    results = scan_directory(temp_repo)
    assert results["gitignore_present"] is False

    (temp_repo / ".gitignore").touch()
    results = scan_directory(temp_repo)
    assert results["gitignore_present"] is True


def test_env_file_detection(temp_repo):
    (temp_repo / ".env").touch()
    results = scan_directory(temp_repo)
    assert results["env_file_detected"] is True


def test_private_key_detection(temp_repo):
    (temp_repo / "server.pem").touch()
    (temp_repo / "id_rsa.key").touch()

    results = scan_directory(temp_repo)

    assert len(results["private_keys"]) == 2
    assert "server.pem" in results["private_keys"]
    assert "id_rsa.key" in results["private_keys"]


def test_secret_pattern_detection(temp_repo):
    code_file = temp_repo / "main.py"
    code_file.write_text(
        'dummy_api_key = "dummy_secret_value"\n'
        'dummy_password = "my_password_123"\n',
        encoding="utf-8",
    )

    results = scan_directory(temp_repo)

    assert len(results["hardcoded_secrets"]) == 2


def test_scoring_system():
    results = {
        "gitignore_present": True,
        "env_file_detected": False,
        "private_keys": [],
        "hardcoded_secrets": [],
        "large_files": [],
        "suspicious_files": [],
    }

    score, status = calculate_score(results)
    assert score == 100
    assert status == "PASS"

    results["env_file_detected"] = True
    results["gitignore_present"] = False

    score, status = calculate_score(results)
    assert score == 65
    assert status == "WARNING"
