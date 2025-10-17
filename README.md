# Python Automation Testing Framework

A comprehensive automation testing framework built with Python, Playwright, Appium, and Pytest for testing web applications (frontend & backend) and mobile applications.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Design Patterns](#design-patterns)
- [Reports](#reports)
- [CI/CD](#cicd)
- [Contributing](#contributing)

## ✨ Features

-  Web UI Testing (Desktop & Mobile Web) with Playwright
-  Native Mobile App Testing (iOS & Android) with Appium
-  API/Backend Testing with Requests
-  Page Object Model (POM) design pattern
-  Cross-browser testing (Chrome, Firefox, Safari, Edge)
-  Cross-platform mobile testing (iOS & Android)
-  Parallel test execution
-  HTML & Allure reports
-  Screenshot capture on failure
-  Logging & debugging
-  CI/CD ready (GitHub Actions)

##  Tech Stack

- **Python 3.11+**
- **Playwright** - Web automation
- **Appium** - Mobile automation
- **Pytest** - Testing framework
- **Requests** - API testing
- **Faker** - Test data generation
- **Allure** - Advanced reporting

## Project Structure
```
automation-framework/
├── pages/                      # Page Object Model
│   ├── base_page.py           # Base page with common methods
│   ├── login_page.py          # Login page object
│   ├── mobile/                # Mobile web pages
│   └── mobile_app/            # Native app pages
├── tests/                      # Test files
│   ├── frontend/              # Web UI tests
│   ├── backend/               # API tests
│   ├── mobile/                # Mobile web tests
│   └── mobile_app/            # Native mobile tests
├── factories/                  # Factory pattern implementations
│   ├── browser_factory.py     # Browser creation
│   ├── mobile_factory.py      # Mobile device contexts
│   └── appium_factory.py      # Appium drivers
├── builders/                   # Builder pattern implementations
│   ├── api_request_builder.py # API request builder
│   └── user_builder.py        # Test data builder
├── strategies/                 # Strategy pattern implementations
│   └── auth_strategy.py       # Authentication strategies
├── utils/                      # Utilities
│   ├── database.py            # Database connection (Singleton)
│   ├── logger.py              # Logger (Singleton)
│   └── helpers.py             # Helper functions
├── config/                     # Configuration files
│   ├── settings.py            # Application settings
│   └── config_manager.py      # Config manager (Singleton)
├── decorators/                 # Decorator pattern implementations
│   └── test_decorators.py     # Test decorators (retry, screenshot)
├── reports/                    # Test reports (gitignored)
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Prerequisites

### For Web Testing:
- Python 3.11 or higher
- pip (Python package manager)

### For Mobile App Testing (Additional):
- **Android:**
    - Android Studio (Android SDK)
    - Java JDK 11+
- **iOS (Mac only):**
    - Xcode
    - Command Line Tools

### For Appium:
- Node.js 16+ and npm
- Appium Server: `npm install -g appium`

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/automation-framework.git
cd automation-framework
```

### 2. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers
```bash
playwright install
```

### 5. Install Appium drivers (if testing mobile apps)
```bash
appium driver install uiautomator2  # Android
appium driver install xcuitest      # iOS
```

## Configuration

### 1. Create `.env` file from template
```bash
cp .env.example .env
```

### 2. Update `.env` with your configuration
```env
BASE_URL=https://your-app.com
API_BASE_URL=https://api.your-app.com
BROWSER=chromium
HEADLESS=false
TIMEOUT=30000
```

### 3. Update `config/settings.py` if needed

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test suite
```bash
# Frontend tests
pytest tests/frontend/

# Backend/API tests
pytest tests/backend/

# Mobile web tests
pytest tests/mobile/

# Mobile app tests
pytest tests/mobile_app/
```

### Run tests by marker
```bash
# Smoke tests only
pytest -m smoke

# Regression tests
pytest -m regression

# Mobile tests
pytest -m mobile

# Android tests
pytest -m android
```

### Run tests in parallel
```bash
pytest -n auto
```

### Run with specific browser
```bash
pytest --browser=firefox
pytest --browser=chromium
pytest --browser=webkit
```

### Run with HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Run with Allure report
```bash
pytest --alluredir=./reports/allure-results
allure serve ./reports/allure-results
```

### Run specific test
```bash
pytest tests/frontend/test_login.py::test_successful_login
```

## Design Patterns Used

| Pattern | Usage | Location |
|---------|-------|----------|
| **Page Object Model** | All UI tests | `pages/` |
| **Singleton** | DB, Logger, Config | `utils/`, `config/` |
| **Factory** | Browser, Mobile, Test Data | `factories/` |
| **Builder** | API Requests, Complex Objects | `builders/` |
| **Strategy** | Authentication Methods | `strategies/` |
| **Decorator** | Retry, Logging, Screenshots | `decorators/` |

## Reports

### HTML Report
After test execution, open `reports/report.html` in browser.

### Allure Report
```bash
# Generate and open Allure report
allure serve ./reports/allure-results
```

### Screenshots
Failed test screenshots are saved in `reports/screenshots/`

### Logs
Test execution logs are in `reports/test_execution.log`

##  CI/CD

This framework is configured for GitHub Actions. See `.github/workflows/tests.yml`

### Running in CI
- Push to `main` branch triggers full test suite
- Pull requests run smoke tests
- Scheduled daily regression runs

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Coding Standards

- Follow PEP 8 style guide
- Write docstrings for all classes and methods
- Add type hints where applicable
- Keep functions focused and testable
- Write meaningful test names

## Known Issues

- None currently

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/automation-framework](https://github.com/yourusername/automation-framework)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

- [Playwright](https://playwright.dev/)
- [Appium](https://appium.io/)
- [Pytest](https://pytest.org/)