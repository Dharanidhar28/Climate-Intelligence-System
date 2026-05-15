import os
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture
def client():
    # Set test flag to disable scheduler
    os.environ["TESTING"] = "true"
    # Patch scheduler to prevent it from starting
    with patch("backend.main.scheduler"):
        test_client = TestClient(app)
        yield test_client
        test_client.close()
    # Clean up
    os.environ.pop("TESTING", None)

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    # 3. Check if the text contains standard HTML markers
    assert "<html" in response.text or "<!DOCTYPE html>" in response.text