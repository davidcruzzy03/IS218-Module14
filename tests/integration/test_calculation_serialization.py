"""Integration test for serializing a Calculation model."""

from app.models.calculation import Calculation
from app.schemas.calculation import CalculationRead


def test_calculation_read_serializes_model(
    db_session,
    test_user,
) -> None:
    calculation = Calculation(
        user_id=test_user.id,
        a=8,
        b=4,
        type="Divide",
        result=2,
    )

    db_session.add(calculation)
    db_session.commit()
    db_session.refresh(calculation)

    response = CalculationRead.model_validate(calculation)

    assert response.id == calculation.id
    assert response.user_id == test_user.id
    assert response.a == 8
    assert response.b == 4
    assert response.type.value == "Divide"
    assert response.result == 2