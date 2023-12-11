import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.sessions import SessionMiddleware

from api.globals import GlobalsMiddleware, g
from api.routers import auth, enrich, system
from config import Settings

g.settings = Settings()

app = FastAPI(default_response_class=ORJSONResponse, version=g.settings.VERSION)
app.add_middleware(GlobalsMiddleware)
app.add_middleware(SessionMiddleware, secret_key="")

# Displayed in this order in documentation
for router in [auth, enrich, system]:
    app.include_router(router.router)


# @app.exception_handler(HTTPException)
# async def handle_401_errors(request: Request, exc: Exception):
#     if status.HTTP_401_UNAUTHORIZED:
#         message = getattr(exc, "description", "Not authenticated")
#         content = {"errors": [AuthorizationError(message).to_dict]}
#
#         return ORJSONResponse(content, status.HTTP_200_OK)


# @app.exception_handler(HTTPException)
# async def handle_500_errors(request: Request, exception: Exception):
#     code = getattr(exception, "code", "Internal server error")
#     message = getattr(exception, "description", "Something went wrong.")
#     content = {"errors": [TRFormattedError(code, message).to_dict]}
#
#     return ORJSONResponse(content, status.HTTP_200_OK)


# @app.exception_handler(CTRBaseError)
# def handle_tr_formatted_error(request: Request, exc: CTRBaseError):
#     # app.logger.error(traceback.format_exc())
#     return ORJSONResponse({"errors": [exc.dict]}, status.HTTP_401_UNAUTHORIZED)


# @app.exception_handler(RequestValidationError)
# def validation_exception_handler(exc: RequestValidationError):
#     modified_details = [
#         InvalidArgumentError(f"{error['loc']}: {error['msg']}").to_dict
#         for error in exc.errors()
#     ]
#     return ORJSONResponse({"errors": modified_details}, status.HTTP_200_OK)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=True)
