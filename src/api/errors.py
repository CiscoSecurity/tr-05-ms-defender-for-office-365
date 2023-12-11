from json import JSONDecodeError

from jose.exceptions import JWTError
from jwt import DecodeError, InvalidAudienceError, InvalidSignatureError
from requests.exceptions import ConnectionError, HTTPError, InvalidURL

EXPECTED_ERRORS_KEY = (ConnectionError, InvalidURL, JSONDecodeError, HTTPError, JWTError)

AUTH_ERROR = "authorization error"
CONNECTION_ERROR = "connection error"
INTERNAL_SERVER_ERROR = "internal error"
INVALID_ARGUMENT = "invalid argument"
INVALID_REQUEST = "invalid request"
INVALID_TIMERANGE = "Invalid time range parameters"
KID_NOT_FOUND = "kid from JWT header not found in API response"
KID_MISSING = "kid is missing in response headers from jwks_host"
NO_AUTH_HEADER = "Authorization header is missing"
PERMISSION_DENIED = "permission denied"
TIME_RANGE_ERROR = "timerange error"
TOO_MANY_REQUESTS = "too many requests"
UNKNOWN = "unknown"
WRONG_AUDIENCE = "Wrong configuration-token-audience"
WRONG_AUTH_TYPE = "Wrong authorization type"
WRONG_CREDENTIALS = "wrong API credentials."
WRONG_PAYLOAD_STRUCTURE = "Wrong JWT payload structure"
WRONG_JWT_STRUCTURE = "Wrong JWT structure"
WRONG_KEY = (
    "Failed to decode JWT with provided key. "
    "Make sure domain in custom_jwks_host "
    "corresponds to your XDR instance region."
)
JWKS_HOST_MISSING = (
    "jwks_host is missing in JWT payload. Make sure "
    "custom_jwks_host field is present in module_type"
)
WRONG_JWKS_HOST = (
    "Wrong jwks_host in JWT payload. Make sure domain follows "
    "the visibility.<region>.cisco.com structure"
)
EXPECTED_ERRORS_TOKEN = {
    KeyError: WRONG_PAYLOAD_STRUCTURE,
    AssertionError: JWKS_HOST_MISSING,
    InvalidSignatureError: WRONG_KEY,
    DecodeError: WRONG_JWT_STRUCTURE,
    InvalidAudienceError: WRONG_AUDIENCE,
    TypeError: KID_NOT_FOUND,
}


class CTRBaseError(Exception):
    def __init__(self, code, message, type_="fatal"):
        super().__init__()
        self.code: str = code or UNKNOWN
        self.message: str = message or "Something went wrong."
        self.type_: str = type_

    @property
    def dict(self) -> dict:
        return {"type": self.type_, "code": self.code, "message": self.message}


class AuthorizationError(CTRBaseError):
    def __init__(self, message):
        super().__init__(AUTH_ERROR, f"Authorization failed: {message}")


class CTRBadRequestError(CTRBaseError):
    def __init__(self, error=None):
        message = "Invalid request to Microsoft Defender for Endpoint."
        if error:
            message += f" {error}"
        super().__init__(INVALID_REQUEST, message)


class CTRInternalServerError(CTRBaseError):
    def __init__(self):
        super().__init__(
            INTERNAL_SERVER_ERROR, "Microsoft Defender for Endpoint internal error."
        )


class CTRInvalidJWTError(CTRBaseError):
    def __init__(self):
        super().__init__(PERMISSION_DENIED, "Invalid Authorization Bearer JWT.")


class CTRSSLError(CTRBaseError):
    def __init__(self, error):
        error = error.args[0].reason.args[0]
        message = getattr(error, "verify_message", error.args[0]).capitalize()
        super().__init__(UNKNOWN, f"Unable to verify SSL certificate: {message}")


class CTRTooManyRequestsError(CTRBaseError):
    def __init__(self):
        message = (
            "Too many requests to Microsoft Defender for Endpoint "
            "have been made. Please try again later."
        )
        super().__init__(TOO_MANY_REQUESTS, message)


class CTRUnexpectedResponseError(CTRBaseError):
    def __init__(self, error):
        if error and error.get("error_description"):
            message = (
                f"Microsoft Defender for Endpoint returned unexpected "
                f'error. Details: {error["error_description"]}'
            )
        else:
            message = "Something went wrong."

        super().__init__(UNKNOWN, message=str(message))


class DefenderForEndpointTimerangeError(CTRBaseError):
    def __init__(self, start_time, end_time):
        super().__init__(
            TIME_RANGE_ERROR,
            "Invalid isoformat string"
            " validate the value of your query parameters:"
            f" {start_time, end_time}",
        )


class DefenderForEndpointConnectionError(CTRBaseError):
    def __init__(self, url):
        msg = (
            "Unable to get token for Microsoft Defender For Endpoint, "
            + f" validate the configured API Authorization URL: {url}"
            if url
            else " you need to provide a URL"
        )

        super().__init__(CONNECTION_ERROR, msg)


class InvalidArgumentError(CTRBaseError):
    def __init__(self, message):
        super().__init__(INVALID_ARGUMENT, str(message))


class TemplateConnectionError(CTRBaseError):
    def __init__(self, url):
        msg = "Unable to connect to Template, validate the configured API endpoint: {url}"
        super().__init__(CONNECTION_ERROR, msg)


class TimerangeError(CTRBaseError):
    def __init__(self, start_time, end_time):
        super().__init__(
            TIME_RANGE_ERROR,
            "Invalid iso format string validate the value of your query parameters:"
            f" {start_time, end_time}",
        )


class TokenExpirationWarning(CTRBaseError):
    def __init__(self, api_key, days_to_expire):
        msg = (
            f"API token, {api_key[:5]}...{api_key[-5:]}, "
            f"will expire in {days_to_expire} days!"
        )
        super().__init__("template-api-token-expires-within-30-days", msg, "warning")


class WatchdogError(CTRBaseError):
    def __init__(self):
        super().__init__(code="health check failed", message="Invalid Health Check")
