from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from app.api.v1.bridge_views.account import account_bridge_router


api_prefix = "/api/v1"

app = FastAPI(
    title="Middleware API",
    redoc_url=None,
    docs_url=None,
    openapi_url=api_prefix + "/middleware/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_bridge_router, prefix=api_prefix)


@app.get("/api/v1/middleware/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url=api_prefix + "/middleware/openapi.json",
        title="Middleware API",
    )


@app.get("/api/v1/middleware/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url=api_prefix + "/middleware/openapi.json",
        title="Middleware API",
    )