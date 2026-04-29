import os
import json
from datetime import datetime
from dotenv import load_dotenv
import anthropic
import time

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SAMPLE_CODE_DIFF = """
+ def calculate_monthly_cost(resources, region='us-east-1'):
+     pricing = get_pricing_data(region)
+     total = 0
+     for resource in resources:
+         if resource['type'] == 'lambda':
+             total += resource['invocations'] * pricing['lambda_per_invocation']
+         elif resource['type'] == 'dynamodb':
+             total += resource['read_units'] * pricing['dynamodb_rcu']
+             total += resource['write_units'] * pricing['dynamodb_wcu']
+         elif resource['type'] == 's3':
+             total += resource['storage_gb'] * pricing['s3_per_gb']
+     return round(total, 4)

- def get_cost(items):
-     return sum(item['cost'] for item in items)
"""

def generate_docs(diff):
    print("Generating documentation with Claude AI...")

    prompt = f"""
You are a senior technical writer. Analyze this code diff and generate:

1. CHANGELOG ENTRY
   - Version bump suggestion
   - What changed and why
   - Breaking changes if any

2. FUNCTION DOCUMENTATION
   - Docstring for the new function
   - Parameters and return values
   - Usage example

3. PR DESCRIPTION
   - Title
   - Summary of changes
   - Testing notes
   - Reviewers checklist

CODE DIFF:
{diff}

Be specific and professional. Format clearly.
    """

    for attempt in range(3):
        try:
            message = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                time.sleep(5)

    return "Documentation unavailable"

def run():
    print("Docs That Write Themselves")
    print("==========================\n")

    print("Step 1: Reading code diff...")
    print(f"Diff size: {len(SAMPLE_CODE_DIFF.split())} words\n")

    print("Step 2: Generating docs with Claude AI...")
    docs = generate_docs(SAMPLE_CODE_DIFF)

    print("\n" + "="*50)
    print("GENERATED DOCUMENTATION")
    print("="*50 + "\n")
    print(docs)

    report = {
        'timestamp': datetime.now().isoformat(),
        'diff': SAMPLE_CODE_DIFF,
        'generated_docs': docs
    }

    with open('docs_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print("\nDocs saved to docs_report.json")
    print("\nDocs Writer complete!")

if __name__ == "__main__":
    run()