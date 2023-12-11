from unittest.mock import patch

from fastapi.testclient import TestClient


@patch("requests.post")
def test_login_valid_credentials(mock_request, client: TestClient):
    response = client.post("/token", data={"username": "johndoe"})

    assert response.status_code == 200
    assert "access_token" in response.json()
