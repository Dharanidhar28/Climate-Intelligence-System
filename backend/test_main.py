from fastapi.testclient import TestClient
from backend.main import app # assuming your FastAPI file is named main.py

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    
    # 3. Check if the text contains standard HTML markers
    assert "<html" in response.text or "<!DOCTYPE html>" in response.text