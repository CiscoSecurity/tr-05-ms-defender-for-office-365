from http import HTTPStatus
from unittest.mock import patch

from pytest import fixture

from src.api.errors import AUTH_ERROR
from unittests.conftest import mock_api_response
from unittests.payloads_for_tests import EXPECTED_JWT, EXPECTED_JWT_WITH_WRONG_KEY
from unittests.utils import get_headers


def routes():
    yield "/health"
    yield "/deliberate/observables"
    yield "/observe/observables"
    yield "/refer/observables"


@fixture(scope="module", params=routes(), ids=lambda route: f"POST {route}")
def route(request):
    return request.param


@fixture(scope="module")
def wrong_jwt_structure():
    return "wrong_jwt_structure"


@fixture(scope="module")
def auth_errors_expected_payload(route):
    def _make_payload_message(message):
        payload = {
            "errors": [
                {
                    "code": AUTH_ERROR,
                    "message": f"Authorization failed: {message}",
                    "type": "fatal",
                }
            ]
        }
        return payload

    return _make_payload_message


UPE_ERROR = {
    "detail": [
        {
            "type": "missing",
            "loc": ["body"],
            "msg": "Field required",
            "input": None,
            "url": "https://errors.pydantic.dev/2.4/v/missing",
        }
    ]
}


def test_call_with_authorization_header_failure(route, client):
    response = client.post(route)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_call_with_out_authentication(route, client, auth_errors_expected_payload):
    response = client.post(route)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_call_with_wrong_authorization_type(
    route, client, valid_jwt, auth_errors_expected_payload
):
    response = client.post(
        route, headers=get_headers(valid_jwt(), auth_type="wrong_type")
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_call_with_wrong_jwt_structure(
    route, client, wrong_jwt_structure, auth_errors_expected_payload
):
    response = client.post(route, headers=get_headers(wrong_jwt_structure))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == UPE_ERROR


@patch("requests.get")
def test_call_with_jwt_encoded_by_wrong_key(
    mock_request, route, client, valid_jwt, auth_errors_expected_payload
):
    mock_request.return_value = mock_api_response(payload=EXPECTED_JWT_WITH_WRONG_KEY)
    response = client.post(route, headers=get_headers(valid_jwt()))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == UPE_ERROR


@patch("requests.get")
def test_call_with_wrong_jwt_payload_structure(
    mock_request, route, client, valid_jwt, auth_errors_expected_payload
):
    mock_request.return_value = mock_api_response(payload=EXPECTED_JWT)
    response = client.post(route, headers=get_headers(valid_jwt(wrong_structure=True)))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == UPE_ERROR


@patch("requests.get")
def test_call_with_wrong_audience(
    mock_request, route, client, valid_jwt, auth_errors_expected_payload
):
    mock_request.return_value = mock_api_response(payload=EXPECTED_JWT)
    response = client.post(route, headers=get_headers(valid_jwt(aud="wrong_aud")))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == UPE_ERROR


@patch("requests.get")
def test_call_with_wrong_kid(
    mock_request, route, client, valid_jwt, auth_errors_expected_payload
):
    mock_request.return_value = mock_api_response(payload=EXPECTED_JWT)
    response = client.post(route, headers=get_headers(valid_jwt(kid="wrong_kid")))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == UPE_ERROR


@patch("requests.get")
def test_call_with_missing_jwks_host(
    mock_request, route, client, valid_jwt, auth_errors_expected_payload
):
    mock_request.return_value = mock_api_response(payload=EXPECTED_JWT)
    response = client.post(route, headers=get_headers(valid_jwt(wrong_jwks_host=True)))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == UPE_ERROR


@patch("requests.get")
def test_login_valid_credentials(mock_request, client):
    response = client.post("/token", data={"username": "johndoe"})

    assert response.status_code == 200
    assert "access_token" in response.json()
