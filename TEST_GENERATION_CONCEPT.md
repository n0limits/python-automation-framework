# Test Automation Agent - Concept Design

## Overview

A test automation agent that reads manual test cases from Azure DevOps or Excel and automatically generates automation test code.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    TEST AUTOMATION AGENT                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  INPUT LAYER: Read Manual Test Cases                            │
├─────────────────────────────────────────────────────────────────┤
│  • Azure DevOps API Integration                                 │
│    - Connect to Azure DevOps project                            │
│    - Query test cases via REST API                              │
│    - Extract: ID, Title, Steps, Expected Results, Priority      │
│                                                                  │
│  • Excel File Parser                                            │
│    - Read .xlsx files (openpyxl/pandas)                         │
│    - Parse test case format (columns: ID, Title, Steps, etc.)   │
│    - Extract structured data                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  PARSING LAYER: Understand Test Cases                           │
├─────────────────────────────────────────────────────────────────┤
│  • Natural Language Processing                                  │
│    - Parse test steps (numbered steps, actions)                 │
│    - Identify: Endpoints, HTTP methods, test data               │
│    - Extract assertions from "Expected Results"                 │
│                                                                  │
│  • Pattern Recognition                                          │
│    - Detect test type: API, UI, E2E, functional                 │
│    - Identify API operations: GET, POST, PUT, DELETE            │
│    - Map to framework patterns                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  INTELLIGENCE LAYER: AI/LLM Processing                          │
├─────────────────────────────────────────────────────────────────┤
│  • Claude API / GPT-4 Integration                               │
│    - Send test case to LLM with context                         │
│    - Prompt: "Convert this manual test to pytest code"          │
│    - Provide framework patterns as examples                     │
│                                                                  │
│  • Code Generation Logic                                        │
│    - Generate test function name                                │
│    - Create AAA pattern (Arrange-Act-Assert)                    │
│    - Add appropriate fixtures                                   │
│    - Generate assertions based on expected results              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  GENERATION LAYER: Create Test Code                             │
├─────────────────────────────────────────────────────────────────┤
│  • Code Template Engine                                         │
│    - Use Jinja2 or similar templating                           │
│    - Apply framework patterns                                   │
│    - Generate pytest-compliant code                             │
│                                                                  │
│  • Code Formatting                                              │
│    - Use black for formatting                                   │
│    - Add imports                                                │
│    - Add docstrings                                             │
│    - Add pytest markers                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  VALIDATION LAYER: Review & Test                                │
├─────────────────────────────────────────────────────────────────┤
│  • Syntax Validation                                            │
│    - Compile generated code                                     │
│    - Check for syntax errors                                    │
│                                                                  │
│  • Dry Run                                                      │
│    - pytest --collect-only (check if tests are discoverable)    │
│    - Validate fixtures exist                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  OUTPUT LAYER: Save Generated Tests                             │
├─────────────────────────────────────────────────────────────────┤
│  • File Management                                              │
│    - Create test files in correct directories                   │
│    - Apply naming conventions (test_*.py)                       │
│    - Organize by test type (smoke, e2e, functional)             │
│                                                                  │
│  • Metadata Tracking                                            │
│    - Link generated test to source test case ID                 │
│    - Add traceability comments                                  │
│    - Update mapping file (testcase_id → test_file)              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example Flow

### Input: Manual Test Case from Azure DevOps

```yaml
Test Case ID: TC-1001
Title: "Verify user can convert 1 ETH to TRX"
Priority: High
Type: E2E

Steps:
  1. Initialize BVNK account and get bearer token
  2. Get current ETH wallet balance
  3. Get current TRX wallet balance
  4. Create a quote to convert 1 ETH to TRX
  5. Accept the quote
  6. Wait for transaction to complete
  7. Verify ETH balance decreased by 1 (+ service fee)
  8. Verify TRX balance increased

Expected Results:
  - Quote is created successfully with valid UUID
  - Quote is accepted without errors
  - Transaction completes within 30 seconds
  - ETH balance decreased by 1.0001 (including 0.01% fee)
  - TRX balance increased by quoted amount
```

