import os
from dotenv import set_key
from ..core.config import ENV_PATH, reload_env

def get_creds() -> tuple[str, str]:
    reload_env()
    return os.getenv("APP_USERNAME", "admin"), os.getenv("APP_PASSWORD", "admin123")

def update_creds(new_username: str, new_password: str) -> None:
    set_key(ENV_PATH, "APP_USERNAME", new_username)
    set_key(ENV_PATH, "APP_PASSWORD", new_password)
    reload_env()