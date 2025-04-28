"""Tests for the JobSpy Docker API."""
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd

def test_health_endpoint(client):
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@patch('app.services.job_service.scrape_jobs')
def test_search_jobs(mock_scrape_jobs, client):
    """Test the search_jobs endpoint."""
    # Setup mock
    mock_df = pd.DataFrame({
        'SITE': ['indeed', 'linkedin'],
        'TITLE': ['Software Engineer', 'Data Scientist'],
        'COMPANY': ['Test Corp', 'Test Inc'],
    })
    mock_scrape_jobs.return_value = mock_df
    
    # Disable auth for testing
    with patch('app.config.settings.ENABLE_API_KEY_AUTH', False):
        response = client.post(
            "/api/v1/search_jobs",
            json={
                "site_name": ["indeed", "linkedin"],
                "search_term": "software engineer",
                "location": "San Francisco",
                "country_indeed": "USA"
            }
        )
    
    # Check response
    assert response.status_code == 200
    assert response.json()["count"] == 2
    assert not response.json()["cached"]
    assert len(response.json()["jobs"]) == 2
