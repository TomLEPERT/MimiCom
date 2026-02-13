from __future__ import annotations
from typing import Any, Dict, Optional, Tuple
from services.request import request


def auth_login(username: str, password: str) -> Tuple[Optional[Any], Optional[Dict[str, Any]]]:
    return request(
        "POST",
        "/auth/login",
        json={"username": username, "password": password}
    )
    
def auth_current() -> Tuple[Optional[Any], Optional[Dict[str, Any]]]:
    return request("GET", "/auth/current")

def auth_update(
    current_username: str,
    current_password: str,
    new_username: str,
    new_password: str,
) -> Tuple[Optional[Any], Optional[Dict[str, Any]]]:
    return request(
        "POST",
        "/auth/update",
        json={
            "current_username": current_username,
            "current_password": current_password,
            "new_username": new_username,
            "new_password": new_password,
        },
    )