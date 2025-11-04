# BVNK API Testing Assignment

This document provides detailed information about the BVNK API testing implementation.

## Assignment Overview

Automated testing suite for the BVNK cryptocurrency conversion API simulator, demonstrating end-to-end and functional API testing capabilities.

**API Base URL:** http://bvnksimulator.pythonanywhere.com  
**Documentation:** http://bvnksimulator.pythonanywhere.com/docs

---

## Software Requirements

### Required Software (Must Have)

#### 1. Python 3.13+ (Core)
- **Version:** 3.13.x
- **Why:** Runs the test framework
- **Download:** https://www.python.org/downloads/
- **Important for Windows:** Python 3.13 requires Microsoft Visual C++ Build Tools
    - Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    - Select: "Desktop development with C++"
    - Size: ~6 GB
    - Time: ~15 minutes
- **Verify:**
```bash
  python --version
  # Should show: Python 3.13.x
```

#### 2. Microsoft Visual C++ Build Tools (Windows Only)
- **Version:** Latest
- **Why:** Required for compiling greenlet package (dependency of Appium and Allure)
- **Download:** https://visualstudio.microsoft.com/visual-cpp-build-tools/
- **Installation:**
    1. Run installer
    2. Select "Desktop development with C++"
    3. Click Install
    4. Restart computer after installation
- **Note:** This is NOT needed on Mac/Linux

#### 3. pip (Python Package Manager)
- **Version:** Latest (comes with Python)
- **Why:** Install Python packages
- **Verify:**
```bash
  pip --version
```

#### 4. Git (Version Control)
- **Version:** Latest
- **Why:** Clone repository and version control
- **Download:** https://git-scm.com/download/win
- **Verify:**
```bash
  git --version
```

### Python Packages (Installed via requirements.txt)

All Python packages are installed with one command:
```bash
pip install -r requirements.txt
```

#### Core Testing Packages
- **pytest** (8.4.2+) - Test framework
- **requests** (2.32.5+) - HTTP/API calls
- **python-dotenv** (1.1.1+) - Environment variable management
- **assertpy** (1.1+) - Fluent assertions
- **faker** (22.0.0+) - Test data generation

#### Reporting Packages
- **pytest-html** (4.1.1+) - HTML test reports
- **allure-pytest** (2.13.2+) - Allure test reports

#### Web Testing Packages (Framework Extension)
- **playwright** (1.55.0+) - Web browser automation

#### Mobile Testing Packages (Framework Extension)
- **Appium-Python-Client** (3.1.0+) - Mobile automation client
- **selenium** (4.15.2+) - WebDriver support

---

## Optional Software (For Framework Extension Only)

These are NOT required for BVNK API tests but are needed for future UI/Mobile testing:

### For Web UI Testing (Playwright)

#### 5. Playwright Browsers
- **Why:** Run web UI tests
- **Install:**
```bash
  python -m playwright install
```

### For Mobile App Testing (Appium)

#### 6. Node.js (20.x LTS)
- **Version:** 20.x LTS (Long Term Support)
- **Why:** Required to run Appium server
- **Download:** https://nodejs.org/ (download LTS version)
- **Verify:**
```bash
  node --version
  npm --version
```

#### 7. Appium Server
- **Version:** 2.x
- **Why:** Mobile automation server
- **Install:**
```bash
  npm install -g appium
  appium driver install uiautomator2
```
- **Verify:**
```bash
  appium --version
```

#### 8. Java JDK (For Android Testing)
- **Version:** JDK 21
- **Why:** Required by Android SDK
- **Download:** https://www.oracle.com/java/technologies/mobile-devices-downloads.html
- **Verify:**
```bash
  java -version
  javac -version
```
- **Environment Variables:**
```
  JAVA_HOME=C:\Program Files\Java\jdk-21
  PATH=%JAVA_HOME%\bin
```

#### 9. Android Studio (For Android Testing)
- **Version:** Latest stable
- **Why:** Android SDK, emulators, ADB
- **Download:** https://developer.android.com/studio
- **Components to Install:**
    - Android SDK Platform-Tools
    - Android SDK Build-Tools
    - Android Emulator
    - Android SDK Platform (API 33+)
- **Environment Variables:**
```
  ANDROID_HOME=C:\Users\YourName\AppData\Local\Android\Sdk
  PATH=%ANDROID_HOME%\platform-tools
  PATH=%ANDROID_HOME%\tools
```
- **Verify:**
```bash
  adb --version
```

