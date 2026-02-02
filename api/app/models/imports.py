from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class ImportRowError(BaseModel):
    row: int
    errors: List[str]
    raw: Optional[Dict[str, Any]] = None

class ImportRowDuplicate(BaseModel):
    row: int
    fields: List[str]
    existing_prospect_id: Optional[str] = None

class ImportPreviewStats(BaseModel):
    total: int
    valid: int
    invalid: int
    duplicates: int

class ImportPreviewOut(BaseModel):
    preview_id: str
    filename: Optional[str] = None
    stats: ImportPreviewStats
    invalid_rows: List[ImportRowError] = []
    duplicate_rows: List[ImportRowDuplicate] = []

class ImportCommitIn(BaseModel):
    preview_id: str
    force: bool = False

class ImportCommitOut(BaseModel):
    preview_id: str
    created: int
    skipped_invalid: int
    skipped_duplicates: int
    forced_created: int
