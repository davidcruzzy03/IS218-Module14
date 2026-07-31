"""
SQLAlchemy model for arithmetic calculations.
"""

import uuid

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Calculation(Base):
    """
    Store an arithmetic calculation in the database.
    """

    __tablename__ = "calculations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    a: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    b: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    result: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="calculations",
    )

    def __repr__(self) -> str:
        return (
            f"<Calculation("
            f"id={self.id}, "
            f"type={self.type}, "
            f"a={self.a}, "
            f"b={self.b}, "
            f"result={self.result})>"
        )