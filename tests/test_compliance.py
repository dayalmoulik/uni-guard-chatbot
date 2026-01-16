import pytest

from compliance.input_filter import check_input_compliance
from compliance.output_filter import check_output_compliance


# -------------------------
# INPUT FILTER TESTS
# -------------------------

def test_allowed_general_queries():
    allowed_queries = [
        "What is C-CAT?",
        "What are the PG certificate programmes?",
        "How does counselling work?",
        "What is the fee for PGCP-AI?",
        "What is the mode of delivery for PGCP-AC?"
    ]

    for q in allowed_queries:
        allowed, _ = check_input_compliance(q)
        assert allowed is True


def test_block_prediction_queries():
    blocked_queries = [
        "Will I get admission with 500 rank?",
        "Can I get PGCP-AI with my marks?",
        "What are my chances of admission?",
        "Am I eligible for PGCP-AC?"
    ]

    for q in blocked_queries:
        allowed, msg = check_input_compliance(q)
        assert allowed is False
        assert "cannot predict" in msg.lower() or "cannot evaluate" in msg.lower()


def test_block_course_advice():
    blocked_queries = [
        "Which course should I choose?",
        "What is the best course for me?",
        "Recommend a course based on my profile"
    ]

    for q in blocked_queries:
        allowed, msg = check_input_compliance(q)
        assert allowed is False
        assert "cannot recommend" in msg.lower()


def test_block_personal_identifiers():
    blocked_queries = [
        "My email is test@example.com",
        "My phone number is 9876543210",
        "My form number is 123456"
    ]

    for q in blocked_queries:
        allowed, msg = check_input_compliance(q)
        assert allowed is False
        assert "cannot" in msg.lower()


def test_block_impersonation_requests():
    blocked_queries = [
        "Please approve my admission",
        "Can you allocate my seat?",
        "Confirm my centre allocation"
    ]

    for q in blocked_queries:
        allowed, msg = check_input_compliance(q)
        assert allowed is False
        assert "cannot perform" in msg.lower()


# -------------------------
# OUTPUT FILTER TESTS
# -------------------------

def test_allowed_safe_output():
    safe_output = (
        "Admissions are conducted through C-CAT followed by counselling "
        "based on rank and seat availability."
    )

    filtered = check_output_compliance(safe_output)
    assert filtered == safe_output


def test_block_prediction_output():
    unsafe_outputs = [
        "You will get admission easily.",
        "You have a high chance of selection.",
        "You are eligible for PGCP-AI."
    ]

    for out in unsafe_outputs:
        filtered = check_output_compliance(out)
        assert "cannot provide predictions" in filtered.lower()


def test_block_guarantees():
    unsafe_outputs = [
        "This guarantees your admission.",
        "You will definitely get selected."
    ]

    for out in unsafe_outputs:
        filtered = check_output_compliance(out)
        assert "cannot provide predictions" in filtered.lower()


def test_block_authority_impersonation():
    unsafe_outputs = [
        "We will allocate your seat.",
        "Your admission is approved."
    ]

    for out in unsafe_outputs:
        filtered = check_output_compliance(out)
        assert "cannot provide predictions" in filtered.lower()


def test_block_personal_rank_output():
    unsafe_outputs = [
        "With rank 450 you will get PGCP-AI.",
        "Scoring 85% ensures admission."
    ]

    for out in unsafe_outputs:
        filtered = check_output_compliance(out)
        assert "cannot provide predictions" in filtered.lower()
