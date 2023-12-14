import uvicorn
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import ORJSONResponse
from starlette.middleware.sessions import SessionMiddleware

from api.errors import CTRBaseError
from api.globals import GlobalsMiddleware, g
from api.routers import auth, enrich, system
from config import Settings

g.SETTINGS = Settings()

app = FastAPI(default_response_class=ORJSONResponse, version=g.SETTINGS.VERSION)
app.add_middleware(GlobalsMiddleware)
app.add_middleware(SessionMiddleware, secret_key="")

# Displayed in this order in documentation
for router in [auth, enrich, system]:
    app.include_router(router.router)


@app.exception_handler(CTRBaseError)
def format_errors(request: Request, exc: CTRBaseError):
    # app.logger.error(traceback.format_exc())
    return ORJSONResponse({"errors": [exc.dict]}, status.HTTP_401_UNAUTHORIZED)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=True)
