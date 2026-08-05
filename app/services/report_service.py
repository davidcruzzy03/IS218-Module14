# app/services/report_service.py

from collections import Counter
from typing import Iterable, Optional

from app.models.calculation import Calculation


def build_report_summary(
    calculations: Iterable[Calculation],
) -> dict:
    """
    Build summary statistics from a user's calculations.

    Returns safe defaults when the user has no calculations.
    """

    calculation_list = list(calculations)
    total = len(calculation_list)

    if total == 0:
        return {
            "total_calculations": 0,
            "average_a": None,
            "average_b": None,
            "operation_counts": {},
            "most_used_operation": None,
        }

    operation_counts = Counter(
        str(calculation.type.value)
        if hasattr(calculation.type, "value")
        else str(calculation.type)
        for calculation in calculation_list
    )

    average_a = sum(float(item.a) for item in calculation_list) / total
    average_b = sum(float(item.b) for item in calculation_list) / total

    most_used_operation: Optional[str] = operation_counts.most_common(1)[0][0]

    return {
        "total_calculations": total,
        "average_a": round(average_a, 2),
        "average_b": round(average_b, 2),
        "operation_counts": dict(operation_counts),
        "most_used_operation": most_used_operation,
    }