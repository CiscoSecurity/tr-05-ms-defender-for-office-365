from http import HTTPStatus

from fastapi.testclient import TestClient

from unittests.utils import get_headers


def test_health_call_success(client: TestClient, valid_jwt):
    response = client.post("/health", headers=get_headers(valid_jwt))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_version_call_success(client: TestClient, valid_jwt):
    response = client.post("/version", headers=get_headers(valid_jwt))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"version": client.app.settings.VERSION}


def test_watchdog_call_success(client: TestClient, valid_jwt):
    headers = {"Health-Check": "test", **get_headers(valid_jwt)}
    response = client.get("/watchdog", headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"data": "test"}
