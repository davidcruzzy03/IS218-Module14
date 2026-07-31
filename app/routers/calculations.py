"""FastAPI routes for calculation BREAD operations."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.calculation import Calculation
from app.models.user import User
from app.schemas.calculation import (
    CalculationCreate,
    CalculationRead,
    CalculationUpdate,
)
from app.security import get_current_user
from app.services.calculation_factory import CalculationFactory


router = APIRouter(
    prefix="/calculations",
    tags=["Calculations"],
)


def get_owned_calculation(
    calculation_id: UUID,
    current_user: User,
    db: Session,
) -> Calculation:
    """Return a calculation only when it belongs to the current user."""

    statement = select(Calculation).where(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id,
    )

    calculation = db.scalar(statement)

    if calculation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found.",
        )

    return calculation


@router.get(
    "",
    response_model=list[CalculationRead],
)
def browse_calculations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Calculation]:
    """Return calculations belonging to the logged-in user."""

    statement = (
        select(Calculation)
        .where(Calculation.user_id == current_user.id)
        .order_by(Calculation.id)
    )

    return list(db.scalars(statement).all())


@router.get(
    "/{calculation_id}",
    response_model=CalculationRead,
)
def read_calculation(
    calculation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Calculation:
    """Return one calculation belonging to the logged-in user."""

    return get_owned_calculation(
        calculation_id=calculation_id,
        current_user=current_user,
        db=db,
    )


@router.post(
    "",
    response_model=CalculationRead,
    status_code=status.HTTP_201_CREATED,
)
def add_calculation(
    calculation_data: CalculationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Calculation:
    """Create a calculation for the logged-in user."""

    try:
        result = CalculationFactory.calculate(
            calculation_data.type.value,
            calculation_data.a,
            calculation_data.b,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    calculation = Calculation(
        user_id=current_user.id,
        a=calculation_data.a,
        b=calculation_data.b,
        type=calculation_data.type.value,
        result=result,
    )

    db.add(calculation)
    db.commit()
    db.refresh(calculation)

    return calculation


@router.put(
    "/{calculation_id}",
    response_model=CalculationRead,
)
def edit_calculation(
    calculation_id: UUID,
    calculation_data: CalculationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Calculation:
    """Update a calculation belonging to the logged-in user."""

    calculation = get_owned_calculation(
        calculation_id=calculation_id,
        current_user=current_user,
        db=db,
    )

    try:
        result = CalculationFactory.calculate(
            calculation_data.type.value,
            calculation_data.a,
            calculation_data.b,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    calculation.a = calculation_data.a
    calculation.b = calculation_data.b
    calculation.type = calculation_data.type.value
    calculation.result = result

    db.commit()
    db.refresh(calculation)

    return calculation


@router.delete(
    "/{calculation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_calculation(
    calculation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    """Delete a calculation belonging to the logged-in user."""

    calculation = get_owned_calculation(
        calculation_id=calculation_id,
        current_user=current_user,
        db=db,
    )

    db.delete(calculation)
    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )