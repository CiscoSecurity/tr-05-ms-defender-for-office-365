from http import HTTPStatus

import httpx
import requests
from httpx import InvalidURL

from api.errors import (
    AuthorizationError,
    CTRBadRequestError,
    CTRConnectionError,
    CTRInternalServerError,
    CTRInvalidJWTError,
    CTRSSLError,
    CTRTooManyRequestsError,
    CTRUnexpectedResponseError,
    WRONG_CREDENTIALS,
)
from api.schemas import ObservableSchema
from config import Settings

s = Settings()


class Client:
    def __init__(self, credentials):
        self.client_id = credentials["client_id"]
        self.client_secret = credentials["client_secret"]
        self.token_url = credentials["token_url"]

        self.alerts = []
        self.session = httpx.Client()

    def request(self, url, params=None, data=None, json=None):
        try:
            if not self.session.headers.get("Authorization"):
                self._auth()

            response = self.session.post(url, params=params, data=data, json=json)
            match response.status_code:
                case HTTPStatus.OK:
                    return response.json()
                case (
                    HTTPStatus.NOT_FOUND
                    | HTTPStatus.FORBIDDEN
                    | HTTPStatus.BAD_GATEWAY
                    | HTTPStatus.SERVICE_UNAVAILABLE
                    | HTTPStatus.GATEWAY_TIMEOUT
                ):
                    raise CTRBadRequestError()
                case HTTPStatus.UNAUTHORIZED:
                    raise AuthorizationError(str(response.json()["error"]))
                case HTTPStatus.TOO_MANY_REQUESTS:
                    raise CTRTooManyRequestsError()
                case HTTPStatus.INTERNAL_SERVER_ERROR:
                    raise CTRInternalServerError
        except requests.exceptions.SSLError as e:
            raise CTRSSLError(e) from e

    def _set_headers(self, response: dict) -> None:
        if not (token := response.get("access_token")):
            raise CTRBadRequestError("Access Token does not exist.")

        headers = {
            "Accept": "application/json",
            "Authorization": f"{response.get('token_type', 'Bearer')} {token}",
            "Content-Type": "application/json",
            **s.CTR_HEADERS,
        }

        self.session.headers.update(headers)

    def _auth(self):
        url = self.token_url
        try:
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
                "scope": s.SCOPE,
            }
            response = self.session.post(url, data=data, headers=s.CTR_HEADERS)
            match response.status_code:
                case HTTPStatus.OK:
                    return self._set_headers(response.json())
                case (HTTPStatus.UNAUTHORIZED | HTTPStatus.BAD_REQUEST):
                    raise AuthorizationError(WRONG_CREDENTIALS)
                case HTTPStatus.NOT_FOUND:
                    raise CTRInvalidJWTError()
                case _:
                    raise CTRUnexpectedResponseError(response.json())
        except (ConnectionError, InvalidURL) as e:
            raise CTRConnectionError(url) from e

    def observe(self, observable: ObservableSchema):
        pass

    def health(self):
        query = {"Query": "AlertEvidence | limit 1 | project Timestamp"}
        return self.request(s.ADVANCED_HUNTING_URL, json=query)
