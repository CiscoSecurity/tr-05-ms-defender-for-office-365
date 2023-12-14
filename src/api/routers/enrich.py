from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse, ORJSONResponse

from api.client import Client
from api.globals import g
from api.mapping import Sighting
from api.routers.auth import get_credentials, oauth2_scheme
from api.routers.mocked_alert_evidence import ALERT_EVIDENCE
from api.schemas import ObservableSchema
from api.utils import format_docs
from config import Settings

router = APIRouter(tags=["Observables"])

s = Settings()


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
    # if not (observables := filter_observables(observables)):
    #     return ORJSONResponse({"data": []})

    g.sightings = []
    limit = s.CTR_DEFAULT_ENTITIES_LIMIT

    client = Client(get_credentials(token, request))
    for observable in observables:
        if len(g.sightings) >= limit:
            break

        _ = client.observe(observable)
        response = ALERT_EVIDENCE

        if response:
            alerts = sorted(
                response["Results"], key=lambda x: x["Timestamp"], reverse=True
            )
        else:
            alerts = []

        sighting_mapping = Sighting(observable)

        for alert in alerts:
            sighting = sighting_mapping.extract(alert)
            g.sightings.append(sighting)

    data = {}
    if g.sightings:
        data["sightings"] = format_docs(g.sightings)

    return ORJSONResponse({"data": data})


@router.post("/refer/observables")
def refer_observables(
    observables: list[ObservableSchema],
    token: Annotated[str, Depends(oauth2_scheme)],
    request: Request,
    start: str = "",
    end: str = "",
) -> JSONResponse:
    return ORJSONResponse({"data": []})
