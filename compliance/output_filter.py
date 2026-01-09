"""
Output Compliance Filter

This module validates LLM-generated responses BEFORE they are shown to the user.
It ensures that the chatbot does not leak private data, give advice, or violate
academic and privacy policies.
"""

import re
from typing import Dict


# -----------------------------
# Forbidden content patterns
# -----------------------------

# Advice / decision language
ADVICE_PATTERNS = [
    r"\byou should\b",
    r"\bi recommend\b",
    r"\byou can\b",
    r"\byou must\b",
    r"\bmy advice\b",
]

# Admission prediction language
ADMISSION_PREDICTION_PATTERNS = [
    r"\byou will get admitted\b",
    r"\byou are likely to get\b",
    r"\bhigh chance of admission\b",
    r"\blow chance of admission\b",
]

# Academic private information
PRIVATE_ACADEMIC_PATTERNS = [
    r"\bgpa\b",
    r"\bcgpa\b",
    r"\bgrades?\b",
    r"\bmarks?\b",
    r"\btranscript\b",
    r"\bpercentage\b",
]

# PII patterns (same philosophy as input filter)
PII_PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone_number": r"\b\d{10}\b",
    "student_id": r"\b\d{7,10}\b",
}


# -----------------------------
# Canned safe responses
# -----------------------------
REFUSAL_MESSAGES = {
    "ADVICE": (
        "I’m sorry, but I can’t provide personalized advice or predictions. "
        "I can share general information about university policies and requirements."
    ),
    "PRIVACY": (
        "I’m sorry, but I can’t share personal or private academic information "
        "due to student privacy regulations."
    ),
    "PII": (
        "I’m sorry, but I can’t process or display personal identifying information."
    ),
}


# -----------------------------
# Helper detection functions
# -----------------------------
def _contains_patterns(text: str, patterns: list) -> bool:
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in patterns)


def _contains_pii(text: str) -> str | None:
    for pii_type, pattern in PII_PATTERNS.items():
        if re.search(pattern, text):
            return pii_type
    return None


# -----------------------------
# Main output compliance function
# -----------------------------
def check_output_compliance(llm_response: str) -> Dict:
    """
    Checks whether the LLM-generated output complies with policies.

    Returns:
        {
            "allowed": bool,
            "rule": str,
            "response": str
        }
    """

    if not llm_response or not llm_response.strip():
        return {
            "allowed": False,
            "rule": "EMPTY_RESPONSE",
            "response": REFUSAL_MESSAGES["PRIVACY"]
        }

    # 1. PII leakage
    pii_type = _contains_pii(llm_response)
    if pii_type:
        return {
            "allowed": False,
            "rule": "PII_LEAKAGE",
            "response": REFUSAL_MESSAGES["PII"]
        }

    # 2. Private academic information
    if _contains_patterns(llm_response, PRIVATE_ACADEMIC_PATTERNS):
        return {
            "allowed": False,
            "rule": "STUDENT_PRIVACY",
            "response": REFUSAL_MESSAGES["PRIVACY"]
        }

    # 3. Personalized advice
    if _contains_patterns(llm_response, ADVICE_PATTERNS):
        return {
            "allowed": False,
            "rule": "NO_ADVICE",
            "response": REFUSAL_MESSAGES["ADVICE"]
        }

    # 4. Admission predictions
    if _contains_patterns(llm_response, ADMISSION_PREDICTION_PATTERNS):
        return {
            "allowed": False,
            "rule": "NO_ADMISSION_PREDICTION",
            "response": REFUSAL_MESSAGES["ADVICE"]
        }

    # 5. Passed all checks
    return {
        "allowed": True,
        "rule": "COMPLIANT",
        "response": llm_response
    }
