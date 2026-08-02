"""End-to-end tests for user registration and login."""

import uuid

from playwright.sync_api import Page, expect


BASE_URL = "http://localhost:8000"


def test_successful_registration(page: Page):
    """Verify a user can register successfully."""

    unique_value = uuid.uuid4().hex[:8]

    page.goto(f"{BASE_URL}/register")

    page.locator("#username").fill(f"user{unique_value}")
    page.locator("#email").fill(f"user{unique_value}@example.com")
    page.locator("#password").fill("SecurePassword123")
    page.locator("#confirm-password").fill("SecurePassword123")
    page.locator("#register-button").click()

    expect(page.locator("#register-message")).to_contain_text(
        "Registration successful"
    )


def test_registration_rejects_short_password(page: Page):
    """Verify client-side validation rejects a short password."""

    unique_value = uuid.uuid4().hex[:8]

    page.goto(f"{BASE_URL}/register")

    page.locator("#username").fill(f"user{unique_value}")
    page.locator("#email").fill(f"user{unique_value}@example.com")
    page.locator("#password").fill("short")
    page.locator("#confirm-password").fill("short")
    page.locator("#register-button").click()

    expect(page.locator("#register-message")).to_contain_text(
        "Password must contain at least 8 characters"
    )


def test_successful_login_stores_token(page: Page):
    """Verify successful login stores a JWT and redirects home."""

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

    # Successful login redirects to the authenticated homepage.
    page.wait_for_url(f"{BASE_URL}/")

    token = page.evaluate(
        "() => window.localStorage.getItem('access_token')"
    )

    assert token is not None
    assert len(token) > 20


def test_login_rejects_wrong_password(page: Page):
    """Verify an incorrect password does not authenticate the user."""

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

    # Clear any token that might remain from another browser action.
    page.evaluate(
        "() => window.localStorage.removeItem('access_token')"
    )

    page.locator("#username").fill(username)
    page.locator("#password").fill("IncorrectPassword123")
    page.locator("#login-button").click()

    # Failed login should remain on the login page.
    expect(page).to_have_url(f"{BASE_URL}/login")

    expect(page.locator("#login-message")).to_contain_text(
        "Invalid username or password"
    )

    token = page.evaluate(
        "() => window.localStorage.getItem('access_token')"
    )

    assert token is None