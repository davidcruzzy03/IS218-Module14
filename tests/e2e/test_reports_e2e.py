"""End-to-end tests for the calculation report dashboard."""

import uuid

import pytest
from playwright.sync_api import expect


BASE_URL = "http://localhost:8000"


def register_and_login_user(page):
    """Register a user through the API and return its JWT token."""

    unique_value = uuid.uuid4().hex[:8]

    username = f"reportuser-{unique_value}"
    email = f"report-{unique_value}@example.com"
    password = "SecurePassword123"

    register_response = page.request.post(
        f"{BASE_URL}/users/register",
        data={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    assert register_response.status in (200, 201), (
        register_response.text()
    )

    login_response = page.request.post(
        f"{BASE_URL}/users/login",
        data={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status == 200, (
        login_response.text()
    )

    login_data = login_response.json()

    return login_data["access_token"]


def create_calculation(page, token, a, b, operation):
    """Create an authenticated calculation through the API."""

    response = page.request.post(
        f"{BASE_URL}/calculations",
        headers={
            "Authorization": f"Bearer {token}",
        },
        data={
            "a": a,
            "b": b,
            "type": operation,
        },
    )

    assert response.status in (200, 201), response.text()


@pytest.mark.e2e
def test_authenticated_user_can_view_report_dashboard(
    page,
    fastapi_server,
):
    """An authenticated user can view report statistics and history."""

    token = register_and_login_user(page)

    create_calculation(
        page=page,
        token=token,
        a=10,
        b=5,
        operation="add",
    )

    create_calculation(
        page=page,
        token=token,
        a=20,
        b=10,
        operation="add",
    )

    page.goto(BASE_URL)

    page.evaluate(
        """
        (token) => {
            localStorage.setItem("access_token", token);
        }
        """,
        token,
    )

    page.goto(f"{BASE_URL}/dashboard")

    expect(
        page.locator("#total-calculations")
    ).to_have_text("2")

    expect(
        page.locator("#average-a")
    ).to_have_text("15")

    expect(
        page.locator("#average-b")
    ).to_have_text("7.5")

    expect(
        page.locator("#most-used-operation")
    ).to_have_text("Addition")

    expect(
        page.locator("#history-table-body tr")
    ).to_have_count(2)


@pytest.mark.e2e
def test_user_can_filter_report_history(
    page,
    fastapi_server,
):
    """The operation filter displays only matching calculations."""

    token = register_and_login_user(page)

    create_calculation(
        page=page,
        token=token,
        a=10,
        b=5,
        operation="add",
    )

    create_calculation(
        page=page,
        token=token,
        a=10,
        b=2,
        operation="divide",
    )

    page.goto(BASE_URL)

    page.evaluate(
        """
        (token) => {
            localStorage.setItem("access_token", token);
        }
        """,
        token,
    )

    page.goto(f"{BASE_URL}/dashboard")

    expect(
        page.locator("#history-table-body tr")
    ).to_have_count(2)

    page.select_option(
        "#operation-filter",
        "division",
    )

    expect(
        page.locator("#history-table-body tr")
    ).to_have_count(1)

    expect(
        page.locator("#history-table-body")
    ).to_contain_text("Division")


@pytest.mark.e2e
def test_user_can_clear_report_history(
    page,
    fastapi_server,
):
    """An authenticated user can clear calculation history."""

    token = register_and_login_user(page)

    create_calculation(
        page=page,
        token=token,
        a=8,
        b=4,
        operation="divide",
    )

    page.goto(BASE_URL)

    page.evaluate(
        """
        (token) => {
            localStorage.setItem("access_token", token);
        }
        """,
        token,
    )

    page.goto(f"{BASE_URL}/dashboard")

    expect(
        page.locator("#total-calculations")
    ).to_have_text("1")

    page.on(
        "dialog",
        lambda dialog: dialog.accept(),
    )

    page.click("#clear-history-button")

    expect(
        page.locator("#report-message")
    ).to_contain_text(
        "Calculation history cleared"
    )

    expect(
        page.locator("#total-calculations")
    ).to_have_text("0")

    expect(
        page.locator("#history-table-body")
    ).to_contain_text(
        "No calculations found"
    )


@pytest.mark.e2e
def test_report_dashboard_redirects_unauthenticated_user(
    page,
    fastapi_server,
):
    """A user without a JWT is redirected to the login page."""

    page.goto(f"{BASE_URL}/dashboard")

    page.wait_for_url("**/login")

    expect(page).to_have_url(
        f"{BASE_URL}/login"
    )