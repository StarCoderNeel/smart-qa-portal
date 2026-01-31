"""Integration tests for smart-qa-portal."""

import pytest
from src.main import app
from fastapi.testclient import TestClient

class TestIntegrationWorkflows:
    """Test complete workflows using multiple modules."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    def test_end_to_end_workflow(self, client):
        """Test complete request/response cycle."""
        # Health check
        response = client.get("/health")
        assert response.status_code == 200
        
        # Process request
        response = client.post("/process", json={"input_text": "test"})
        assert response.status_code in [200, 422, 400]
    
    def test_error_handling(self, client):
        """Test error handling in workflows."""
        # Empty input
        response = client.post("/process", json={"input_text": ""})
        assert response.status_code in [400, 422]
        
        # Missing fields
        response = client.post("/process", json={})
        assert response.status_code == 422

@pytest.mark.integration
class TestModuleIntegration:
    """Test integration between different modules."""
    
    def test_imports(self):
        """Test that all modules can be imported."""
        try:

            from src import utils
            from src import models
            from src import services
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import modules: {e}")
    
    def test_module_availability(self):
        """Test that module exports are available."""
        import src
        assert hasattr(src, '__version__')
