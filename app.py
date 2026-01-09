"""
Main Application Pipeline

This file connects input compliance filtering, LLM/RAG processing,
and output compliance filtering into a single safe workflow.
"""

from compliance.input_filter import check_input_compliance
from compliance.output_filter import check_output_compliance


# --------------------------------
# Mock LLM response (temporary)
# --------------------------------
def mock_llm_response(user_query: str) -> str:
    """
    This simulates an LLM response.
    Replace this with a real RAG + LLM call later.
    """
    if "deadline" in user_query.lower():
        return "The application deadline for MSc Computer Science is March 31."
    if "gpa" in user_query.lower():
        return "With a GPA of 8.5, you have a high chance of admission."
    return "Please contact the admissions office for more details."


# --------------------------------
# Main chatbot handler
# --------------------------------
def handle_user_query(user_query: str) -> str:
    """
    End-to-end safe query handler.
    """

    # 1. Input compliance check
    input_check = check_input_compliance(user_query)
    if not input_check["allowed"]:
        return (
            f"❌ Cannot process your request.\n"
            f"Reason: {input_check['reason']}"
        )

    # 2. Get response from LLM (mocked)
    raw_response = mock_llm_response(user_query)

    # 3. Output compliance check
    output_check = check_output_compliance(raw_response)
    if not output_check["allowed"]:
        return output_check["response"]

    # 4. Safe response
    return output_check["response"]


# --------------------------------
# CLI testing loop
# --------------------------------
if __name__ == "__main__":
    print("🎓 UniGuard Chatbot (Type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = handle_user_query(user_input)
        print(f"Bot: {response}\n")
