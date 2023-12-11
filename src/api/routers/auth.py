import json
from typing import Annotated

import requests
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from api.errors import (
    AUTH_ERROR,
    AuthorizationError,
    EXPECTED_ERRORS_KEY,
    JWKS_HOST_MISSING,
    KID_MISSING,
    WRONG_JWKS_HOST,
)
from api.schemas import OAuth2RequestForm
from api.utils import set_entities_limit
from config import Settings

s = Settings()

description = """>`How to:`\n\n
Use **username** for **tenant_id** (skipp password)\n\n
Use **Client credentials location** for **client_id/secret**.\n\n
> `Note:` Switch Client credentials location to **Request body**"""

router = APIRouter(tags=["Authorization"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", description=description)


@router.post("/token", description=description, summary="Generate JWT token")
async def login(request: Request, form_data: Annotated[OAuth2RequestForm, Depends()]):
    return {"access_token": generate_token(form_data, request), "token_type": "bearer"}


def generate_token(creds: OAuth2RequestForm, request: Request) -> str:
    payload = {
        "api_base_url": s.BASE_URL,
        "aud": f"{request.url.scheme}://{request.url.hostname}:{request.url.port}",
        "jwks_host": s.JWK_HOST,
        "tenant_id": creds.username,
        # "password": creds.password,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
    }
    return jwt.encode(payload, s.PRIVATE_KEY, "RS256", s.HEADER)


def get_public_key(jwks_host: str, token: str) -> str:
    """Get public key by requesting it from specified jwks host."""

    try:
        response = requests.get(f"https://{jwks_host}/.well-known/jwks")
        response.raise_for_status()
        jwks = response.json()

        public_keys = {}
        for jwk in jwks["keys"]:
            kid = jwk["kid"]
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
        kid = jwt.get_unverified_header(token)["kid"]
        return public_keys.get(kid)
    except EXPECTED_ERRORS_KEY as e:
        raise AuthorizationError(WRONG_JWKS_HOST) from e
    except KeyError as e:
        raise AuthorizationError(KID_MISSING) from e


def get_credentials(token, request=None):
    if request and "Authorization" not in request.headers:
        raise AuthorizationError(AUTH_ERROR)

    if not token:
        # if not (auth := request.headers.get("Authorization")):
        #     raise AuthorizationError(AUTH_ERROR)
        scheme, token = request.headers.get("Authorization").split()
        assert scheme.lower() == "bearer"

    jwks_payload = jwt.decode(token, options={"verify_signature": False})
    assert "jwks_host" in jwks_payload

    jwks_host = jwks_payload.get("jwks_host")
    if not jwks_host:
        raise AuthorizationError(JWKS_HOST_MISSING)
    key = get_public_key(jwks_host, token)
    aud = f"{request.url.scheme}://{request.url.hostname}:{request.url.port}"
    payload = jwt.decode(token, key, ["RS256"], audience=aud)
    set_entities_limit(payload)

    return payload
