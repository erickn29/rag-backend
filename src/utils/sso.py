from uuid import UUID

from core.config import config
from core.log import logger
from repository.user import ServiceUser

from httpx import AsyncClient, RequestError
from pydantic import ValidationError


class HandlerSSO:
    def __init__(
        self,
        host: str = config.sso.host,
        port: int = config.sso.port,
        path: str = config.sso.path,
    ):
        self.host = host
        self.port = port
        self.path = path

    async def get_user(self, user_id: UUID) -> ServiceUser | None:
        response = await self._get_response(
            method="GET",
            path=f"{self.path}/user/{user_id}/",
        )
        if not response:
            return None
        return ServiceUser.model_validate(response)

    async def verify_token(self, token: str) -> bool | None:
        response = await self._get_response(
            method="POST",
            path=f"{self.path}/auth/token/verify/",
            data={"token": token},
        )
        if not response:
            return None
        return response.get("is_valid")

    async def _get_response(
        self, method: str, path: str, data: dict | None = None
    ) -> dict | None:
        async with AsyncClient() as client:
            client.headers["x-api-key"] = config.app.sso_api_key
            try:
                response = await client.request(
                    method=method,
                    url=f"http://{self.host}:{self.port}{path}",
                    json=data,
                )
                if not response:
                    logger.error("No response from SSO")
                    return None
                if response.status_code != 200:
                    logger.error("Bad response from SSO")
                    return None
                return response.json()
            except (RequestError, ValidationError) as err:
                logger.error(str(err))
                return None


sso_handler = HandlerSSO()
