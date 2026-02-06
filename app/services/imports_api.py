from typing import Any, Dict, Optional, Tuple

from services.request import request, request_files


def preview_import_csv(*, filename: str, file_bytes: bytes) -> Tuple[Optional[Any], Optional[Dict[str, Any]]]:
    return request_files(
        "POST",
        "/imports/preview",
        files={"file": (filename, file_bytes, "text/csv")},
    )


def start_commit_async(
    *,
    import_id: str,
    merge_strategy: str,
    overrides: Optional[Dict[str, str]] = None,
) -> Tuple[Optional[Any], Optional[Dict[str, Any]]]:
    payload: Dict[str, Any] = {"import_id": import_id, "merge_strategy": merge_strategy}
    if overrides:
        payload["overrides"] = overrides  # {"12":"force_add", ...}
    return request("POST", "/imports/commit-async", json=payload)


def get_import_progress(*, import_id: str) -> Tuple[Optional[Any], Optional[Dict[str, Any]]]:
    return request("GET", "/imports/progress", params={"import_id": import_id})


def get_import_result(*, import_id: str) -> Tuple[Optional[Any], Optional[Dict[str, Any]]]:
    return request("GET", "/imports/result", params={"import_id": import_id})