### For Advanced Reporting

#### 10. Allure Command Line
- **Version:** 2.x
- **Why:** Generate beautiful test reports
- **Install (Windows - using Scoop):**
```bash
  # Install Scoop package manager
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  irm get.scoop.sh | iex
  
  # Install Allure
  scoop install allure
```
- **Install (Mac):**
```bash
  brew install allure
```
- **Verify:**
```bash
  allure --version
```

---

## Complete Software List

### For BVNK API Testing ONLY (Minimal)

| Software | Version | Required | Download |
|----------|---------|----------|----------|
| **Python** | 3.13+ | YES | https://www.python.org/downloads/ |
| **Visual C++ Build Tools** | Latest | YES (Windows) | https://visualstudio.microsoft.com/visual-cpp-build-tools/ |
| **pip** | Latest | YES | Comes with Python |
| **Git** | Latest | YES | https://git-scm.com/download/win |
| **pytest** | 8.4.2+ | YES | `pip install -r requirements.txt` |
| **requests** | 2.32.5+ | YES | `pip install -r requirements.txt` |
| **python-dotenv** | 1.1.1+ | YES | `pip install -r requirements.txt` |
| **assertpy** | 1.1+ | YES | `pip install -r requirements.txt` |
| **faker** | 22.0.0+ | YES | `pip install -r requirements.txt` |
| **pytest-html** | 4.1.1+ | YES | `pip install -r requirements.txt` |
| **allure-pytest** | 2.13.2+ | YES | `pip install -r requirements.txt` |
| **Allure CLI** | 2.x | Optional | https://github.com/allure-framework/allure2/releases |

### For Full Framework (With UI/Mobile Extension)

| Software | Version | Required | Download |
|----------|---------|----------|----------|
| **Node.js** | 20.x LTS | For Mobile | https://nodejs.org/ |
| **Appium** | 2.x | For Mobile | `npm install -g appium` |
| **Java JDK** | 11/17/21 | For Android | https://adoptium.net/ |
| **Android Studio** | Latest | For Android | https://developer.android.com/studio |
| **playwright** | 1.55.0+ | For Web UI | `pip install -r requirements.txt` |
| **Appium-Python-Client** | 3.1.0+ | For Mobile | `pip install -r requirements.txt` |
| **selenium** | 4.15.2+ | For Mobile | `pip install -r requirements.txt` |

---

## Installation Quick Start

### Minimal Installation (BVNK Tests Only)
```bash
# 1. Install Visual C++ Build Tools (Windows only)
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Select "Desktop development with C++"
# Restart computer after installation

# 2. Install Python 3.13 from python.org
# 3. Install Git from git-scm.com

# 4. Clone repository
git clone <your-repo-url>
cd python-automation-framework

# 5. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# 6. Install Python packages
pip install -r requirements.txt

# 7. Configure environment
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# 8. Run tests
pytest tests/bvnk/ -v -s
```

### Full Installation (With UI/Mobile)
```bash
# Steps 1-7 from above, then:

# 8. Install Playwright browsers
python -m playwright install

# 9. Install Node.js from nodejs.org

# 10. Install Appium
npm install -g appium
appium driver install uiautomator2

# 11. Install Java JDK

# 12. Install Android Studio from developer.android.com

# 13. Install Allure CLI
scoop install allure  # Windows
brew install allure   # Mac

# 14. Run BVNK tests
pytest tests/bvnk/ -v -s
```

---

## Disk Space Requirements

| Software | Disk Space |
|----------|------------|
| Python 3.13 | ~500 MB |
| Visual C++ Build Tools | ~6 GB |
| Git | ~300 MB |
| Python packages | ~200 MB |
| Node.js | ~200 MB |
| Appium | ~100 MB |
| Java JDK | ~300 MB |
| Android Studio | ~8 GB |
| Allure | ~50 MB |
| **Total (Minimal)** | **~7 GB** |
| **Total (Full)** | **~16 GB** |

---

## Verification Commands

After installation, verify everything works:
```bash
# Python and packages
python --version
pip --version
pytest --version

# Git
git --version

# Python packages
python -c "import pytest, requests, playwright; print('All packages installed')"

# Node.js (if installed)
node --version
npm --version

# Appium (if installed)
appium --version
appium driver list

# Java (if installed)
java -version

# Android SDK (if installed)
adb --version

# Allure (if installed)
allure --version

# Framework config
python -c "from config.settings import settings; print('Config loaded')"
```

