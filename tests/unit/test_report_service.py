# tests/unit/test_report_service.py

from types import SimpleNamespace

from app.services.report_service import build_report_summary


def make_calculation(a, b, operation):
    """Create a simple calculation object for unit testing."""

    return SimpleNamespace(
        a=a,
        b=b,
        type=operation,
    )


def test_build_report_summary_with_calculations():
    """Summary should calculate totals, averages, and operation counts."""

    calculations = [
        make_calculation(10, 5, "add"),
        make_calculation(20, 10, "add"),
        make_calculation(6, 2, "divide"),
    ]

    result = build_report_summary(calculations)

    assert result["total_calculations"] == 3
    assert result["average_a"] == 12.0
    assert result["average_b"] == 5.67

    assert result["operation_counts"]["addition"] == 2
    assert result["operation_counts"]["division"] == 1

    assert result["most_used_operation"] == "addition"


def test_build_report_summary_with_no_calculations():
    """An empty list should return safe default values."""

    result = build_report_summary([])

    assert result["total_calculations"] == 0
    assert result["average_a"] is None
    assert result["average_b"] is None
    assert result["operation_counts"] == {}
    assert result["most_used_operation"] is None


def test_report_summary_rounds_averages():
    """Operand averages should be rounded to two decimal places."""

    calculations = [
        make_calculation(10, 1, "add"),
        make_calculation(11, 2, "subtract"),
        make_calculation(12, 2, "multiply"),
    ]

    result = build_report_summary(calculations)

    assert result["average_a"] == 11.0
    assert result["average_b"] == 1.67


def test_report_summary_normalizes_operation_names():
    """Different operation forms should use consistent report names."""

    calculations = [
        make_calculation(10, 2, "add"),
        make_calculation(10, 2, "addition"),
        make_calculation(10, 2, "subtract"),
        make_calculation(10, 2, "multiply"),
        make_calculation(10, 2, "divide"),
    ]

    result = build_report_summary(calculations)

    assert result["operation_counts"] == {
        "addition": 2,
        "subtraction": 1,
        "multiplication": 1,
        "division": 1,
    }


def test_report_summary_handles_enum_style_strings():
    """Enum-style strings should be converted to normal operation names."""

    calculations = [
        make_calculation(10, 5, "CalculationType.ADDITION"),
        make_calculation(10, 5, "CalculationType.DIVISION"),
    ]

    result = build_report_summary(calculations)

    assert result["operation_counts"]["addition"] == 1
    assert result["operation_counts"]["division"] == 1