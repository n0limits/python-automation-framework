# Quick Start Guide - BVNK API Tests

## Prerequisites

### Required Software

Before starting, install these:

1. **Python 3.12+** - https://www.python.org/downloads/
2. **Git** - https://git-scm.com/downloads
3. **pip** - Comes with Python

### Optional Software (For Future Framework Extension)

NOT needed for BVNK tests but good to have:

4. **Node.js 20.x LTS** - https://nodejs.org/ (for Appium)
5. **Appium** - `npm install -g appium` (for mobile testing)
6. **Java JDK 11/17/21** - https://adoptium.net/ (for Android)
7. **Android Studio** - https://developer.android.com/studio (for Android)
8. **Allure CLI** - `scoop install allure` (for advanced reports)

---

## Quick Installation (5 Minutes)

### Step 1: Install Python & Git
```bash
# Download and install:
# - Python 3.12+: https://www.python.org/downloads/
# - Git: https://git-scm.com/downloads

# Verify installation
python --version  # Should show: Python 3.12.x
git --version
```

### Step 2: Clone & Setup
```bash
# Clone repository
git clone <repo-url>
cd python-automation-framework

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate              # Windows
source .venv/bin/activate           # Mac/Linux

# Install dependencies (this installs all Python packages)
pip install -r requirements.txt
```

### Step 3: Configure
```bash
# Copy environment template (optional - defaults work fine)
copy .env.example .env              # Windows
cp .env.example .env                # Mac/Linux

# Edit .env if needed (default values work for BVNK)
```

### Step 4: Verify
```bash
# Test installation
python -c "from config.settings import settings; print('Config loaded')"

# Run tests
pytest tests/bvnk/ -v -n auto
```

Done! You're ready to run BVNK tests.

---

## What Gets Installed

When you run `pip install -r requirements.txt`, these packages are installed:

### Core Testing (Required for BVNK)
- pytest 8.4.2 - Test framework
- pytest-xdist 3.8.0 - Parallel execution
- pytest-order 1.2.0+ - Test ordering
- pytest-html 4.1.1 - HTML reports
- pytest-metadata 3.1.1 - Report metadata
- requests 2.32.5 - HTTP/API calls
- python-dotenv 1.2.1 - Environment variables
- assertpy 1.1 - Fluent assertions
- faker 37.12.0 - Test data generation
- allure-pytest 2.15.0 - Allure reports

### Framework Extension (Optional, pre-installed)
- playwright 1.55.0 - Web UI testing
- Appium-Python-Client 4.2.0 - Mobile testing
- selenium 4.27.1 - WebDriver support

---

## Setup (One Time) - Detailed

### 1. Install Python 3.12+
```bash
# Windows:
# 1. Download from https://www.python.org/downloads/
# 2. Run installer
# 3. CHECK "Add Python to PATH"
# 4. Click "Install Now"

# Verify
python --version
# Should show: Python 3.12.x
```

**Note:** Python 3.12 has pre-built wheels for all dependencies. No compiler needed!

### 2. Install Git
```bash
# Windows:
# 1. Download from https://git-scm.com/downloads
# 2. Run installer with default settings

# Verify
git --version
```

### 3. Clone Repository
```bash
git clone <repo-url>
cd python-automation-framework
```

### 4. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

**Troubleshooting:** If activation fails on Windows:
```bash
# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
.venv\Scripts\activate
```

### 5. Install Python Packages
```bash
# Upgrade pip first (recommended)
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

**What happens:**
- All test framework packages installed
- All API testing packages installed
- All reporting packages installed
- Optional web/mobile packages installed (for future use)

### 6. Configure Environment (Optional)
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env

# .env contains:
# BVNK_API_BASE_URL=http://bvnksimulator.pythonanywhere.com
# (default values work, no changes needed)
```

### 7. Verify Installation
```bash
# Test configuration loads
python -c "from config.settings import settings; print('Config OK')"

# Test imports work
python -c "import pytest, requests; print('Packages OK')"

# Run quick check
pytest tests/bvnk/functional/test_api_endpoints.py::test_authentication_echo -v -s
```

---

## Optional: Install Additional Software

