# tests/e2e/test_e2e.py

"""End-to-end tests for authenticated calculation workflows."""

import uuid

import pytest
from playwright.sync_api import Page, expect


BASE_URL = "http://localhost:8000"


def register_and_login(page: Page) -> None:
    """Register and log in a unique user."""

    unique_value = uuid.uuid4().hex[:8]
    username = f"user{unique_value}"
    email = f"user{unique_value}@example.com"
    password = "SecurePassword123"

    page.goto(f"{BASE_URL}/register")

    page.locator("#username").fill(username)
    page.locator("#email").fill(email)
    page.locator("#password").fill(password)
    page.locator("#confirm-password").fill(password)
    page.locator("#register-button").click()

    expect(page.locator("#register-message")).to_contain_text(
        "Registration successful"
    )

    page.goto(f"{BASE_URL}/login")

    page.locator("#username").fill(username)
    page.locator("#password").fill(password)
    page.locator("#login-button").click()

    page.wait_for_url(f"{BASE_URL}/")

    token = page.evaluate(
        "() => window.localStorage.getItem('access_token')"
    )

    assert token is not None
    assert len(token) > 20


@pytest.mark.e2e
def test_authenticated_homepage(page: Page, fastapi_server):
    """Verify the calculation page loads after authentication."""

    register_and_login(page)

    expect(page).to_have_url(f"{BASE_URL}/")
    expect(page.locator("h1")).to_contain_text("Calculation")


@pytest.mark.e2e
def test_calculator_add(page: Page, fastapi_server):
    """Verify a logged-in user can create an addition calculation."""

    register_and_login(page)

    page.locator("#number-a").fill("10")
    page.locator("#number-b").fill("5")
    page.locator("#calculation-type").select_option("Add")
    page.locator("#submit-button").click()

    expect(page.locator("#calculation-message")).to_contain_text(
        "success"
    )

    expect(
        page.locator("#calculations-table-body")
    ).to_contain_text("15")


@pytest.mark.e2e
def test_calculator_divide_by_zero(page: Page, fastapi_server):
    """Verify division by zero displays an error."""

    register_and_login(page)

    page.locator("#number-a").fill("10")
    page.locator("#number-b").fill("0")
    page.locator("#calculation-type").select_option("Divide")
    page.locator("#submit-button").click()

    expect(page.locator("#calculation-message")).to_contain_text(
        "divide by zero"
    )