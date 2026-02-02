import csv
import io
from typing import Any, Dict, List, Tuple, Optional

from app.models.prospect import ProspectCreate
from app.utils.normalizers import normalize_str

TYPE_MAP = {
    "Asso jdr": "Asso JDR",
    "Editeur": "Éditeur",
    "Mediatheque": "Médiathèque",
    "CSCS": "CSCS",
    "Bar à jeux": "Bar à jeux",
    "Influenceur": "Influenceur",
    "MJC": "MJC",
    "Mediathèque": "Médiathèque",
    "Artisan": "Artisan",
    "Editeur": "Éditeur",
    "Asso JDR": "Asso JDR",
    "Boutique spécialisée": "Boutique spécialisée",
    "Ludotheque": "Ludothèque",
}

def _to_bool_oui_non(v: Any) -> Optional[bool]:
    if v is None:
        return None
    s = str(v).strip().lower()
    if s in ["oui", "o", "true", "1", "yes"]:
        return True
    if s in ["non", "n", "false", "0", "no"]:
        return False
    return None

def _to_int(v: Any) -> Optional[int]:
    if v is None:
        return None
    s = str(v).strip()
    if s == "":
        return None
    try:
        return int(float(s))
    except ValueError:
        return None

def map_csv_row_to_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    # Normalise toutes les valeurs texte (trim + "" -> None)
    def n(x): return normalize_str(x)

    type_val = n(raw.get("Type"))
    if type_val in TYPE_MAP:
        type_val = TYPE_MAP[type_val]

    payload = {
        "nom_structure": n(raw.get("Nom")),
        "nom_contact": n(raw.get("Nom_contact")) or n(raw.get("Nom Contact")),
        "type_prospect": type_val,
        "email": n(raw.get("Email")),
        "telephone": n(raw.get("Tel")),

        "pays": n(raw.get("Pays")),
        "region": n(raw.get("Region")),
        "departement": n(raw.get("Departement")),
        "ville": n(raw.get("Ville")),
        "adresse": n(raw.get("Adresse")) or n(raw.get("Adresse_postal")),

        "nb_aderents": _to_int(raw.get("nb_adherent")),

        "facebook": n(raw.get("FB")),
        "facebook_followers": _to_int(raw.get("FB_nb_aderent")),

        "x": n(raw.get("Twitter")),
        "x_followers": _to_int(raw.get("Twitter_nb_aderent")),

        "instagram": n(raw.get("Insta")),
        "instagram_followers": _to_int(raw.get("Insta_nb_aderent")),

        "youtube": n(raw.get("Youtube")),
        "youtube_followers": _to_int(raw.get("Youtube_nb_aderent")),

        "tictok": n(raw.get("Tiktok")),
        "tictok_followers": _to_int(raw.get("Tiktok_nb_aderent")),

        "sit_web": n(raw.get("Web_site")),

        "accepte_contact": _to_bool_oui_non(raw.get("Accepte_com")) or False,
        "methode_contact": n(raw.get("Methode_contact")),

        "commentaires": n(raw.get("Commentaire")),
    }

    return payload

def parse_csv_bytes(csv_bytes: bytes) -> List[Dict[str, Any]]:
    text = csv_bytes.decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    return list(reader)

def validate_rows(rows: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Tuple[int, List[str], Dict[str, Any]]]]:
    valid_payloads: List[Dict[str, Any]] = []
    invalid: List[Tuple[int, List[str], Dict[str, Any]]] = []

    for idx, raw in enumerate(rows, start=2):  # start=2 si ligne 1 = header
        try:
            payload = map_csv_row_to_payload(raw)
            # Pydantic valide ici (nom_structure + type_prospect obligatoires + email/tel rule)
            ProspectCreate(**payload)
            valid_payloads.append(payload)
        except Exception as e:
            invalid.append((idx, [str(e)], raw))

    return valid_payloads, invalid
