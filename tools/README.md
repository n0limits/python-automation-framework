# Test Generation Tools - AI QA Automation Agent

**Automatically generate pytest test code from manual test cases stored in Azure DevOps or Excel files.**

---

## 📋 Overview

### Can the current framework generate tests automatically?

**Current framework**:  Cannot generate tests automatically

**What you can build**:  AI-powered test generator that:
- Reads manual test cases (Azure DevOps, Excel, CSV)
- Uses Claude API to generate pytest code
- Follows your framework's patterns (AAA, helpers, fixtures)
- Outputs to `tests/bvnk/generated/`

---

## 🚀 Try It Now (3 Steps)

### 1. Install dependencies
```bash
pip install anthropic pandas openpyxl
```

### 2. Set Claude API key
```bash
# Get your API key from: https://console.anthropic.com/

# Windows
set ANTHROPIC_API_KEY=your_key_here

# Mac/Linux
export ANTHROPIC_API_KEY=your_key_here
```

### 3. Run the example generator
```bash
python tools/simple_test_generator.py
```

**What happens**:
- Generates test code for TC-1001
- Saves to `tests/bvnk/generated/test_tc_1001.py`
- Prints the generated code to console

---

## 📊 What You Get

### Input (Manual Test Case):
```yaml
ID: TC-1001
Title: Verify user can convert 1 ETH to TRX
Steps:
  1. Initialize BVNK account and get bearer token
  2. Create quote to convert 1 ETH to TRX
  3. Accept the quote
  4. Verify balance changes correctly
Expected Results: Transaction completes with correct balance changes
```

### Output (Generated pytest code):
```python
@pytest.mark.bvnk
@pytest.mark.e2e
@pytest.mark.azure_tc("TC-1001")
def test_tc_1001(bvnk_api, wallet_balances):
    """Verify user can convert 1 ETH to TRX"""

    # Arrange
    helper = ConversionTestHelper(bvnk_api)
    helper.verify_sufficient_balance(wallet_balances, 'ETH', 1.0)

    # Act
    result = helper.execute_conversion('ETH', 'TRX', 1.0)

    # Assert
    helper.verify_balance_changes(wallet_balances, 'ETH', 'TRX', 1.0)
    print(f"✓ TEST PASSED: TC-1001")
```

---

## 🔧 Integration Options

| Source | Status | Implementation |
|--------|--------|----------------|
| **Manual Input** |  Ready | `simple_test_generator.py` |
| **CSV/Excel** |  Ready | Use pandas to read + generator |
| **Azure DevOps** | 📝 Concept | See `TEST_GENERATION_CONCEPT.md` |

---

## ⚠️ Important Notes

1. **AI generates code** - Always review before using in production!
2. **Requires API key** - Claude API costs approximately $0.01 per test case
3. **Not 100% perfect** - Generated tests may need manual adjustments
4. **Best for** - Standard API tests following existing framework patterns
5. **Not for** - Complex business logic or highly unique test scenarios

---

## 💡 Why This Framework is Perfect for AI Generation

Your framework has everything needed for successful AI test generation:
-  Clear patterns (AAA pattern, helpers, fixtures)
-  Reusable components (ConversionTestHelper, ApiValidationHelper)
-  Consistent structure (same test organization across all tests)
-  Good examples for AI to learn from

The AI uses your existing tests as examples to generate new ones following the same patterns.

---

## 📚 Files Created for You

| File | Description | Status |
|------|-------------|--------|
| `tools/simple_test_generator.py` | Working prototype - ready to use! |  Ready |
| `tools/README.md` | This documentation |  Ready |
| `test_cases/example_test_cases.csv` | Sample CSV format for test cases |  Ready |
| `TEST_GENERATION_CONCEPT.md` | Full architecture & advanced features | 📝 Reference |

---

## Quick Start

### Prerequisites

1. **Install required dependencies**:
   ```bash
   pip install anthropic pandas openpyxl
   ```

2. **Set up Claude API key**:
   ```bash
   # Windows
   set ANTHROPIC_API_KEY=your_api_key_here

   # Mac/Linux
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

   Get your API key from: https://console.anthropic.com/

---

## Usage

### Option 1: Simple Test Generator (Prototype)

**Generate a single test from a manual test case**:

```python
from tools.simple_test_generator import SimpleTestGenerator

# Initialize
generator = SimpleTestGenerator()

# Define test case
test_case = {
    'id': 'TC-1001',
    'title': 'Verify user can convert 1 ETH to TRX',
    'steps': [
        'Initialize BVNK account',
        'Create quote for 1 ETH to TRX',
        'Accept quote',
        'Verify balance changes'
    ],
    'expected_results': 'Balance changes correctly'
}

