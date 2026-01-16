"""
Output Compliance Filter

This module validates LLM-generated responses BEFORE they are shown to the user.
It ensures that the chatbot does not leak private data, give advice, or violate
academic and privacy policies.
"""

import re
from typing import Tuple

# -------------------------
# Unsafe output patterns
# -------------------------

GUARANTEE_PATTERN = re.compile(
    r"\b(guarantee|sure\s+shot|definitely\s+get|confirmed\s+admission)\b",
    re.I
)

PREDICTION_PATTERN = re.compile(
    r"\b(you\s+will\s+get|you\s+are\s+eligible|high\s+chance|likely\s+to\s+get)\b",
    re.I
)

AUTHORITY_PATTERN = re.compile(
    r"\b(we\s+will\s+allocate|your\s+seat\s+is|approved\s+by)\b",
    re.I
)

PERSONAL_DATA_PATTERN = re.compile(
    r"\b(rank\s+\d+|\d+\s+marks|\d+%)\b",
    re.I
)

SHORT_CONFIRMATION_PATTERN = re.compile(
    r"^(yes|yeah|yep|sure)$",
    re.I
)

ELIGIBILITY_LANGUAGE_PATTERN = re.compile(
    r"\b(enough|eligible|chance|likely|sure\s+shot)\b",
    re.I
)

# -------------------------
# Main filter
# -------------------------

def check_output_compliance(model_output: str) -> Tuple[bool, str]:
    """
    Returns:
    - Safe output if compliant
    - Policy refusal message if non-compliant
    """

    if (
        GUARANTEE_PATTERN.search(model_output)
        or PREDICTION_PATTERN.search(model_output)
        or AUTHORITY_PATTERN.search(model_output)
        or PERSONAL_DATA_PATTERN.search(model_output)
        or SHORT_CONFIRMATION_PATTERN.match(model_output.strip())
        or ELIGIBILITY_LANGUAGE_PATTERN.search(model_output)
    ):
        return (
            False,
            "I’m sorry, but I cannot provide predictions, guarantees, or personal admission outcomes. "
            "Admission decisions are made through the official counselling process."
        )

    return (True, model_output)

