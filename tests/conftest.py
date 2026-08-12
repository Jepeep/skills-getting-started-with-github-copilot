import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture()
def client():
    """Provide a TestClient and restore in-memory `activities` after each test."""
    backup = copy.deepcopy(activities)
    with TestClient(app) as c:
        yield c
    activities.clear()
    activities.update(backup)
