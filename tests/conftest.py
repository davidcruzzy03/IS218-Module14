"""Shared pytest fixtures for database and API integration tests."""

import os
import uuid

os.environ["TESTING"] = "true"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.models.calculation import Calculation  # noqa: F401
from app.models.user import User
from app.security import get_current_user, hash_password
from main import app


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/calculator_test_db",
)


@pytest.fixture(scope="session")
def engine():
    """Create the SQLAlchemy test engine."""

    test_engine = create_engine(TEST_DATABASE_URL)

    Base.metadata.create_all(bind=test_engine)

    yield test_engine

    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture()
def db_session(engine):
    """Provide an isolated database session for each test."""

    connection = engine.connect()
    transaction = connection.begin()

    testing_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
    )

    session = testing_session()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def test_user(db_session):
    """Create a database user for calculation tests."""

    unique_value = uuid.uuid4().hex[:8]

    user = User(
        email=f"test-{unique_value}@example.com",
        username=f"testuser-{unique_value}",
        password_hash=hash_password("SecurePassword123"),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture()
def client(db_session, test_user):
    """Provide an authenticated FastAPI test client."""

    def override_get_db():
        """Use the current test database session."""
        yield db_session

    def override_get_current_user():
        """Treat the fixture user as authenticated."""
        return test_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()