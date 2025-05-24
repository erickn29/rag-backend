from datetime import datetime
from uuid import UUID

from core.cache import cache_service
from core.config import config
from core.constants import TZ
from repository.user import ServiceUser, UserRepoV1
from service.auth import AuthService
from starlette.authentication import (
    AuthCredentials,
    AuthenticationError,
    UnauthenticatedUser,
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection
from starlette.types import Receive, Scope, Send
from utils.sso import sso_handler


class SSOAuthMiddleware(AuthenticationMiddleware):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope)
        if not any(
            map(
                lambda x: x in conn.url.path,
                ["/docs", "/redoc", "/openapi.json"],
            )
        ):
            try:
                auth_result = await self.backend.authenticate(conn)
            except AuthenticationError as exc:
                response = self.on_error(conn, exc)
                if scope["type"] == "websocket":
                    await send({"type": "websocket.close", "code": 1000})
                else:
                    await response(scope, receive, send)
                return

            if auth_result is None:
                auth_result = AuthCredentials(), UnauthenticatedUser()
            scope["auth"], scope["user"] = auth_result
        await self.app(scope, receive, send)


class SSOAuthBackend:
    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, ServiceUser] | None:
        if token := conn.cookies.get("access_token"):  # noqa SIM102
            if user := await self._get_user(token):
                return AuthCredentials(["authenticated"]), user
        return None

    async def _get_user(self, token: str) -> ServiceUser | None:
        user_id = await self._get_user_id(token)
        if not user_id:
            return None
        return await self._find_user(user_id)

    async def _get_user_id(self, token: str) -> UUID | None:
        await self._verify_token(token)
        token_data = self._get_token_payload(token)
        self._check_iat(token_data)
        return self._validate_user_id(token_data.get("id", ""))

    @staticmethod
    async def _verify_token(token: str):
        if await cache_service.get(token):
            return True
        if await sso_handler.verify_token(token):
            await cache_service.set(token, "True", config.auth.access_token_expire - 10)
            return None
        raise AuthenticationError("Token is not valid")

    @staticmethod
    async def _find_user(user_id: UUID) -> ServiceUser | None:
        return await UserRepoV1().get_user_sso(user_id)

    @staticmethod
    def _validate_user_id(user_id: str) -> UUID | None:
        if not user_id:
            return None
        try:
            user_id_uuid = UUID(user_id)
            return user_id_uuid
        except ValueError:
            return None

    @staticmethod
    def _get_token_payload(token: str) -> dict:
        if payload := AuthService().get_payload(token):
            return payload
        raise AuthenticationError("Error decode token")

    @staticmethod
    def _check_iat(payload: dict):
        if not payload or not payload.get("expat"):
            raise AuthenticationError("Expat not found")
        try:
            expat = float(payload.get("expat", 0))
        except ValueError:
            raise AuthenticationError("Bad date format (need timestamp)") from None
        if datetime.now(tz=TZ.MSK).timestamp() > expat:
            raise AuthenticationError("Please, refresh token")
