import streamlit as st
from typing import List, Dict, Any
from components.import_export import build_invalid_csv_bytes
from collections import defaultdict


def render_invalid_rows(invalid: List[Dict[str, Any]]) -> None:
    if not invalid:
        return

    st.subheader("Lignes invalides")

    st.dataframe(
        [
            {
                "Ligne": r["row_number"],
                "Erreurs": " | ".join(r.get("errors", [])),
            }
            for r in invalid
        ],
        use_container_width=True,
    )

    # Export CSV erreurs
    csv_bytes = build_invalid_csv_bytes(invalid)
    st.download_button(
        label="Télécharger CSV des erreurs",
        data=csv_bytes,
        file_name="import_errors.csv",
        mime="text/csv",
    )

def _dup_key(d: Dict[str, Any]) -> str:
    """
    Clé de groupement lisible.
    """
    email = d.get("email_normalized") or ""
    tel = d.get("telephone_normalized") or ""
    match_on = d.get("match_on") or ""

    if match_on == "email":
        return f"EMAIL:{email}"
    if match_on == "telephone":
        return f"TEL:{tel}"
    # both
    return f"BOTH:{email} | {tel}"


def render_duplicates(duplicates: List[Dict[str, Any]]) -> None:
    if not duplicates:
        return

    st.subheader("Doublons détectés")

    # Split csv vs db
    dups_csv = [d for d in duplicates if d.get("source") == "csv"]
    dups_db = [d for d in duplicates if d.get("source") == "db"]

    c1, c2 = st.columns(2)
    c1.metric("Doublons CSV", len(dups_csv))
    c2.metric("Doublons DB", len(dups_db))

    st.divider()

    # -----------------------------
    # Doublons CSV (warning)
    # -----------------------------
    if dups_csv:
        st.warning("Doublons **dans le fichier CSV** : 2 lignes (ou plus) ont le même email/téléphone.")

        grouped = defaultdict(list)
        for d in dups_csv:
            grouped[_dup_key(d)].append(d)

        for key, items in grouped.items():
            with st.expander(f"CSV — {key} ({len(items)} occurrence(s))", expanded=False):
                rows = []
                for d in items:
                    rows.append({
                        "Ligne CSV": d.get("row_number"),
                        "Match": d.get("match_on"),
                        "Email": d.get("email_normalized"),
                        "Téléphone": d.get("telephone_normalized"),
                        "Détail": d.get("existing_snapshot", {}),
                    })
                st.dataframe(rows, use_container_width=True)

    # -----------------------------
    # Doublons DB (error/info)
    # -----------------------------
    if dups_db:
        st.error("Doublons **avec la base de données** : ces lignes matchent déjà un prospect existant.")

        grouped = defaultdict(list)
        for d in dups_db:
            grouped[_dup_key(d)].append(d)

        for key, items in grouped.items():
            # On affiche l’id existant si dispo
            existing_ids = list({i.get("existing_prospect_id") for i in items if i.get("existing_prospect_id")})
            extra = f" → existing: {', '.join(existing_ids)}" if existing_ids else ""

            with st.expander(f"DB — {key} ({len(items)} occurrence(s)){extra}", expanded=False):
                rows = []
                for d in items:
                    rows.append({
                        "Ligne CSV": d.get("row_number"),
                        "Match": d.get("match_on"),
                        "Email": d.get("email_normalized"),
                        "Téléphone": d.get("telephone_normalized"),
                        "Prospect existant": d.get("existing_prospect_id"),
                    })
                st.dataframe(rows, use_container_width=True)

                # Snapshot existant
                snap = items[0].get("existing_snapshot")
                if snap:
                    st.caption("Snapshot du prospect existant")
                    st.json(snap, expanded=False)

