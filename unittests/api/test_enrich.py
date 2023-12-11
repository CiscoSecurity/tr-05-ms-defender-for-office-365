from http import HTTPStatus
from unittest.mock import patch

from pytest import fixture

from unittests.conftest import mock_api_response
from unittests.payloads_for_tests import EXPECTED_JWT
from unittests.utils import get_headers


def routes():
    yield "/deliberate/observables"
    yield "/observe/observables"
    yield "/refer/observables"


@fixture(scope="module", params=routes(), ids=lambda route: f"POST {route}")
def route(request):
    return request.param


@fixture(scope="module")
def invalid_json_value():
    return [{"type": "ip", "value": ""}]


@patch("requests.get")
def test_enrich_call_with_valid_jwt_but_invalid_json_value(
    mock_request,
    route,
    client,
    valid_jwt,
    invalid_json_value,
    invalid_json_expected_payload,
):
    mock_request.return_value = mock_api_response(payload=EXPECTED_JWT)
    response = client.post(
        route, headers=get_headers(valid_jwt()), json=invalid_json_value
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY  # 422
    assert response.json() == {
        "detail": [
            {
                "type": "string_too_short",
                "loc": ["body", 0, "value"],
                "msg": "String should have at least 3 characters",
                "input": "",
                "ctx": {"min_length": 3},
                "url": "https://errors.pydantic.dev/2.4/v/string_too_short",
            }
        ]
    }


@fixture(scope="module")
def valid_json():
    return [{"type": "domain", "value": "cisco.com"}]


@patch("requests.get")
def test_enrich_call_success(mock_request, route, client, valid_jwt, valid_json):
    mock_request.return_value = mock_api_response(payload=EXPECTED_JWT)
    response = client.post(route, headers=get_headers(valid_jwt()), json=valid_json)
    assert response.status_code == HTTPStatus.OK
