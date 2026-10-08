# 🛡️ Mini DevSecOps Security Scanner

### 🚀 Live Demo
**[Open the Live Security Scanner][((https://mini-devsecops-security-scanner-deployed-url.streamlit.app/))]

> A Python-based DevSecOps security scanner with an interactive Streamlit dashboard.

### 📦 GitHub Repository

This repository contains the complete source code, tests, documentation, Git workflow, and project files.

A lightweight DevSecOps security scanning project built using **Python, Streamlit, Git, and GitHub**.

The project scans software projects for common security, configuration, and file-hygiene risks. It provides both a **command-line scanner** and an interactive **web dashboard** with a security score, detailed findings, and security recommendations.

---

## 🎯 Project Objective

The objective of this project is to demonstrate a practical DevSecOps workflow by combining:

- Automated security scanning
- Version control using Git
- GitHub-based collaboration
- Feature-based branching
- Pull Requests
- Automated testing
- Documentation
- Release tagging
- Web-based security reporting

The project follows the principle of identifying security issues early in the software development lifecycle.

---

## 🚀 Key Features

### 🔐 Security Scanning

The scanner checks a project for:

- Hardcoded passwords
- API keys
- Access tokens
- Common secret patterns
- Private key files
- `.env` files
- Large files
- Suspicious executable/archive files
- Missing `.gitignore`

### 📊 Security Score

The scanner calculates a security score between **0 and 100**.

| Score | Status | Meaning |
|---|---|---|
| 85–100 | 🟢 PASS | Good security posture |
| 60–84 | 🟡 WARNING | Security issues require attention |
| 0–59 | 🔴 FAIL | Significant security issues detected |

---

# 🌐 Web Dashboard

The project includes an interactive **Streamlit web dashboard**.

The dashboard provides two scanning options.

## 🧪 1. Sample Project Scan

The project contains an intentionally vulnerable `sample-project`.

It can be scanned directly from the dashboard without uploading a file.

The sample project contains **dummy credentials** so that the scanner can demonstrate secret detection.

Example result:

```text
Security Score: 70/100
Final Status:   WARNING
Issues Detected: 2



📦 2. Upload Project ZIP
Users can upload their own project as a .zip file.
The application automatically performs the following workflow:
Upload ZIP
    ↓
Extract Project
    ↓
Scan Project
    ↓
Calculate Security Score
    ↓
Display Findings
    ↓
Generate Recommendations

The uploaded project is extracted into a temporary directory for scanning.
The application also checks ZIP paths before extraction to reduce the risk of ZIP path traversal.
📊 Dashboard Features
The dashboard displays the following information.
📦 Project Information
- Project name
- Scanner name
📈 Security Overview
- Security score
- Final status
- Total issues detected
🔐 Security Checks
- .gitignore
- .env
- Private keys
- Hardcoded secrets
- Large files
- Suspicious files
📋 Findings Summary
The dashboard provides individual counts for:
- 🔴 Secrets
- 🔴 Private keys
- 🟡 Large files
- 🟡 Suspicious files
🔎 Detailed Findings
Detected issues are displayed with their file paths and line numbers wherever applicable.
💡 Security Recommendations
The scanner provides recommendations such as:
- Move secrets to environment variables
- Remove private key files
- Avoid committing .env files
- Review large files
- Review suspicious executable/archive files
- Create a .gitignore
🏗️ System Workflow
                  ┌─────────────────────┐
                  │   User / Developer  │
                  └──────────┬──────────┘
                             │
                             ↓
                  ┌─────────────────────┐
                  │    Streamlit UI     │
                  │                     │
                  │ Sample / ZIP Upload │
                  └──────────┬──────────┘
                             │
                             ↓
                  ┌─────────────────────┐
                  │ Project Extraction  │
                  └──────────┬──────────┘
                             │
                             ↓
                  ┌─────────────────────┐
                  │  Security Scanner   │
                  │     scanner.py      │
                  └──────────┬──────────┘
                             │
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
        Secret Scan     File Scan      Config Scan
              │              │              │
              └──────────────┼──────────────┘
                             ↓
                  ┌─────────────────────┐
                  │   Security Score    │
                  │  PASS/WARNING/FAIL  │
                  └──────────┬──────────┘
                             │
                             ↓
                  ┌─────────────────────┐
                  │ Findings &          │
                  │ Recommendations    │
                  └─────────────────────┘

📁 Project Structure
devsecops-security-scanner/
│
├── app.py
│   └── Streamlit web dashboard
│
├── scanner.py
│   └── Core security scanning engine
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│   └── Project documentation
│
├── .gitignore
│   └── Git ignore configuration
│
├── tests/
│   └── test_scanner.py
│       └── Automated scanner tests
│
├── docs/
│   ├── security-checks.md
│   │   └── Security checks documentation
│   │
│   └── git-workflow.md
│       └── Git workflow documentation
│
├── sample-project/
│   ├── app.py
│   ├── config.txt
│   └── README.md
│
└── screenshots/
    ├── dashboard.png
    ├── sample-scan.png
    ├── upload-scan.png
    ├── findings.png
    └── github-repository.png

⚙️ Technologies Used
Technology	Purpose
Python	Security scanning engine
Streamlit	Interactive web dashboard
Pytest	Automated testing
Git	Version control
GitHub	Repository hosting and collaboration
Markdown	Project documentation


💻 Installation
1. Clone the Repository
git clone https://github.com/Tanvi-1496/mini-devsecops-security-scanner.git

2. Enter the Project Directory
cd mini-devsecops-security-scanner

3. Install Dependencies
python -m pip install -r requirements.txt

▶️ Running the CLI Scanner
The scanner can be executed directly from the command line.
To scan the included sample project:
python scanner.py sample-project

Example output:
==================================================
          Mini DevSecOps Security Scanner
==================================================

Target Directory: sample-project

Security Checks Results:
  [PASS] .gitignore file present
  [PASS] No .env file detected
  [PASS] No private key files detected
  [WARN] Hardcoded secret(s) found
  [PASS] No large files detected
  [PASS] No suspicious executable/archive extensions detected

--------------------------------------------------
Security Score: 70/100
Final Status:   WARNING
==================================================

The sample project intentionally contains fake credentials for testing the scanner.
Note: No real credentials should be placed in the sample project.

🌐 Running the Streamlit Dashboard
Start the application using:
python -m streamlit run app.py

The application will open in the browser.
The dashboard allows users to choose between:
🧪 Sample Project

and
📦 Upload Project ZIP

🧪 Automated Testing
The project uses Pytest for automated testing.
Run:
python -m pytest

Expected result:
5 passed

The tests validate important scanner functionality including:
- .gitignore detection
- Secret detection
- Private key detection
- Suspicious file detection
- Security score calculation
🌿 Git Branching Strategy
The project follows a feature-based Git workflow.
                    ┌──────────────┐
                    │     main     │
                    │ Stable Code  │
                    └──────▲───────┘
                           │
                      Pull Request
                           │
                    ┌──────┴───────┐
                    │      dev     │
                    │ Development  │
                    └──────▲───────┘
                           │
                      Pull Request
                           │
                 ┌─────────┴─────────┐
                 │     feature/*     │
                 │ Feature Development│
                 └───────────────────┘

Branches Used
Branch	Purpose
main	Stable and release-ready code
dev	Development and integration branch
feature/*	Individual feature development


🔄 Git Workflow Implemented
The following Git workflow was used during development.
Step 1: Initialize Git
git init
git branch -M main

Step 2: Create Development Branch
git checkout -b dev

Step 3: Create Feature Branch
git checkout -b feature/security-dashboard

Step 4: Develop and Test
The application was developed and tested locally before committing changes.
Step 5: Commit Changes
git add .
git commit -m "Add Streamlit security dashboard"

Step 6: Push Feature Branch
git push -u origin feature/security-dashboard

Step 7: Create Pull Request
The feature branch was merged into:
feature/security-dashboard → dev

Step 8: Merge Development Branch
After testing:
dev → main

Step 9: Create Release Tag
git tag -a v1.1.0 -m "Release Streamlit security dashboard"
git push origin v1.1.0

🏷️ Release History
Version	Description
v1.0.0	Initial security scanner, Git workflow and documentation
v1.1.0	Streamlit dashboard, sample scan and ZIP upload scanning


🔐 Security Considerations
The project demonstrates basic DevSecOps security practices.
🔑 Secret Detection
The scanner identifies common hardcoded secret patterns.
📄 .env Detection
Environment files are detected because they may contain sensitive credentials.
🔐 Private Key Detection
Common private key file extensions such as:
.pem
.key
.p12
.pfx
.asc

are detected.
⚠️ Suspicious Files
Potentially risky executable and archive extensions are reported.
📁 .gitignore
The project uses .gitignore to prevent unnecessary or sensitive files from being committed.
📦 ZIP Security
Uploaded ZIP files are checked for unsafe paths before extraction.
🗂️ Temporary Processing
Uploaded projects are extracted into temporary directories during scanning.


📚 Documentation
Additional documentation is available in the docs directory.
Security Checks
docs/security-checks.md

Contains information about the security checks implemented by the scanner.
Git Workflow
docs/git-workflow.md

Documents the branching strategy and Git workflow used in the project.




📈 Future Enhancements
Possible future improvements include:
- GitHub Actions integration
- Automated security scanning on every Pull Request
- Additional secret-detection patterns
- Dependency vulnerability scanning
- Static Application Security Testing (SAST)
- Container image scanning
- PDF security reports
- Historical scan results
- Authentication and role-based access
- Cloud deployment
- Integration with tools such as Bandit, Trivy, and OWASP ZAP


👩‍💻 Author
Tanvi Jaware
B.Tech Information Technology
Vidyalankar Institute of Technologyv
