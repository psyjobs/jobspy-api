"""Pytest configuration for JobSpy Docker API tests."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Get a TestClient instance for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client