---

## Common Installation Issues

### Issue 1: Python not found
**Solution:** Add Python to PATH during installation or manually add to system PATH

### Issue 2: pip not recognized
**Solution:** Python installation issue, reinstall Python with "Add to PATH" checked

### Issue 3: Virtual environment activation fails (Windows)
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 4: Greenlet compilation error
**Problem:** "error: Microsoft Visual C++ 14.0 or greater is required"
**Solution:** Install Visual C++ Build Tools (see Software Requirements section above)

### Issue 5: Module 'config' not found
**Solution:** Ensure root conftest.py exists and adds project to Python path

### Issue 6: npm not recognized (Windows)
**Solution:** Restart terminal after Node.js installation

---

## Operating System Compatibility

| OS | BVNK Tests | Web UI | Mobile (Android) | Mobile (iOS) |
|----|------------|--------|------------------|--------------|
| **Windows 10/11** | YES | YES | YES | NO |
| **macOS 10.15+** | YES | YES | YES | YES |
| **Linux (Ubuntu 20.04+)** | YES | YES | YES | NO |

Note: iOS testing requires macOS with Xcode

---

## Assignment Requirements - Test Organization

### Mandatory E2E Tests (3)

1. **Test 1:** Convert/trade 1 ETH for TRX
    - File: `tests/bvnk/e2e/test_currency_conversions.py`
    - Function: `test_convert_1_eth_to_trx`
    - Status: COMPLETED

2. **Test 2:** Convert/trade 420 TRX for USDT
    - File: `tests/bvnk/e2e/test_currency_conversions.py`
    - Function: `test_convert_420_trx_to_usdt`
    - Status: COMPLETED

3. **Test 3:** Convert/trade 987 TRX for ETH
    - File: `tests/bvnk/e2e/test_currency_conversions.py`
    - Function: `test_convert_987_trx_to_eth`
    - Status: COMPLETED

### Additional Functional Tests (5)

4. **Test 4:** Authentication validation
    - File: `tests/bvnk/functional/test_api_endpoints.py`
    - Function: `test_authentication_echo`
    - Validates: Bearer token authentication works correctly

5. **Test 5:** Wallet listing verification
    - File: `tests/bvnk/functional/test_api_endpoints.py`
    - Function: `test_list_all_wallets`
    - Validates: All wallets are returned with correct structure

6. **Test 6:** Quote expiry validation
    - File: `tests/bvnk/functional/test_api_endpoints.py`
    - Function: `test_quote_expiry`
    - Validates: Quotes expire after 20 seconds as specified

7. **Test 7:** Insufficient balance handling
    - File: `tests/bvnk/functional/test_api_endpoints.py`
    - Function: `test_insufficient_balance`
    - Validates: System correctly rejects trades with insufficient balance

8. **Test 8:** Service fee calculation
    - File: `tests/bvnk/functional/test_api_endpoints.py`
    - Function: `test_service_fee_calculation`
    - Validates: 0.01% service fee is correctly applied

### Verification Tests (6 tests)
**Location:** `tests/bvnk/verification/test_verification.py`

Debug and exploration tests (skipped by default):
- `test_debug_wallet_structure` - Explore wallet API response
- `test_debug_quote_api` - Test quote payload formats
- `test_init_endpoint_directly` - Verify init endpoint
- `test_complete_api_flow` - Test full workflow
- `test_verify_api_response_structures` - Document API structures
- `test_verify_error_responses` - Test error handling

