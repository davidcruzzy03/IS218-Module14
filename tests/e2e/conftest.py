"""Fixtures for Playwright end-to-end tests."""

import os
import subprocess
import sys
import time
from collections.abc import Generator
from urllib.error import URLError
from urllib.request import urlopen

import pytest
from sqlalchemy import create_engine

from app.database import Base
from app.models.calculation import Calculation  # noqa: F401
from app.models.user import User  # noqa: F401


BASE_URL = "http://127.0.0.1:8000"

E2E_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/"
    "calculator_test_db",
)


@pytest.fixture(scope="session")
def fastapi_server() -> Generator[None, None, None]:
    """Start FastAPI with the host-accessible test database."""

    test_engine = create_engine(E2E_DATABASE_URL)
    Base.metadata.create_all(bind=test_engine)

    server_environment = os.environ.copy()
    server_environment["DATABASE_URL"] = E2E_DATABASE_URL
    server_environment["TEST_DATABASE_URL"] = E2E_DATABASE_URL
    server_environment["TESTING"] = "false"

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        env=server_environment,
    )

    try:
        for _ in range(30):
            try:
                with urlopen(
                    f"{BASE_URL}/health",
                    timeout=1,
                ) as response:
                    if response.status == 200:
                        break
            except (URLError, ConnectionError):
                time.sleep(1)
        else:
            raise RuntimeError(
                "FastAPI server did not start within 30 seconds."
            )

        yield

    finally:
        process.terminate()

        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)

        test_engine.dispose()