These are NOT required for BVNK tests but useful for framework extension:

### Install Playwright Browsers (For Web UI Testing)
```bash
python -m playwright install
```

### Install Node.js & Appium (For Mobile Testing)
```bash
# 1. Install Node.js from https://nodejs.org/

# 2. Install Appium
npm install -g appium
appium driver install uiautomator2

# 3. Verify
node --version
appium --version
```

### Install Allure CLI (For Advanced Reports)
```bash
# Windows (using Scoop)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
scoop install allure

# Mac
brew install allure

# Verify
allure --version
```

---

## Verification Checklist

After installation, verify everything:

**Required (Must Work):**
```bash
python --version              # Python 3.12.x
pip --version                 # pip 24.x+
git --version                 # git 2.x+
pytest --version              # pytest 8.4.2
python -c "import requests"   # No error
pytest tests/bvnk/ -v -n auto # Tests run
```

**Optional (For Framework Extension):**
```bash
node --version                # Node.js 20.x
npm --version                 # npm 10.x
appium --version              # Appium 2.x
java -version                 # Java 11/17/21
adb --version                 # Android Platform Tools
allure --version              # Allure 2.x
```

---

## Troubleshooting Installation

### Python Issues

**Problem:** "python is not recognized"
```bash
# Solution: Add Python to PATH
# Windows: Reinstall Python and check "Add to PATH"
# Or manually add: C:\Users\YourName\AppData\Local\Programs\Python\Python312
```

**Problem:** "pip is not recognized"
```bash
# Solution: pip comes with Python
python -m pip --version
# If that works, use: python -m pip install ...
```

### Virtual Environment Issues

**Problem:** Cannot activate virtual environment (Windows)
```bash
# Solution: Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
.venv\Scripts\activate
```

**Problem:** Wrong Python version in virtual environment
```bash
# Solution: Specify Python version
py -3.12 -m venv .venv
```

### Package Installation Issues

**Problem:** Package installation fails
```bash
# Solution 1: Upgrade pip
python -m pip install --upgrade pip

# Solution 2: Install with --user flag
pip install --user -r requirements.txt

# Solution 3: Clear cache and retry
pip cache purge
pip install -r requirements.txt
```

**Problem:** "Module 'config' not found"
```bash
# Solution: Ensure root conftest.py exists
# It should add project root to sys.path

# Verify Python path
python -c "import sys; print(sys.path)"
```

### Git Issues

**Problem:** "git is not recognized"
```bash
# Solution: Install Git from https://git-scm.com/downloads
# Restart terminal after installation
```

---

## Quick Commands Reference
```bash
# Activate environment
.venv\Scripts\activate              # Windows
source .venv/bin/activate           # Mac/Linux

# Install packages
pip install -r requirements.txt

# Run all tests
pytest tests/bvnk/ -v -n auto

# Run specific test category
pytest tests/bvnk/smoke/ -v         # Health checks
pytest tests/bvnk/e2e/ -v -n auto   # E2E conversions
pytest tests/bvnk/functional/ -v -n auto  # Functional tests

# Generate report
pytest tests/bvnk/ -v -n auto --html=reports/bvnk_report.html --self-contained-html

# View report
start reports/bvnk_report.html      # Windows
open reports/bvnk_report.html       # Mac

# Debug mode (sequential, verbose)
pytest tests/bvnk/ -v -s -n0

# Check what's installed
pip list

# Update packages
pip install --upgrade -r requirements.txt
```

---

## System Requirements

### Minimum Requirements (BVNK Tests Only)
- **OS:** Windows 10/11, macOS 10.15+, or Linux Ubuntu 20.04+
- **RAM:** 4 GB
- **Disk Space:** 1 GB
- **Internet:** Required for API calls

### Recommended Requirements (Full Framework)
- **OS:** Windows 10/11, macOS 10.15+, or Linux Ubuntu 20.04+
- **RAM:** 8 GB
- **Disk Space:** 5 GB (with optional tools)
- **Internet:** Required for API calls and downloads

---

## Common Test Commands

### Run All Tests
```bash
# With parallel execution (fastest)
pytest tests/bvnk/ -v -n auto

# Sequential (for debugging)
pytest tests/bvnk/ -v -s -n0
```

