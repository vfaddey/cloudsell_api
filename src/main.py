from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.v1.pricing_plans import router as servers_router
from src.api.v1.providers import router as providers_router
from src.api.v1.orders import router as orders_router
from src.api.v1.users import router as users_router
from src.core.config import settings

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    root_path="/",
    title=settings.APP_NAME
)

app.include_router(servers_router)
app.include_router(providers_router)
app.include_router(orders_router)
app.include_router(users_router)


app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)