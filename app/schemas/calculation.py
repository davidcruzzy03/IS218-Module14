"""Pydantic schemas for calculation validation and serialization."""

from enum import Enum
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    field_serializer,
    field_validator,
    model_validator,
)


class CalculationType(str, Enum):
    """Supported arithmetic calculation types."""

    ADD = "Add"
    SUB = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"


def normalize_type_value(value):
    """Convert common operation names into CalculationType values."""

    if isinstance(value, str):
        normalized_types = {
            "add": "Add",
            "addition": "Add",
            "sub": "Sub",
            "subtract": "Sub",
            "subtraction": "Sub",
            "multiply": "Multiply",
            "multiplication": "Multiply",
            "divide": "Divide",
            "division": "Divide",
        }

        return normalized_types.get(
            value.strip().lower(),
            value,
        )

    return value


class CalculationCreate(BaseModel):
    """Validate data used to create a calculation."""

    a: float
    b: float
    type: CalculationType

    @field_validator("type", mode="before")
    @classmethod
    def normalize_calculation_type(cls, value):
        """Normalize incoming calculation type values."""

        return normalize_type_value(value)

    @model_validator(mode="after")
    def validate_operands(self) -> "CalculationCreate":
        """Reject division when the second operand is zero."""

        if (
            self.type == CalculationType.DIVIDE
            and self.b == 0
        ):
            raise ValueError("Cannot divide by zero.")

        return self


class CalculationUpdate(BaseModel):
    """Validate data used to update a calculation."""

    a: float
    b: float
    type: CalculationType

    @field_validator("type", mode="before")
    @classmethod
    def normalize_calculation_type(cls, value):
        """Normalize incoming calculation type values."""

        return normalize_type_value(value)

    @model_validator(mode="after")
    def validate_operands(self) -> "CalculationUpdate":
        """Reject division when the second operand is zero."""

        if (
            self.type == CalculationType.DIVIDE
            and self.b == 0
        ):
            raise ValueError("Cannot divide by zero.")

        return self


class CalculationRead(BaseModel):
    """Serialize a saved calculation."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    a: float
    b: float
    type: CalculationType
    result: float

    @field_serializer("type")
    def serialize_calculation_type(
        self,
        calculation_type: CalculationType,
    ) -> str:
        """Return descriptive lowercase operation names in API JSON."""

        response_names = {
            CalculationType.ADD: "addition",
            CalculationType.SUB: "subtraction",
            CalculationType.MULTIPLY: "multiplication",
            CalculationType.DIVIDE: "division",
        }

        return response_names[calculation_type]