**Run verification tests manually:**
```bash
# All verification tests
pytest tests/bvnk/verification/test_verification.py -v -s

# Specific test
pytest tests/bvnk/verification/test_verification.py::test_debug_wallet_structure -v -s

---

## Test Execution

### Run All BVNK Tests
```bash
pytest tests/bvnk/ -v -s
```

### Run E2E Tests Only
```bash
pytest tests/bvnk/e2e/ -v -s
```

### Run Functional Tests Only
```bash
pytest tests/bvnk/functional/ -v -s
```

### Run Specific Test
```bash
pytest tests/bvnk/e2e/test_currency_conversions.py::test_convert_1_eth_to_trx -v -s
```

### Run with HTML Report
```bash
pytest tests/bvnk/ --html=reports/bvnk_report.html --self-contained-html
```

### Run with Allure Report
```bash
pytest tests/bvnk/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## Project Structure
```
python-automation-framework/
│
├── tests/bvnk/                              # BVNK test suite
│   ├── e2e/
│   │   └── test_currency_conversions.py     # 3 E2E conversion tests
│   └── functional/
│       └── test_api_endpoints.py            # 5 functional tests
│   └── verification/
        ├── __init__.py                     # NEW
        ├── conftest.py                     # NEW
│       └── test_verification.py             # 6 verification tests
│
│
├── utils/bvnk/                              # BVNK utilities
│   ├── api_client.py                        # API client wrapper
│   └── helpers.py                           # Helper functions
│
├── config/
│   └── settings.py                          # Configuration management
│
├── tests/conftest.py                        # Test fixtures
├── tests/bvnk/conftest.py                   # BVNK-specific fixtures
│
└── reports/                                 # Test reports
    ├── bvnk_report.html                     # HTML report
    ├── allure-results/                      # Allure data
    └── screenshots/                         # Failed test screenshots (UI)
```

---

## Implementation Details

### API Client

**Location:** `utils/bvnk/api_client.py`

The `BVNKApiClient` class provides methods for all BVNK API endpoints:

- `init_account()` - Initialize new account and get bearer token
- `echo(payload)` - Test authentication
- `list_wallets()` - List all wallets
- `get_wallet(wallet_id)` - Get specific wallet details
- `create_quote(from_currency, to_currency, amount)` - Create conversion quote
- `accept_quote(quote_uuid)` - Accept and execute quote
- `get_quote(quote_uuid)` - Get quote details

**Features:**
- Automatic bearer token management
- Session-based connection pooling
- Proper error handling
- Clean API abstraction

### Helper Functions

**Location:** `utils/bvnk/helpers.py`

Utility functions for common operations:

- `get_wallet_balance(wallets, currency)` - Extract balance for specific currency
- `calculate_expected_fee(amount, fee_percent)` - Calculate service fee
- `calculate_net_amount(gross_amount, fee_percent)` - Calculate net after fee
- `validate_quote_response(quote)` - Validate quote structure

### Test Fixtures

**Location:** `tests/conftest.py` and `tests/bvnk/conftest.py`

Key fixtures:

- `bvnk_api` - Fresh BVNK API client for each test
- `bvnk_client` - Session-scoped BVNK client
- `wallet_balances` - Initial wallet balances
- `print_test_header` - Formatted test output

---

## Test Methodology

### E2E Test Flow

Each E2E test follows this pattern:

1. **Get Initial State**
    - Retrieve wallet balances before conversion
    - Verify sufficient balance exists

2. **Create Quote**
    - Request conversion quote
    - Validate quote response structure
    - Verify quote parameters (from, to, amount, rate)

3. **Execute Conversion**
    - Accept the quote
    - Wait for conversion completion

4. **Verify Final State**
    - Retrieve wallet balances after conversion
    - Calculate balance changes
    - Verify expected amounts were transferred

5. **Validate Business Rules**
    - Correct currencies involved
    - Proper fee application
    - Balance consistency

### Functional Test Approach

Functional tests validate:

- **Authentication:** Bearer token works correctly
- **Data Retrieval:** Wallets and quotes return proper structure
- **Business Rules:** Fees, expiry times, balance checks
- **Error Handling:** Proper rejection of invalid requests

---

## Assertions and Validations

### Balance Verification
```python
# Verify balance decreased
assert_that(eth_change).is_close_to(1.0, 0.0001)

# Verify balance increased
assert_that(trx_change).is_greater_than(0)
```

### Quote Validation
```python
# Verify quote structure
assert_that(quote).contains_key('uuid', 'from', 'to', 'amount', 'rate')

# Verify quote parameters
assert_that(quote['from']).is_equal_to('ETH')
assert_that(quote['to']).is_equal_to('TRX')
```

### Error Handling
```python
# Verify proper error codes
try:
    bvnk_api.accept_quote(expired_quote_uuid)
    pytest.fail("Expected quote to be expired")
except requests.exceptions.HTTPError as e:
    assert_that(e.response.status_code).is_in(400, 404, 410)
```

---

## Configuration

### Environment Variables (.env)
```env
# BVNK API
BVNK_API_BASE_URL=http://bvnksimulator.pythonanywhere.com
BVNK_BEARER_TOKEN=

# Test Settings
SERVICE_FEE_PERCENT=0.01
QUOTE_EXPIRY_SECONDS=20

# Logging
LOG_LEVEL=INFO
```