# Generate test code
test_code = generator.generate_test(
    test_case_id=test_case['id'],
    title=test_case['title'],
    steps=test_case['steps'],
    expected_results=test_case['expected_results']
)

# Save to file
generator.save_test(test_code, test_case['id'])
```

**Run the example**:
```bash
python tools/simple_test_generator.py
```

This will:
1. Generate test code for TC-1001
2. Save it to `tests/bvnk/generated/test_tc_1001.py`
3. Print the generated code

---

### Option 2: Batch Generation from CSV/Excel

**Create a CSV file** (`test_cases/example_test_cases.csv`):
```csv
ID,Title,Type,Priority,Steps,Expected Results
TC-1001,Convert ETH to TRX,e2e,High,"Step 1\nStep 2\nStep 3","Expected result"
TC-1002,Test API auth,functional,Medium,"Step 1\nStep 2","Expected result"
```

**Generate all tests**:
```python
import pandas as pd
from tools.simple_test_generator import SimpleTestGenerator

# Read test cases from CSV
df = pd.read_csv('test_cases/example_test_cases.csv')

generator = SimpleTestGenerator()

for _, row in df.iterrows():
    steps = row['Steps'].split('\n')

    test_code = generator.generate_test(
        test_case_id=row['ID'],
        title=row['Title'],
        steps=steps,
        expected_results=row['Expected Results']
    )

    generator.save_test(test_code, row['ID'])
    print(f"✓ Generated {row['ID']}")
```

---

### Option 3: Azure DevOps Integration (Advanced)

See `TEST_GENERATION_CONCEPT.md` for complete implementation details.

**Basic example**:
```python
from tools.azure_devops_reader import AzureDevOpsTestCaseReader

# Connect to Azure DevOps
reader = AzureDevOpsTestCaseReader(
    organization='your-org',
    project='your-project',
    pat_token='your_pat_token'
)

# Get all test cases
test_cases = reader.get_test_cases()

# Generate tests for each
for test_case in test_cases:
    # ... use SimpleTestGenerator to create tests
```

---

## Generated Test Example

**Input** (Manual Test Case):
```
ID: TC-1001
Title: Verify user can convert 1 ETH to TRX
Steps:
  1. Initialize BVNK account
  2. Create quote to convert 1 ETH to TRX
  3. Accept quote
  4. Verify balance changes
```

**Output** (Generated Python Test):
```python
"""
Generated from Test Case: TC-1001
Title: Verify user can convert 1 ETH to TRX
"""
import pytest
from utils.bvnk.conversion_helper import ConversionTestHelper

@pytest.mark.bvnk
@pytest.mark.e2e
@pytest.mark.azure_tc("TC-1001")
def test_tc_1001(bvnk_api, wallet_balances):
    """Verify user can convert 1 ETH to TRX"""

    # Arrange
    helper = ConversionTestHelper(bvnk_api)
    helper.verify_sufficient_balance(wallet_balances, 'ETH', 1.0)

    # Act
    result = helper.execute_conversion('ETH', 'TRX', 1.0)

    # Assert
    helper.verify_balance_changes(wallet_balances, 'ETH', 'TRX', 1.0)
    print(f"✓ TEST PASSED: TC-1001")
```

---

## Directory Structure

```
python-automation-framework/
├── tools/
│   ├── README.md                       # This file
│   ├── simple_test_generator.py        # Minimal prototype (ready to use)
│   ├── azure_devops_reader.py          # Azure DevOps integration (concept)
│   └── excel_reader.py                 # Excel integration (concept)
│
├── test_cases/
│   ├── example_test_cases.csv          # Example CSV format
│   └── azure_devops_mapping.json       # Traceability mapping
│
├── tests/bvnk/
│   ├── generated/                      # Auto-generated tests go here
│   │   ├── test_tc_1001.py
│   │   └── test_tc_1002.py
│   └── manual/                         # Manually written tests
│       ├── e2e/
│       ├── functional/
│       └── smoke/
```

---

## Testing Generated Code

After generating tests, run them:

```bash
# Run single generated test
pytest tests/bvnk/generated/test_tc_1001.py -v -s

# Run all generated tests
pytest tests/bvnk/generated/ -v