### Processing: AI Agent Analyzes

```python
# Agent detects:
- Test Type: E2E (end-to-end workflow)
- API Endpoints: /init, /api/wallet, /api/v1/quote, /api/v1/quote/accept/{uuid}
- Actions: GET balance, POST quote, PUT accept, polling loop
- Assertions: Balance changes, transaction completion
- Test Data: from_currency='ETH', to_currency='TRX', amount=1.0
```

### Output: Generated Test Code

```python
"""
Generated from Azure DevOps Test Case: TC-1001
Title: Verify user can convert 1 ETH to TRX
Auto-generated on: 2025-11-29
"""
import pytest
from utils.bvnk.conversion_helper import ConversionTestHelper
from utils.bvnk.test_data import CONVERSION_TEST_CASES


@pytest.mark.bvnk
@pytest.mark.e2e
@pytest.mark.azure_tc("TC-1001")  # Traceability marker
def test_convert_1_eth_to_trx_tc1001(bvnk_api, wallet_balances):
    """
    E2E Test: Convert 1 ETH to TRX

    Azure DevOps Test Case: TC-1001

    Steps:
    1. Initialize BVNK account and get bearer token
    2. Get current ETH wallet balance
    3. Get current TRX wallet balance
    4. Create a quote to convert 1 ETH to TRX
    5. Accept the quote
    6. Wait for transaction to complete
    7. Verify ETH balance decreased by 1 (+ service fee)
    8. Verify TRX balance increased
    """
    # === ARRANGE ===
    helper = ConversionTestHelper(bvnk_api)

    from_currency = 'ETH'
    to_currency = 'TRX'
    amount = 1.0

    initial_eth_balance = wallet_balances[from_currency]
    initial_trx_balance = wallet_balances[to_currency]

    helper.verify_sufficient_balance(wallet_balances, from_currency, amount)

    # === ACT ===
    conversion_result = helper.execute_conversion(
        from_currency,
        to_currency,
        amount
    )

    # === ASSERT ===
    helper.verify_balance_changes(
        wallet_balances,
        from_currency,
        to_currency,
        amount
    )

    print(f"\n✓ TEST PASSED: TC-1001 - Convert 1 ETH to TRX")
```

---

## Implementation Options

### Option 1: AI/LLM-Based Agent (Recommended)

**Pros**:
- Handles complex, varied test case formats
- Understands natural language
- Can adapt to different writing styles
- Can infer missing information

**Cons**:
- Requires API key (cost per request)
- Requires internet connection
- May need human review of generated code

**Implementation**:
```python
# tools/test_generator.py
from anthropic import Anthropic
import os

class TestCaseGenerator:
    def __init__(self, framework_path):
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.framework_path = framework_path

    def generate_test_from_manual_case(self, test_case_dict):
        """
        Generate pytest test code from manual test case

        Args:
            test_case_dict: {
                'id': 'TC-1001',
                'title': 'Test title',
                'steps': ['Step 1', 'Step 2', ...],
                'expected_results': 'Expected outcome',
                'type': 'e2e'  # or 'functional', 'smoke', etc.
            }
        """
        # Load framework examples for context
        example_tests = self._load_framework_examples()

        prompt = f"""
You are a test automation code generator. Generate pytest test code based on this manual test case.

MANUAL TEST CASE:
ID: {test_case_dict['id']}
Title: {test_case_dict['title']}
Type: {test_case_dict['type']}

Steps:
{self._format_steps(test_case_dict['steps'])}

Expected Results:
{test_case_dict['expected_results']}

FRAMEWORK EXAMPLES:
{example_tests}

REQUIREMENTS:
1. Follow AAA pattern (Arrange-Act-Assert)
2. Use existing helpers (ConversionTestHelper, ApiValidationHelper)
3. Add appropriate pytest markers (@pytest.mark.bvnk, @pytest.mark.e2e)
4. Add traceability marker: @pytest.mark.azure_tc("{test_case_dict['id']}")
5. Include docstring with test case ID
6. Use existing fixtures (bvnk_api, wallet_balances)

Generate complete, runnable pytest test code.
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        generated_code = response.content[0].text
        return self._clean_code(generated_code)

    def _load_framework_examples(self):
        # Read existing tests as examples
        with open(f"{self.framework_path}/tests/bvnk/e2e/test_currency_conversions.py") as f:
            return f.read()[:2000]  # First 2000 chars as example

    def _format_steps(self, steps):
        return "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])

    def _clean_code(self, code):
        # Remove markdown code blocks if present
        code = code.replace("```python", "").replace("```", "")
        return code.strip()
```

