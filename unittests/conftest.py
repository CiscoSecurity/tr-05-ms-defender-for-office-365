from http import HTTPStatus
from unittest.mock import MagicMock

import jwt
from fastapi.testclient import TestClient
from pytest import fixture

import main
from api.errors import INVALID_ARGUMENT
from config import Settings
from unittests.payloads_for_tests import PRIVATE_KEY


@fixture(scope="session")
def client():
    main.app.rsa_private_key = PRIVATE_KEY
    main.app.testing = True
    main.app.SETTINGS = Settings()

    with TestClient(main.app) as client:
        yield client


@fixture(scope="session")
def valid_jwt(client):
    def _make_jwt(
        key="some_key",
        jwks_host="visibility.amp.cisco.com",
        aud="http://testserver:None",
        kid="02B1174234C29F8EFB69911438F597FF3FFEE6B7",
        wrong_structure=False,
        wrong_jwks_host=False,
    ):
        payload = {"key": key, "jwks_host": jwks_host, "aud": aud}

        if wrong_jwks_host:
            payload.pop("jwks_host")

        if wrong_structure:
            payload.pop("key")

        return jwt.encode(payload, client.app.rsa_private_key, "RS256", {"kid": kid})

    return _make_jwt


@fixture(scope="module")
def invalid_json_expected_payload():
    def _make_message(message):
        return {
            "errors": [{"code": INVALID_ARGUMENT, "message": message, "type": "fatal"}]
        }

    return _make_message


def mock_api_response(status_code=HTTPStatus.OK, payload=None, data=None):
    mock_response = MagicMock()

    mock_response.status_code = status_code
    mock_response.ok = status_code == HTTPStatus.OK

    mock_response.json = lambda: payload

    return mock_response
