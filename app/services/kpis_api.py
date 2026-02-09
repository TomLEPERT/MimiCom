"""Service to call the FastAPI backend for KPI calculations."""

import os
import streamlit as st
import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")

# List of valid filter parameters for the KPI endpoint
VALID_KPI_PARAMS = {
    "nom", "type_prospect", "region", "departement", "statut",
    "accepte_contact", "email", "telephone", "sit_web",
    "min_nb_aderents", "max_nb_aderents",
    "min_followers_total", "max_followers_total"
}


def get_prospects_kpis(
    nom: Optional[str] = None,
    type_prospect: Optional[str] = None,
    region: Optional[str] = None,
    departement: Optional[str] = None,
    statut: Optional[str] = None,
    accepte_contact: Optional[bool] = None,
    email: Optional[bool] = None,
    telephone: Optional[bool] = None,
    sit_web: Optional[bool] = None,
    min_nb_aderents: Optional[int] = None,
    max_nb_aderents: Optional[int] = None,
    min_followers_total: Optional[int] = None,
    max_followers_total: Optional[int] = None,
    **kwargs
):
    try:
        params = {
            k: v for k, v in locals().items()
            if k != "kwargs" and v is not None
        }

        response = requests.get(
            f"{API_BASE_URL}/kpis/prospects",
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        # ✅ ALWAYS return tuple
        return response.json(), None

    except Exception as e:
        logger.exception("KPI API failed")

        # ✅ ALWAYS return tuple
        return None, {"message": str(e)}


