from datetime import date, datetime
from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator, model_validator

from ..utils.normalizers import normalize_str, normalize_phone, validate_phone


INT_FIELDS = (
    "nb_aderents",
    "facebook_followers",
    "x_followers",
    "instagram_followers",
    "tictok_followers",
    "youtube_followers",
)


class ProspectType(str, Enum):
    CSCS = "CSCS"
    BAR_A_JEUX = "Bar à jeux"
    INFLUENCEUR = "Influenceur"
    MJC = "MJC"
    MEDIATHEQUE = "Médiathèque"
    ARTISAN = "Artisan"
    EDITEUR = "Éditeur"
    ASSO_JDR = "Asso JDR"
    BOUTIQUE_SPECIALISEE = "Boutique spécialisée"
    LUDOTHEQUE = "Ludothèque"


class ProspectBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nom_structure: Optional[str] = Field(default=None, max_length=200)
    nom_contact: Optional[str] = Field(default=None, max_length=200)

    email: Optional[EmailStr] = None
    telephone: Optional[str] = Field(default=None, max_length=30)

    type_prospect: Optional[ProspectType] = None

    pays: Optional[str] = Field(default=None, max_length=100)
    region: Optional[str] = Field(default=None, max_length=100)
    departement: Optional[str] = Field(default=None, max_length=100)
    ville: Optional[str] = Field(default=None, max_length=120)
    adresse: Optional[str] = Field(default=None, max_length=300)

    # Géolocalisation
    lat: Optional[float] = Field(default=None, ge=-90, le=90)
    lon: Optional[float] = Field(default=None, ge=-180, le=180)

    nb_aderents: Optional[int] = Field(default=None, ge=0)

    facebook: Optional[str] = Field(default=None, max_length=300)
    facebook_followers: Optional[int] = Field(default=None, ge=0)

    x: Optional[str] = Field(default=None, max_length=300)
    x_followers: Optional[int] = Field(default=None, ge=0)

    instagram: Optional[str] = Field(default=None, max_length=300)
    instagram_followers: Optional[int] = Field(default=None, ge=0)

    tictok: Optional[str] = Field(default=None, max_length=300)
    tictok_followers: Optional[int] = Field(default=None, ge=0)

    youtube: Optional[str] = Field(default=None, max_length=300)
    youtube_followers: Optional[int] = Field(default=None, ge=0)

    sit_web: Optional[str] = Field(default=None, max_length=300)

    accepte_contact: bool = False
    methode_contact: Optional[str] = Field(default=None, max_length=50)

    contacte: bool = False
    date_dernier_contact: Optional[date] = None

    commentaires: Optional[str] = None
    
    # -------------------------
    # Géocodage (optionnel)
    # -------------------------
    geocode_status: Optional[str] = None        # ok / failed
    geocode_error: Optional[str] = None         # no_result / api_error / etc
    geocode_label: Optional[str] = None         # adresse normalisée
    geocode_provider: Optional[str] = None      # ban / nominatim / google

    # -------------------------
    # Normalisation textes
    # -------------------------
    @field_validator(
        "nom_structure",
        "nom_contact",
        "pays",
        "region",
        "departement",
        "ville",
        "adresse",
        "facebook",
        "x",
        "instagram",
        "tictok",
        "youtube",
        "sit_web",
        "methode_contact",
        "commentaires",
        mode="before",
    )
    @classmethod
    def strip_strings(cls, v: Any) -> Any:
        return normalize_str(v)

    # -------------------------
    # Normalisation téléphone + validation
    # -------------------------
    @field_validator("telephone", mode="before")
    @classmethod
    def normalize_telephone(cls, v: Any) -> Any:
        return normalize_phone(v)

    @field_validator("telephone")
    @classmethod
    def check_phone(cls, v: Optional[str]) -> Optional[str]:
        return validate_phone(v)

    # -------------------------
    # Parse ints depuis CSV (évite "unable to parse string as an integer")
    # -------------------------
    @field_validator(*INT_FIELDS, mode="before")
    @classmethod
    def parse_optional_int(cls, v: Any) -> Optional[int]:
        if v is None:
            return None
        if isinstance(v, bool):
            # évite True/False converti en 1/0 par erreur
            raise ValueError("Input should be a valid integer")
        if isinstance(v, int):
            return v
        if isinstance(v, float):
            return int(v)

        if isinstance(v, str):
            s = v.strip()
            if s == "" or s.lower() in {"none", "null", "nan"}:
                return None

            # "12 000" / "12_000" / "12,000" -> "12000"
            s = s.replace(" ", "").replace("_", "").replace(",", "")

            # "12.0"
            try:
                f = float(s)
                if f.is_integer():
                    return int(f)
            except ValueError:
                pass

            if s.isdigit():
                return int(s)

        raise ValueError("Input should be a valid integer")

    # -------------------------
    # Parse floats (lat/lon) depuis CSV
    # -------------------------
    @field_validator("lat", "lon", mode="before")
    @classmethod
    def parse_optional_float(cls, v: Any) -> Optional[float]:
        if v is None:
            return None
        if isinstance(v, bool):
            raise ValueError("Input should be a valid float")
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            s = v.strip()
            if s == "" or s.lower() in {"none", "null", "nan"}:
                return None
            # virgule décimale -> point
            s = s.replace(",", ".")
            try:
                return float(s)
            except ValueError:
                raise ValueError("Input should be a valid float")
        raise ValueError("Input should be a valid float")

    # -------------------------
    # Normalise type_prospect (Editeur -> Éditeur, Asso jdr -> Asso JDR)
    # -------------------------
    @field_validator("type_prospect", mode="before")
    @classmethod
    def normalize_type_prospect(cls, v: Any) -> Any:
        if v is None:
            return None
        if isinstance(v, str):
            s = v.strip()
            if s == "":
                return None

            mapping = {
                "Editeur": "Éditeur",
                "editeur": "Éditeur",
                "Éditeur": "Éditeur",
                "Asso jdr": "Asso JDR",
                "Asso Jdr": "Asso JDR",
                "asso jdr": "Asso JDR",
                "Asso JDR": "Asso JDR",
            }
            return mapping.get(s, s)
        return v
    
    # -------------------------
    # Email: vide -> None
    # -------------------------
    @field_validator("email", mode="before")
    @classmethod
    def normalize_email_empty(cls, v: Any) -> Any:
        if v is None:
            return None
        if isinstance(v, str):
            s = v.strip()
            if s == "" or s.lower() in {"none", "null", "nan"}:
                return None
            return s
        return v


    # -------------------------
    # Date: vide -> None, parse ISO date/datetime
    # -------------------------
    @field_validator("date_dernier_contact", mode="before")
    @classmethod
    def normalize_date_dernier_contact(cls, v: Any) -> Optional[date]:
        if v is None:
            return None
        if isinstance(v, date) and not isinstance(v, datetime):
            return v
        if isinstance(v, datetime):
            return v.date()

        if isinstance(v, str):
            s = v.strip()
            if s == "" or s.lower() in {"none", "null", "nan"}:
                return None

            # "YYYY-MM-DD"
            try:
                return date.fromisoformat(s)
            except ValueError:
                pass

            # datetime ISO "YYYY-MM-DDTHH:MM:SS..."
            try:
                return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
            except ValueError:
                return None  # <- option tolérante

        return None


class ProspectCreate(ProspectBase):
    nom_structure: str = Field(..., min_length=1, max_length=200)
    type_prospect: ProspectType = Field(...)

    prospect_id: Optional[str] = Field(default=None, exclude=True)

    @model_validator(mode="after")
    def check_at_least_one_contact(self):
        if not self.email and not self.telephone:
            raise ValueError("Vous devez renseigner au moins un moyen de contact : email ou téléphone.")
        return self


class ProspectUpdate(ProspectBase):
    prospect_id: Optional[str] = Field(default=None, exclude=True)


class ProspectOut(ProspectBase):
    prospect_id: str
    nb_follower_total: Optional[int] = None
