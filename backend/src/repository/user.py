import json

from datetime import datetime
from uuid import UUID

from core.cache import cache_service
from core.config import config
from pydantic import BaseModel
from utils.sso import sso_handler


class ServiceUser(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    services: list
    is_active: bool
    is_admin: bool
    is_service: bool
    created_at: datetime
    updated_at: datetime


class UserRepoV1:
    model = ServiceUser
    user_cache_key = "user:"

    async def get_user_sso(self, user_id: UUID) -> ServiceUser | None:
        if user := await self._get_user_from_cache(user_id):
            return user
        user = await sso_handler.get_user(user_id)
        if not user:
            return None
        await self._set_user_to_cache(user)
        return user

    async def _set_user_to_cache(self, user: ServiceUser):
        user_json = self.model.model_dump_json(user)
        await cache_service.set(
            name=self.user_cache_key + str(user.id),
            value=user_json,
            ex=config.auth.access_token_expire,
        )

    async def _get_user_from_cache(self, user_id: UUID) -> ServiceUser | None:
        if user := await cache_service.get(self.user_cache_key + str(user_id)):
            return self.model.model_validate(json.loads(user))
        return None
