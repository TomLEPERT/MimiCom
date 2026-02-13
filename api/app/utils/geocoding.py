from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

import httpx

from app.core.config import (
    GEOCODING_PROVIDER,
    GEOCODING_API_KEY,
    GEOCODING_TIMEOUT_SECONDS,
    GEOCODING_USER_AGENT,
)


@dataclass
class GeocodeResult:
    lat: float
    lon: float
    label: Optional[str] = None
    score: Optional[float] = None
    provider: str = GEOCODING_PROVIDER


def build_query_from_fields(
    adresse: Optional[str],
    ville: Optional[str],
    departement: Optional[str],
    region: Optional[str],
    pays: Optional[str],
) -> Optional[str]:
    parts = []
    for p in (adresse, ville, departement, region, pays):
        if p and str(p).strip():
            parts.append(str(p).strip())
    if not parts:
        return None
    return ", ".join(parts)


def geocode(query: str) -> Optional[GeocodeResult]:
    """Retourne (lat, lon) pour une requête texte, ou None si pas trouvé."""
    provider = (GEOCODING_PROVIDER or "ban").lower().strip()

    timeout = httpx.Timeout(GEOCODING_TIMEOUT_SECONDS)

    headers = {"User-Agent": GEOCODING_USER_AGENT}

    with httpx.Client(timeout=timeout, headers=headers) as client:
        if provider == "ban":
            # API Adresse (France) : https://api-adresse.data.gouv.fr
            # Réponse: features[0].geometry.coordinates = [lon, lat]
            r = client.get(
                "https://api-adresse.data.gouv.fr/search/",
                params={"q": query, "limit": 1},
            )
            r.raise_for_status()
            data = r.json()
            features = data.get("features") or []
            if not features:
                return None
            f0 = features[0]
            coords = (f0.get("geometry") or {}).get("coordinates") or []
            if len(coords) != 2:
                return None
            lon, lat = float(coords[0]), float(coords[1])
            props = f0.get("properties") or {}
            return GeocodeResult(
                lat=lat,
                lon=lon,
                label=props.get("label"),
                score=props.get("score"),
                provider="ban",
            )

        if provider == "nominatim":
            # Nominatim (OpenStreetMap) - attention aux limites d'usage
            # https://nominatim.org/release-docs/latest/api/Search/
            r = client.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": query, "format": "json", "limit": 1},
            )
            r.raise_for_status()
            arr = r.json()
            if not arr:
                return None
            item = arr[0]
            return GeocodeResult(
                lat=float(item["lat"]),
                lon=float(item["lon"]),
                label=item.get("display_name"),
                score=None,
                provider="nominatim",
            )

        # Placeholder pour d'autres providers (Google, Mapbox, etc.)
        raise ValueError(f"Provider geocoding non supporté: {provider}")
