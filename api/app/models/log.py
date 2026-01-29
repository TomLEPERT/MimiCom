from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class LogOut(BaseModel):
    """
    Modèle de sortie pour un log.
    """
    model_config = ConfigDict(extra="forbid")

    prospect_id: str
    field: str

    old_value: Optional[Any] = None
    new_value: Optional[Any] = None

    changed_at: datetime
    user: str = Field(default="system")

# ajout class loginfastapi

class LoginRequest(BaseModel):
    email: str
    password: str
