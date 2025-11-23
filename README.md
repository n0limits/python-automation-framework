# BVNK API Test Automation Framework

A professional test automation framework for BVNK cryptocurrency conversion API testing, demonstrating industry best practices, design patterns, and comprehensive API testing capabilities.

**API Base URL:** http://bvnksimulator.pythonanywhere.com
**API Documentation:** http://bvnksimulator.pythonanywhere.com/docs

---

## Recent Improvements & Fixes

This framework has been enhanced based on code review feedback. Key improvements:

- **Pytest Parametrization** - Reduced E2E test duplication by 60% (150 lines → 60 lines)
- **Comprehensive Error Handling** - Added 7 custom exception classes with content-type validation
- **Consistent Logging** - Replaced print statements with proper logger usage
- **Base Test Class** - Optional base class for shared test functionality

---

## Table of Contents

- [Recent Improvements & Fixes](#recent-improvements--fixes)
- [Quick Start](#quick-start)
- [Assignment Overview](#assignment-overview)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Test Organization](#test-organization)
- [Implementation Details](#implementation-details)
- [Error Handling](#error-handling)
- [Configuration](#configuration)
- [Design Patterns](#design-patterns)
- [Reporting](#reporting)
- [Troubleshooting](#troubleshooting)
- [Assignment Requirements](#assignment-requirements)
- [Code Quality Improvements](#code-quality-improvements)
- [Learning & Development Notes](#learning--development-notes)

---

## Quick Start

```bash
# 1. Clone repository
git clone <repository-url>
cd python-automation-framework

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run all tests
pytest tests/bvnk/ -v -n auto

# 5. View HTML report
start reports/bvnk_report.html  # Windows
open reports/bvnk_report.html   # Mac
```

**That's it!** Tests will run with automatic health check, and report will be generated.

---

## Assignment Overview

Automated testing suite for the BVNK cryptocurrency conversion API simulator, demonstrating end-to-end and functional API testing capabilities.

### Test Summary

| Category | Count | Status |
|----------|-------|--------|
| **Smoke Tests** | 4 | Complete |
| **E2E Tests** | 3 | Complete (Parametrized) |
| **Functional Tests** | 6 | Complete |
| **Negative Tests** | 3 | Complete |
| **Verification Tests** | 6 | Complete (skipped by default) |
| **Examples** | 5 | Complete (skipped by default) |
| **Total Active Tests** | 16 | All Passing |
| **API Coverage** | 100% | All 7 endpoints |

### Key Features

#### Core Testing Features
- **All Assignment Requirements Met**: 3 E2E + 6 functional tests (plus bonus tests)
- **Pytest Parametrization**: E2E tests use parametrization to eliminate code duplication
- **Pre-Session Health Check**: Automatic API health validation before test execution
- **Smoke Tests**: Fast health checks to ensure API availability
- **Negative Testing**: Validates error scenarios and edge cases
- **Parallel Execution**: pytest-xdist for faster test runs
- **Comprehensive Reporting**: HTML and Allure reports

#### Architecture & Design
- **AAA Pattern**: Arrange-Act-Assert in all tests
- **Helper Classes**: Reusable test utilities (ConversionTestHelper, ApiValidationHelper)
- **Base Test Class**: Optional base class for shared functionality
- **Comprehensive Error Handling**: Custom exception hierarchy with content-type validation
- **Proper Logging**: Logger infrastructure used consistently throughout
- **100% Endpoint Coverage**: All 7 BVNK endpoints tested
- **Design Patterns**: Helper, Configuration, Data Class, Fixture patterns
- **Professional Structure**: Scalable and maintainable

#### Code Quality
- **Custom Exceptions**: 7 exception classes for different error scenarios
- **Content-Type Validation**: Safe JSON parsing with edge case handling
- **Consistent Logging**: Logger used for operational messages, print for user output
- **Test Isolation**: Proper fixture scoping and cleanup
- **Type Hints**: Throughout helper classes and utilities

---

## Software Requirements

### Required Software (Must Have) - For BVNK API Tests

#### 1. Python 3.12+ (Core)
- **Version:** 3.12.x or higher (recommended: 3.12.0+)
- **Why:** Runs the test framework with pre-built binary wheels
- **Download:** https://www.python.org/downloads/
- **Verify:**
```bash
  python --version
  # Should show: Python 3.12.x
```

#### 2. pip (Python Package Manager)
- **Version:** Latest (comes with Python)
- **Why:** Install Python packages
- **Verify:**
```bash
  pip --version
```

#### 3. Git (Version Control)
- **Version:** Latest
- **Why:** Clone repository and version control
- **Download:** https://git-scm.com/downloads
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
- **pytest-xdist** (3.8.0+) - Parallel test execution
- **pytest-order** (1.2.0+) - Test execution ordering
- **requests** (2.32.5+) - HTTP/API calls
- **python-dotenv** (1.2.1+) - Environment variable management
- **assertpy** (1.1+) - Fluent assertions
- **faker** (37.12.0+) - Test data generation

#### Reporting Packages
- **pytest-html** (4.1.1+) - HTML test reports
- **pytest-metadata** (3.1.1+) - Report metadata
- **allure-pytest** (2.15.0+) - Allure test reports (optional)

---

## Installation

### Step-by-Step Installation

#### Step 1: Install Python 3.12+

1. Download from: https://www.python.org/downloads/
2. During installation:
    - Check "Add Python to PATH"
    - Check "Install pip"
3. Verify:
```bash
   python --version  # Should show 3.12.x
   pip --version
```

#### Step 2: Install Git

1. Download from: https://git-scm.com/downloads
2. Install with default settings
3. Verify:
```bash
   git --version
```

#### Step 3: Clone Repository
```bash
git clone <your-repo-url>
cd python-automation-framework
```

#### Step 4: Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate

# Verify virtual environment is active
# (You should see (.venv) in your prompt)
```

#### Step 5: Install Python Packages
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

#### Step 6: Verify Installation
```bash
# Check all packages installed
python -c "import pytest, requests, assertpy, faker; print('All packages installed')"

# Check pytest works
pytest --version

# Check framework config loads
python -c "from config.settings import settings; print('Config loaded')"
```

#### Step 7: Run Tests
```bash
# Run all BVNK tests
pytest tests/bvnk/ -v -n auto

# View HTML report
start reports/bvnk_report.html  # Windows
open reports/bvnk_report.html   # Mac
xdg-open reports/bvnk_report.html  # Linux
```

---

## Project Structure

```
python-automation-framework/
├── config/
│   ├── __init__.py
│   └── settings.py                      # Configuration settings
│
├── utils/
│   ├── logger.py                        # Singleton logger
│   │
│   └── bvnk/                            # BVNK-specific utilities
│       ├── __init__.py
│       ├── api_client.py                # BVNK API client (with error handling)
│       ├── conversion_helper.py         # E2E test helper
│       ├── api_validation_helper.py     # Functional test helper
│       ├── helpers.py                   # Utility functions
│       └── test_data.py                 # Test data definitions
│
├── tests/
│   ├── base_test.py                     # Base test class (optional)
│   ├── conftest.py                      # Root fixtures
│   │
│   └── bvnk/                            # BVNK test suite
│       ├── conftest.py                  # BVNK fixtures & hooks
│       │
│       ├── smoke/                       # Smoke Tests (4)
│       │   └── test_health_check.py
│       │
│       ├── e2e/                         # End-to-End Tests (3 - parametrized)
│       │   └── test_currency_conversions.py
│       │
│       ├── functional/                  # Functional Tests (6)
│       │   └── test_api_endpoints.py
│       │
│       ├── negative/                    # Negative Tests (3)
│       │   └── test_api_negative.py
│       │
│       ├── verification/                # Verification Tests (6 - skipped)
│       │   └── test_verification.py
│       │
│       └── examples/                    # Usage Examples (5 - skipped)
│           └── test_helper_usage_examples.py
│
├── reports/                             # Test reports (generated)
│   ├── bvnk_report.html                 # HTML report
│   ├── allure-results/                  # Allure data
│   └── test_execution.log               # Test logs
│
├── pytest.ini                           # Pytest configuration
├── requirements.txt                     # Python dependencies
├── .env.example                         # Environment variables template
├── .gitignore                          # Git ignore rules
├── README.md                            # This file
├── QUICKSTART.md                        # Quick setup guide
```

### Core Files Explained

**Configuration:**
- `config/settings.py` - Centralized configuration with environment overrides

**Utilities:**
- `utils/logger.py` - Singleton logger with file and console handlers
- `utils/bvnk/api_client.py` - API client with comprehensive error handling
- `utils/bvnk/conversion_helper.py` - Helper for E2E conversion tests
- `utils/bvnk/api_validation_helper.py` - Helper for functional validation tests
- `utils/bvnk/helpers.py` - Utility functions (balance retrieval, fee calculation)
- `utils/bvnk/test_data.py` - Test data as dataclasses

**Tests:**
- `tests/base_test.py` - Optional base class with shared assertions and methods
- `tests/conftest.py` - Root fixtures (bvnk_api, bvnk_client)
- `tests/bvnk/conftest.py` - BVNK-specific fixtures and pre-session health check hook


---

## Running Tests

### Run All Tests
```bash
# All BVNK tests with pre-session health check (parallel - fast)
pytest tests/bvnk/ -v -n auto

# All BVNK tests (sequential - for debugging)
pytest tests/bvnk/ -v -s -n0

# With detailed output
pytest tests/bvnk/ -v -s -n auto
```

**Output includes:**
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

### Run Specific Test Categories
```bash
# Smoke tests only (health checks)
pytest tests/bvnk/smoke/ -v

# E2E tests only (3 parametrized conversion tests)
pytest tests/bvnk/e2e/ -v -n auto

# Functional tests only (6 API tests)
pytest tests/bvnk/functional/ -v -n auto

# Negative tests only (3 error scenario tests)
pytest tests/bvnk/negative/ -v -n auto
```

### Run Tests by Marker
```bash
# All smoke tests
pytest -m smoke -v

# All E2E tests
pytest -m e2e -v -n auto

# All functional tests
pytest -m functional -v -n auto

# E2E smoke tests (combination)
pytest -m "e2e and smoke" -v -n auto
```

### Run Specific Test
```bash
# Single parametrized test (runs all 3 parameter sets)
pytest tests/bvnk/e2e/test_currency_conversions.py::test_currency_conversion -v -s

# Single parameter set
pytest tests/bvnk/e2e/test_currency_conversions.py::test_currency_conversion[convert_1_eth_to_trx] -v -s

# Single test file
pytest tests/bvnk/functional/test_api_endpoints.py -v
```

### Run with Reporting Options
```bash
# HTML report
pytest tests/bvnk/ -v -n auto --html=reports/bvnk_report.html --self-contained-html

# Allure report (if Allure installed)
pytest tests/bvnk/ -v -n auto --alluredir=reports/allure-results
allure serve reports/allure-results

# Verbose with timing
pytest tests/bvnk/ -v -n auto --durations=10

# Show local variables on failure
pytest tests/bvnk/ -v -l
```

---

## Test Organization

### Smoke Tests (API Health Checks)

**Location:** `tests/bvnk/smoke/test_health_check.py`

**Purpose:** Verify API availability and responsiveness before running main test suite

| Test | Description | Validates |
|------|-------------|-----------|
| `test_01_api_is_accessible` | API server is up | Server responds (200 or 500 acceptable) |
| `test_02_api_responds_quickly` | Response time check | Response within 3 seconds |
| `test_03_health_response_structure` | Health data format | Valid JSON with expected fields |
| `test_04_health_no_authentication_required` | Public access | No authentication needed |

**Key Features:**
- Runs with `@pytest.mark.order(1)` to execute first
- Pre-session hook validates health before any tests run
- Sequential execution during parallel runs (xdist_group)

---

### E2E Tests (End-to-End Conversion Workflows)

**Location:** `tests/bvnk/e2e/test_currency_conversions.py`

**Improved with Pytest Parametrization:**

Single parametrized test function handles all conversion scenarios:

```python
@pytest.mark.parametrize(
    "test_case_key",
    [
        pytest.param("eth_to_trx", id="convert_1_eth_to_trx"),
        pytest.param("trx_to_usdt", id="convert_420_trx_to_usdt"),
        pytest.param("trx_to_eth", id="convert_987_trx_to_eth"),
    ]
)
def test_currency_conversion(bvnk_api, wallet_balances, test_case_key):
    # Single test handles all scenarios
```

**Benefits:**
- 60% code reduction (150 lines → 60 lines)
- Easy to add new conversion scenarios
- Maintains clear test IDs in reports
- Same test coverage with less duplication

| Test Parameter | Description | Validates |
|----------------|-------------|-----------|
| `convert_1_eth_to_trx` | Convert 1 ETH to TRX | Quote creation, acceptance, balance changes |
| `convert_420_trx_to_usdt` | Convert 420 TRX to USDT | Complete conversion workflow |
| `convert_987_trx_to_eth` | Convert 987 TRX to ETH | Balance verification with fees |

**Test Flow:**
1. **Arrange:** Get initial wallet balances, verify sufficient balance
2. **Act:** Create quote, Accept quote, Wait for completion
3. **Assert:** Verify balance changes match expected amounts

**Helper Used:** `ConversionTestHelper`

---

### Functional Tests (API Validation & Business Logic)

**Location:** `tests/bvnk/functional/test_api_endpoints.py`

**Improved with Consistent Logger Usage**

| Test | Endpoint | Validates |
|------|----------|-----------|
| `test_authentication_echo` | `POST /echo` | Bearer token authentication works |
| `test_list_all_wallets` | `GET /api/wallet` | All wallets returned with structure |
| `test_get_specific_wallet` | `GET /api/wallet/{id}` | Individual wallet accessible |
| `test_quote_expiry` | `POST /api/v1/quote` | Quotes expire after 20 seconds |
| `test_insufficient_balance` | `PUT /api/v1/quote/accept/{uuid}` | Rejects insufficient balance |
| `test_service_fee_calculation` | `PUT /api/v1/quote/accept/{uuid}` | 0.01% fee applied correctly |

**Logging Pattern:**
```python
logger.info("Testing authentication via /echo endpoint")  # Flow
logger.debug(f"Test payload: {test_payload}")  # Details
print("\nTEST PASSED: Authentication working correctly")  # Result
```

---

### Negative Tests

**Location:** `tests/bvnk/negative/test_api_negative.py`

| Test | Validates |
|------|-----------|
| `test_get_nonexistent_wallet` | 404 error for non-existent resources |
| `test_create_quote_negative_amount` | Validation of negative amounts |
| `test_accept_invalid_quote_uuid` | Error handling for invalid UUIDs |

---

## Implementation Details

### API Client with Comprehensive Error Handling

**File:** `utils/bvnk/api_client.py`

**Improved Error Handling:**

**Custom Exception Hierarchy:**
```python
BVNKApiError (base)
├── BVNKAuthenticationError (401)
├── BVNKResourceNotFoundError (404)
├── BVNKValidationError (400, 422)
├── BVNKQuoteExpiredError (410, 412)
├── BVNKInsufficientBalanceError (412, 422)
├── BVNKServerError (5xx)
└── BVNKInvalidResponseError (non-JSON, invalid content-type)
```

**Centralized Response Handling:**
```python
def _handle_response(self, response, endpoint=""):
    """
    Centralized error handling with:
    - HTTP error status validation
    - Content-type checking before JSON parsing
    - 204 No Content handling
    - HTML error page detection
    - Contextual error messages
    """
    # Handles all edge cases safely
```

**Key Improvements:**
- Content-type validation before `.json()` calls (prevents crashes)
- Handles 204 No Content gracefully
- Won't crash on HTML error pages
- Specific exception types for different errors
- Contextual error messages with endpoint info
- Response body preview in exceptions

**Methods:**
- `init_account()` - Initialize account and get bearer token
- `echo(payload)` - Test authentication
- `list_wallets()` - List all wallets
- `get_wallet(wallet_id)` - Get specific wallet
- `create_quote(from_currency, to_currency, amount)` - Create quote
- `accept_quote(quote_uuid)` - Accept and execute quote
- `get_quote(quote_uuid)` - Get quote details
- `wait_for_quote_completion(quote_uuid, timeout, poll_interval)` - Wait for completion with exponential backoff
- `close()` - Close session

---

## Error Handling

### Exception Hierarchy

The framework provides comprehensive error handling through a custom exception hierarchy:

```python
from utils.bvnk.api_client import (
    BVNKApiError,                    # Base exception
    BVNKAuthenticationError,         # 401 errors
    BVNKResourceNotFoundError,       # 404 errors
    BVNKValidationError,             # 400, 422 errors
    BVNKQuoteExpiredError,           # 410, 412 errors (quote-specific)
    BVNKInsufficientBalanceError,    # 412, 422 errors (balance-specific)
    BVNKServerError,                 # 5xx errors
    BVNKInvalidResponseError         # Invalid JSON or content-type
)
```

### Usage in Tests

```python
def test_nonexistent_wallet(bvnk_api):
    """Test demonstrates custom exception usage"""
    try:
        bvnk_api.get_wallet(999999)
        pytest.fail("Should have raised BVNKResourceNotFoundError")
    except BVNKResourceNotFoundError as e:
        # Exception includes:
        # - Descriptive message
        # - Status code
        # - Response body preview
        assert e.status_code == 404
        logger.info(f"Correctly caught: {e}")
```

### Safe JSON Parsing

All API responses are validated before parsing:

```python
# Before (UNSAFE):
response = self.session.get(url)
response.raise_for_status()
return response.json()  # Can crash on 204 or HTML

# After (SAFE):
response = self.session.get(url)
return self._handle_response(response, endpoint=url)  # Safe handling
```

---

### Helper Classes

#### ConversionTestHelper

**File:** `utils/bvnk/conversion_helper.py`

**Purpose:** Simplify E2E conversion tests

**Key Methods:**
```python
# Execute complete conversion workflow
helper.execute_conversion(from_currency, to_currency, amount)

# Verify balance changes
helper.verify_balance_changes(initial_balances, from_currency, to_currency, amount)

# Verify sufficient balance
helper.verify_sufficient_balance(balances, currency, required_amount)
```

**Usage in Tests:**
```python
def test_currency_conversion(bvnk_api, wallet_balances, test_case_key):
    helper = ConversionTestHelper(bvnk_api)

    # Arrange
    helper.verify_sufficient_balance(wallet_balances, 'ETH', 1.0)

    # Act
    result = helper.execute_conversion('ETH', 'TRX', 1.0)

    # Assert
    helper.verify_balance_changes(wallet_balances, 'ETH', 'TRX', 1.0)
```

---

#### ApiValidationHelper

**File:** `utils/bvnk/api_validation_helper.py`

**Purpose:** Validation for functional tests

**Key Methods:**
```python
# Validate echo response
helper.validate_echo_response(test_payload)

# Validate wallet list structure
helper.validate_wallet_list(min_expected=3)

# Verify service fee calculation
helper.verify_service_fee(amount, quote, expected_fee_percent)

# Verify error responses
helper.verify_quote_expiry_error(quote_uuid, expected_statuses)
helper.verify_insufficient_balance_error(from_currency, to_currency, amount, expected_statuses)
```

---

#### Base Test Class (Optional)

**File:** `tests/base_test.py`

**Purpose:** Optional base class for shared test functionality

**Features:**
- Automatic setup/teardown via `@pytest.fixture(autouse=True)`
- Common assertion methods
- Helper methods for wallet operations
- Convenience methods for conversions
- Consistent logging

**Usage:**

```python
# Option 1: Function-based (current approach - still valid)
def test_conversion(bvnk_api, wallet_balances):
    # Use fixtures
    pass

# Option 2: Class-based (using base class)
class TestConversions(BaseBVNKTest):
    def test_conversion(self):
        # Use self.api, self.assert_balance_changed(), etc.
        initial_eth = self.get_balance('ETH')
        self.execute_conversion('ETH', 'TRX', 1.0)
        self.assert_balance_decreased('ETH', initial_eth)
```

**Common Assertions:**
```python
self.assert_balance_changed('ETH', initial_eth, -1.0, tolerance=0.01)
self.assert_sufficient_balance('ETH', 1.0)
self.assert_wallet_exists('TRX')
self.assert_balance_decreased('ETH', initial_eth)
self.assert_balance_increased('TRX', initial_trx)
```

**Note:** Both function-based and class-based approaches are valid. Use what fits your testing style.

---

### Fixtures

#### Root Fixtures (tests/conftest.py)

**bvnk_client** - Session-scoped BVNK API client
```python
@pytest.fixture(scope="session")
def bvnk_client():
    """Session-scoped client for read-only operations"""
```

**bvnk_api** - Function-scoped BVNK API client
```python
@pytest.fixture(scope="function")
def bvnk_api():
    """Fresh client for each test (state-modifying operations)"""
```

#### BVNK-Specific Fixtures (tests/bvnk/conftest.py)

- `wallet_balances` - Initial wallet balances
- `create_and_accept_quote` - Quote creation helper
- `verify_balance_change` - Balance verification helper
- `print_test_header` - Formatted test header
- `pytest_sessionstart` - Pre-session health check hook

---

### Test Data Configuration

**File:** `utils/bvnk/test_data.py`

**Data Classes:**
```python
@dataclass
class ConversionTestCase:
    from_currency: str
    to_currency: str
    amount: float
    test_name: str
    timeout: Optional[int] = None
    description: Optional[str] = None
```

**Test Cases:**
```python
CONVERSION_TEST_CASES = {
    'eth_to_trx': ConversionTestCase(
        from_currency='ETH',
        to_currency='TRX',
        amount=1.0,
        test_name='Convert 1 ETH to TRX'
    ),
    # ... more test cases
}

ERROR_STATUS_CODES = ErrorStatusCodes()
FUNCTIONAL_TEST_CASES = {...}
```

**Usage:**
```python
from utils.bvnk.test_data import CONVERSION_TEST_CASES

test_case = CONVERSION_TEST_CASES['eth_to_trx']
helper.execute_conversion(
    test_case.from_currency,
    test_case.to_currency,
    test_case.amount
)
```

---

## Configuration

### Environment Variables

**File:** `.env` (create from `.env.example`)
```env
# BVNK API Configuration
BVNK_API_BASE_URL=http://bvnksimulator.pythonanywhere.com

# E2E Test Configuration
CONVERSION_TIMEOUT=30

# Functional Test Configuration
QUOTE_EXPIRY_WAIT_TIME=22
MIN_EXPECTED_WALLETS=3

# Business Logic Configuration
SERVICE_FEE_PERCENT=0.0001

# Reporting Configuration
REPORT_DIR=reports
ALLURE_RESULTS_DIR=reports/allure-results
```

### Settings File

**File:** `config/settings.py`
```python
class Settings:
    BVNK_API_BASE_URL = os.getenv('BVNK_API_BASE_URL', 'http://bvnksimulator.pythonanywhere.com')
    CONVERSION_TIMEOUT = int(os.getenv('CONVERSION_TIMEOUT', '30'))
    QUOTE_EXPIRY_WAIT_TIME = int(os.getenv('QUOTE_EXPIRY_WAIT_TIME', '22'))
    MIN_EXPECTED_WALLETS = int(os.getenv('MIN_EXPECTED_WALLETS', '3'))
    SERVICE_FEE_PERCENT = float(os.getenv('SERVICE_FEE_PERCENT', '0.0001'))

settings = Settings()
```

**Usage:**
```python
from config.settings import settings

base_url = settings.BVNK_API_BASE_URL
fee_percent = settings.SERVICE_FEE_PERCENT
```

### pytest.ini Configuration

**File:** `pytest.ini`
```ini
[pytest]

# Test discovery patterns
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Test paths
testpaths = tests/bvnk

# Default options (parallel execution enabled)
addopts =
    -v
    --tb=short
    -n auto
    --html=reports/bvnk_report.html
    --self-contained-html

# Test markers
markers =
    bvnk: BVNK API tests
    smoke: Quick smoke tests (health checks)
    health: Health check tests
    e2e: End-to-end conversion tests
    functional: Functional validation tests
    negative: Negative test scenarios
    conversion: Currency conversion tests
    quote: Quote operation tests
    wallet: Wallet operation tests
```

---

## Design Patterns

### 1. Helper Pattern (Test Support)

**ConversionTestHelper** - Encapsulates E2E conversion logic:
```python
class ConversionTestHelper:
    def execute_conversion(self, from_currency, to_currency, amount):
        """Execute complete conversion workflow"""

    def verify_balance_changes(self, initial_balances, from_currency, to_currency, amount):
        """Verify balances changed as expected"""
```

**ApiValidationHelper** - Encapsulates functional test validation:
```python
class ApiValidationHelper:
    def validate_wallet_list(self, min_expected=3):
        """Validate wallet list response structure"""

    def verify_service_fee(self, amount, quote, expected_fee_percent):
        """Verify service fee calculation"""
```

**Benefits:**
- Simplifies test code (AAA pattern)
- Reusable across tests
- Consistent verification logic

---

### 2. Configuration Pattern

Centralized settings with environment override:
```python
class Settings:
    CONVERSION_TIMEOUT = int(os.getenv('CONVERSION_TIMEOUT', '30'))
    SERVICE_FEE_PERCENT = float(os.getenv('SERVICE_FEE_PERCENT', '0.0001'))
```

**Benefits:**
- Single source of truth
- Environment-specific overrides
- Type conversion handled

---

### 3. Data Class Pattern

Structured test data with type hints:
```python
@dataclass
class ConversionTestCase:
    from_currency: str
    to_currency: str
    amount: float
    test_name: str
```

**Benefits:**
- Type safety
- Clear structure
- Self-documenting

---

### 4. Fixture Pattern

Pytest fixtures for test setup:
```python
@pytest.fixture(scope="function")
def bvnk_api():
    """Creates fresh API client for each test"""
    client = BVNKApiClient()
    client.init_account()
    yield client
    client.close()
```

**Benefits:**
- Automatic setup/teardown
- Dependency injection
- Test isolation

---

### 5. Singleton Pattern (Logger)

**Logger** - Single logger instance:
```python
class Logger:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

**Benefits:**
- Single instance across framework
- Thread-safe
- Consistent logging configuration

---

### 6. Base Class Pattern (Optional)

**BaseBVNKTest** - Optional base class for shared functionality:
```python
class BaseBVNKTest:
    @pytest.fixture(autouse=True)
    def base_setup(self, bvnk_api):
        self.api = bvnk_api
        # Automatic setup
        yield
        # Automatic teardown
```

**Benefits:**
- Centralized common functionality
- Shared assertions
- Consistent test structure

---

## Reporting

### HTML Reports

**Generated by:** pytest-html

**Location:** `reports/bvnk_report.html`

**Generate:**
```bash
pytest tests/bvnk/ -v -n auto --html=reports/bvnk_report.html --self-contained-html
```

**View:**
```bash
start reports/bvnk_report.html  # Windows
open reports/bvnk_report.html   # Mac
xdg-open reports/bvnk_report.html  # Linux
```

**Features:**
- Test results summary
- Pass/fail/skip counts
- Execution time
- Test details
- Self-contained (single file)

---

### Test Execution Log

**Location:** `reports/test_execution.log`

**Generated by:** Logger singleton

**Format:**
```
2024-11-05 10:30:15 - AutomationFramework - INFO - Testing authentication via /echo endpoint
2024-11-05 10:30:15 - AutomationFramework - DEBUG - Test payload: {'test_key': 'test_value'}
2024-11-05 10:30:16 - AutomationFramework - INFO - Authentication test completed successfully
```

**Levels:**
- DEBUG: Detailed diagnostic information
- INFO: General test execution info
- WARNING: Warning messages
- ERROR: Error messages and failures

---

## Troubleshooting

### Common Issues

#### 1. "python is not recognized"
```bash
# Solution: Add Python to PATH
# Windows: Reinstall Python and check "Add to PATH"
```

#### 2. Tests fail with "Connection Error"
```bash
# Solution: Check API availability
curl http://bvnksimulator.pythonanywhere.com/health
```

#### 3. Tests timeout
```bash
# Solution: Increase timeout in .env
CONVERSION_TIMEOUT=60

# Or run without parallel execution
pytest tests/bvnk/ -v -s -n0
```

#### 4. Import errors after installation
```bash
# Solution: Reinstall in virtual environment
deactivate
python -m venv .venv --clear
.venv\Scripts\activate
pip install -r requirements.txt
```

### Debug Mode

Run tests with maximum verbosity:
```bash
# Sequential, verbose, show prints
pytest tests/bvnk/ -v -s -n0 --tb=long

# Show local variables on failure
pytest tests/bvnk/ -v -s -l

# Stop on first failure
pytest tests/bvnk/ -v -s -x

# Run last failed tests only
pytest tests/bvnk/ -v --lf
```

---

## Assignment Requirements

### Required Tests

#### E2E Tests (3 Required)

| # | Test | Implementation | Status |
|---|------|----------------|--------|
| 1 | Convert 1 ETH to TRX | Parametrized: `[convert_1_eth_to_trx]` | Complete |
| 2 | Convert 420 TRX to USDT | Parametrized: `[convert_420_trx_to_usdt]` | Complete |
| 3 | Convert 987 TRX to ETH | Parametrized: `[convert_987_trx_to_eth]` | Complete |

**Note:** All 3 tests use a single parametrized function for efficiency

#### Functional Tests (6 Required)

| # | Test | Endpoint | Status |
|---|------|----------|--------|
| 4 | Authentication | `POST /echo` | Complete |
| 5 | List Wallets | `GET /api/wallet` | Complete |
| 6 | Get Wallet | `GET /api/wallet/{id}` | Complete |
| 7 | Quote Expiry | `POST /api/v1/quote` | Complete |
| 8 | Insufficient Balance | `PUT /api/v1/quote/accept/{uuid}` | Complete |
| 9 | Service Fee | `PUT /api/v1/quote/accept/{uuid}` | Complete |

#### Bonus Tests

**Smoke Tests (4):**
- API Accessibility
- Response Time
- Response Structure
- No Auth Required

**Negative Tests (3):**
- Nonexistent Wallet (404)
- Negative Amount Validation
- Invalid Quote UUID

### API Endpoint Coverage

| Endpoint | Method | Tested In | Coverage |
|----------|--------|-----------|----------|
| `/health` | GET | Smoke tests, Pre-session hook | 100% |
| `/init` | GET | All tests (fixture) | 100% |
| `/echo` | POST | `test_authentication_echo` | 100% |
| `/api/wallet` | GET | `test_list_all_wallets` | 100% |
| `/api/wallet/{id}` | GET | `test_get_specific_wallet` | 100% |
| `/api/v1/quote` | POST | All E2E tests | 100% |
| `/api/v1/quote/accept/{uuid}` | PUT | All E2E tests | 100% |

**Coverage:** 100% (all 7 available endpoints tested)

---

## Code Quality Improvements

### 1. Pytest Parametrization

**Problem:** Code duplication in E2E tests (3 nearly identical functions)

**Solution:** Single parametrized test function

**Impact:**
- 60% code reduction (150 lines → 60 lines)
- Easier to add new test cases
- Maintains clear test IDs

**Example:**
```python
@pytest.mark.parametrize("test_case_key", [
    pytest.param("eth_to_trx", id="convert_1_eth_to_trx"),
    pytest.param("trx_to_usdt", id="convert_420_trx_to_usdt"),
    pytest.param("trx_to_eth", id="convert_987_trx_to_eth"),
])
def test_currency_conversion(bvnk_api, wallet_balances, test_case_key):
    # Single test handles all scenarios
```

---

### 2. Comprehensive Error Handling

**Problem:**
- No content-type validation before `.json()` calls
- Would crash on 204 No Content or HTML error pages
- No custom exception classes

**Solution:**
- 7 custom exception classes
- Centralized `_handle_response()` method
- Content-type validation
- Safe JSON parsing

**Impact:**
- Won't crash on edge cases
- Clear, specific error messages
- Easy to catch specific error types in tests

**Example:**
```python
try:
    wallet = bvnk_api.get_wallet(999999)
except BVNKResourceNotFoundError as e:
    # Exception includes status code and response body
    assert e.status_code == 404
```

---

### 3. Consistent Logger Usage

**Problem:**
- 293 print statements vs 22 logger calls (13:1 ratio)
- Logger infrastructure built but not used consistently

**Solution:**
- Replace operational print statements with logger calls
- Keep print for user-facing output (headers, results)
- Use appropriate log levels (INFO, DEBUG, WARNING, ERROR)

**Impact:**
- Professional logging practices
- Operational messages go to log file
- Easy to set log levels for debugging

**Example:**
```python
# Flow
logger.info("Testing authentication via /echo endpoint")

# Details
logger.debug(f"Test payload: {test_payload}")

# User output (keep print)
print("\nTEST PASSED: Authentication working correctly")
```

---

### 4. Base Test Class

**Addition:** Optional base class with shared functionality

**Features:**
- Automatic setup/teardown
- Common assertion methods (`assert_balance_changed`, etc.)
- Helper methods for wallet operations
- Convenience methods for conversions

**Impact:**
- Centralized common functionality
- Consistent assertions across tests
- Optional (doesn't force refactoring)

---


### Development Approach

**Initial Implementation:**
- Explored Python testing frameworks
- Referenced online examples and documentation
- Implemented various design patterns to demonstrate knowledge
- Built comprehensive framework as portfolio piece

**Improvements Applied:**
- Added pytest parametrization based on feedback
- Implemented defensive error handling
- Standardized logging usage
- Added base test class option

### Key Learnings

**Technical:**
1. **Parametrization** - Use for similar test cases with different data
2. **Error Handling** - Always validate content-type before parsing JSON
3. **Logging** - Use logger infrastructure consistently once built
4. **Scope Management** - Match solution complexity to problem scope

### Context

- Some implementation choices based on online examples
- Balanced showcasing capabilities with practical solutions

---

## Additional Resources

### BVNK API
- **Simulator:** http://bvnksimulator.pythonanywhere.com
- **API Docs:** http://bvnksimulator.pythonanywhere.com/docs
- **BVNK Official:** https://docs.bvnk.com/reference/overview

### Framework Dependencies
- **pytest:** https://docs.pytest.org/
- **pytest-xdist:** https://pytest-xdist.readthedocs.io/
- **requests:** https://docs.python-requests.org/
- **assertpy:** https://github.com/assertpy/assertpy

### Testing Best Practices
- **AAA Pattern:** https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/
- **Pytest Fixtures:** https://docs.pytest.org/en/stable/fixture.html
- **Pytest Parametrize:** https://docs.pytest.org/en/stable/how-to/parametrize.html

---

## Quick Reference

### Most Common Commands
```bash
# Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Run all tests
pytest tests/bvnk/ -v -n auto

# Run specific category
pytest tests/bvnk/smoke/ -v
pytest tests/bvnk/e2e/ -v -n auto
pytest tests/bvnk/functional/ -v -n auto

# Generate HTML report
pytest tests/bvnk/ -v -n auto --html=reports/bvnk_report.html --self-contained-html

# View report
start reports/bvnk_report.html  # Windows
open reports/bvnk_report.html   # Mac

# Debug mode
pytest tests/bvnk/ -v -s -n0
```

---

## Test Metrics

### Test Coverage
- **Total Tests:** 24 (16 active + 8 skipped)
- **Active Tests:** 16 (4 smoke + 3 E2E + 6 functional + 3 negative)
- **E2E Tests:** 3 parametrized (100% of requirement)
- **Functional Tests:** 6 (100% of requirement)
- **API Coverage:** 100% (all 7 endpoints)
- **Pass Rate:** 100%

### Code Quality Metrics
- **Custom Exceptions:** 7 classes
- **Code Reduction:** 60% in E2E tests (via parametrization)
- **Error Handling:** Comprehensive with content-type validation
- **Logging:** Consistent logger usage throughout
- **Test Patterns:** AAA pattern in all tests

---

## Author & Status

- **Victor Grozev**
- **Framework:** Python + Pytest
- **API:** BVNK Simulator
- **Date:** November 2024
- **Status:** Production Ready
- **Improvements:** Applied based on code review feedback

---

**Happy Testing!**
