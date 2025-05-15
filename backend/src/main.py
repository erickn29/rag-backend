from api.router_general import router as general_router
from core.config import config
from core.middleware.auth import SSOAuthBackend, SSOAuthMiddleware
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware import Middleware


middleware = [
    Middleware(SSOAuthMiddleware, backend=SSOAuthBackend()),  # type: ignore
]

app = FastAPI(
    debug=config.app.debug,
    title="rag_backend",
    version="0.1.0",
    docs_url="/docs/" if config.app.debug else None,
    redoc_url="/redoc/" if config.app.debug else None,
    middleware=middleware,
)

app.include_router(general_router)

Instrumentator().instrument(app).expose(app)
