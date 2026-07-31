# tests/integration/test_calculation_routes.py


def create_calculation(client):
    return client.post(
        "/calculations",
        json={
            "a": 10,
            "b": 5,
            "type": "addition",
        },
    )


def test_create_calculation(client):
    response = create_calculation(client)

    assert response.status_code == 201

    data = response.json()

    assert data["a"] == 10
    assert data["b"] == 5
    assert data["type"] == "addition"
    assert data["result"] == 15


def test_browse_calculations(client):
    create_calculation(client)

    response = client.get("/calculations")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_read_calculation(client):
    create_response = create_calculation(client)
    calculation_id = create_response.json()["id"]

    response = client.get(
        f"/calculations/{calculation_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == calculation_id


def test_update_calculation(client):
    create_response = create_calculation(client)
    calculation_id = create_response.json()["id"]

    response = client.put(
        f"/calculations/{calculation_id}",
        json={
            "a": 20,
            "b": 4,
            "type": "division",
        },
    )

    assert response.status_code == 200
    assert response.json()["result"] == 5


def test_delete_calculation(client):
    create_response = create_calculation(client)
    calculation_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/calculations/{calculation_id}"
    )

    read_response = client.get(
        f"/calculations/{calculation_id}"
    )

    assert delete_response.status_code == 204
    assert read_response.status_code == 404


def test_division_by_zero(client):
    response = client.post(
        "/calculations",
        json={
            "a": 10,
            "b": 0,
            "type": "division",
        },
    )

    assert response.status_code == 400
    assert "divide by zero" in response.json()["detail"].lower()


def test_invalid_calculation_type(client):
    response = client.post(
        "/calculations",
        json={
            "a": 10,
            "b": 5,
            "type": "square-root-of-everything",
        },
    )

    assert response.status_code == 422


def test_missing_calculation(client):
    response = client.get(
        "/calculations/00000000-0000-0000-0000-000000000001"
    )

    assert response.status_code == 404