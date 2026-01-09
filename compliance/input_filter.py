"""
Input Compliance Filter

This module validates user queries BEFORE they reach the LLM.
It enforces privacy, PII protection, and academic compliance rules.
"""

import re
from typing import Dict

try:
    import spacy
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False


# -----------------------------
# Regex-based PII patterns
# -----------------------------
PII_PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone_number": r"\b\d{10}\b",
    "student_id": r"\b\d{7,10}\b"
}

# -----------------------------
# Private academic information keywords
# -----------------------------
PRIVATE_ACADEMIC_KEYWORDS = [
    "gpa",
    "cgpa",
    "grades",
    "grade",
    "marks",
    "score",
    "transcript",
    "rank",
    "percentage"
]

# -----------------------------
# Admission decision / advice keywords
# -----------------------------
ADMISSION_ADVICE_KEYWORDS = [
    "will i get admitted",
    "will i get admission",
    "chance of admission",
    "can i get into",
    "am i eligible",
    "should i apply"
]

# -----------------------------
# Load spaCy NER model (optional)
# -----------------------------
_nlp = None
if NLP_AVAILABLE:
    try:
        _nlp = spacy.load("en_core_web_sm")
    except OSError:
        _nlp = None


# -----------------------------
# Helper functions
# -----------------------------
def _contains_pii(text: str) -> Dict | None:
    """Detect PII using regex."""
    for pii_type, pattern in PII_PATTERNS.items():
        if re.search(pattern, text):
            return {
                "allowed": False,
                "rule": "PII_PROTECTION",
                "reason": f"Detected personal identifier: {pii_type}"
            }
    return None


def _contains_private_academic_info(text: str) -> Dict | None:
    """Detect requests for private academic information."""
    text_lower = text.lower()
    for keyword in PRIVATE_ACADEMIC_KEYWORDS:
        if keyword in text_lower:
            return {
                "allowed": False,
                "rule": "STUDENT_PRIVACY",
                "reason": "Request for private academic information"
            }
    return None


def _contains_admission_advice(text: str) -> Dict | None:
    """Detect personalized admission advice or predictions."""
    text_lower = text.lower()
    for phrase in ADMISSION_ADVICE_KEYWORDS:
        if phrase in text_lower:
            return {
                "allowed": False,
                "rule": "NO_ADMISSION_ADVICE",
                "reason": "Request for personalized admission advice or prediction"
            }
    return None


def _contains_person_name(text: str) -> bool:
    """
    Detect PERSON entities using spaCy (if available).
    Used to strengthen privacy checks.
    """
    if not _nlp:
        return False

    doc = _nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return True
    return False


# -----------------------------
# Main compliance function
# -----------------------------
def check_input_compliance(user_query: str) -> Dict:
    """
    Checks whether a user query complies with defined rules.

    Returns:
        {
            "allowed": bool,
            "rule": str,
            "reason": str
        }
    """

    if not user_query or not user_query.strip():
        return {
            "allowed": False,
            "rule": "INVALID_INPUT",
            "reason": "Empty or invalid query"
        }

    # 1. PII detection
    pii_check = _contains_pii(user_query)
    if pii_check:
        return pii_check

    # 2. Private academic information
    academic_check = _contains_private_academic_info(user_query)
    if academic_check:
        # Strengthen rule if person name is detected
        if _contains_person_name(user_query):
            academic_check["reason"] += " about an individual"
        return academic_check

    # 3. Admission advice / prediction
    advice_check = _contains_admission_advice(user_query)
    if advice_check:
        return advice_check

    # 4. Passed all checks
    return {
        "allowed": True,
        "rule": "COMPLIANT",
        "reason": "Query complies with all input policies"
    }
