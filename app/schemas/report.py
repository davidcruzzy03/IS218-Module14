# app/schemas/report.py

from typing import Dict, Optional
from pydantic import BaseModel, Field


class ReportSummary(BaseModel):
    """Summary statistics for a user's calculations."""

    total_calculations: int = Field(ge=0)
    average_a: Optional[float] = None
    average_b: Optional[float] = None
    operation_counts: Dict[str, int]
    most_used_operation: Optional[str] = None


class HistoryDeleteResponse(BaseModel):
    """Response returned after clearing calculation history."""

    message: str
    deleted_count: int = Field(ge=0)