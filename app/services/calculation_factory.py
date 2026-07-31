"""Factory for performing supported arithmetic calculations."""

from typing import Callable


class CalculationFactory:
    """Select and execute arithmetic operations by name."""

    _operations: dict[str, Callable[[float, float], float]] = {
        "Add": lambda a, b: a + b,
        "Sub": lambda a, b: a - b,
        "Multiply": lambda a, b: a * b,
    }

    @classmethod
    def calculate(
        cls,
        calculation_type: str,
        a: float,
        b: float,
    ) -> float:
        """Calculate a result using the requested operation."""

        if calculation_type == "Divide":
            if b == 0:
                raise ValueError("Cannot divide by zero.")
            return a / b

        operation = cls._operations.get(calculation_type)

        if operation is None:
            raise ValueError(
                f"Unsupported calculation type: {calculation_type}"
            )

        return operation(a, b)