# Run with coverage
pytest tests/bvnk/generated/ -v --cov=utils
```

---

## Best Practices

### 1. **Review Generated Code**
- AI-generated code should be reviewed before committing
- Verify test logic matches intent
- Add/adjust assertions as needed

### 2. **Provide Good Test Case Descriptions**
- Clear, numbered steps
- Specific expected results
- Include test data where possible

### 3. **Use Traceability Markers**
- Add `@pytest.mark.azure_tc("TC-ID")` to link back to source
- Maintain mapping file for bidirectional traceability

### 4. **Iterate on Prompts**
- If generated code isn't quite right, adjust the prompt in `simple_test_generator.py`
- Provide better examples from your framework
- Add more specific requirements

### 5. **Version Control**
- Commit generated tests separately from manual tests
- Document which tests are auto-generated
- Consider keeping source test cases in version control

---

## Limitations

**What the generator CAN do**:
-  Generate syntactically correct pytest code
-  Follow your framework's patterns
-  Use existing helpers and fixtures
-  Create appropriate test structure

**What it CANNOT do**:
-  Understand complex business logic without clear description
-  Know API-specific details not in test case
-  Guarantee 100% correct test logic
-  Handle edge cases not described in test case

**Always review generated tests before using in production!**

---

## Troubleshooting

### "anthropic module not found"
```bash
pip install anthropic
```

### "ANTHROPIC_API_KEY not set"
```bash
# Set environment variable
export ANTHROPIC_API_KEY=your_key_here
```

### Generated test doesn't work
1. Review the generated code
2. Check if helpers/fixtures exist
3. Adjust test logic manually
4. Update prompt in generator to improve future generations

### Want to customize generation
1. Edit `simple_test_generator.py`
2. Modify the prompt (lines 23-42)
3. Add more framework examples
4. Adjust code cleaning logic

---

## Next Steps

1. **Start with prototype**: Use `simple_test_generator.py` for a few test cases
2. **Review results**: See what works and what needs adjustment
3. **Refine prompts**: Improve generation quality
4. **Scale up**: Build batch processing for multiple test cases
5. **Add integrations**: Implement Azure DevOps or Excel readers if needed

See `TEST_GENERATION_CONCEPT.md` for comprehensive architecture and advanced features.

---

## 📖 Complete Documentation Index

| Document | Purpose | Audience |
|----------|---------|----------|
| `tools/README.md` | Quick start & usage guide | Everyone (start here!) |
| `tools/simple_test_generator.py` | Working code - run this! | Developers |
| `TEST_GENERATION_CONCEPT.md` | Full architecture & design | Architects/Advanced users |
| `test_cases/example_test_cases.csv` | Sample test case format | Test case writers |

---

## 💰 Cost Estimate

**Claude API Pricing** (approximate):
- Cost per test: ~$0.01 - $0.03 USD
- 100 tests: ~$1 - $3 USD
- 1000 tests: ~$10 - $30 USD

**Alternative**: Use rule-based generation (free, but less flexible)

---

## 🎯 Recommended Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Write Manual Test Cases in Azure DevOps or Excel        │
│    (ID, Title, Steps, Expected Results)                     │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Export or Read Test Cases                                │
│    - Azure DevOps API                                       │
│    - Excel/CSV file                                         │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Run Test Generator                                       │
│    python tools/simple_test_generator.py                    │
│    or use batch processing                                  │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Review Generated Tests                                   │
│    - Check test logic                                       │
│    - Verify assertions                                      │
│    - Adjust as needed                                       │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Run Tests                                                │
│    pytest tests/bvnk/generated/ -v                          │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Fix Failures & Commit                                    │
│    - Debug failed tests                                     │
│    - Commit to version control                              │
│    - Update traceability mapping                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔗 Quick Links

- **Claude API Console**: https://console.anthropic.com/
- **Anthropic Python SDK**: https://github.com/anthropics/anthropic-sdk-python
- **Azure DevOps REST API**: https://learn.microsoft.com/en-us/rest/api/azure/devops/
- **Pandas Documentation**: https://pandas.pydata.org/docs/

---

## 📞 Support & Feedback

**Having issues?**
1. Check the [Troubleshooting](#troubleshooting) section
2. Review your test case format (clear steps + expected results)
3. Check Claude API key is set correctly
4. Review generated code for syntax errors

**Want to improve generation quality?**
1. Edit prompts in `simple_test_generator.py` (lines 23-47)
2. Add more framework examples
3. Provide clearer test case descriptions
4. Iterate on a few tests before scaling up

---

##  Summary

**What you have now**:
-  Working test generator prototype (`simple_test_generator.py`)
-  Example test case format (CSV)
-  Complete documentation
-  Concept design for Azure DevOps integration

**What you can do**:
1. Generate single test: `python tools/simple_test_generator.py`
2. Batch generate from CSV
3. Integrate with Azure DevOps (requires implementation)
4. Customize for your specific needs

**What you need**:
- Claude API key (get from https://console.anthropic.com/)
- Manual test cases (Azure DevOps or CSV/Excel)
- Python 3.12+
- Dependencies: `anthropic`, `pandas`, `openpyxl`

---

**Ready to start? Run the generator now:**
```bash
python tools/simple_test_generator.py
```
