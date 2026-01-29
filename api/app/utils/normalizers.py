import re
from typing import Any, Optional

# --- Regex ---
# Format de téléphone tolérant :
# +33612345678
# 06 12 34 56 78
# 06-12-34-56-78
PHONE_REGEX = re.compile(r"^\+?[0-9][0-9\s().-]{6,20}$")


def normalize_str(v: Any) -> Optional[str]:
    """
    Nettoie une chaîne de caractères :
    - supprime les espaces en début / fin
    - convertit les chaînes vides en None
    """
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        return s if s != "" else None
    return v


def normalize_phone(v: Any) -> Optional[str]:
    """
    Normalise un numéro de téléphone :
    - trim
    - collapse les espaces multiples
    - conserve le + s'il est présent
    """
    v = normalize_str(v)
    if v is None:
        return None
    return re.sub(r"\s+", " ", v).strip()


def validate_phone(v: Optional[str]) -> Optional[str]:
    """
    Valide le format d'un numéro de téléphone.
    """
    if v is None:
        return None
    if not PHONE_REGEX.match(v):
        raise ValueError(
            "Téléphone invalide. Format attendu : +33612345678 ou 06 12 34 56 78."
        )
    return v

def normalize_email_for_db(email: Optional[str]) -> Optional[str]:
    """
    Normalisation email pour la base Mongo :
    - trim
    - lower
    - chaîne vide → None
    Utilisée pour les index d'unicité.
    """
    if email is None:
        return None
    e = email.strip().lower()
    return e if e != "" else None


def normalize_phone_for_db(phone: Optional[str]) -> Optional[str]:
    """
    Normalisation téléphone pour la base Mongo :
    - trim
    - suppression de TOUS les espaces
    - chaîne vide → None
    Utilisée pour les index d'unicité.
    """
    if phone is None:
        return None
    p = phone.strip()
    # supprime tous les espaces
    p = re.sub(r"\s+", "", p)
    return p if p != "" else None