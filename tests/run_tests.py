"""
Automated Evaluation & Red-Team Testing

This script tests the chatbot against compliant and non-compliant queries
to evaluate correctness and safety.
"""


import json
from pathlib import Path

from uni_guard_chatbot.app import handle_user_query
from uni_guard_chatbot.compliance.input_filter import check_input_compliance


BASE_DIR = Path(__file__).resolve().parent
TEST_FILE = BASE_DIR / "red_team_tests.json"


def run_tests():
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        tests = json.load(f)

    passed = 0
    failed = 0

    print("\n🔍 RUNNING ALLOWED QUERY TESTS\n")

    for test in tests["allowed_queries"]:
        query = test["query"]
        response = handle_user_query(query)

        if "cannot process" in response.lower():
            print(f"❌ FAIL: {query}")
            failed += 1
        else:
            print(f"✅ PASS: {query}")
            passed += 1

    print("\n🚨 RUNNING RED-TEAM (BLOCKED) TESTS\n")

    for test in tests["blocked_queries"]:
        query = test["query"]
        expected_rule = test["rule"]

        input_check = check_input_compliance(query)

        if not input_check["allowed"] and expected_rule in input_check["rule"]:
            print(f"✅ PASS (Blocked): {query}")
            passed += 1
        else:
            print(f"❌ FAIL (Not Blocked): {query}")
            failed += 1

    print("\n📊 TEST SUMMARY")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    run_tests()
