from unittest import TestCase
from starlette.testclient import TestClient
from src.main import api

client = TestClient(api)


class UnitTest(TestCase):
    """
    Tests /v1/indicator endpoint
    """
    def test_indicators(self):
        response = client.get("/v1/indicator")
        assert response.status_code == 200
        assert len(response.json()) == 30

    """
    Tests /v1/indicator/{id}
    """
    def test_indicator_by_id(self):
        test_id = 4
        response = client.get(f"/v1/indicator/{test_id}")
        response_json = response.json()
        assert response.status_code == 200
        assert type(response_json) == dict
        assert response_json["id"] == test_id
        assert "method" in response_json
        assert "category" in response_json
        assert "indicator" in response_json
        assert "unit" in response_json

    """
    Tests /v1/entry
    """
    def test_entries(self):
        response = client.get("/v1/entry")
        assert response.status_code == 200
        assert len(response.json()) == 87

    """
    Tests /v1/entry/{entry_id}
    """
    def test_entry_by_id(self):
        test_id = 10
        response = client.get(f"/v1/entry/{test_id}")
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json
        assert "product_name" in response_json
        assert "geography" in response_json
        assert "unit" in response_json
        assert "impact" in response_json
        assert len(response_json["impact"]) >= 0

    """
    Tests /v1/impact?entry_id={entry_id}&indicator_id={indicator_id}
    """
    def test_impact(self):
        entry_id = 1
        impact_id = 13
        response = client.get(f"/v1/impact?entry_id={entry_id}&indicator_id={impact_id}")
        response_json = response.json()
        assert response.status_code == 200
        assert "id" in response_json
        assert "indicator" in response_json
        assert "entry" in response_json
        assert "coefficient" in response_json
