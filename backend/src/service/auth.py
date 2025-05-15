from datetime import datetime

import jwt

from core.cache import Cache, cache_service
from core.constants import TZ
from core.log import logger
from fastapi import HTTPException
from jwt import InvalidTokenError


class AuthService:
    def __init__(self, cache: Cache = cache_service):
        self._cache = cache

    def verify_token(self, token: str) -> bool:
        """Check payload and token expires time"""
        payload = self.get_payload(token)
        if not payload:
            return False
        try:
            self._check_expat(payload)
        except (HTTPException, ValueError):
            logger.error("Token expired")
            return False
        return True

    @staticmethod
    def get_payload(token: str) -> dict[str, str] | None:
        try:
            return jwt.decode(jwt=token, options={"verify_signature": False})
        except InvalidTokenError:
            return None

    @staticmethod
    def _check_expat(payload: dict | None):
        if not payload or not payload.get("expat"):
            raise HTTPException(400, "Не найден expat")
        try:
            expat = float(payload.get("expat", 0))
        except ValueError:
            raise HTTPException(400, "Неверный формат даты в jwt") from None
        if datetime.now(tz=TZ.MSK).timestamp() > expat:
            raise HTTPException(400, "Обновите токен")