### Option 2: Rule-Based Generator

**Pros**:
- No API costs
- Works offline
- Deterministic output
- Fast

**Cons**:
- Requires strict test case format
- Limited flexibility
- Can't handle variations well
- Requires extensive pattern library

**Implementation**:
```python
# tools/rule_based_generator.py
from jinja2 import Template

class RuleBasedGenerator:
    def __init__(self):
        self.templates = self._load_templates()

    def generate_test(self, test_case):
        """Generate test using template matching"""

        # Detect test type by keywords
        test_type = self._detect_test_type(test_case)

        # Extract parameters
        params = self._extract_parameters(test_case)

        # Select template
        template = self.templates[test_type]

        # Render
        return template.render(**params)

    def _detect_test_type(self, test_case):
        title_lower = test_case['title'].lower()

        if 'convert' in title_lower or 'conversion' in title_lower:
            return 'e2e_conversion'
        elif 'list' in title_lower or 'get' in title_lower:
            return 'functional_api'
        elif 'health' in title_lower or 'ping' in title_lower:
            return 'smoke'
        else:
            return 'generic'

    def _extract_parameters(self, test_case):
        # Extract currencies, amounts, endpoints, etc.
        # This requires pattern matching on steps
        import re

        params = {
            'test_id': test_case['id'],
            'test_title': test_case['title'],
            'steps': test_case['steps']
        }

        # Example: Extract "1 ETH to TRX" from title
        match = re.search(r'(\d+(?:\.\d+)?)\s+(\w+)\s+to\s+(\w+)', test_case['title'])
        if match:
            params['amount'] = match.group(1)
            params['from_currency'] = match.group(2)
            params['to_currency'] = match.group(3)

        return params

    def _load_templates(self):
        return {
            'e2e_conversion': Template('''
"""
Generated from Test Case: {{ test_id }}
Title: {{ test_title }}
"""
import pytest
from utils.bvnk.conversion_helper import ConversionTestHelper

@pytest.mark.bvnk
@pytest.mark.e2e
@pytest.mark.azure_tc("{{ test_id }}")
def test_{{ test_id|lower|replace('-', '_') }}(bvnk_api, wallet_balances):
    """{{ test_title }}"""
    helper = ConversionTestHelper(bvnk_api)

    # Arrange
    helper.verify_sufficient_balance(wallet_balances, '{{ from_currency }}', {{ amount }})

    # Act
    result = helper.execute_conversion('{{ from_currency }}', '{{ to_currency }}', {{ amount }})

    # Assert
    helper.verify_balance_changes(wallet_balances, '{{ from_currency }}', '{{ to_currency }}', {{ amount }})
    print(f"✓ TEST PASSED: {{ test_id }}")
''')
        }
```

---

## Integration with Azure DevOps