### Run Specific Category
```bash
# Health checks (smoke tests)
pytest tests/bvnk/smoke/ -v

# E2E conversion tests
pytest tests/bvnk/e2e/ -v -n auto

# Functional API tests
pytest tests/bvnk/functional/ -v -n auto
```

### Run by Marker
```bash
# All smoke tests
pytest -m smoke -v

# All E2E tests
pytest -m e2e -v -n auto

# All functional tests
pytest -m functional -v -n auto
```

### Run Specific Test
```bash
# Single test with full output
pytest tests/bvnk/e2e/test_currency_conversions.py::test_convert_1_eth_to_trx -v -s

# Single test file
pytest tests/bvnk/functional/test_api_endpoints.py -v
```

### Generate Reports
```bash
# HTML report
pytest tests/bvnk/ -v -n auto --html=reports/bvnk_report.html --self-contained-html

# Allure report (if installed)
pytest tests/bvnk/ -v -n auto --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## Understanding Test Output

### Pre-Session Health Check
```
======================================================================
PRE-SESSION HEALTH CHECK
======================================================================
Verifying BVNK API is ready...
Health URL: http://bvnksimulator.pythonanywhere.com/health

API HEALTH CHECK PASSED
├─ Uptime: 48 days, 17 hours, 31 minutes
├─ DB Size: 4.56 MB
└─ Total Requests: 6029
======================================================================
Proceeding with test execution...
```

This runs automatically before all tests to ensure API is available.

### Test Results
```
========================= test session starts =========================
platform win32 -- Python 3.12.x, pytest-8.4.2

tests/bvnk/smoke/test_health_check.py::test_01_api_is_accessible PASSED
tests/bvnk/e2e/test_currency_conversions.py::test_convert_1_eth_to_trx PASSED
...

========================= 13 passed, 11 skipped in 28.28s =========================
```

- **PASSED** - Test succeeded
- **FAILED** - Test failed (will show error details)
- **SKIPPED** - Test skipped (verification/example tests)

---

## Project Structure Overview

```
python-automation-framework/
├── config/                   # Configuration
│   └── settings.py
│
├── utils/                    # Utilities
│   └── bvnk/                 # BVNK-specific
│       ├── api_client.py
│       ├── conversion_helper.py
│       ├── api_validation_helper.py
│       ├── helpers.py
│       └── test_data.py
│
├── tests/                    # Tests
│   └── bvnk/
│       ├── smoke/            # Health checks (4)
│       ├── e2e/              # Conversions (3)
│       ├── functional/       # API tests (6)
│       ├── verification/     # Debug tests (6)
│       └── examples/         # Usage examples (5)
│
├── reports/                  # Generated reports
├── pytest.ini                # Pytest config
└── requirements.txt          # Dependencies
```

---

## Next Steps

After installation:

1. **Run tests:** `pytest tests/bvnk/ -v -n auto`
2. **Generate report:** `pytest tests/bvnk/ -v -n auto --html=reports/bvnk_report.html`
3. **View report:** `start reports/bvnk_report.html` (Windows) or `open reports/bvnk_report.html` (Mac)
4. **Read full docs:** `README.md`
5. **Understand tests:** Review code in `tests/bvnk/`

---

## Getting Help

If you encounter issues:

1. **Check Troubleshooting section** in this guide
2. **Review README.md** for detailed documentation
3. **Check test logs:** `reports/test_execution.log`
4. **Review API docs:** http://bvnksimulator.pythonanywhere.com/docs
5. **Run verification tests:** `pytest tests/bvnk/verification/ -v -s -n0`

---

## Summary

**Installation Steps:**
1. Install Python 3.12+ and Git
2. Clone repository
3. Create virtual environment
4. Install requirements: `pip install -r requirements.txt`
5. Run tests: `pytest tests/bvnk/ -v -n auto`

**Total Time:** 5-10 minutes

**Disk Space:** approximately 1 GB

**Test Count:** 13 active tests (4 smoke + 3 E2E + 6 functional)

**Status:** Ready for BVNK API testing!

---

## Author

**Victor Grozev**

---

**Happy Testing!**