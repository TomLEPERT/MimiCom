import streamlit as st
import pandas as pd

from services.imports_api import preview_import_prospects, commit_import_prospects

# ------------------------------------------------------------
# Config page
# ------------------------------------------------------------
st.set_page_config(page_title="Import CSV prospects", layout="wide")
st.title("Import CSV — Prospects")

st.page_link("pages/Visualisation_BDD.py", label="⬅ Retour BDD")
st.divider()

# ------------------------------------------------------------
# Session state
# ------------------------------------------------------------
if "import_preview" not in st.session_state:
    st.session_state.import_preview = None

if "import_commit_result" not in st.session_state:
    st.session_state.import_commit_result = None


def reset_import():
    st.session_state.import_preview = None
    st.session_state.import_commit_result = None


# ------------------------------------------------------------
# UI Upload
# ------------------------------------------------------------
st.subheader("1) Charger un CSV")

uploaded = st.file_uploader("Fichier CSV", type=["csv"])

c1, c2 = st.columns(2)
with c1:
    do_preview = st.button("Preview", disabled=(uploaded is None), use_container_width=True)
with c2:
    if st.button("Réinitialiser", use_container_width=True):
        reset_import()
        st.rerun()

# ------------------------------------------------------------
# Preview
# ------------------------------------------------------------
if do_preview and uploaded is not None:
    preview, err = preview_import_prospects(uploaded)
    if err:
        st.error(err.get("message", "Erreur preview import"))
        if err.get("detail"):
            st.json(err["detail"])
    else:
        st.session_state.import_preview = preview
        st.session_state.import_commit_result = None
        st.success("Preview générée")
        st.rerun()

preview = st.session_state.import_preview
if not preview:
    st.info("Charge un CSV puis clique sur Preview.")
    st.stop()

# ------------------------------------------------------------
# Affichage preview
# ------------------------------------------------------------
st.subheader("2) Résultat preview")

stats = preview.get("stats", {})
colA, colB, colC, colD = st.columns(4)
colA.metric("Total", stats.get("total", 0))
colB.metric("Valides", stats.get("valid", 0))
colC.metric("Invalides", stats.get("invalid", 0))
colD.metric("Doublons", stats.get("duplicates", 0))

st.caption(f"Fichier : {preview.get('filename') or '—'}")
st.caption(f"Preview ID : {preview.get('preview_id')}")
st.divider()

invalid_rows = preview.get("invalid_rows", [])
duplicate_rows = preview.get("duplicate_rows", [])

# Invalid rows
st.write("### Lignes invalides")
if invalid_rows:
    df_invalid = pd.DataFrame(
        [
            {
                "row": r.get("row"),
                "errors": " | ".join(r.get("errors", [])),
            }
            for r in invalid_rows[:50]  # on limite l’affichage
        ]
    )
    st.dataframe(df_invalid, use_container_width=True, hide_index=True)
    if len(invalid_rows) > 50:
        st.caption(f"Affichage limité à 50 lignes sur {len(invalid_rows)}.")
    with st.expander("Voir le détail (raw)"):
        st.json(invalid_rows)
else:
    st.success("Aucune ligne invalide")

st.divider()

# Duplicates
st.write("### Doublons détectés")
if duplicate_rows:
    df_dup = pd.DataFrame(
        [
            {
                "row": r.get("row"),
                "fields": ", ".join(r.get("fields", [])),
                "existing_prospect_id": r.get("existing_prospect_id"),
            }
            for r in duplicate_rows[:50]
        ]
    )
    st.dataframe(df_dup, use_container_width=True, hide_index=True)
    if len(duplicate_rows) > 50:
        st.caption(f"Affichage limité à 50 lignes sur {len(duplicate_rows)}.")
else:
    st.success("Aucun doublon détecté")

st.divider()

# ------------------------------------------------------------
# Commit
# ------------------------------------------------------------
st.subheader("3) Importer en base")

c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    commit_normal = st.button("Importer (sans force)", use_container_width=True)
with c2:
    commit_force = st.button("Importer (force doublons)", use_container_width=True)
with c3:
    st.info(
        "Sans force : les doublons seront ignorés\n"
        "Force : les doublons seront créés (allow_duplicate=true)"
    )

if commit_normal:
    res, err = commit_import_prospects(preview_id=preview["preview_id"], force=False)
    if err:
        st.error(err.get("message", "Erreur import"))
        if err.get("detail"):
            st.json(err["detail"])
    else:
        st.session_state.import_commit_result = res
        st.success("Import terminé")
        st.rerun()

if commit_force:
    res, err = commit_import_prospects(preview_id=preview["preview_id"], force=True)
    if err:
        st.error(err.get("message", "Erreur import (force)"))
        if err.get("detail"):
            st.json(err["detail"])
    else:
        st.session_state.import_commit_result = res
        st.success("Import terminé (force)")
        st.rerun()

# ------------------------------------------------------------
# Résultat
# ------------------------------------------------------------
if st.session_state.import_commit_result:
    st.divider()
    st.subheader("Résultat import")

    res = st.session_state.import_commit_result

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Créés", res.get("created", 0))
    c2.metric("Forcés", res.get("forced_created", 0))
    c3.metric("Invalides ignorés", res.get("skipped_invalid", 0))
    c4.metric("Doublons ignorés", res.get("skipped_duplicates", 0))

    st.success("Tu peux retourner dans la BDD pour voir les nouveaux prospects.")