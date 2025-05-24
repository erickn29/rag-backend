from api.v1.router_v1 import router as router_v1
from deps.auth import is_admin_or_service

from fastapi import APIRouter, Depends


router = APIRouter(prefix="/api")

router.include_router(router_v1)


@router.get(
    "/healthcheck/", status_code=200, dependencies=[Depends(is_admin_or_service)]
)
async def health_check():
    return {"status": "ok"}
