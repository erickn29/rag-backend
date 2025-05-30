import uuid

from datetime import datetime

from core.config import config
from core.constants import TZ

import jwt


async def test_healthcheck_admin_200(init_data, client_admin):
    payload_data = {
        "id": str(init_data["admin"].id),
        "expat": datetime.now(tz=TZ.MSK).timestamp() + 300,
    }
    jwt_ = jwt.encode(payload_data, config.app.secret_key, "HS256")
    client_admin.cookies = {"access_token": jwt_}
    response = await client_admin.get("/api/healthcheck/")
    assert response.status_code == 200


async def test_healthcheck_admin_400_expired(init_data, client_admin):
    payload_data = {
        "id": str(init_data["admin"].id),
        "expat": datetime.now(tz=TZ.MSK).timestamp() - 10,
    }
    jwt_ = jwt.encode(payload_data, config.app.secret_key, "HS256")
    client_admin.cookies = {"access_token": jwt_}
    response = await client_admin.get("/api/healthcheck/")
    assert response.status_code == 400
    assert response.text == "Please, refresh token"


async def test_healthcheck_admin_400_no_exp(init_data, client_admin):
    payload_data = {
        "id": str(init_data["admin"].id),
        # "expat": datetime.now(tz=TZ.MSK).timestamp() - 10
    }
    jwt_ = jwt.encode(payload_data, config.app.secret_key, "HS256")
    client_admin.cookies = {"access_token": jwt_}
    response = await client_admin.get("/api/healthcheck/")
    assert response.status_code == 400
    assert response.text == "Expat not found"


async def test_healthcheck_admin_400_bad_exp(init_data, client_admin):
    payload_data = {
        "id": str(init_data["admin"].id),
        "expat": str(datetime.now(tz=TZ.MSK)),
    }
    jwt_ = jwt.encode(payload_data, config.app.secret_key, "HS256")
    client_admin.cookies = {"access_token": jwt_}
    response = await client_admin.get("/api/healthcheck/")
    assert response.status_code == 400
    assert response.text == "Bad date format (need timestamp)"


async def test_healthcheck_admin_400_payload_err(init_data, client_admin):
    payload_data = {
        "id": str(init_data["admin"].id),
        "expat": datetime.now(tz=TZ.MSK).timestamp() + 300,
    }
    jwt_ = jwt.encode(payload_data, config.app.secret_key, "HS256")
    jwt_ += "x"
    client_admin.cookies = {"access_token": jwt_}
    response = await client_admin.get("/api/healthcheck/")
    assert response.status_code == 400
    assert response.text == "Error decode token"


async def test_healthcheck_admin_400_bad_sing(init_data, client_admin):
    payload_data = {
        "id": str(init_data["admin"].id),
        "expat": datetime.now(tz=TZ.MSK).timestamp() + 300,
    }
    jwt_ = jwt.encode(payload_data, config.app.secret_key + "1", "HS256")
    client_admin.cookies = {"access_token": jwt_}
    response = await client_admin.get("/api/healthcheck/")
    assert response.status_code == 400
    assert response.text == "Error decode token"


async def test_healthcheck_service_200(init_data, client_service):
    response = await client_service.get("/api/healthcheck/")
    assert response.status_code == 200


async def test_healthcheck_service_401_bad_key(init_data, client_service):
    client_service.headers = {"x-api-key": str(uuid.uuid4())}
    response = await client_service.get("/api/healthcheck/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"


async def test_healthcheck_anonym_401_bad_key(init_data, client_anonym):
    response = await client_anonym.get("/api/healthcheck/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"


async def test_healthcheck_blocked_service_401_bad_key(
    init_data, client_blocked_service
):
    response = await client_blocked_service.get("/api/healthcheck/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"
