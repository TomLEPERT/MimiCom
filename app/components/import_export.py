import csv
import io
from typing import Any, Dict, List


def build_invalid_csv_bytes(invalid: List[Dict[str, Any]]) -> bytes:
    """
    Transforme preview["invalid"] en CSV téléchargeable.
    Colonnes:
      - row_number
      - errors
      - + toutes les clés trouvées dans raw
    """
    # collecter toutes les colonnes raw
    raw_keys = set()
    for item in invalid:
        raw = item.get("raw") or {}
        raw_keys.update(raw.keys())

    raw_keys = sorted(raw_keys)

    fieldnames = ["row_number", "errors"] + raw_keys

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()

    for item in invalid:
        raw = item.get("raw") or {}
        row = {
            "row_number": item.get("row_number"),
            "errors": " | ".join(item.get("errors", [])),
            **raw,
        }
        writer.writerow(row)

    return output.getvalue().encode("utf-8-sig")
