import streamlit as st
from typing import Dict, Any


def render_import_summary(summary: Dict[str, Any]) -> None:
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total lignes", summary.get("total_rows", 0))
    c2.metric("Valides", summary.get("valid_rows", 0))
    c3.metric("Invalides", summary.get("invalid_rows", 0))
    c4.metric("Doublons CSV", summary.get("duplicates_in_csv", 0))
    c5.metric("Doublons DB", summary.get("duplicates_in_db", 0))
