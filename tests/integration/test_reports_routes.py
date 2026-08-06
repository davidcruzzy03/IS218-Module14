"""Integration tests for calculation report routes."""


def create_calculation(
    client,
    first_operand,
    second_operand,
    calculation_type,
):
    """Create a calculation through the API."""

    response = client.post(
        "/calculations",
        json={
            "a": first_operand,
            "b": second_operand,
            "type": calculation_type,
        },
    )

    assert response.status_code in (200, 201), response.text

    return response.json()


def test_empty_report_summary(client):
    """An authenticated user with no calculations gets an empty report."""

    response = client.get("/reports/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["total_calculations"] == 0
    assert data["average_a"] is None
    assert data["average_b"] is None
    assert data["operation_counts"] == {}
    assert data["most_used_operation"] is None


def test_report_summary_with_calculations(client):
    """Report summary correctly calculates user statistics."""

    create_calculation(
        client=client,
        first_operand=10,
        second_operand=5,
        calculation_type="add",
    )

    create_calculation(
        client=client,
        first_operand=20,
        second_operand=10,
        calculation_type="add",
    )

    create_calculation(
        client=client,
        first_operand=9,
        second_operand=3,
        calculation_type="divide",
    )

    response = client.get("/reports/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["total_calculations"] == 3
    assert data["average_a"] == 13.0
    assert data["average_b"] == 6.0

    assert data["operation_counts"]["addition"] == 2
    assert data["operation_counts"]["division"] == 1

    assert data["most_used_operation"] == "addition"


def test_report_history_returns_user_calculations(client):
    """History returns calculations belonging to the authenticated user."""

    create_calculation(
        client=client,
        first_operand=8,
        second_operand=2,
        calculation_type="divide",
    )

    create_calculation(
        client=client,
        first_operand=4,
        second_operand=2,
        calculation_type="multiply",
    )

    response = client.get("/reports/history")

    assert response.status_code == 200

    history = response.json()

    assert len(history) == 2

    calculation_types = {
        calculation["type"]
        for calculation in history
    }

    assert "division" in calculation_types
    assert "multiplication" in calculation_types


def test_clear_report_history(client):
    """Authenticated users can clear their own history."""

    create_calculation(
        client=client,
        first_operand=100,
        second_operand=20,
        calculation_type="divide",
    )

    create_calculation(
        client=client,
        first_operand=15,
        second_operand=5,
        calculation_type="subtract",
    )

    response = client.delete("/reports/history")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Calculation history cleared"
    assert data["deleted_count"] == 2

    history_response = client.get("/reports/history")

    assert history_response.status_code == 200
    assert history_response.json() == []


def test_clear_empty_history(client):
    """Clearing an empty history returns a zero deletion count."""

    response = client.delete("/reports/history")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Calculation history cleared"
    assert data["deleted_count"] == 0


def test_report_summary_requires_authentication(
    unauthenticated_client,
):
    """Users without authentication cannot view report summaries."""

    response = unauthenticated_client.get("/reports/summary")

    assert response.status_code == 401


def test_report_history_requires_authentication(
    unauthenticated_client,
):
    """Users without authentication cannot view calculation history."""

    response = unauthenticated_client.get("/reports/history")

    assert response.status_code == 401


def test_clear_history_requires_authentication(
    unauthenticated_client,
):
    """Users without authentication cannot delete calculation history."""

    response = unauthenticated_client.delete("/reports/history")

    assert response.status_code == 401