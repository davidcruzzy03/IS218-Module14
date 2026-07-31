"""Unit tests for the calculation factory."""

import pytest

from app.services.calculation_factory import CalculationFactory


@pytest.mark.parametrize(
    "calculation_type,a,b,expected",
    [
        ("Add", 10, 5, 15),
        ("Sub", 10, 5, 5),
        ("Multiply", 10, 5, 50),
        ("Divide", 10, 5, 2),
    ],
)
def test_factory_calculates_supported_operations(
    calculation_type: str,
    a: float,
    b: float,
    expected: float,
) -> None:
    result = CalculationFactory.calculate(
        calculation_type,
        a,
        b,
    )

    assert result == expected


def test_factory_rejects_unknown_operation() -> None:
    with pytest.raises(
        ValueError,
        match="Unsupported calculation type",
    ):
        CalculationFactory.calculate(
            "Power",
            2,
            3,
        )


def test_factory_rejects_division_by_zero() -> None:
    with pytest.raises(
        ValueError,
        match="Cannot divide by zero",
    ):
        CalculationFactory.calculate(
            "Divide",
            10,
            0,
        )