from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st


def render_prospects_table(
    prospects: List[Dict[str, Any]],
    *,
    title: str = "Résultats",
    key: str = "prospects_table",
    show_actions: bool = True,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Affiche une liste de prospects sous forme de tableau + actions.

    - Affiche tous les champs présents dans les prospects.
    - Permet de sélectionner une ligne et d'exécuter une action.

    Retour :
      (selected_row, action)
        selected_row : dict ou None
        action : "view" | "edit" | "delete" | None
    """

    st.subheader(title)

    if not prospects:
        st.info("Aucun prospect trouvé.")
        return None, None

    # DataFrame avec tous les colonnes disponibles
    df = pd.DataFrame(prospects)

    # Optionnel : ordre de colonnes "confort", mais on garde tout le reste
    preferred = [
        "prospect_id",
        "nom_structure",
        "nom_contact",
        "type_prospect",
        "ville",
        "region",
        "departement",
        "pays",
        "email",
        "telephone",
        "sit_web",
        "accepte_contact",
        "contacte",
        "date_dernier_contact",
    ]
    cols = [c for c in preferred if c in df.columns] + [c for c in df.columns if c not in preferred]
    df = df[cols]

    # Tableau Streamlit avec sélection
    event = st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key=f"{key}_df",
    )

    selected_rows = event.selection.get("rows", [])
    if not selected_rows:
        st.info("Sélectionne une ligne pour afficher les actions.")
        return None, None

    row_index = selected_rows[0]
    selected = df.iloc[row_index].to_dict()

    if not show_actions:
        return selected, None

    st.divider()
    st.write(
        f"**Prospect sélectionné :** {selected.get('nom_structure') or '—'} "
        f"— **ID :** `{selected.get('prospect_id')}`"
    )

    col1, col2, col3 = st.columns(3)
    action = None

    with col1:
        if st.button("Visualiser", width="stretch", key=f"{key}_view"):
            action = "view"

    with col2:
        if st.button("Modifier", width="stretch", key=f"{key}_edit"):
            action = "edit"

    with col3:
        if st.button("Supprimer", width="stretch", key=f"{key}_delete"):
            action = "delete"

    return selected, action
