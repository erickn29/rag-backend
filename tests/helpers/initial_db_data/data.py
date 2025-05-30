import uuid

from model import User
from service.user import UserServiceV1

from sqlalchemy.ext.asyncio import AsyncSession


async def set_initial_data(session: AsyncSession):
    admin_password = str(uuid.uuid4())
    admin = User(
        password=UserServiceV1().get_password_hash(admin_password),
        email=str(uuid.uuid4().hex) + "@mail.com",
        first_name=str(uuid.uuid4().hex[:7]),
        last_name=str(uuid.uuid4().hex[:7]),
        is_active=True,
        is_admin=True,
        is_service=False,
    )
    session.add(admin)
    await session.flush()

    default = User(
        password=UserServiceV1().get_password_hash(str(uuid.uuid4())),
        email=str(uuid.uuid4().hex) + "@mail.com",
        first_name=str(uuid.uuid4().hex[:7]),
        last_name=str(uuid.uuid4().hex[:7]),
        is_active=True,
        is_admin=False,
        is_service=False,
    )
    session.add(default)
    await session.flush()

    service = User(
        password=UserServiceV1().get_password_hash(str(uuid.uuid4())),
        email=str(uuid.uuid4().hex) + "@mail.com",
        first_name=str(uuid.uuid4().hex[:7]),
        last_name=str(uuid.uuid4().hex[:7]),
        is_active=True,
        is_admin=False,
        is_service=True,
    )
    session.add(service)
    await session.flush()

    blocked_service = User(
        password=UserServiceV1().get_password_hash(str(uuid.uuid4())),
        email=str(uuid.uuid4().hex) + "@mail.com",
        first_name=str(uuid.uuid4().hex[:7]),
        last_name=str(uuid.uuid4().hex[:7]),
        is_active=False,
        is_admin=False,
        is_service=True,
    )
    session.add(blocked_service)
    await session.flush()

    return {
        "admin": admin,
        "admin_password": admin_password,
        "service": service,
        "blocked_service": blocked_service,
        "default": default,
    }