```python
# tools/azure_devops_reader.py
import requests
from typing import List, Dict

class AzureDevOpsTestCaseReader:
    def __init__(self, organization, project, pat_token):
        """
        Initialize Azure DevOps reader

        Args:
            organization: Azure DevOps organization name
            project: Project name
            pat_token: Personal Access Token for authentication
        """
        self.organization = organization
        self.project = project
        self.base_url = f"https://dev.azure.com/{organization}/{project}/_apis"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self._encode_pat(pat_token)}'
        }

    def get_test_cases(self, query_id=None) -> List[Dict]:
        """
        Retrieve test cases from Azure DevOps

        Args:
            query_id: Optional query ID to filter test cases

        Returns:
            List of test case dictionaries
        """
        # Use Work Item Query Language (WIQL)
        wiql = """
        SELECT [System.Id], [System.Title], [System.State]
        FROM WorkItems
        WHERE [System.WorkItemType] = 'Test Case'
        AND [System.State] = 'Design'
        """

        query_url = f"{self.base_url}/wit/wiql?api-version=7.1"
        response = requests.post(query_url, headers=self.headers, json={"query": wiql})
        response.raise_for_status()

        work_item_ids = [item['id'] for item in response.json()['workItems']]

        # Get detailed work item data
        test_cases = []
        for work_item_id in work_item_ids:
            test_case = self.get_test_case_details(work_item_id)
            test_cases.append(test_case)

        return test_cases

    def get_test_case_details(self, work_item_id: int) -> Dict:
        """Get detailed test case information"""
        url = f"{self.base_url}/wit/workitems/{work_item_id}?api-version=7.1"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        data = response.json()
        fields = data['fields']

        # Parse test steps (stored in XML format in Azure DevOps)
        steps = self._parse_test_steps(fields.get('Microsoft.VSTS.TCM.Steps', ''))

        return {
            'id': f"TC-{work_item_id}",
            'title': fields.get('System.Title', ''),
            'state': fields.get('System.State', ''),
            'priority': fields.get('Microsoft.VSTS.Common.Priority', 2),
            'steps': steps,
            'expected_results': self._extract_expected_results(steps),
            'type': self._infer_test_type(fields.get('System.Title', ''))
        }

    def _parse_test_steps(self, steps_xml: str) -> List[str]:
        """Parse test steps from Azure DevOps XML format"""
        import xml.etree.ElementTree as ET

        if not steps_xml:
            return []

        try:
            root = ET.fromstring(steps_xml)
            steps = []
            for step in root.findall('.//step'):
                action = step.find('parameterizedString[@isformatted="true"]')
                if action is not None and action.text:
                    steps.append(action.text.strip())
            return steps
        except:
            return []

    def _extract_expected_results(self, steps: List[str]) -> str:
        """Extract expected results from steps"""
        # Last step often contains expected results
        if steps:
            return steps[-1]
        return "Test should pass"

    def _infer_test_type(self, title: str) -> str:
        """Infer test type from title"""
        title_lower = title.lower()
        if 'e2e' in title_lower or 'end-to-end' in title_lower or 'convert' in title_lower:
            return 'e2e'
        elif 'api' in title_lower or 'endpoint' in title_lower:
            return 'functional'
        elif 'smoke' in title_lower or 'health' in title_lower:
            return 'smoke'
        else:
            return 'functional'

    @staticmethod
    def _encode_pat(pat_token: str) -> str:
        """Encode PAT token for Basic authentication"""
        import base64
        return base64.b64encode(f":{pat_token}".encode()).decode()
```

---

## Integration with Excel

