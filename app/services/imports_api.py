from typing import Any, Dict, Optional, Tuple

from .request import request, request_files


# -------------------------------------------------------------------
# Imports : Prospects CSV
# -------------------------------------------------------------------
def preview_import_prospects(uploaded_file) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    POST /imports/prospects/preview (multipart/form-data)
    """
    files = {
        "file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv"),
    }
    return request_files("POST", "/imports/prospects/preview", files=files)


def commit_import_prospects(
    preview_id: str,
    force: bool = False,
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    POST /imports/prospects/commit
    """
    payload = {"preview_id": preview_id, "force": force}
    return request("POST", "/imports/prospects/commit", json=payload)
