import csv
import io
from typing import Dict, List, Tuple


def _decode_bytes(data: bytes) -> str:
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    # fallback
    return data.decode("utf-8", errors="replace")


def read_csv_bytes(data: bytes) -> Tuple[List[str], List[Dict[str, str]]]:
    """
    Retourne (headers, rows) où rows est une liste de dict {col: value}
    """
    text = _decode_bytes(data)
    sio = io.StringIO(text)

    # Détecter le delimiter
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=";,|\t")
    except csv.Error:
        dialect = csv.excel
        dialect.delimiter = ","  # fallback

    reader = csv.DictReader(sio, dialect=dialect)

    headers = reader.fieldnames or []
    rows: List[Dict[str, str]] = []
    for r in reader:
        # DictReader peut retourner None si ligne vide
        if r is None:
            continue
        rows.append({k: (v if v is not None else "") for k, v in r.items()})
    return headers, rows
