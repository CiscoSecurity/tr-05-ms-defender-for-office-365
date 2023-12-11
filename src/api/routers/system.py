from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import ORJSONResponse

from api.errors import WatchdogError
from api.globals import g
from api.routers.auth import oauth2_scheme

router = APIRouter(tags=["System checks"], dependencies=[Depends(oauth2_scheme)])
Token = Annotated[str, Depends(oauth2_scheme)]


@router.post("/health")
def health(token: Token, request: Request) -> ORJSONResponse:
    # credentials = get_credentials(token, request)
    # data = client(credentials).health()
    # return ORJSONResponse({"status": "ok"})
    return ORJSONResponse(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body"],
                    "msg": "Field required",
                    "input": None,
                    "url": "https://errors.pydantic.dev/2.4/v/missing",
                }
            ]
        },
        422,
    )


@router.post("/version")
def version() -> ORJSONResponse:
    return ORJSONResponse({"version": g.settings.VERSION})


@router.get("/watchdog")
def watchdog(request: Request) -> ORJSONResponse:
    try:
        return ORJSONResponse({"data": request.headers["health-check"]})
    except KeyError as e:
        raise WatchdogError from e
