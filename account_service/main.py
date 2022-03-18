from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from app.settings.database_configs.database_connection import async_engine, Base
from app.api.v1.views.authorization_views import authorization_router
from app.api.v1.views.registration_views import registration_router
from app.api.v1.middleware.views.account import middleware_account_router

api_prefix = "/api/v1"

app = FastAPI(
    title="Account API",
    redoc_url=None,
    docs_url=None,
    openapi_url=api_prefix + "/accounts/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authorization_router, prefix=api_prefix)
app.include_router(registration_router, prefix=api_prefix)

app.include_router(middleware_account_router, prefix=api_prefix)


@app.get("/api/v1/accounts/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url=api_prefix + "/accounts/openapi.json",
        title="Account API",
    )


@app.get("/api/v1/accounts/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url=api_prefix + "/accounts/openapi.json",
        title="Account API",
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors_dict = {"detail": []}
    for error in exc.errors():
        err = {error['loc'][1]: error["msg"]}
        errors_dict["detail"].append(err)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=errors_dict,
    )


@app.on_event("startup")
async def startup():
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    pass