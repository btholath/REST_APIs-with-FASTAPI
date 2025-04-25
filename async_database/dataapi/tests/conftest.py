import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

os.environ["ENV_STATE"] = "dev"
from dataapi.database import database  # noqa: E402
from dataapi.main import app  # noqa: E402


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield
    await database.disconnect()

@pytest.fixture(autouse=True)
async def clean_tables():
    # Assuming you have a `posts` and `comments` table
    await database.execute("DELETE FROM comments")
    await database.execute("DELETE FROM posts")

@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    #async with AsyncClient(app=app, base_url=client.base_url) as ac:
    #    yield ac
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as ac:
        yield ac
