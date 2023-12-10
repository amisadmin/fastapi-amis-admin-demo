import os
import sys
from pathlib import Path
from typing import List

from fastapi_amis_admin import admin
from fastapi_amis_admin.utils.pydantic import PYDANTIC_V2

if PYDANTIC_V2:
    from pydantic_settings import SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BACKEND_DIR.__str__())


class Settings(admin.Settings):
    if PYDANTIC_V2:
        model_config = SettingsConfigDict(extra="ignore")

    name: str = "FastAPI-Amis-Admin-Demo"
    host: str = "127.0.0.1"
    port: int = 8000
    secret_key: str = ""
    allow_origins: List[str] = None


# 设置FAA_GLOBALS环境变量
os.environ.setdefault("FAA_GLOBALS", "core.globals")

settings = Settings(_env_file=os.path.join(BACKEND_DIR, ".env"))
