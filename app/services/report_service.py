"""Service functions for calculation reports."""

from collections import Counter
from typing import Iterable

from app.models.calculation import Calculation


def get_operation_name(calculation: Calculation) -> str:
    """
    Return a normalized operation name regardless of how the
    operation is stored (enum, string, etc.).
    """

    operation = calculation.type

    # Handle Enum values
    if hasattr(operation, "value"):
        operation = operation.value

    operation_name = str(operation).lower()

    # Handle values like "CalculationType.ADDITION"
    if "." in operation_name:
        operation_name = operation_name.split(".")[-1]

    # Normalize names
    mapping = {
        "add": "addition",
        "addition": "addition",

        "subtract": "subtraction",
        "subtraction": "subtraction",

        "multiply": "multiplication",
        "multiplication": "multiplication",

        "divide": "division",
        "division": "division",
    }

    return mapping.get(operation_name, operation_name)


def build_report_summary(
    calculations: Iterable[Calculation],
):
    """
    Build summary statistics for a user's calculations.
    """

    calculations = list(calculations)

    total = len(calculations)

    if total == 0:
        return {
            "total_calculations": 0,
            "average_a": None,
            "average_b": None,
            "operation_counts": {},
            "most_used_operation": None,
        }

    operation_counts = Counter(
        get_operation_name(calculation)
        for calculation in calculations
    )

    average_a = round(
        sum(float(c.a) for c in calculations) / total,
        2,
    )

    average_b = round(
        sum(float(c.b) for c in calculations) / total,
        2,
    )

    return {
        "total_calculations": total,
        "average_a": average_a,
        "average_b": average_b,
        "operation_counts": dict(operation_counts),
        "most_used_operation": operation_counts.most_common(1)[0][0],
    }