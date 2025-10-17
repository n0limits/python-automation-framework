# Python Automation Testing Framework

A comprehensive automation testing framework built with Python, Playwright, Appium, and Pytest for testing web applications (frontend & backend) and mobile applications.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Writing Tests](#writing-tests)
- [Running Tests](#running-tests)
- [Design Patterns](#design-patterns)
- [Reports](#reports)
- [Mobile Testing Setup](#mobile-testing-setup)
- [Troubleshooting](#troubleshooting)
- [CI/CD Integration](#cicd-integration)
- [Contributing](#contributing)

---

## Features

- Web UI Testing - Desktop browsers with Playwright (Chrome, Firefox, Safari, Edge)
- Mobile Web Testing - Responsive testing with device emulation
- Native Mobile App Testing - iOS & Android with Appium
- API Testing - Backend/REST API testing with Requests library
- Page Object Model - Maintainable test structure with POM design pattern
- Design Patterns - Factory, Builder, Strategy, Singleton, and Decorator patterns
- Test Data Generation - Dynamic test data with Faker
- Fluent Assertions - Readable assertions with assertpy
- Parallel Execution - Run tests faster with pytest-xdist
- HTML Reports - Beautiful test reports with pytest-html
- Allure Reports - Advanced reporting with detailed analytics
- Configuration Management - Environment-based config with python-dotenv
- Screenshot on Failure - Automatic screenshot capture for failed tests
- Comprehensive Logging - Detailed logging for debugging
- CI/CD Ready - Easy integration with GitHub Actions, Jenkins, etc.

---

## Tech Stack

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Language** | Python | 3.11+ (3.12 recommended) | Core language |
| **Test Framework** | pytest | 8.4+ | Test execution and organization |
| **Web Automation** | Playwright | 1.55+ | Browser automation |
| **Mobile Automation** | Appium | 2.x | Native mobile app testing |
| **API Testing** | Requests | 2.32+ | HTTP/REST API testing |
| **Assertions** | assertpy | 1.1 | Fluent, readable assertions |
| **Test Data** | Faker | 22.0+ | Generate realistic test data |
| **Reporting** | pytest-html | 4.1+ | HTML test reports |
| **Advanced Reporting** | Allure | 2.x | Beautiful, detailed reports |
| **Configuration** | python-dotenv | 1.1+ | Environment variable management |

---

## Project Structure
```
python-automation-framework/
│
├── config/                         # Configuration management
│   ├── __init__.py
│   └── settings.py                # Loads settings from .env
│
├── pages/                          # Page Object Model
│   ├── __init__.py
│   ├── base_page.py               # Base class with common methods
│   ├── login_page.py              # Example: Login page object
│   ├── dashboard_page.py          # Example: Dashboard page object
│   ├── mobile/                    # Mobile web page objects
│   │   ├── __init__.py
│   │   ├── mobile_base_page.py   # Mobile gestures (swipe, tap, etc.)
│   │   └── mobile_login_page.py  # Mobile-specific login
│   └── mobile_app/                # Native mobile app pages
│       ├── __init__.py
│       ├── base_app_page.py      # Base Appium page
│       └── login_app_page.py     # Native app login
│
├── tests/                          # Test suites
│   ├── __init__.py
│   ├── conftest.py                # Shared pytest fixtures
│   ├── frontend/                  # Web UI tests
│   │   ├── __init__.py
│   │   └── test_ui_login.py
│   ├── backend/                   # API tests
│   │   ├── __init__.py
│   │   └── test_api_users.py
│   ├── mobile/                    # Mobile web tests
│   │   ├── __init__.py
│   │   └── test_mobile_login.py
│   └── mobile_app/                # Native mobile app tests
│       ├── __init__.py
│       ├── android/
│       │   └── test_android_login.py
│       └── ios/
│           └── test_ios_login.py
│
├── verification/                   # Framework verification tests
│   ├── __init__.py
│   ├── test_quick_check.py       # Quick smoke test
│   ├── test_verification.py      # Comprehensive framework test
│   └── test_faker_assertpy.py    # Test data & assertion examples
│
├── factories/                      # Factory pattern implementations
│   ├── __init__.py
│   ├── browser_factory.py         # Create different browsers
│   ├── mobile_factory.py          # Mobile device contexts
│   ├── appium_factory.py          # Appium drivers
│   └── test_data_factory.py      # Generate test data
│
├── builders/                       # Builder pattern implementations
│   ├── __init__.py
│   ├── api_request_builder.py     # Build complex API requests
│   └── user_builder.py            # Build test user objects
│
├── strategies/                     # Strategy pattern implementations
│   ├── __init__.py
│   └── auth_strategy.py           # Different authentication methods
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   ├── logger.py                  # Logging utility (Singleton)
│   ├── database.py                # Database connection (Singleton)
│   └── helpers.py                 # Helper functions
│
├── decorators/                     # Decorator pattern implementations
│   ├── __init__.py
│   └── test_decorators.py         # Retry, logging, screenshot decorators
│
├── reports/                        # Test reports (gitignored)
│   ├── screenshots/
│   ├── logs/
│   ├── allure-results/
│   └── allure-report/
│
├── .env                            # Environment variables (gitignored)
├── .env.example                   # Template for environment variables
├── .gitignore                     # Git ignore rules
├── pytest.ini                     # Pytest configuration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## Prerequisites

### System Requirements:
- **Python:** 3.11 or higher (Python 3.12 recommended for easier setup on Windows)
- **Node.js:** 16+ (required for Appium)
- **pip:** Python package manager (included with Python)
- **Git:** For version control
- **IDE:** IntelliJ IDEA, PyCharm, or VS Code (recommended)

### For Windows Users:
- **Option A:** Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (6GB, ~15 min install)
    - Required for compiling greenlet (dependency of Appium and Allure)
    - Select "Desktop development with C++" during installation
- **Option B:** Use Python 3.12 instead of 3.14 (easier, has pre-built wheels for greenlet)

### For Android Testing:
- Android Studio with Android SDK
- Java JDK 11+
- Android Emulator or physical device
- ADB (Android Debug Bridge)

### For iOS Testing (Mac only):
- Xcode (from App Store)
- Xcode Command Line Tools
- iOS Simulator or physical device

### Operating System:
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+)

---

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/n0limits/python-automation-framework.git
cd python-automation-framework
```

### Step 2: Choose Your Python Version

**Option A: Use Python 3.12 (Recommended for Windows)**
```bash
# Check if you have Python 3.12
py -3.12 --version

# Create virtual environment with Python 3.12
py -3.12 -m venv .venv
```

**Option B: Use Python 3.14 (Requires Build Tools on Windows)**
```bash
# Requires Microsoft C++ Build Tools installed first!
python -m venv .venv
```

### Step 3: Activate Virtual Environment
```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### Step 4: Install Python Dependencies
```bash
# Install all packages
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 5: Install Playwright Browsers
```bash
# Install Chromium, Firefox, and WebKit
python -m playwright install

# Or install specific browser
python -m playwright install chromium
```

### Step 6: Install Node.js and Appium (For Mobile Testing)
```bash
# 1. Install Node.js from https://nodejs.org/

# 2. Verify Node.js installation
node --version
npm --version

# 3. Install Appium globally
npm install -g appium

# 4. Install Appium drivers
appium driver install uiautomator2  # For Android
appium driver install xcuitest      # For iOS (Mac only)

# 5. Verify Appium installation
appium --version

# 6. List installed drivers
appium driver list
```

### Step 7: Install Allure Command Line (For Advanced Reports)

**Windows (using Scoop):**
```powershell
# Install Scoop package manager
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Install Allure
scoop install allure
```

**Mac:**
```bash
brew install allure
```

**Linux:**
```bash
# Download from GitHub releases
# https://github.com/allure-framework/allure2/releases
# Extract and add to PATH
```

**Windows (using Chocolatey):**
```powershell
choco install allure
```

**Verify Allure:**
```bash
allure --version
```

### Step 8: Verify Complete Installation
```bash
# Run verification tests
pytest verification/test_quick_check.py -v -s

# Test Playwright browsers
pytest verification/test_verification.py::TestFrameworkVerification::test_playwright_chromium -v -s

# Test Allure report generation
pytest verification/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## Configuration

### 1. Create Environment File

Copy the example environment file and customize it:
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

### 2. Edit .env File

Open `.env` in your editor and configure:
```env
# Application URLs
BASE_URL=https://your-app.com
API_BASE_URL=https://api.your-app.com

# Browser Settings
BROWSER=chromium              # Options: chromium, firefox, webkit
HEADLESS=false                # Run browser in headless mode (true/false)
TIMEOUT=30000                 # Default timeout in milliseconds

# Test Credentials
TEST_USERNAME=your_test_user
TEST_PASSWORD=your_test_password

# API Configuration
API_KEY=your_api_key_here

# Mobile Device Settings (for mobile web testing)
MOBILE_DEVICE=iPhone 13
MOBILE_VIEWPORT_WIDTH=390
MOBILE_VIEWPORT_HEIGHT=844

# Appium Settings (for native mobile app testing)
ANDROID_DEVICE=Android Emulator
ANDROID_VERSION=13.0
IOS_DEVICE=iPhone 13
IOS_VERSION=16.0
APPIUM_SERVER=http://localhost:4723
```

### 3. Verify Configuration
```bash
# Test that settings load correctly
python -c "from config.settings import settings; print(f'BASE_URL: {settings.BASE_URL}')"
```

---

## Writing Tests

### Example 1: Simple UI Test

Create `tests/frontend/test_login.py`:
```python
import pytest
from assertpy import assert_that
from pages.login_page import LoginPage
from config.settings import settings


@pytest.mark.smoke
@pytest.mark.frontend
def test_successful_login(page):
    """Test that user can login with valid credentials"""
    # Arrange
    login_page = LoginPage(page)
    
    # Act
    login_page.open()
    login_page.login(settings.TEST_USERNAME, settings.TEST_PASSWORD)
    
    # Assert
    assert_that(page.url).contains('/dashboard')


@pytest.mark.frontend
def test_login_with_invalid_credentials(page):
    """Test that login fails with invalid credentials"""
    login_page = LoginPage(page)
    
    login_page.open()
    login_page.login('invalid_user', 'wrong_password')
    
    assert_that(login_page.is_error_displayed()).is_true()
    assert_that(login_page.get_error_message()).contains('Invalid')
```

### Example 2: API Test

Create `tests/backend/test_api_users.py`:
```python
import pytest
import requests
from assertpy import assert_that
from config.settings import settings


@pytest.mark.smoke
@pytest.mark.backend
def test_get_user_by_id():
    """Test GET user endpoint"""
    url = f"{settings.API_BASE_URL}/users/1"
    
    response = requests.get(url)
    
    assert_that(response.status_code).is_equal_to(200)
    
    data = response.json()
    assert_that(data).contains_key('id', 'name', 'email')
    assert_that(data['id']).is_equal_to(1)


@pytest.mark.backend
def test_create_user():
    """Test POST create user endpoint"""
    url = f"{settings.API_BASE_URL}/users"
    payload = {
        'name': 'Test User',
        'email': 'test@example.com'
    }
    
    response = requests.post(url, json=payload)
    
    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.json()['name']).is_equal_to(payload['name'])
```

### Example 3: Data-Driven Test with Faker
```python
import pytest
from faker import Faker
from assertpy import assert_that
import requests
from config.settings import settings

fake = Faker()


@pytest.mark.backend
def test_create_user_with_generated_data():
    """Test creating user with Faker-generated data"""
    user_data = {
        'name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number()
    }
    
    response = requests.post(f"{settings.API_BASE_URL}/users", json=user_data)
    
    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.json()['email']).is_equal_to(user_data['email'])
```

### Example 4: Test with Allure Reporting
```python
import pytest
import allure
from assertpy import assert_that
from pages.login_page import LoginPage
from config.settings import settings


@allure.feature('Authentication')
@allure.story('User Login')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_login_with_allure(page):
    """Test user login with Allure reporting"""
    
    with allure.step('Open login page'):
        login_page = LoginPage(page)
        login_page.open()
        allure.attach(
            page.screenshot(),
            name='login_page',
            attachment_type=allure.attachment_type.PNG
        )
    
    with allure.step('Enter credentials'):
        login_page.enter_username(settings.TEST_USERNAME)
        login_page.enter_password(settings.TEST_PASSWORD)
    
    with allure.step('Click login button'):
        login_page.click_login()
    
    with allure.step('Verify redirect to dashboard'):
        assert_that(page.url).contains('/dashboard')
        allure.attach(
            page.screenshot(),
            name='dashboard',
            attachment_type=allure.attachment_type.PNG
        )
```

### Example 5: Mobile App Test with Appium

Create `tests/mobile_app/test_android_login.py`:
```python
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from assertpy import assert_that


@pytest.mark.mobile_app
@pytest.mark.android
def test_android_app_login():
    """Test login on Android app"""
    
    # Configure Android options
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.device_name = 'Android Emulator'
    options.app = '/path/to/your/app.apk'
    options.automation_name = 'UiAutomator2'
    
    # Create driver
    driver = webdriver.Remote(
        command_executor='http://localhost:4723',
        options=options
    )
    
    # Test login
    username_field = driver.find_element('id', 'username')
    password_field = driver.find_element('id', 'password')
    login_button = driver.find_element('id', 'loginButton')
    
    username_field.send_keys('testuser')
    password_field.send_keys('testpass')
    login_button.click()
    
    # Verify
    assert_that(driver.current_activity).contains('MainActivity')
    
    # Close
    driver.quit()
```

---

## Running Tests

### Basic Test Execution
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with live output (see print statements)
pytest -v -s

# Run and stop on first failure
pytest -x

# Run last failed tests
pytest --lf
```

### Run Specific Tests
```bash
# Run specific test file
pytest tests/frontend/test_login.py

# Run specific test function
pytest tests/frontend/test_login.py::test_successful_login

# Run all tests in a directory
pytest tests/frontend/

# Run verification tests
pytest verification/ -v -s
```

### Run by Test Markers
```bash
# Run only smoke tests
pytest -m smoke

# Run only frontend tests
pytest -m frontend

# Run only backend tests
pytest -m backend

# Run only mobile app tests
pytest -m mobile_app

# Run only Android tests
pytest -m android

# Run only iOS tests
pytest -m ios

# Run smoke AND frontend tests
pytest -m "smoke and frontend"

# Run all except slow tests
pytest -m "not slow"
```

### Parallel Execution
```bash
# Run tests in parallel (auto-detect CPU cores)
pytest -n auto

# Run with specific number of workers
pytest -n 4
```

### Generate Reports
```bash
# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Generate Allure results
pytest --alluredir=reports/allure-results

# Open Allure report (starts local web server)
allure serve reports/allure-results

# Generate static Allure report
allure generate reports/allure-results -o reports/allure-report --clean

# Run tests with both reports
pytest --html=reports/report.html --alluredir=reports/allure-results
```

### Run with Different Browsers
```bash
# Run with Firefox
pytest --browser=firefox

# Run with WebKit (Safari engine)
pytest --browser=webkit

# Run in headless mode
pytest --headless
```

### Mobile Testing
```bash
# Start Appium server (in separate terminal)
appium

# Run mobile web tests
pytest tests/mobile/ -v

# Run native mobile app tests
pytest tests/mobile_app/ -v

# Run Android specific tests
pytest tests/mobile_app/ -m android -v

# Run iOS specific tests
pytest tests/mobile_app/ -m ios -v
```

---

## Design Patterns Used

This framework implements several design patterns for maintainability and scalability:

| Pattern | Purpose | Location | Example Use |
|---------|---------|----------|-------------|
| **Page Object Model** | Separate page structure from test logic | `pages/` | `LoginPage`, `DashboardPage` |
| **Singleton** | Single instance of shared resources | `utils/`, `config/` | `Logger`, `DatabaseConnection`, `Settings` |
| **Factory** | Create objects dynamically | `factories/` | `BrowserFactory`, `TestDataFactory` |
| **Builder** | Build complex objects step-by-step | `builders/` | `UserBuilder`, `APIRequestBuilder` |
| **Strategy** | Swap algorithms at runtime | `strategies/` | `AuthStrategy` (Basic, Bearer, OAuth2) |
| **Decorator** | Add behavior to functions | `decorators/` | `@retry`, `@screenshot_on_failure` |

---

## Reports

### HTML Report (pytest-html)
```bash
pytest --html=reports/report.html --self-contained-html
```

Open `reports/report.html` in any browser to view test results, execution time, logs, and screenshots for failed tests.

### Allure Report (Advanced)
```bash
# Run tests and generate Allure results
pytest --alluredir=reports/allure-results

# Open interactive report (starts web server)
allure serve reports/allure-results

# Or generate static HTML report
allure generate reports/allure-results -o reports/allure-report --clean
```

**Allure Features:**
- Beautiful graphs and charts
- Screenshots and attachments
- Step-by-step test execution
- Categorization by features and stories
- Trend analysis across test runs
- Execution time breakdown
- Retry history
- Test categories and severity levels

### Screenshots

Failed tests automatically capture screenshots:
- Location: `reports/screenshots/`
- Format: `failure_{test_name}_{timestamp}.png`
- Attached to Allure reports automatically

### Logs

Test execution logs:
- Location: `reports/test_execution.log`
- Contains: INFO, DEBUG, ERROR messages

---

## Mobile Testing Setup

### Android Setup:

**1. Install Android Studio**
- Download from: https://developer.android.com/studio

**2. Configure Android SDK**
- Open Android Studio > SDK Manager
- Install: Platform-Tools, Build-Tools, Emulator, SDK Platform

**3. Set Environment Variables**

Windows:
```powershell
Variable: ANDROID_HOME
Value: C:\Users\YourUsername\AppData\Local\Android\Sdk

PATH: %ANDROID_HOME%\platform-tools
PATH: %ANDROID_HOME%\tools
```

Mac/Linux:
```bash
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

**4. Create Android Virtual Device (AVD)**
- Device Manager > Create Device > Select device > Create AVD

**5. Start Emulator**
```bash
emulator -list-avds
emulator -avd Pixel_5_API_33
```

**6. Verify**
```bash
adb devices
```

### iOS Setup (Mac Only):

**1. Install Xcode** from App Store

**2. Install Command Line Tools**
```bash
xcode-select --install
```

**3. Accept License**
```bash
sudo xcodebuild -license accept
```

**4. Start Simulator**
```bash
open -a Simulator
```

### Run Mobile Tests:
```bash
# Terminal 1: Start Appium
appium

# Terminal 2: Run tests
pytest tests/mobile_app/ -m android -v -s
pytest tests/mobile_app/ -m ios -v -s
```

---

## Troubleshooting

### Issue: Python not found
**Solution:**
```bash
# Windows: Use 'py' command
py --version
py -m venv .venv
```

### Issue: Greenlet compilation error
**Solution 1:** Install Microsoft C++ Build Tools
**Solution 2:** Use Python 3.12
```bash
py -3.12 -m venv .venv
```

### Issue: Playwright browsers not installed
**Solution:**
```bash
python -m playwright install
```

### Issue: Module not found
**Solution:**
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Appium server not starting
**Solution:**
```bash
npm install -g appium
appium driver list
```

### Issue: Android device not detected
**Solution:**
```bash
adb devices
adb kill-server
adb start-server
```

### Issue: Allure command not found
**Solution:**
```bash
scoop install allure  # Windows
brew install allure   # Mac
```

---

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/tests.yml`:
```yaml
name: Automation Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.11, 3.12]
        browser: [chromium, firefox, webkit]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        playwright install ${{ matrix.browser }}
    
    - name: Run smoke tests
      run: pytest -m smoke -v
    
    - name: Generate Allure report
      if: always()
      run: pytest --alluredir=reports/allure-results
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: reports/
```

---

## Contributing

**1. Fork the repository**

**2. Create feature branch**
```bash
git checkout -b feature/amazing-feature
```

**3. Make changes and test**
```bash
pytest
```

**4. Commit changes**
```bash
git commit -m 'Add amazing feature'
```

**5. Push to branch**
```bash
git push origin feature/amazing-feature
```

**6. Open Pull Request**

### Coding Standards
- Follow PEP 8 style guide
- Write docstrings for all classes and methods
- Add type hints where applicable
- Use Page Object Model for UI tests
- Add appropriate test markers

---

## Additional Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [Appium Documentation](https://appium.io/docs/)
- [Allure Documentation](https://docs.qameta.io/allure/)
- [assertpy Documentation](https://github.com/assertpy/assertpy)
- [Faker Documentation](https://faker.readthedocs.io/)

---

## Contact & Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/n0limits/python-automation-framework/issues)
- **GitHub Discussions:** [Ask questions](https://github.com/n0limits/python-automation-framework/discussions)
- **Repository:** [https://github.com/n0limits/python-automation-framework](https://github.com/n0limits/python-automation-framework)

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Acknowledgments

- [Playwright](https://playwright.dev/) - Modern web automation
- [Appium](https://appium.io/) - Mobile automation
- [pytest](https://pytest.org/) - Testing framework
- [Allure](https://docs.qameta.io/allure/) - Test reporting
- [assertpy](https://github.com/assertpy/assertpy) - Fluent assertions
- [Faker](https://faker.readthedocs.io/) - Test data generation

---

## Project Status

**Current Version:** 1.0.0  
**Status:** Active Development  
**Python Support:** 3.11, 3.12, 3.14  
**Last Updated:** October 2025

---

## Quick Reference

### Installation
```bash
git clone https://github.com/n0limits/python-automation-framework.git
cd python-automation-framework
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install
npm install -g appium
scoop install allure
```

### Run Tests
```bash
pytest                              # All tests
pytest -m smoke                     # Smoke tests
pytest -m frontend                  # Frontend tests
pytest -m backend                   # Backend tests
pytest -m mobile_app                # Mobile app tests
pytest --html=reports/report.html   # With HTML report
pytest --alluredir=reports/allure-results  # With Allure
allure serve reports/allure-results # View Allure report
```

### Mobile Testing
```bash
appium                              # Start Appium server
pytest tests/mobile_app/ -m android # Android tests
pytest tests/mobile_app/ -m ios     # iOS tests
```