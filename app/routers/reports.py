# app/routers/reports.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.calculation import Calculation
from app.models.user import User
from app.schemas.calculation import CalculationRead
from app.schemas.report import HistoryDeleteResponse, ReportSummary
from app.services.report_service import build_report_summary
from app.security import get_current_user


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get(
    "/history",
    response_model=list[CalculationRead],
)
def get_calculation_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return calculations belonging only to the current user."""

    return (
        db.query(Calculation)
        .filter(Calculation.user_id == current_user.id)
        .order_by(Calculation.id.desc())
        .all()
    )


@router.get(
    "/summary",
    response_model=ReportSummary,
)
def get_calculation_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return statistical information for the current user's history."""

    calculations = (
        db.query(Calculation)
        .filter(Calculation.user_id == current_user.id)
        .all()
    )

    return build_report_summary(calculations)


@router.delete(
    "/history",
    response_model=HistoryDeleteResponse,
    status_code=status.HTTP_200_OK,
)
def clear_calculation_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete only the current user's calculations."""

    deleted_count = (
        db.query(Calculation)
        .filter(Calculation.user_id == current_user.id)
        .delete(synchronize_session=False)
    )

    db.commit()

    return {
        "message": "Calculation history cleared",
        "deleted_count": deleted_count,
    }