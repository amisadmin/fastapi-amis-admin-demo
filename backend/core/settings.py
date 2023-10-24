import os
import sys
from pathlib import Path
from typing import List

from fastapi_amis_admin import admin

# Define the backend directory
BACKEND_DIR = Path(__file__).resolve().parent.parent
# Add the backend directory to a system path
sys.path.append(str(BACKEND_DIR))


# Define a Settings class inheriting from admin.Settings
class Settings(admin.Settings):
    name: str = "FastAPI-Amis-Admin-Demo"
    host: str = "127.0.0.1"
    port: int = 8000
    secret_key: str = ""
    allow_origins: List[str] = None


# Set the FAA_GLOBALS environment variable
os.environ.setdefault("FAA_GLOBALS", "core.globals")

# Initialize settings with values from the .env file
settings = Settings(_env_file=os.path.join(BACKEND_DIR, ".env"))