```python
# tools/excel_reader.py
import pandas as pd
from typing import List, Dict

class ExcelTestCaseReader:
    def __init__(self, excel_path: str):
        """
        Initialize Excel reader

        Args:
            excel_path: Path to Excel file containing test cases
        """
        self.excel_path = excel_path

    def read_test_cases(self, sheet_name: str = 'Test Cases') -> List[Dict]:
        """
        Read test cases from Excel file

        Expected Excel format:
        | ID | Title | Type | Priority | Steps | Expected Results |

        Args:
            sheet_name: Name of sheet containing test cases

        Returns:
            List of test case dictionaries
        """
        df = pd.read_excel(self.excel_path, sheet_name=sheet_name)

        test_cases = []
        for _, row in df.iterrows():
            test_case = {
                'id': str(row['ID']),
                'title': row['Title'],
                'type': row.get('Type', 'functional').lower(),
                'priority': row.get('Priority', 2),
                'steps': self._parse_steps(row['Steps']),
                'expected_results': row.get('Expected Results', ''),
            }
            test_cases.append(test_case)

        return test_cases

    def _parse_steps(self, steps_text: str) -> List[str]:
        """Parse steps from text (numbered list or newline-separated)"""
        if pd.isna(steps_text):
            return []

        # Split by newlines
        lines = steps_text.strip().split('\n')

        # Remove numbering (1. 2. etc.)
        import re
        steps = []
        for line in lines:
            # Remove leading numbers and dots
            cleaned = re.sub(r'^\d+\.\s*', '', line.strip())
            if cleaned:
                steps.append(cleaned)

        return steps
```

---

## Complete Usage Example

```python
# tools/automated_test_generator.py
from tools.azure_devops_reader import AzureDevOpsTestCaseReader
from tools.excel_reader import ExcelTestCaseReader
from tools.test_generator import TestCaseGenerator
import os

class AutomatedTestGenerator:
    def __init__(self, framework_path):
        self.framework_path = framework_path
        self.generator = TestCaseGenerator(framework_path)

    def generate_from_azure_devops(
        self,
        organization: str,
        project: str,
        pat_token: str,
        output_dir: str = None
    ):
        """Generate tests from Azure DevOps test cases"""
        print(f"Reading test cases from Azure DevOps ({organization}/{project})...")

        # Read test cases
        reader = AzureDevOpsTestCaseReader(organization, project, pat_token)
        test_cases = reader.get_test_cases()

        print(f"Found {len(test_cases)} test cases")

        # Generate tests
        output_dir = output_dir or f"{self.framework_path}/tests/bvnk/generated"
        os.makedirs(output_dir, exist_ok=True)

        for test_case in test_cases:
            print(f"Generating test for {test_case['id']}: {test_case['title']}")

            # Generate code
            test_code = self.generator.generate_test_from_manual_case(test_case)

            # Save to file
            filename = f"test_{test_case['id'].lower().replace('-', '_')}.py"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, 'w') as f:
                f.write(test_code)

            print(f"  ✓ Generated: {filepath}")

        print(f"\n Generated {len(test_cases)} test files in {output_dir}")

    def generate_from_excel(self, excel_path: str, output_dir: str = None):
        """Generate tests from Excel file"""
        print(f"Reading test cases from Excel: {excel_path}...")

        # Read test cases
        reader = ExcelTestCaseReader(excel_path)
        test_cases = reader.read_test_cases()

        print(f"Found {len(test_cases)} test cases")

        # Generate tests
        output_dir = output_dir or f"{self.framework_path}/tests/bvnk/generated"
        os.makedirs(output_dir, exist_ok=True)

        for test_case in test_cases:
            print(f"Generating test for {test_case['id']}: {test_case['title']}")

            # Generate code
            test_code = self.generator.generate_test_from_manual_case(test_case)

            # Save to file
            filename = f"test_{test_case['id'].lower().replace('-', '_')}.py"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, 'w') as f:
                f.write(test_code)

            print(f"  ✓ Generated: {filepath}")

        print(f"\n Generated {len(test_cases)} test files in {output_dir}")


# Usage
if __name__ == '__main__':
    framework_path = os.getcwd()
    generator = AutomatedTestGenerator(framework_path)

    # Option 1: Generate from Azure DevOps
    generator.generate_from_azure_devops(
        organization='my-org',
        project='my-project',
        pat_token=os.environ['AZURE_PAT_TOKEN']
    )

    # Option 2: Generate from Excel
    generator.generate_from_excel('test_cases.xlsx')
```

