"""Unit tests for calculation Pydantic schemas."""

import pytest
from pydantic import ValidationError

from app.schemas.calculation import (
    CalculationCreate,
    CalculationType,
)


@pytest.mark.parametrize(
    "calculation_type",
    [
        "Add",
        "Sub",
        "Multiply",
        "Divide",
    ],
)
def test_calculation_create_accepts_supported_types(
    calculation_type: str,
) -> None:
    schema = CalculationCreate(
        a=10,
        b=5,
        type=calculation_type,
    )

    assert schema.a == 10
    assert schema.b == 5
    assert schema.type.value == calculation_type


def test_calculation_create_rejects_unknown_type() -> None:
    with pytest.raises(ValidationError):
        CalculationCreate(
            a=10,
            b=5,
            type="Power",
        )


def test_calculation_create_rejects_zero_divisor() -> None:
    with pytest.raises(
        ValidationError,
        match="Cannot divide by zero",
    ):
        CalculationCreate(
            a=10,
            b=0,
            type=CalculationType.DIVIDE,
        )


def test_calculation_create_rejects_non_numeric_a() -> None:
    with pytest.raises(ValidationError):
        CalculationCreate(
            a="hello",
            b=5,
            type="Add",
        )


def test_calculation_create_rejects_non_numeric_b() -> None:
    with pytest.raises(ValidationError):
        CalculationCreate(
            a=10,
            b="hello",
            type="Add",
        )