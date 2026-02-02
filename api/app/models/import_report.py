from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict


class ImportRowError(BaseModel):
    row: int
    field: Optional[str] = None
    message: str
    raw: Optional[Dict[str, Any]] = None


class ImportDuplicate(BaseModel):
    row: int
    field: str                   # "email" | "telephone"
    value: str                   # valeur normalisée
    conflict: str                # "csv" | "db"
    existing_prospect_id: Optional[str] = None  # si conflict="db"
    other_row: Optional[int] = None             # si conflict="csv"


class ImportReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_rows: int
    valid_rows: int
    invalid_rows: int

    errors: List[ImportRowError]

    duplicates: List[ImportDuplicate]

    preview: bool = True
