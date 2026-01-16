"""
Input Compliance Filter

This module validates user queries BEFORE they reach the LLM.
It enforces privacy, PII protection, and academic compliance rules.
"""

import re
from typing import Tuple

# -------------------------
# Regex patterns
# -------------------------

EMAIL_PATTERN = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w{2,}\b")
PHONE_PATTERN = re.compile(r"\b\d{10}\b")
FORM_NUMBER_PATTERN = re.compile(r"\b(form\s*number|ccat\s*form\s*no)\b", re.I)

RANK_PATTERN = re.compile(
    r"\b(rank|score|marks|percentile|cut[- ]?off)\b", re.I
)

PREDICTION_PATTERN = re.compile(
    r"\b(will\s+i\s+get|can\s+i\s+get|chance\s+of|get\s+admission|eligible\s+for\s+me)\b",
    re.I
)

ADVICE_PATTERN = re.compile(
    r"\b(which\s+course\s+should\s+i|best\s+course\s+for\s+me|what\s+should\s+i\s+choose)\b",
    re.I
)

IMPERSONATION_PATTERN = re.compile(
    r"\b(approve|confirm|allocate\s+seat|change\s+centre)\b", re.I
)

IMPLICIT_PREDICTION_PATTERN = re.compile(
    r"\b(chance|chances|enough|likely|possibility|odds)\b",
    re.I
)

COURSE_ADVICE_PATTERN = re.compile(
    r"\b(which|what|suggest|recommend).*(course|pg|programme)\b",
    re.I
)

IMPERATIVE_AUTHORITY_PATTERN = re.compile(
    r"\b(allocate|assign|confirm|give\s+me|change|approve)\b",
    re.I
)

GUARANTEE_INPUT_PATTERN = re.compile(
    r"\b(sure\s*shot|guarantee|guaranteed|certain|definite)\b",
    re.I
)


# -------------------------
# Main filter
# -------------------------

def check_input_compliance(user_query: str) -> Tuple[bool, str]:
    """
    Returns:
    (is_allowed, message_or_sanitized_query)
    """

    # 1. Block personal identifiers
    if EMAIL_PATTERN.search(user_query) or PHONE_PATTERN.search(user_query):
        return (
            False,
            "Please do not share personal contact information. "
            "I can only answer general admission-related questions."
        )

    if FORM_NUMBER_PATTERN.search(user_query):
        return (
            False,
            "I cannot access or use application form numbers or personal identifiers."
        )

    # 2. Block prediction / eligibility judgement
    if PREDICTION_PATTERN.search(user_query) or RANK_PATTERN.search(user_query):
        return (
            False,
            "I cannot predict admission outcomes or evaluate eligibility based on rank or marks. "
            "Admissions depend on official counselling and seat availability."
        )

    # 3. Block course advice
    if ADVICE_PATTERN.search(user_query):
        return (
            False,
            "I cannot recommend or choose a course for you. "
            "I can provide factual information about available programmes."
        )

    # 4. Block impersonation / authority actions
    if IMPERSONATION_PATTERN.search(user_query):
        return (
            False,
            "I cannot perform or simulate official admission actions."
        )

    # 5. Block implicit admission prediction
    if IMPLICIT_PREDICTION_PATTERN.search(user_query):
        return (
            False,
            "I cannot assess chances, likelihood, or eligibility for admission. "
            "Admissions depend on official counselling and seat availability."
        )

    # 6. Block course recommendation requests
    if COURSE_ADVICE_PATTERN.search(user_query):
        return (
            False,
            "I cannot recommend or choose a course for you. "
            "I can provide factual information about available programmes."
        )

    # 7. Block imperative authority commands
    if IMPERATIVE_AUTHORITY_PATTERN.search(user_query):
        return (
            False,
            "I cannot perform or simulate official admission actions."
        )

    # 8. Block guarantee-style admission questions
    if GUARANTEE_INPUT_PATTERN.search(user_query):
        return (
            False,
            "I cannot guarantee or assure admission outcomes. "
            "Admissions depend on official counselling and seat availability."
        )

    # 9. Allowed
    return True, user_query
