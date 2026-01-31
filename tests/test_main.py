"""Comprehensive test suite for smart-qa-portal."""

import pytest
from fastapi.testclient import TestClient
import json

try:
    from src.main import app
except ImportError:
    app = None


class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def setup_method(self):
        """Setup test client."""
        if app:
            self.client = TestClient(app)
    
    @pytest.mark.skipif(app is None, reason="App not available")
    def test_health_check_success(self):
        """Test that health check returns 200 with correct structure."""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert data["healthy"] is True
        assert "timestamp" in data
    
    @pytest.mark.skipif(app is None, reason="App not available")
    def test_health_check_content_type(self):
        """Test that health endpoint returns JSON."""
        response = self.client.get("/health")
        assert "application/json" in response.headers.get("content-type", "")


class TestProcessEndpoint:
    """Tests for the process data endpoint."""
    
    def setup_method(self):
        """Setup test client."""
        if app:
            self.client = TestClient(app)
    
    @pytest.mark.skipif(app is None, reason="App not available")
    def test_process_valid_input(self):
        """Test processing with valid input."""
        response = self.client.post("/process", json={"input_text": "test input"})
        assert response.status_code == 200
        data = response.json()
        assert "output" in data
        assert data["status"] == "success"
        assert "metadata" in data
    
    @pytest.mark.skipif(app is None, reason="App not available")
    def test_process_long_input(self):
        """Test processing with long input."""
        long_text = "a" * 5000
        response = self.client.post("/process", json={"input_text": long_text})
        assert response.status_code == 200
        assert response.json()["status"] == "success"
    
    @pytest.mark.skipif(app is None, reason="App not available")
    def test_process_empty_input(self):
        """Test processing with empty input."""
        response = self.client.post("/process", json={"input_text": ""})
        assert response.status_code == 400
        assert "detail" in response.json()
    
    @pytest.mark.skipif(app is None, reason="App not available")
    def test_process_whitespace_only(self):
        """Test processing with whitespace-only input."""
        response = self.client.post("/process", json={"input_text": "   "})
        assert response.status_code == 400
    
    @pytest.mark.skipif(app is None, reason="App not available")
    def test_process_missing_field(self):
        """Test processing with missing required field."""
        response = self.client.post("/process", json={})
        assert response.status_code == 422
    
    @pytest.mark.skipif(app is None, reason="App not available")
    def test_process_with_options(self):
        """Test processing with optional parameters."""
        response = self.client.post("/process", json={
            "input_text": "test",
            "options": {"key": "value"}
        })
        assert response.status_code == 200
        assert response.json()["metadata"]["options"] is not None


class TestRootEndpoint:
    """Tests for the root endpoint."""
    
    def setup_method(self):
        """Setup test client."""
        if app:
            self.client = TestClient(app)
    
    @pytest.mark.skipif(app is None, reason="App not available")
    def test_root_endpoint(self):
        """Test root endpoint returns API info."""
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "endpoints" in data
        assert data["status"] == "running"


class TestIntegration:
    """Integration tests for the application."""
    
    def setup_method(self):
        """Setup test client."""
        if app:
            self.client = TestClient(app)
    
    @pytest.mark.skipif(app is None, reason="App not available")
    def test_full_workflow(self):
        """Test complete request/response workflow."""
        # Check health
        health = self.client.get("/health")
        assert health.status_code == 200
        
        # Process data
        response = self.client.post("/process", json={"input_text": "integration test"})
        assert response.status_code == 200
        assert response.json()["status"] == "success"
    
    @pytest.mark.skipif(app is None, reason="App not available")
    def test_multiple_sequential_requests(self):
        """Test multiple sequential requests to endpoints."""
        for i in range(3):
            response = self.client.post("/process", json={"input_text": f"request {i}"})
            assert response.status_code == 200
            assert response.json()["status"] == "success"
    
    @pytest.mark.skipif(app is None, reason="App not available")
    def test_error_recovery(self):
        """Test that API recovers after error."""
        # Send invalid request
        response = self.client.post("/process", json={"input_text": ""})
        assert response.status_code == 400
        
        # Send valid request - should still work
        response = self.client.post("/process", json={"input_text": "recovery test"})
        assert response.status_code == 200


@pytest.mark.parametrize("text,expected_status", [
    ("valid input", 200),
    ("", 400),
    ("a" * 100, 200),
])
class TestParametrizedProcessing:
    """Parametrized tests for different inputs."""
    
    def setup_method(self):
        """Setup test client."""
        if app:
            self.client = TestClient(app)
    
    @pytest.mark.skipif(app is None, reason="App not available")
    def test_various_inputs(self, text, expected_status):
        """Test process endpoint with various inputs."""
        if text == "":
            response = self.client.post("/process", json={"input_text": text})
        else:
            response = self.client.post("/process", json={"input_text": text})
        
        assert response.status_code == expected_status
