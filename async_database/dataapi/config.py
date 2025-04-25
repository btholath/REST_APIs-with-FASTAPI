"""
📘 Config Management Script for FastAPI Projects
------------------------------------------------

This script provides a structured and scalable way to manage configuration settings
for a FastAPI (or any Python) project using `pydantic`'s settings management system.
It supports loading environment-specific variables from `.env` files with optional
prefixes for better namespacing and separation of concerns.

🔍 Key Features:
- Uses Pydantic's `BaseSettings` for automatic environment variable parsing and validation.
- Loads variables from a `.env` file using `SettingsConfigDict(env_file=".env")`.
- Supports multiple environments (dev, prod, test) with optional prefixes:
  - `DEV_` for development
  - `PROD_` for production
  - `TEST_` for test mode
- Includes `lru_cache` to prevent re-parsing config multiple times during app lifecycle.
- Provides a `get_config()` function to select the correct config class based on the `ENV_STATE` value.

👨‍💻 How to Use:
- Set `ENV_STATE=dev`, `ENV_STATE=prod`, or `ENV_STATE=test` in your `.env` file.
- Add relevant prefixed config variables (e.g., `DEV_DATABASE_URL`, `PROD_DATABASE_URL`, etc.).
- Import and use `config` from this module across your app for consistent access to settings.

📦 Example:
.env file:
    ENV_STATE=dev
    DEV_DATABASE_URL=postgresql+asyncpg://user:pass@localhost/devdb

In app:
    from config_module import config
    print(config.DATABASE_URL)  # Outputs: postgresql+asyncpg://user:pass@localhost/devdb

🧪 Benefits:
- Simplifies managing multiple environments in a clean, extensible way.
- Reduces hardcoding and encourages 12-factor app design.
- Promotes testability with `DB_FORCE_ROLL_BACK` flag for isolated test environments.

Based on the configuration principles shared by Redowan Delowar:
https://rednafi.github.io/digressions/python/2020/06/03/python-configs.html
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    """Loads the dotenv file. Including this is necessary to get
    pydantic to load a .env file."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")


class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True

    model_config = SettingsConfigDict(env_prefix="TEST_")


@lru_cache()
def get_config(env_state: str):
    """Instantiate config based on the environment."""
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)
