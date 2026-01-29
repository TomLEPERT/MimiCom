from typing import Dict, Any, List, Optional

import streamlit as st

from utils.constants import (
    TYPE_PROSPECT_OPTIONS,
    REGION_FRANCE_OPTIONS,
    DEPARTEMENT_OPTIONS,
    METHODE_CONTACT_OPTIONS,
    PAYS_OPTIONS,
    TRI_BOOL,
)

# ------------------------------------------------------------
# Helper : tri-state bool (None/True/False)
# ------------------------------------------------------------

def _tri_bool_label(v: Optional[bool]) -> str:
    if v is None:
        return "Indifférent"
    return "Présent" if v else "Absent"


def render_prospects_filters(
    *,
    key: str,
    fields: List[str],
    show_sort: bool = True,
) -> Dict[str, Any]:
    """
    Composant de filtres réutilisable.

    fields : liste des filtres à afficher (ex: ["nom","email","telephone"])
    show_sort : affiche ou non sort_by/sort_dir

    Retourne un dict prêt à passer à search_prospects(**filters).
    On n'inclut que les champs non vides / non None.
    """

    state_key = f"{key}_filters"
    if state_key not in st.session_state:
        st.session_state[state_key] = {}

    filters: Dict[str, Any] = st.session_state[state_key]

    with st.expander("Filtres", expanded=True):
        # ------------------------------------------------------------
        # LAYOUT : on met en colonnes selon le nombre de filtres affichés
        # ------------------------------------------------------------
        nb_cols = 3 if len(fields) >= 3 else max(1, len(fields))
        cols = st.columns(nb_cols)

        def col(i: int):
            return cols[i % nb_cols]

        # ------------------------------------------------------------
        # Champs (selon "fields")
        # ------------------------------------------------------------

        # NOM
        if "nom" in fields:
            with col(0):
                filters["nom"] = st.text_input(
                    "Nom (structure)",
                    value=filters.get("nom", "") or "",
                    key=f"{key}_nom",
                ).strip() or None

        # TYPE_PROSPECT
        if "type_prospect" in fields:
            with col(1):
                current = filters.get("type_prospect")
                try:
                    idx = TYPE_PROSPECT_OPTIONS.index(current) if current else None
                except ValueError:
                    idx = None

                filters["type_prospect"] = st.selectbox(
                    "Type prospect",
                    TYPE_PROSPECT_OPTIONS,
                    index=idx,
                    placeholder="Indifférent",
                    key=f"{key}_type_prospect",
                ) or None

        # REGION
        if "region" in fields:
            with col(2):
                current = filters.get("region")
                try:
                    idx = REGION_FRANCE_OPTIONS.index(current) if current else None
                except ValueError:
                    idx = None

                filters["region"] = st.selectbox(
                    "Région",
                    REGION_FRANCE_OPTIONS,
                    index=idx,
                    placeholder="Indifférent",
                    key=f"{key}_region",
                ) or None

        # DEPARTEMENT
        if "departement" in fields:
            with col(0):
                current = filters.get("departement")
                try:
                    idx = DEPARTEMENT_OPTIONS.index(current) if current else None
                except ValueError:
                    idx = None

                filters["departement"] = st.selectbox(
                    "Département",
                    DEPARTEMENT_OPTIONS,
                    index=idx,
                    placeholder="Indifférent",
                    key=f"{key}_departement",
                ) or None

        # PAYS
        if "pays" in fields:
            with col(2):
                current = filters.get("pays")
                try:
                    idx = PAYS_OPTIONS.index(current) if current else None
                except ValueError:
                    # Par défaut : France
                    idx = PAYS_OPTIONS.index("France") if "France" in PAYS_OPTIONS else None

                filters["pays"] = st.selectbox(
                    "Pays",
                    PAYS_OPTIONS,
                    index=idx,
                    placeholder="Indifférent",
                    key=f"{key}_pays",
                ) or None

        # STATUT
        if "statut" in fields:
            with col(1):
                filters["statut"] = st.text_input(
                    "Statut",
                    value=filters.get("statut", "") or "",
                    key=f"{key}_statut",
                ).strip() or None
                # Si tu as une liste STATUT_OPTIONS -> remplace par selectbox.

        # ACCEPTE_CONTACT
        if "accepte_contact" in fields:
            with col(2):
                # tri-state bool (None/True/False)
                cur = filters.get("accepte_contact", None)
                filters["accepte_contact"] = st.selectbox(
                    "Accepte d’être contacté",
                    options=TRI_BOOL,
                    format_func=lambda x: "Indifférent" if x is None else ("Oui" if x else "Non"),
                    index=TRI_BOOL.index(cur),
                    key=f"{key}_accepte_contact",
                )
        
        # METHODE_CONTACT
        if "methode_contact" in fields:
            with col(0):
                current = filters.get("methode_contact")
                try:
                    idx = METHODE_CONTACT_OPTIONS.index(current) if current else None
                except ValueError:
                    idx = None

                filters["methode_contact"] = st.selectbox(
                    "Méthode de contact",
                    METHODE_CONTACT_OPTIONS,
                    index=idx,
                    placeholder="Indifférent",
                    key=f"{key}_methode_contact",
                ) or None

        st.divider()

        # ------------------------------------------------------------
        # Champs booléens : email / telephone / sit_web
        # ------------------------------------------------------------
        if any(x in fields for x in ["email", "telephone", "sit_web"]):
            st.write("### Champs présents / absents")

            c1, c2, c3 = st.columns(3)

            if "email" in fields:
                cur = filters.get("email", None)
                with c1:
                    filters["email"] = st.selectbox(
                        "Email",
                        options=TRI_BOOL,
                        format_func=_tri_bool_label,
                        index=TRI_BOOL.index(cur),
                        key=f"{key}_email",
                    )

            if "telephone" in fields:
                cur = filters.get("telephone", None)
                with c2:
                    filters["telephone"] = st.selectbox(
                        "Téléphone",
                        options=TRI_BOOL,
                        format_func=_tri_bool_label,
                        index=TRI_BOOL.index(cur),
                        key=f"{key}_telephone",
                    )

            if "sit_web" in fields:
                cur = filters.get("sit_web", None)
                with c3:
                    filters["sit_web"] = st.selectbox(
                        "Site web",
                        options=TRI_BOOL,
                        format_func=_tri_bool_label,
                        index=TRI_BOOL.index(cur),
                        key=f"{key}_sit_web",
                    )

            st.divider()

        # ------------------------------------------------------------
        # Filtres numériques
        # ------------------------------------------------------------
        if any(x in fields for x in ["nb_aderents", "followers_total"]):
            st.write("### Filtres numériques")

            if "nb_aderents" in fields:
                n1, n2 = st.columns(2)
                with n1:
                    filters["min_nb_aderents"] = st.number_input(
                        "Min adhérents",
                        min_value=0,
                        value=int(filters.get("min_nb_aderents") or 0),
                        step=1,
                        key=f"{key}_min_nb_aderents",
                    )
                    if filters["min_nb_aderents"] == 0:
                        filters["min_nb_aderents"] = None

                with n2:
                    filters["max_nb_aderents"] = st.number_input(
                        "Max adhérents",
                        min_value=0,
                        value=int(filters.get("max_nb_aderents") or 0),
                        step=1,
                        key=f"{key}_max_nb_aderents",
                    )
                    if filters["max_nb_aderents"] == 0:
                        filters["max_nb_aderents"] = None

            if "followers_total" in fields:
                f1, f2 = st.columns(2)
                with f1:
                    filters["min_followers_total"] = st.number_input(
                        "Min followers (max réseau)",
                        min_value=0,
                        value=int(filters.get("min_followers_total") or 0),
                        step=1,
                        key=f"{key}_min_followers_total",
                    )
                    if filters["min_followers_total"] == 0:
                        filters["min_followers_total"] = None

                with f2:
                    filters["max_followers_total"] = st.number_input(
                        "Max followers (max réseau)",
                        min_value=0,
                        value=int(filters.get("max_followers_total") or 0),
                        step=1,
                        key=f"{key}_max_followers_total",
                    )
                    if filters["max_followers_total"] == 0:
                        filters["max_followers_total"] = None

            st.divider()

        # ------------------------------------------------------------
        # TRI
        # ------------------------------------------------------------
        if show_sort:
            st.write("### Tri")

            allowed_sort = [
                "nom_structure",
                "type_prospect",
                "region",
                "departement",
                "nb_aderents",
                "nb_follower_total",
            ]

            s1, s2 = st.columns(2)
            with s1:
                cur = filters.get("sort_by", "nom_structure")
                if cur not in allowed_sort:
                    cur = "nom_structure"
                filters["sort_by"] = st.selectbox(
                    "Trier par",
                    options=allowed_sort,
                    index=allowed_sort.index(cur),
                    key=f"{key}_sort_by",
                )

            with s2:
                cur = filters.get("sort_dir", "asc")
                filters["sort_dir"] = st.selectbox(
                    "Direction",
                    options=["asc", "desc"],
                    index=0 if cur == "asc" else 1,
                    key=f"{key}_sort_dir",
                )

            st.divider()

        # ------------------------------------------------------------
        # Reset
        # ------------------------------------------------------------
        if st.button("Réinitialiser les filtres", key=f"{key}_reset"):
            # Supprimer l'état des filtres
            st.session_state[state_key] = {}

            # Supprimer l'état des widgets associés
            for k in list(st.session_state.keys()):
                if k.startswith(f"{key}_"):
                    del st.session_state[k]

            st.rerun()

    # ------------------------------------------------------------
    # Nettoyage : on ne renvoie que ce qui a une valeur utile
    # ------------------------------------------------------------
    cleaned: Dict[str, Any] = {}

    for k, v in filters.items():
        if v is None:
            continue
        if isinstance(v, str) and v.strip() == "":
            continue
        cleaned[k] = v

    return cleaned
