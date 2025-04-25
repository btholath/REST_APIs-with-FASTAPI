
# 🌀 Async Database Setup in FastAPI with Configuration Management

This document provides a high-level overview and practical implementation steps for setting up an **asynchronous database** in **FastAPI**, using **Pydantic for configuration**, environment-based settings, lifecycle event management, and test-ready execution.

---

## 📦 1. Requirements for Async Database in FastAPI

- `fastapi`: Web framework for building APIs
- `databases`: Async database library compatible with SQLAlchemy
- `sqlalchemy`: ORM and database schema toolkit
- `pydantic`: Data validation and settings management
- `asyncpg` or `aiosqlite`: Async drivers for PostgreSQL or SQLite respectively
- `pytest-asyncio`: For async test support

```bash
pip install fastapi[all] databases sqlalchemy pydantic asyncpg
```

---

## ⚙️ 2. Configuration File Using Pydantic

**Why use Pydantic?**
- Strong typing and validation
- Environment variable support
- Easy to switch between development, production, and test environments

### Example: `config.py`

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DB_FORCE_ROLL_BACK: bool = False
    ENV: str = "development"

    class Config:
        env_file = ".env"

config = Settings()
```

---

## 🌍 3. Configuration per Environment

Create multiple `.env` files like:
- `.env.dev`
- `.env.prod`
- `.env.test`

Each contains:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/db
DB_FORCE_ROLL_BACK=False
ENV=development
```

---

## 🚀 4. Caching and Getting the Config Object

Avoid reloading `.env` every time:

```python
from functools import lru_cache
from .config import Settings

@lru_cache()
def get_settings():
    return Settings()
```

Usage:
```python
settings = get_settings()
```

---

## 🔌 5. Async Database Setup with FastAPI

### `db.py`

```python
from databases import Database
from sqlalchemy import create_engine, MetaData
from .config import get_settings

settings = get_settings()

database = Database(settings.DATABASE_URL, force_rollback=settings.DB_FORCE_ROLL_BACK)
metadata = MetaData()
```

---

## 🌱 6. Lifespan Events for Connection Management

```python
from fastapi import FastAPI
from .db import database

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
```

---

## 🧪 7. Executing FastAPI in "Test" Mode

Set environment for testing:

```bash
ENV=test
DB_FORCE_ROLL_BACK=True
```

Use `TestClient` and override settings as needed:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
```

---

## 🔄 8. Using the Database in FastAPI Router

```python
from fastapi import APIRouter
from .db import database

router = APIRouter()

@router.get("/posts")
async def get_posts():
    query = "SELECT * FROM posts"
    return await database.fetch_all(query=query)
```

---

## ✅ Summary

- Use **Pydantic** for validated and environment-specific configuration
- Setup **databases** for async DB interaction
- Manage connection lifecycle using **FastAPI lifespan events**
- Enable testing with **rollback logic**
- Inject the DB into your **routers** seamlessly

This pattern ensures a **robust**, **scalable**, and **testable** architecture for your FastAPI applications.
