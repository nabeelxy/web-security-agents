"""
Evaluation Dataset Creator

This script creates a structured evaluation dataset for testing the security agent.
The dataset includes test cases with expected outcomes.
"""

import json
from pathlib import Path


def create_eval_dataset():
    """
    Create a comprehensive evaluation dataset for the security agent.

    The dataset includes:
    - Legitimate domains (expected: SAFE)
    - Typosquatting attempts (expected: SUSPICIOUS or DANGEROUS)
    - Clear phishing domains (expected: DANGEROUS)
    - Edge cases for robustness testing

    Returns:
        list: List of evaluation cases
    """

    eval_cases = [
        # Category 1: Legitimate domains - Should be marked SAFE
        {
            "id": "safe_001",
            "category": "legitimate",
            "input": "Is google.com safe?",
            "expected_verdict": "SAFE",
            "expected_reasoning": "google.com is a well-known legitimate domain",
            "notes": "Top brand, should be immediately recognized"
        },
        {
            "id": "safe_002",
            "category": "legitimate",
            "input": "Is microsoft.com safe?",
            "expected_verdict": "SAFE",
            "expected_reasoning": "microsoft.com is a well-known legitimate domain",
            "notes": "Major tech company"
        },
        {
            "id": "safe_003",
            "category": "legitimate",
            "input": "Should I trust paypal.com?",
            "expected_verdict": "SAFE",
            "expected_reasoning": "paypal.com is the official PayPal domain",
            "notes": "Financial service, critical to identify correctly"
        },
        {
            "id": "safe_004",
            "category": "legitimate",
            "input": "Is amazon.com legitimate?",
            "expected_verdict": "SAFE",
            "expected_reasoning": "amazon.com is a well-known legitimate e-commerce site",
            "notes": "E-commerce giant"
        },
        {
            "id": "safe_005",
            "category": "legitimate",
            "input": "Can I trust github.com?",
            "expected_verdict": "SAFE",
            "expected_reasoning": "github.com is a legitimate developer platform",
            "notes": "Developer tool, common target for phishing"
        },
        {
            "id": "safe_006",
            "category": "legitmate",
            "input": "Should I trust paypal-login.com?",
            "expected_verdict": "SAFE",
            "expected_reasoning": "Belongs to PayPal domain",
            "notes": "Paypal defensive registration"
        },

        # Category 2: Typosquatting - Should be marked SUSPICIOUS or DANGEROUS
        {
            "id": "typo_001",
            "category": "typosquatting",
            "input": "Is g00gle.com safe?",
            "expected_verdict": "SUSPICIOUS",
            "expected_reasoning": "Uses zeros instead of 'o' - likely typosquatting",
            "notes": "Classic character substitution"
        },
        {
            "id": "typo_002",
            "category": "typosquatting",
            "input": "Should I trust paypal-verify.com?",
            "expected_verdict": "SUSPICIOUS",
            "expected_reasoning": "Does not belong to PayPal domain",
            "notes": "-verify append"
        },
        {
            "id": "typo_003",
            "category": "typosquatting",
            "input": "Is micros0ft.com legitimate?",
            "expected_verdict": "SUSPICIOUS",
            "expected_reasoning": "Uses zero instead of 'o' - typosquatting attempt",
            "notes": "Character substitution with zero"
        },
        {
            "id": "typo_004",
            "category": "typosquatting",
            "input": "Can I trust amaz0n.com?",
            "expected_verdict": "SUSPICIOUS",
            "expected_reasoning": "Character substitution, not official Amazon",
            "notes": "Zero instead of 'o'"
        },

        # Category 3: Obvious phishing - Should be marked DANGEROUS
        {
            "id": "phish_001",
            "category": "phishing",
            "input": "Is paypal-secure-login.xyz safe?",
            "expected_verdict": "DANGEROUS",
            "expected_reasoning": "Suspicious TLD and fake security terminology",
            "notes": "Combines suspicious TLD with fake security terms"
        },
        {
            "id": "phish_002",
            "category": "phishing",
            "input": "Should I trust microsoft-support.xyz?",
            "expected_verdict": "DANGEROUS",
            "expected_reasoning": "Not official Microsoft domain, suspicious TLD",
            "notes": "Impersonates support services"
        },
        {
            "id": "phish_003",
            "category": "phishing",
            "input": "Is google-verify.info legitimate?",
            "expected_verdict": "DANGEROUS",
            "expected_reasoning": "Not official Google domain, suspicious verification claim",
            "notes": "Fake verification site"
        },
        {
            "id": "phish_004",
            "category": "phishing",
            "input": "Can I trust secure-paypal.tk?",
            "expected_verdict": "DANGEROUS",
            "expected_reasoning": "Free TLD (.tk) with PayPal brand, likely phishing",
            "notes": "Free TLD often used for phishing"
        },

        # Category 4: Edge cases - Testing robustness
        {
            "id": "edge_001",
            "category": "edge_case",
            "input": "Is gooogle.com safe?",  # Extra 'o'
            "expected_verdict": "SAFE",
            "expected_reasoning": "Belongs to Google domain, minor typo with extra character",
            "notes": "Defensive registration by Google"
        },
        {
            "id": "edge_002",
            "category": "edge_case",
            "input": "Is goggle.com safe?",  # Missing 'o'
            "expected_verdict": "SAFE",
            "expected_reasoning": "Typosquatting, but belongs to Google",
            "notes": "Defensive registration by Google"
        },
        {
            "id": "edge_003",
            "category": "edge_case",
            "input": "Should I visit apple.co?",
            "expected_verdict": "SAFE",
            "expected_reasoning": "apple.com is official, .co domain is a variant of it.",
            "notes": "Defensive registration by Apple"
        },
        {
            "id": "edge_004",
            "category": "edge_case",
            "input": "Is amazonprime.com legitimate?",
            "expected_verdict": "SAFE",
            "expected_reasoning": "Redirects to amazon.com",
            "notes": "Defensively registered domain"
        },

        # Category 5: Variations in question phrasing
        {
            "id": "phrase_001",
            "category": "phrasing_variation",
            "input": "Tell me if facebook.com is safe",
            "expected_verdict": "SAFE",
            "expected_reasoning": "facebook.com is a legitimate social media platform",
            "notes": "Testing different question format"
        },
        {
            "id": "phrase_002",
            "category": "phrasing_variation",
            "input": "facebook-security.com - is this legitimate?",
            "expected_verdict": "SUSPICIOUS",
            "expected_reasoning": "Not official Facebook domain",
            "notes": "Testing different question format with suspicious domain"
        },
    ]

    return eval_cases