---

## Required Dependencies

Add to `requirements.txt`:
```
# Test Generation Dependencies
anthropic>=0.18.0           # Claude API for AI generation
pandas>=2.0.0               # Excel reading
openpyxl>=3.1.0             # Excel file support
jinja2>=3.1.0               # Template engine (if using rule-based)
requests>=2.32.0            # Azure DevOps API (already in requirements)
```

---

## Directory Structure After Implementation

```
python-automation-framework/
├── tools/                                    # NEW: Test generation tools
│   ├── __init__.py
│   ├── automated_test_generator.py          # Main orchestrator
│   ├── test_generator.py                    # AI-based generator
│   ├── rule_based_generator.py              # Rule-based generator
│   ├── azure_devops_reader.py               # Azure DevOps integration
│   ├── excel_reader.py                      # Excel integration
│   └── templates/                           # Jinja2 templates (if using)
│       ├── e2e_template.py.j2
│       ├── functional_template.py.j2
│       └── smoke_template.py.j2
│
├── tests/bvnk/
│   ├── generated/                           # NEW: Auto-generated tests
│   │   ├── test_tc_1001.py
│   │   ├── test_tc_1002.py
│   │   └── ...
│   └── manual/                              # Manually written tests
│       ├── e2e/
│       ├── functional/
│       └── smoke/
│
└── test_cases/                              # NEW: Input test cases
    ├── azure_devops_mapping.json            # Traceability mapping
    └── test_cases.xlsx                      # Excel test cases (optional)
```

---

## Traceability: Linking Generated Tests to Source

```python
# tools/traceability_manager.py
import json
from pathlib import Path

class TraceabilityManager:
    def __init__(self, mapping_file='test_cases/azure_devops_mapping.json'):
        self.mapping_file = mapping_file
        self.mapping = self._load_mapping()

    def _load_mapping(self):
        if Path(self.mapping_file).exists():
            with open(self.mapping_file) as f:
                return json.load(f)
        return {}

    def add_mapping(self, test_case_id, test_file_path, metadata=None):
        """Record mapping between test case and generated test"""
        self.mapping[test_case_id] = {
            'test_file': test_file_path,
            'generated_at': str(pd.Timestamp.now()),
            'metadata': metadata or {}
        }
        self._save_mapping()

    def _save_mapping(self):
        Path(self.mapping_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.mapping_file, 'w') as f:
            json.dump(self.mapping, f, indent=2)

    def get_test_file(self, test_case_id):
        """Find generated test file for a test case ID"""
        return self.mapping.get(test_case_id, {}).get('test_file')
```

---

## Limitations & Considerations

### What AI Can Do Well:
-  Parse natural language test cases
-  Understand test intent
-  Generate syntactically correct code
-  Follow patterns from examples
-  Adapt to variations in test case format

### What AI Cannot Do:
-  Understand business logic without context
-  Know API-specific details (endpoints, auth, data models)
-  Generate tests for undocumented features
-  Guarantee 100% correct test logic
-  Handle complex multi-system integrations

### Human Review Required:
- Verify generated test logic is correct
- Add missing assertions
- Adjust test data
- Handle edge cases
- Review and commit code

---

## Recommendation

**For this use case, I recommend**:

1. **Build a separate tool/CLI** that:
   - Reads test cases from Azure DevOps or Excel
   - Uses Claude API to generate test code
   - Follows the current framework patterns
   - Outputs tests to `tests/bvnk/generated/`

2. **Use the current framework as the foundation**:
   - Provide existing tests as examples to the AI
   - Use the helpers, fixtures, and patterns
   - Keep the same directory structure

3. **Start with a prototype**:
   - Generate 3-5 tests manually to test the approach
   - Iterate on the prompt engineering
   - Refine the output format
   - Then scale to batch generation

This way, we leverage the framework's patterns while adding AI-powered generation capabilities.
