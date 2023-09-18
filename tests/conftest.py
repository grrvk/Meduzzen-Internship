import pytest

from typing import Generator
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def test_client() -> Generator:
    yield TestClient(app)

    # after test running, analogue tear down
