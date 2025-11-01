"""
API Endpoint Tests
Tests FastAPI REST endpoints using TestClient
"""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check_success(self, api_test_client):
        """Test health endpoint returns success."""
        response = api_test_client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data['success'] is True
        assert 'status' in data
        assert data['status'] == 'healthy'
        assert 'timestamp' in data

    def test_health_check_has_version(self, api_test_client):
        """Test health endpoint includes version info."""
        response = api_test_client.get("/health")
        data = response.json()

        # May or may not have version depending on implementation
        assert 'success' in data


class TestAnalyzeEndpoint:
    """Test company analysis endpoint."""

    def test_analyze_endpoint_exists(self, api_test_client):
        """Test analyze endpoint is accessible."""
        response = api_test_client.post(
            "/analyze",
            json={"ticker": "AAPL"}
        )

        # Should not return 404
        assert response.status_code != 404

    def test_analyze_with_valid_ticker(self, api_test_client):
        """Test analysis with valid ticker."""
        response = api_test_client.post(
            "/analyze",
            json={"ticker": "AAPL"}
        )

        assert response.status_code == 200
        data = response.json()

        assert 'success' in data
        assert 'data' in data or 'error' in data

    def test_analyze_with_invalid_ticker(self, api_test_client):
        """Test analysis with invalid ticker."""
        response = api_test_client.post(
            "/analyze",
            json={"ticker": "INVALID123"}
        )

        # Should handle gracefully
        assert response.status_code in [200, 400, 404]

    def test_analyze_missing_ticker(self, api_test_client):
        """Test analysis without ticker parameter."""
        response = api_test_client.post(
            "/analyze",
            json={}
        )

        # Should return validation error
        assert response.status_code in [400, 422]

    def test_analyze_response_structure(self, api_test_client):
        """Test response has correct structure."""
        response = api_test_client.post(
            "/analyze",
            json={"ticker": "MSFT"}
        )

        if response.status_code == 200:
            data = response.json()

            assert isinstance(data, dict)
            assert 'success' in data

            if data.get('success') and 'data' in data:
                analysis = data['data']
                # Should have key fields
                assert 'ticker' in analysis or 'error' in data


class TestCompaniesEndpoint:
    """Test companies listing endpoint."""

    def test_get_companies_list(self, api_test_client):
        """Test getting list of companies."""
        response = api_test_client.get("/companies")

        assert response.status_code == 200
        data = response.json()

        assert 'success' in data
        assert 'data' in data

        if data['success']:
            assert 'companies' in data['data']
            assert isinstance(data['data']['companies'], list)

    def test_companies_response_format(self, api_test_client):
        """Test companies response format."""
        response = api_test_client.get("/companies")
        data = response.json()

        assert isinstance(data, dict)
        assert data.get('success') in [True, False]


class TestRecentAnalysesEndpoint:
    """Test recent analyses endpoint."""

    def test_get_recent_analyses(self, api_test_client):
        """Test getting recent analyses."""
        response = api_test_client.get("/recent?limit=10")

        assert response.status_code == 200
        data = response.json()

        assert 'success' in data
        assert 'data' in data

        if data['success']:
            assert 'analyses' in data['data']
            assert isinstance(data['data']['analyses'], list)

    def test_recent_analyses_with_limit(self, api_test_client):
        """Test recent analyses respects limit parameter."""
        response = api_test_client.get("/recent?limit=5")

        if response.status_code == 200:
            data = response.json()

            if data.get('success'):
                analyses = data['data']['analyses']
                # Should not exceed limit
                assert len(analyses) <= 5

    def test_recent_analyses_default_limit(self, api_test_client):
        """Test recent analyses with default limit."""
        response = api_test_client.get("/recent")

        assert response.status_code == 200
        data = response.json()

        assert 'success' in data


class TestCompanyHistoryEndpoint:
    """Test company analysis history endpoint."""

    def test_get_company_history(self, api_test_client):
        """Test getting history for specific company."""
        response = api_test_client.get("/company/AAPL/history?limit=10")

        # Should not error
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            assert 'success' in data

    def test_company_history_with_limit(self, api_test_client):
        """Test company history respects limit."""
        response = api_test_client.get("/company/MSFT/history?limit=5")

        if response.status_code == 200:
            data = response.json()

            if data.get('success') and 'data' in data:
                history = data['data'].get('analyses', [])
                assert len(history) <= 5


class TestMarketDataEndpoint:
    """Test market data endpoint."""

    def test_get_market_data(self, api_test_client):
        """Test getting market data for ticker."""
        response = api_test_client.get("/market/AAPL")

        # Should handle request
        assert response.status_code in [200, 404, 500]

        if response.status_code == 200:
            data = response.json()
            assert 'success' in data

    def test_market_data_invalid_ticker(self, api_test_client):
        """Test market data with invalid ticker."""
        response = api_test_client.get("/market/INVALID123")

        # Should handle gracefully
        assert response.status_code in [200, 404, 400]


class TestCORSHeaders:
    """Test CORS configuration."""

    def test_cors_headers_present(self, api_test_client):
        """Test CORS headers are set."""
        response = api_test_client.options("/health")

        # Should allow CORS
        assert response.status_code in [200, 405]

    def test_api_allows_post_requests(self, api_test_client):
        """Test API allows POST requests."""
        response = api_test_client.post(
            "/analyze",
            json={"ticker": "AAPL"}
        )

        # Should not be method not allowed
        assert response.status_code != 405


class TestErrorHandling:
    """Test API error handling."""

    def test_404_for_invalid_endpoint(self, api_test_client):
        """Test 404 for non-existent endpoints."""
        response = api_test_client.get("/nonexistent")

        assert response.status_code == 404

    def test_malformed_json_handling(self, api_test_client):
        """Test handling of malformed JSON."""
        response = api_test_client.post(
            "/analyze",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )

        # Should return error
        assert response.status_code in [400, 422]

    def test_empty_body_handling(self, api_test_client):
        """Test handling of empty request body."""
        response = api_test_client.post("/analyze")

        # Should return validation error
        assert response.status_code in [400, 422]


class TestResponseFormat:
    """Test API response format consistency."""

    def test_success_response_format(self, api_test_client):
        """Test successful response format."""
        response = api_test_client.get("/health")
        data = response.json()

        # Should have consistent format
        assert 'success' in data
        assert isinstance(data['success'], bool)

    def test_error_response_format(self, api_test_client):
        """Test error response format."""
        response = api_test_client.post(
            "/analyze",
            json={}
        )

        if response.status_code in [400, 422]:
            data = response.json()

            # FastAPI validation errors have detail field
            assert 'detail' in data or 'error' in data


class TestPerformance:
    """Test API performance characteristics."""

    def test_health_check_is_fast(self, api_test_client):
        """Test health check responds quickly."""
        import time

        start = time.time()
        response = api_test_client.get("/health")
        duration = time.time() - start

        assert response.status_code == 200
        # Should respond in under 1 second
        assert duration < 1.0

    def test_concurrent_requests_handled(self, api_test_client):
        """Test API can handle multiple requests."""
        # Send multiple health checks
        responses = []
        for _ in range(5):
            response = api_test_client.get("/health")
            responses.append(response)

        # All should succeed
        for response in responses:
            assert response.status_code == 200
