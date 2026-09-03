"""
Basic API tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "DeepResearch Agent API"
    assert data["status"] == "running"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_config_endpoint():
    """Test config endpoint"""
    response = client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    assert "llm_provider" in data
    assert "max_research_iterations" in data


def test_start_research():
    """Test starting a research session"""
    payload = {
        "query": "What is artificial intelligence?",
        "research_depth": "standard"
    }
    response = client.post("/api/research/start", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["status"] == "pending"


def test_get_research_session():
    """Test getting research session details"""
    # First create a session
    payload = {
        "query": "Test query",
        "research_depth": "quick"
    }
    create_response = client.post("/api/research/start", json=payload)
    session_id = create_response.json()["session_id"]
    
    # Then get the session
    response = client.get(f"/api/research/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == session_id
    assert data["user_query"] == "Test query"


def test_invalid_session():
    """Test getting a non-existent session"""
    response = client.get("/api/research/invalid-session-id")
    assert response.status_code == 404
