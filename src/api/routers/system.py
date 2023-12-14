from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import ORJSONResponse

from api.client import Client
from api.errors import WatchdogError
from api.globals import g
from api.routers.auth import get_credentials, oauth2_scheme

router = APIRouter(tags=["System checks"], dependencies=[Depends(oauth2_scheme)])
Token = Annotated[str, Depends(oauth2_scheme)]


@router.post("/health")
def health(request: Request, token: Token) -> ORJSONResponse:
    Client(get_credentials(token, request)).health()
    return ORJSONResponse({"data": {"status": "ok"}})


@router.post("/version")
def version() -> ORJSONResponse:
    return ORJSONResponse({"version": g.SETTINGS.VERSION})


@router.get("/watchdog")
def watchdog(request: Request) -> ORJSONResponse:
    try:
        return ORJSONResponse({"data": request.headers["health-check"]})
    except KeyError as e:
        raise WatchdogError from e
