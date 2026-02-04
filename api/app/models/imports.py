from enum import Enum
from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel, Field


# -----------------------------
# Status global du preview
# -----------------------------
class ImportStatus(str, Enum):
    OK_TO_MERGE = "OK_TO_MERGE"
    INVALID_CSV = "INVALID_CSV"
    DUPLICATES_FOUND = "DUPLICATES_FOUND"


# -----------------------------
# Stratégies de merge
# -----------------------------
class MergeStrategy(str, Enum):
    IGNORE_DUPLICATES = "ignore_duplicates"
    REPLACE_EXISTING = "replace_existing"
    FORCE_ADD = "force_add"


# -----------------------------
# Erreur d'une ligne CSV
# -----------------------------
class InvalidRowError(BaseModel):
    row_number: int = Field(..., ge=1, description="Numéro de ligne dans le CSV (1 = première ligne de data)")
    raw: Dict[str, Any] = Field(default_factory=dict, description="Contenu brut (colonnes -> valeurs)")
    errors: List[str] = Field(default_factory=list, description="Liste des erreurs de validation/format")


# -----------------------------
# Doublon détecté
# -----------------------------
class DuplicateMatch(BaseModel):
    # Quel champ a matché ?
    match_on: Literal["email", "telephone", "both"]

    # Valeurs normalisées utilisées pour comparer
    email_normalized: Optional[str] = None
    telephone_normalized: Optional[str] = None

    # Ligne CSV concernée
    row_number: int = Field(..., ge=1)
    csv_row: Dict[str, Any] = Field(default_factory=dict)

    # Prospect existant en base (minimum utile au front)
    existing_prospect_id: Optional[str] = None
    existing_snapshot: Dict[str, Any] = Field(
        default_factory=dict,
        description="Petit snapshot du document existant (nom_structure, email, telephone, etc.)"
    )

    # Source du doublon
    source: Literal["csv", "db"] = "db"


# -----------------------------
# Résumé du preview
# -----------------------------
class ImportPreviewSummary(BaseModel):
    total_rows: int = 0
    valid_rows: int = 0
    invalid_rows: int = 0
    duplicates_in_csv: int = 0
    duplicates_in_db: int = 0


# -----------------------------
# Réponse preview
# -----------------------------
class ImportPreviewResponse(BaseModel):
    status: ImportStatus

    # Identifiant temporaire pour commiter ensuite
    import_id: str = Field(..., description="Identifiant du preview (sert à commit)")

    summary: ImportPreviewSummary = Field(default_factory=ImportPreviewSummary)

    # Détails
    invalid: List[InvalidRowError] = Field(default_factory=list)
    duplicates: List[DuplicateMatch] = Field(default_factory=list)

    # Optionnel : infos utiles au front (colonnes attendues etc.)
    required_columns: List[str] = Field(default_factory=list)
    detected_columns: List[str] = Field(default_factory=list)
    message: Optional[str] = None


# -----------------------------
# Request commit
# -----------------------------
class ImportCommitRequest(BaseModel):
    import_id: str
    merge_strategy: MergeStrategy

    # override par ligne: { 12: "force_add", 18: "ignore_duplicates" }
    overrides: Optional[Dict[int, MergeStrategy]] = None


# -----------------------------
# Résultat commit
# -----------------------------
class ImportCommitResponse(BaseModel):
    import_id: str
    merge_strategy: MergeStrategy

    inserted: int = 0
    updated: int = 0
    ignored: int = 0

    # si certains updates/inserts échouent
    errors: List[str] = Field(default_factory=list)

    message: Optional[str] = None
