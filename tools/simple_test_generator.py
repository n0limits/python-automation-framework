"""
Simple Test Generator - Minimal Prototype

Generates pytest tests from manual test case descriptions using Claude API.
"""
import os
from anthropic import Anthropic


class SimpleTestGenerator:
    """Minimal test generator using Claude API"""

    def __init__(self, api_key=None):
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    def generate_test(self, test_case_id: str, title: str, steps: list, expected_results: str) -> str:
        """
        Generate pytest test code from manual test case

        Args:
            test_case_id: Test case identifier (e.g., "TC-1001")
            title: Test case title
            steps: List of test steps
            expected_results: Expected test results

        Returns:
            Generated Python test code as string
        """
        # Read existing test as example
        example_test = self._load_example_test()

        # Create prompt for Claude
        prompt = f"""
You are a test automation expert. Generate pytest test code for this manual test case.

MANUAL TEST CASE:
ID: {test_case_id}
Title: {title}

Steps:
{self._format_steps(steps)}

Expected Results:
{expected_results}

FRAMEWORK EXAMPLE (use this pattern):
{example_test}

REQUIREMENTS:
1. Use AAA pattern (Arrange-Act-Assert)
2. Use fixtures: bvnk_api, wallet_balances
3. Use ConversionTestHelper or ApiValidationHelper
4. Add pytest markers: @pytest.mark.bvnk, @pytest.mark.e2e (or appropriate type)
5. Add traceability marker: @pytest.mark.azure_tc("{test_case_id}")
6. Include detailed docstring
7. Follow the example's coding style exactly

Generate ONLY the Python code, no explanations.
"""

        # Call Claude API
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract generated code
        generated_code = response.content[0].text

        # Clean up (remove markdown if present)
        generated_code = generated_code.replace("```python", "").replace("```", "").strip()

        return generated_code

    def _load_example_test(self) -> str:
        """Load an example test from the framework"""
        example_path = "tests/bvnk/e2e/test_currency_conversions.py"

        if os.path.exists(example_path):
            with open(example_path) as f:
                content = f.read()
                # Return first test function only (up to 1000 chars)
                return content[:1000]
        else:
            # Fallback minimal example
            return '''
import pytest
from utils.bvnk.conversion_helper import ConversionTestHelper

@pytest.mark.bvnk
@pytest.mark.e2e
def test_example(bvnk_api, wallet_balances):
    """Example test following AAA pattern"""
    # Arrange
    helper = ConversionTestHelper(bvnk_api)

    # Act
    result = helper.execute_conversion('ETH', 'TRX', 1.0)

    # Assert
    helper.verify_balance_changes(wallet_balances, 'ETH', 'TRX', 1.0)
'''

    def _format_steps(self, steps: list) -> str:
        """Format steps as numbered list"""
        return "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])

    def save_test(self, test_code: str, test_case_id: str, output_dir: str = "tests/bvnk/generated"):
        """Save generated test to file"""
        os.makedirs(output_dir, exist_ok=True)

        filename = f"test_{test_case_id.lower().replace('-', '_')}.py"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(test_code)

        print(f"✓ Generated test saved to: {filepath}")
        return filepath


# ============================================
# EXAMPLE USAGE
# ============================================

if __name__ == '__main__':
    # Initialize generator (requires ANTHROPIC_API_KEY environment variable)
    generator = SimpleTestGenerator()

    # Example: Manual test case from Azure DevOps or Excel
    test_case = {
        'id': 'TC-1001',
        'title': 'Verify user can convert 1 ETH to TRX',
        'steps': [
            'Initialize BVNK account and get bearer token',
            'Get current ETH wallet balance',
            'Get current TRX wallet balance',
            'Create a quote to convert 1 ETH to TRX',
            'Accept the quote',
            'Wait for transaction to complete',
            'Verify ETH balance decreased by 1 (+ service fee)',
            'Verify TRX balance increased'
        ],
        'expected_results': 'Transaction completes successfully with correct balance changes'
    }

    # Generate test code
    print(f"Generating test for {test_case['id']}: {test_case['title']}")
    print("-" * 80)

    test_code = generator.generate_test(
        test_case_id=test_case['id'],
        title=test_case['title'],
        steps=test_case['steps'],
        expected_results=test_case['expected_results']
    )

    print("\nGENERATED CODE:")
    print("=" * 80)
    print(test_code)
    print("=" * 80)

    # Save to file
    generator.save_test(test_code, test_case['id'])

    print("\n Test generation complete!")
    print("\nNext steps:")
    print("1. Review the generated test code")
    print("2. Run: pytest tests/bvnk/generated/test_tc_1001.py -v")
    print("3. Adjust if needed")
