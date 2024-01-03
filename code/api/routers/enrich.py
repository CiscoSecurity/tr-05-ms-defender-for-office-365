from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from api.routers.auth import oauth2_scheme
from api.schemas import ObservableSchema

router = APIRouter(tags=["Observables"])


@router.post("/deliberate/observables")
def deliberate_observables(
    observables: list[ObservableSchema],
    token: Annotated[str, Depends(oauth2_scheme)],
    request: Request,
    start: str = "",
    end: str = "",
) -> JSONResponse:
    return JSONResponse({"data": []})


@router.post("/observe/observables")
def observe_observables(
    observables: list[ObservableSchema],
    token: Annotated[str, Depends(oauth2_scheme)],
    request: Request,
    start: str = "",
    end: str = "",
) -> JSONResponse:
    # _ = filter_observables(observables, request)
    # _ = request.settings["CTR_ENTITIES_LIMIT"]
    return JSONResponse({"data": []})


@router.post("/refer/observables")
def refer_observables(
    observables: list[ObservableSchema],
    token: Annotated[str, Depends(oauth2_scheme)],
    request: Request,
    start: str = "",
    end: str = "",
) -> JSONResponse:
    return JSONResponse({"data": []})
