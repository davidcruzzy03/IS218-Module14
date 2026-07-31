"""Integration tests for the Calculation SQLAlchemy model."""

from app.models.calculation import Calculation
from app.services.calculation_factory import CalculationFactory


def test_store_and_retrieve_calculation(
    db_session,
    test_user,
) -> None:
    result = CalculationFactory.calculate(
        "Multiply",
        6,
        7,
    )

    calculation = Calculation(
        user_id=test_user.id,
        a=6,
        b=7,
        type="Multiply",
        result=result,
    )

    db_session.add(calculation)
    db_session.commit()
    db_session.refresh(calculation)

    saved = (
        db_session.query(Calculation)
        .filter(Calculation.id == calculation.id)
        .first()
    )

    assert saved is not None
    assert saved.user_id == test_user.id
    assert saved.a == 6
    assert saved.b == 7
    assert saved.type == "Multiply"
    assert saved.result == 42

def test_delete_calculation(
    db_session,
    test_user,
) -> None:
    calculation = Calculation(
        user_id=test_user.id,
        a=10,
        b=2,
        type="Divide",
        result=5,
    )

    db_session.add(calculation)
    db_session.commit()

    calculation_id = calculation.id

    db_session.delete(calculation)
    db_session.commit()

    deleted = (
        db_session.query(Calculation)
        .filter(Calculation.id == calculation_id)
        .first()
    )

    assert deleted is None