def save_eval_dataset(dataset, output_path="eval_dataset.json"):
    """
    Save the evaluation dataset to a JSON file.

    Args:
        dataset (list): List of evaluation cases
        output_path (str): Path to save the dataset

    Returns:
        str: Path to the saved file
    """

    output_file = Path(output_path)

    # Create metadata
    eval_data = {
        "metadata": {
            "version": "1.0",
            "description": "Security agent evaluation dataset",
            "total_cases": len(dataset),
            "categories": {
                "legitimate": len([c for c in dataset if c["category"] == "legitimate"]),
                "typosquatting": len([c for c in dataset if c["category"] == "typosquatting"]),
                "phishing": len([c for c in dataset if c["category"] == "phishing"]),
                "edge_case": len([c for c in dataset if c["category"] == "edge_case"]),
                "phrasing_variation": len([c for c in dataset if c["category"] == "phrasing_variation"]),
            }
        },
        "test_cases": dataset
    }

    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(eval_data, f, indent=2, ensure_ascii=False)

    print(f"✓ Created evaluation dataset: {output_file}")
    print(f"  Total test cases: {len(dataset)}")
    print(f"  Categories:")
    for category, count in eval_data["metadata"]["categories"].items():
        print(f"    - {category}: {count}")

    return str(output_file)


def load_eval_dataset(dataset_path="eval_dataset.json"):
    """
    Load an evaluation dataset from a JSON file.

    Args:
        dataset_path (str): Path to the dataset file

    Returns:
        dict: Loaded evaluation dataset with metadata
    """

    with open(dataset_path, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    print("Creating evaluation dataset for security agent...\n")

    # Create the dataset
    dataset = create_eval_dataset()

    # Save to file
    save_eval_dataset(dataset)

    print("\n✓ Dataset created successfully!")
    print("\nNext steps:")
    print("1. Review eval_dataset.json")
    print("2. Run evaluations with: python run_eval.py")
    print("3. Analyze results with: python analyze_results.py")
