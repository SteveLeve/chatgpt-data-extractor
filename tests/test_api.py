from fastapi.testclient import TestClient
from web.app import app
from web.services import manager
from unittest.mock import MagicMock

client = TestClient(app)

def test_stats():
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "ingestion_status" in data
    assert "ingestion_progress" in data
    assert "agent_initialized" in data

def test_chat_mock():
    # Mock the agent
    mock_agent = MagicMock()
    async def mock_astream_chat(message):
        mock_response = MagicMock()
        async def async_gen():
            yield "Hello"
            yield " World"
        mock_response.async_response_gen = async_gen
        return mock_response
        
    mock_agent.astream_chat = mock_astream_chat
    manager.agent = mock_agent
    
    response = client.post("/api/chat", json={"message": "Hi"})
    assert response.status_code == 200
    assert response.text == "Hello World"

def test_upload_invalid_file():
    response = client.post("/api/upload", files={"file": ("test.txt", b"content", "text/plain")})
    assert response.status_code == 400
    assert response.json()["detail"] == "Only .zip files are allowed"
