"""
Main Application Pipeline

This file connects input compliance filtering, LLM/RAG processing,
and output compliance filtering into a single safe workflow.
"""

from compliance.input_filter import check_input_compliance
from compliance.output_filter import check_output_compliance
from rag.query import retrieve_context
from rag.llm import generate_answer


def handle_user_query(user_query: str) -> str:
    # 1. Input compliance
    input_check = check_input_compliance(user_query)
    if not input_check["allowed"]:
        return (
            f"❌ Cannot process your request.\n"
            f"Reason: {input_check['reason']}"
        )

    # 2. Retrieve context
    context = retrieve_context(user_query)

    if not context.strip():
        return "I don’t have that information in my knowledge base."

    # 3. Generate LLM answer
    raw_response = generate_answer(context, user_query)

    # 4. Output compliance
    output_check = check_output_compliance(raw_response)
    if not output_check["allowed"]:
        return output_check["response"]

    # 5. Safe response
    return output_check["response"]
