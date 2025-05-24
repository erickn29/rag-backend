from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


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

    @property
    def is_authenticated(self):
        return True
