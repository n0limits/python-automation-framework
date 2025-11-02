# Quick Start Guide - BVNK API Tests

## Prerequisites

### Required Software

Before starting, install these:

1. **Python 3.12+** - https://www.python.org/downloads/
2. **Git** - https://git-scm.com/download/win
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
# - Python 3.12: https://www.python.org/downloads/
# - Git: https://git-scm.com/download/win

# Verify installation
python --version  # Should show: Python 3.12.x
git --version
```

### Step 2: Clone & Setup
```bash
# Clone repository
git clone <your-repo-url>
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
# Copy environment template
copy .env.example .env              # Windows
cp .env.example .env                # Mac/Linux

# Edit .env if needed (default values work for BVNK)
```

### Step 4: Verify
```bash
# Test installation
python -c "from config.settings import settings; print('Config loaded')"

# Run tests
pytest tests/bvnk/ -v -s
```

Done! You're ready to run BVNK tests.

---

## What Gets Installed

When you run `pip install -r requirements.txt`, these packages are installed:

### Core Testing (Required for BVNK)
- pytest 8.4.2 - Test framework
- requests 2.32.5 - HTTP/API calls
- python-dotenv 1.1.1 - Environment variables
- assertpy 1.1 - Fluent assertions
- faker 22.0.0 - Test data generation

### Reporting (Required for BVNK)
- pytest-html 4.1.1 - HTML reports
- allure-pytest 2.13.2 - Allure reports

### Framework Extension (Optional, pre-installed)
- playwright 1.55.0 - Web UI testing
- Appium-Python-Client 3.1.0 - Mobile testing
- selenium 4.15.2 - WebDriver support

---

## Setup (One Time) - Detailed

### 1. Install Python 3.12
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

### 2. Install Git
```bash
# Windows:
# 1. Download from https://git-scm.com/download/win
# 2. Run installer with default settings

# Verify
git --version
```

### 3. Clone Repository
```bash
git clone <your-repo-url>
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

### 5. Install Python Packages
```bash
# This installs all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

### 6. Configure Environment
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
```bash
# Required (Must Work)
[ ] python --version              # Python 3.12.x
[ ] pip --version                 # pip 24.x
[ ] git --version                 # git 2.x
[ ] pytest --version              # pytest 8.4.2
[ ] python -c "import requests"   # No error
[ ] pytest tests/bvnk/ -v         # Tests run

# Optional (For Framework Extension)
[ ] node --version                # Node.js 20.x
[ ] npm --version                 # npm 10.x
[ ] appium --version              # Appium 2.x
[ ] java -version                 # Java 11/17/21
[ ] adb --version                 # Android Platform Tools
[ ] allure --version              # Allure 2.x
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

**Problem:** "greenlet requires Visual C++"
```bash
# Solution: Use Python 3.12 (not 3.13/3.14)
# Python 3.12 has pre-built wheels, no compilation needed
```

**Problem:** "Module 'config' not found"
```bash
# Solution: Ensure root conftest.py exists
# It should add project root to sys.path
```

### Git Issues

**Problem:** "git is not recognized"
```bash
# Solution: Install Git from https://git-scm.com/download/win
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

# Run tests
pytest tests/bvnk/ -v -s

# Generate report
pytest tests/bvnk/ --html=reports/bvnk_report.html

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
- **Disk Space:** 10 GB (with Android Studio)
- **Internet:** Required for API calls and downloads

---

## Next Steps

After installation:

1. **Run tests:** `pytest tests/bvnk/ -v -s`
2. **Generate report:** `pytest tests/bvnk/ --html=reports/bvnk_report.html`
3. **Read full docs:** `README_BVNK.md`
4. **Understand tests:** Review code in `tests/bvnk/`

---