### Settings

Key configuration values:

- **Service Fee:** 0.01% on all conversions
- **Quote Expiry:** 20 seconds
- **Base URL:** http://bvnksimulator.pythonanywhere.com

---

## Test Results

### Expected Output
```
tests/bvnk/e2e/test_currency_conversions.py::test_convert_1_eth_to_trx 
======================================================================
TEST: Convert 1 ETH to TRX
======================================================================

Account initialized. Token expires: 2025-11-03T12:00:00Z

Initial ETH balance: 10.0
Initial TRX balance: 50000.0

Quote created:
  UUID: abc-123-def-456
  Rate: 50123.45

Quote accepted: {'status': 'success', 'trade_id': 'trade-789'}

Final ETH balance: 9.0
Final TRX balance: 100123.45

Balance changes:
  ETH decreased by: 1.0
  TRX increased by: 50123.45

TEST PASSED: 1 ETH successfully converted to TRX
PASSED
```

### Success Criteria

All tests should:
- Execute without errors
- Complete within reasonable time
- Verify all assertions pass
- Generate proper reports

---

## Reports

### HTML Report

**Location:** `reports/bvnk_report.html`

Features:
- Test execution summary
- Pass/fail status for each test
- Execution time
- Detailed logs
- Screenshots for failures

### Allure Report

**Location:** `reports/allure-results/`

Features:
- Interactive web interface
- Test categorization
- Timeline view
- Detailed steps
- Historical trends
- Attachments and screenshots

---

## Design Decisions

### Architecture

**Layered Approach:**
- API Client Layer - Low-level API communication
- Helper Layer - Business logic utilities
- Test Layer - Test scenarios and assertions

**Benefits:**
- Clear separation of concerns
- Reusable components
- Easy to extend
- Maintainable code

### Design Patterns

**Patterns Used:**
- **Fixture Pattern** - pytest fixtures for setup/teardown
- **Client Pattern** - API client wrapper
- **Helper Functions** - DRY principle for calculations
- **Page Object Model** - Structure ready for UI tests (future)

### Testing Strategy

**Pyramid Approach:**
- E2E Tests - High-level business scenarios
- Functional Tests - API endpoint validation
- Helper Tests - Utility function validation

---

## Evaluation Criteria Coverage

### Correctness
- All 8 tests execute successfully
- Proper verification at each step
- Accurate assertions

### Code Quality
- Well-organized structure
- Clear naming conventions
- Comprehensive documentation
- Reusable components

### Testing Principles
- Appropriate test coverage
- Proper validation points
- Error handling
- Business rule verification

### Approach
- Logical project structure
- Scalable architecture
- Clear test strategy
- Professional implementation

---

## Known Limitations

1. **Account Initialization** - Each test session creates a new account
2. **Test Isolation** - Tests modify wallet balances
3. **Rate Fluctuation** - Exchange rates vary, tests use ranges
4. **Network Dependency** - Tests require API availability

---

## Future Enhancements

Potential improvements:
- Parallel test execution
- Performance testing
- Negative test scenarios
- Data-driven tests with multiple currencies
- Mock server for offline testing
- CI/CD pipeline integration

---

## Troubleshooting

### Common Issues

**Issue: Module not found**
```bash
# Ensure you're in project root and venv is activated
cd python-automation-framework
.venv\Scripts\activate
pip install -r requirements.txt
```

**Issue: API connection error**
```bash
# Verify API is accessible
curl http://bvnksimulator.pythonanywhere.com/docs
```

**Issue: Tests fail with authentication error**
```bash
# Account initialization happens automatically
# Check API is accessible and working
pytest tests/bvnk/functional/test_api_endpoints.py::test_authentication_echo -v -s
```

---

## Contact

For questions or issues:
- Review test code in `tests/bvnk/`
- Check API documentation at http://bvnksimulator.pythonanywhere.com/docs
- Refer to main README.md for framework details

---

## Summary

**Tests Implemented:** 8 (3 E2E + 5 Functional)  
**Test Coverage:** All required endpoints  
**Validation:** Comprehensive assertions  
**Documentation:** Complete and detailed  
**Status:** Production ready

This implementation demonstrates professional API testing practices with clean code, proper structure, and thorough validation.